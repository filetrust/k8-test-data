import os
from dotenv import load_dotenv

# env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()


class Config(object):
    DEBUG = True
    download_path = "/usr/src/app/download/"

    COMPRESSION_LEVEL = os.environ["COMPRESSION_DEPTH"]

    LOCAL_REPO_PATH = os.path.join(os.getcwd(), 'multilevel_folder')
    if not os.path.exists(LOCAL_REPO_PATH):
        os.mkdir(LOCAL_REPO_PATH)

    S3_URL = os.environ["S3_ENDPOINT"]
    S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY_ID"]
    S3_SECRET_KEY = os.environ["S3_SECRET_ACCESS_KEY"]
    S3_REGION = os.environ["S3_REGION"]
    S3_BUCKET = os.environ["S3_BUCKET"]
    FINAL_S3_BUCKET = os.environ["FINAL_S3_BUCKET"]
    S3_FOLDER_NAME = os.environ["S3_FOLDER_NAME"]
