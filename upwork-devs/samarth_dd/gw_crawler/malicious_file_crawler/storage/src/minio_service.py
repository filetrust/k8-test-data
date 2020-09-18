import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from storage.src.minio_adapter import MinioAdapter
from storage import settings
from storage.utils.read_confg import ConfigReader

logging.basicConfig(filename="testdata.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class MinioService(object):
    @staticmethod
    def get_storage_adapter():
        storage_type = settings.target_storage
        section = storage_type.upper()
        config = ConfigReader(section).read_config()
        return MinioAdapter(config)
