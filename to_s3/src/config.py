import os


def get_envar(k, required=True):
    val = os.environ.get(k, None)
    if not val and required:
        exit(f"{k} not supplied")
    return val


class Config(object):
    DEBUG = True
    download_path = "/usr/src/app/minio_files/"

    # Set S3 credentials
    S3_ENDPOINT = get_envar("S3_ENDPOINT", required=True)
    S3_ACCESS_KEY_ID = get_envar("S3_ACCESS_KEY_ID", required=True)
    S3_SECRET_ACCESS_KEY = get_envar("S3_SECRET_ACCESS_KEY", required=True)
    S3_REGION = get_envar("S3_REGION", required=False)

    # Set Minio Credentials
    MINIO_ENDPOINT = get_envar("MINIO_ENDPOINT", required=True)
    MINIO_ACCESS_KEY_ID = get_envar("MINIO_ACCESS_KEY_ID", required=True)
    MINIO_SECRET_ACCESS_KEY = get_envar("MINIO_SECRET_ACCESS_KEY", required=True)
    MINIO_SECURE = get_envar("MINIO_SECURE", required=False)
