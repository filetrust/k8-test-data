import logging

from minio import Minio
from src.config import Config

logger = logging.getLogger("GW: RabbitMQ Publisher")


class MinioClient(object):

    def __init__(self):
        try:
            self.minio = Minio(endpoint=Config.MINIO_ENDPOINT,
                               access_key=Config.MINIO_ACCESS_KEY_ID,
                               secret_key=Config.MINIO_SECRET_ACCESS_KEY,
                               secure=bool(Config.MINIO_SECURE))
            logger.info("Connected to Minio Server")
        except KeyError as err:
            logger.error(err)
            raise Exception("Error! Please set appropriate values .env file.")

    def bucket_exists(self, bucket_name):
        if self.minio.bucket_exists(bucket_name):
            return True
        return False

    def get_all_files(self, bucket_name):
        if self.bucket_exists(bucket_name):
            try:
                minio_objs = self.minio.list_objects(bucket_name)
                return [objs.object_name for objs in minio_objs]
            except Exception as err:
                raise err

    def get_all_buckets(self):
        try:
            list = []
            bucket_list = self.minio.list_buckets()
            for bucket in bucket_list:
                list.append(bucket.name)
            logger.info(f'Buckets are {list}')
            return list
        except Exception as err:
            raise err
