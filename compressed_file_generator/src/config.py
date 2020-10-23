import os

from dotenv import load_dotenv

env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()


class Config(object):
    DEBUG = True
    download_path = "download/"
    upload_path = "upload/"

    S3_URL = os.environ.get("S3_ENDPOINT",None)
    S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY_ID",None)
    S3_SECRET_KEY = os.environ.get("S3_SECRET_ACCESS_KEY",None)
    S3_REGION = os.environ.get("S3_REGION",None)

    SOURCE_S3_BUCKET = os.environ.get("SOURCE_S3_BUCKET",None)
    TARGET_S3_BUCKET = os.environ.get("TARGET_S3_BUCKET",None)

    NUM_OF_FILES = int(os.environ["NUM_OF_FILES"])

    MINIO_URL = os.environ.get("MINIO_URL",None)
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY",None)
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY",None)
