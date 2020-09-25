from os import environ
import json
import logging
import pika

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger("GW:RabbitClient")


class RabbitClient(object):

    MQ_USERNAME = environ.get("MQ_USERNAME", "guest")
    MQ_PASSWORD = environ.get("MQ_PASSWORD", "guest")
    MQ_HOST = environ.get("MQ_HOST", "localhost")
    MQ_PORT = environ.get("MQ_PORT", "5672")
    MQ_VHOST = environ.get("MQ_VHOST", "/")
    MQ_CONNECTION_ATTEMPTS = environ.get("MQ_CONNECTION_ATTEMPTS", 3)
    MQ_HEART_BEAT = environ.get("MQ_HEART_BEAT", 600)
    MQ_PROTO = environ.get("MQ_PROTO", "amqp://")

    MQ_URL = (
        MQ_PROTO
        + MQ_USERNAME
        + ":"
        + MQ_PASSWORD
        + "@"
        + MQ_HOST
        + ":"
        + MQ_PORT
        + "/"
        + MQ_VHOST
    )
    MQ_EXCHANGE = environ.get("MQ_EXCHANGE", "")
    MQ_EXCHANGE_TYPE = environ.get("MQ_EXCHANGE_TYPE", "")
    MQ_QUEUE = environ.get("MQ_QUEUE", "")
    MQ_ROUTING_KEY = environ.get("MQ_ROUTING_KEY", "")

    def __init__(self):

        LOGGER.info("Initiating RabbitMQ connection")

        self.url = self.MQ_URL
        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.MQ_QUEUE)

    def publish_job(self, payload):

        self.channel.basic_publish(
            exchange=self.MQ_EXCHANGE,
            routing_key=self.MQ_ROUTING_KEY,
            body=json.dumps(payload),
            properties=pika.BasicProperties(content_type="application/json"),
        )

        LOGGER.info("Job published")
