import logging
import os
import sys

import requests

sys.path.append(os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ))
)

logger = logging.getLogger("GW:minio")


class MinioClient:
    """
            It calls storage adapter to get minio client
    """
    server_base_url = os.environ["storage_adapter_url"]

    @staticmethod
    def upload_file(bucket_name, minio_path, file, server_base_url=server_base_url):
        try:
            data = {'bucket_name': bucket_name,
                    "minio_path": minio_path,
                    "file": file, }
            return requests.post(server_base_url + "upload", json=data)
        except Exception as e:
            logger.error(f'MinioClient : upload_file : {e} ')

    @staticmethod
    def upload_stream(bucket_name, name, data, length, metadata, server_base_url=server_base_url):
        try:
            params = {'bucket_name': bucket_name, 'name': name, 'length': length, 'metadata': metadata}
            return requests.post(server_base_url + "upload_stream", data=data, params=params)
        except Exception as e:
            logger.error(f'MinioClient : upload_stream : {e} ')
