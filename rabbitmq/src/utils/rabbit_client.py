"""
    Reference taken from Pika Example: 
    https://github.com/pika/pika/blob/master/examples/asynchronous_publisher_example.py
"""

import json
import logging
import time

import pika
from src.config import Config

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger("GW: RabbitMQ Client")


class RabbitClient(object):
    EXCHANGE = Config.MQ_EXCHANGE
    EXCHANGE_TYPE = Config.MQ_EXCHANGE_TYPE
    PUBLISH_INTERVAL = Config.MQ_PUBLISH_INTERVAL
    QUEUE = Config.MQ_QUEUE
    ROUTING_KEY = Config.MQ_ROUTING_KEY
    MQ_URL = Config.MQ_URL

    def __init__(self, job_queue):

        self._connection = None
        self._channel = None

        self._deliveries = None
        self._acked = None
        self._nacked = None
        self._message_number = None

        self._stopping = False
        self._url = self.MQ_URL

        self.queue = job_queue
        self.run()

    def connect(self):
        LOGGER.info('Connecting to %s', self._url)
        return pika.SelectConnection(
            pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    def on_connection_open(self, _unused_connection):
        LOGGER.info('Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        LOGGER.error('Connection open failed, reopening in 5 seconds: %s', err)
        self._connection.ioloop.call_later(5, self._connection.ioloop.stop)

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._stopping:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reopening in 5 seconds: %s',
                           reason)
            self._connection.ioloop.call_later(5, self._connection.ioloop.stop)

    def open_channel(self):
        LOGGER.info('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        LOGGER.info('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_queue(self.QUEUE)

    def add_on_channel_close_callback(self):
        LOGGER.info('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        LOGGER.warning('Channel %i was closed: %s', channel, reason)
        self._channel = None
        if not self._stopping:
            self._connection.close()

    def setup_queue(self, queue_name):
        LOGGER.info('Declaring queue %s', queue_name)
        self._channel.queue_declare(
            queue=queue_name, callback=self.on_bindok)

    def on_bindok(self, _unused_frame):
        LOGGER.info('Queue bound')
        self.start_publishing()

    def start_publishing(self):
        LOGGER.info('Issuing consumer related RPC commands')
        self.enable_delivery_confirmations()
        self.schedule_next_message()

    def enable_delivery_confirmations(self):
        LOGGER.info('Issuing Confirm.Select RPC command')
        self._channel.confirm_delivery(self.on_delivery_confirmation)

    def on_delivery_confirmation(self, method_frame):
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()
        LOGGER.info('Received %s for delivery tag: %i', confirmation_type,
                    method_frame.method.delivery_tag)
        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1
        self._deliveries.remove(method_frame.method.delivery_tag)
        LOGGER.info(
            'Published %i messages, %i have yet to be confirmed, '
            '%i were acked and %i were nacked', self._message_number,
            len(self._deliveries), self._acked, self._nacked)

    def schedule_next_message(self):
        LOGGER.info('Scheduling next message for %0.1f seconds',
                    self.PUBLISH_INTERVAL)
        self._connection.ioloop.call_later(self.PUBLISH_INTERVAL,
                                           self.publish_message)

    def publish_message(self):
        if self._channel is None or not self._channel.is_open:
            return
        try:
            if self.queue.empty():
                LOGGER.info(f'RabbitClient : publish_message : queue is empty')
                time.sleep(60)
                self.schedule_next_message()
            else:
                properties = pika.BasicProperties(
                    content_type='application/json'
                )
                message = self.queue.get(True, 0.01)
                self._channel.basic_publish(self.EXCHANGE, self.ROUTING_KEY,
                                            json.dumps(message, ensure_ascii=False),
                                            properties)

                self._message_number += 1
                self._deliveries.append(self._message_number)
                LOGGER.info('Published message # %i', self._message_number)
                self.schedule_next_message()
        except Exception as err:
            LOGGER.error(err)
            LOGGER.error('Error in fetching Job Queue: {0}'.format(err))

    def run(self):
        while not self._stopping:
            self._connection = None
            self._deliveries = []
            self._acked = 0
            self._nacked = 0
            self._message_number = 0

            try:
                self._connection = self.connect()
                self._connection.ioloop.start()
            except KeyboardInterrupt:
                self.stop()
                if (self._connection is not None and
                        not self._connection.is_closed):
                    # Finish closing
                    self._connection.ioloop.start()

        LOGGER.info('Stopped')

    def stop(self):
        LOGGER.info('Stopping')
        self._stopping = True
        self.close_channel()
        self.close_connection()

    def close_channel(self):
        if self._channel is not None:
            LOGGER.info('Closing the channel')
            self._channel.close()

    def close_connection(self):
        if self._connection is not None:
            LOGGER.info('Closing connection')
            self._connection.close()
