import logging
import os
import sys

from malicious_file_crawler.storage.src.minio_service import MinioService

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
print(sys.path)

logger = logging.getLogger("GW:minio")


class MinioClient:

    @staticmethod
    def get_client():
        client = MinioService.get_storage_adapter()
        return client
