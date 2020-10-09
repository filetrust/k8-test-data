import logging
import time

import json
import os
import pika
import requests
import sys

from src.config import Config

logger = logging.getLogger('GW: RabbitMQ Consumer')


class Consumer:
    logger.info("Consumer ")

    QUEUE = Config.MQ_QUEUE

    MQ_URL = Config.MQ_URL

    def __init__(self):

        self.connection = None
        self.channel = None
        self.host = Config.MQ_HOST
        self.queue = Config.MQ_QUEUE
        self.receivers = {
            "process_zip": self._handler_process_zip,
            "s3_sync": self._handler_s3_sync,
        }

    def _handler_process_zip(self, payload):
        try:
            logger.info("calling file_processor service..")
            requests.post("http://k8-file-processor:5000/process", json=payload)
        except Exception as error:
            logger.error(f'Consumer : _handler_process_zip : error : {error}')

    def _handler_s3_sync(self, payload):
        try:
            logger.info("calling s3_sync service..")
            requests.post("http://k8-s3-sync:5004/tos3", json=payload)
        except Exception as e:
            logger.error(f'Consumer : _handler_process_zip : error : {e}')

    def on_message_receive(self, ch, method, properties, body):
        logger.info(" [x] Received ")
        msg = body.decode()
        logger.info(msg)
        try:
            payload = json.loads(msg)
        except:
            logger.error("Error loading json payload")
        else:
            handler = self.receivers.get(payload["type"], None)
            if not handler:
                logger.info("invalid payload type.")
            handler(payload)

        logger.info(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def connect(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ["MQ_HOST"])
        )
        channel = connection.channel()

        channel.queue_declare(queue=os.environ["MQ_QUEUE"])

        def callback(ch, method, properties, body):
            logger.info(" [x] Received ")
            msg = body.decode()
            logger.info(msg)
            try:
                payload = json.loads(msg)
            except:
                logger.error("Error loading json payload")
            else:
                handler = self.receivers.get(payload["type"], None)
                if not handler:
                    logger.info("invalid payload type.")
                handler(payload)

            logger.info(" [x] Done")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=os.environ["MQ_QUEUE"], on_message_callback=self.on_message_receive)

        logger.info(" [*] starting receiver..")
        channel.start_consuming()

    @staticmethod
    def run():
        try:
            Consumer().connect()
        except KeyboardInterrupt:
            logger.info("Interrupted")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

