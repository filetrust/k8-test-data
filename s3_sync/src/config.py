import os


def get_envar(k, required=True):
    val = os.environ.get(k, None)
    if not val and required:
        exit(f"{k} not supplied")
    return val


class Config(object):
    DEBUG = True
    download_path = "/usr/src/app/downloads"

    S3_URL = get_envar("S3_ENDPOINT", required=True)
    S3_ACCESS_KEY = get_envar("S3_ACCESS_KEY_ID", required=True)
    S3_SECRET_KEY = get_envar("S3_SECRET_ACCESS_KEY", required=True)
    S3_REGION = get_envar("S3_REGION", required=True)
    S3_BUCKET = get_envar("S3_BUCKET", required=True)
    
    MINIO_URL = get_envar("MINIO_URL", required=True)
    MINIO_ACCESS_KEY = get_envar("MINIO_ACCESS_KEY", required=True)
    MINIO_SECRET_KEY = get_envar("MINIO_SECRET_KEY", required=True)

    SQLALCHEMY_DATABASE_URI = get_envar("DB_URL", required=True)
