import os


def get_envar(k, required=True):
    val = os.environ.get(k, None)
    if not val and required:
        exit(f"{k} not supplied")
    return val

class Config(object):
    DEBUG = True

    MINIO_ENDPOINT = get_envar("MINIO_ENDPOINT", required=True)
    MINIO_ACCESS_KEY_ID = get_envar("MINIO_ACCESS_KEY_ID", required=True)
    MINIO_SECRET_ACCESS_KEY = get_envar("MINIO_SECRET_ACCESS_KEY", required=True)

    MINIO_SECURE = get_envar("MINIO_SECURE", required=True)
    if MINIO_SECURE == "True":
        MINIO_SECURE = True
    else:
        MINIO_SECURE = False

    MINIO_BUCKET = get_envar("MINIO_BUCKET", required=True)
    MQ_USERNAME = get_envar("MQ_USERNAME", required=True)
    MQ_PASSWORD = get_envar("MQ_PASSWORD", required=True)
    MQ_HOST = get_envar("MQ_HOST", required=True)
    MQ_PORT = get_envar("MQ_PORT", required=True)

    MQ_CONNECTION_ATTEMPTS = get_envar("MQ_CONNECTION_ATTEMPTS", required=False)
    if MQ_CONNECTION_ATTEMPTS is None:
        MQ_CONNECTION_ATTEMPTS = str(3)

    MQ_HEART_BEAT = get_envar("MQ_HEART_BEAT", required=False)
    if MQ_HEART_BEAT is None:
        MQ_HEART_BEAT = str(600)

    MQ_EXCHANGE = get_envar("MQ_EXCHANGE", required=False)
    if MQ_EXCHANGE is None:
        MQ_EXCHANGE = ''

    MQ_EXCHANGE_TYPE = get_envar("MQ_EXCHANGE_TYPE", required=False)
    MQ_QUEUE = get_envar("MQ_QUEUE", required=True)
    MQ_ROUTING_KEY = get_envar("MQ_ROUTING_KEY", required=True)

    MQ_PROTO = get_envar("MQ_PROTO", required=False)
    if MQ_PROTO is None:
        MQ_PROTO = 'amqp://'

    MQ_VHOST = get_envar("MQ_VHOST", required=False)
    if MQ_VHOST is None:
        MQ_VHOST = '%2F'

    MQ_PUBLISH_INTERVAL = get_envar("MQ_PUBLISH_INTERVAL", required=False)
    if MQ_PUBLISH_INTERVAL is None:
        MQ_PUBLISH_INTERVAL = 0.1

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
            + "?connection_attempts="
            + MQ_CONNECTION_ATTEMPTS
            + "&heartbeat="
            + MQ_HEART_BEAT
    )
