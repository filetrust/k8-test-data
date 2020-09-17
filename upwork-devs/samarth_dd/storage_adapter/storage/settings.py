import os
from dotenv import load_dotenv
load_dotenv()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURR_DIR = os.path.abspath(os.path.dirname(__file__))

CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.ini')


target_storage='MINIO'

#target_storage='S3'