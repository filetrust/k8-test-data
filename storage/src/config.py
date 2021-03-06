import os
from dotenv import load_dotenv
env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()


class Config(object):
    DEBUG = True
    download_path = "/usr/src/app"

    s3_download_path = "src/download"
    if not os.path.exists(s3_download_path):
        os.makedirs(s3_download_path)

    S3_URL = os.environ["S3_ENDPOINT"]
    S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY_ID"]
    S3_SECRET_KEY = os.environ["S3_SECRET_ACCESS_KEY"]
    S3_REGION = os.environ["S3_REGION"]

    MINIO_ENDPOINT = os.environ["MINIO_HOSTNAME"]
    MINIO_SECRET_KEY = os.environ["MINIO_ACCESS_KEY_ID"]
    MINIO_ACCESS_KEY = os.environ["MINIO_SECRET_ACCESS_KEY"]

    minio_downlaod="src/download"
    s3_upload_path = "src/upload"

    azure_account_key=os.environ.get("azure_account_key",None)
    azure_account_name=os.environ.get("azure_account_name",None)

    conn_str=os.environ.get("conn_str",None)
    share_name =os.environ.get("share_name",None)
    parent_dir_name =os.environ.get("parent_dir_name",None)
