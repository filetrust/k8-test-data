import os
from dotenv import load_dotenv

# env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()


class Config(object):
    DEBUG = True
    download_path = "/usr/src/app/download/"

    LOCAL_REPO_PATH = os.path.join(os.getcwd(), 's3_download', 'gov_uk')
    if not os.path.exists(LOCAL_REPO_PATH):
        os.makedirs(LOCAL_REPO_PATH)

    S3_URL = os.environ["S3_ENDPOINT"]
    S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY_ID"]
    S3_SECRET_KEY = os.environ["S3_SECRET_ACCESS_KEY"]
    S3_REGION = os.environ["S3_REGION"]
    S3_BUCKET = os.environ["S3_BUCKET"]

    S3_SUB_FOLDER_PREFIX = os.environ["S3_SUB_FOLDER_PREFIX"]
    RABBIT_MQ_API = os.environ["rabbit_mq_api"]

    MINIO_ENDPOINT = os.environ["MINIO_URL"]
    MINIO_SECRET_KEY = os.environ["MINIO_SECRET_KEY"]
    MINIO_ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]

    S3_LIST_BUCKET_FILES_URL = "http://localhost:5002/list_bucket_files"
    S3_FILE_DOWNLOAD_URL = "http://localhost:5002/s3_file_download"


