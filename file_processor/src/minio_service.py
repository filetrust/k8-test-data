import logging

from botocore.exceptions import ClientError
from minio import Minio

logger = logging.getLogger("GW:minio")


class MinioService:
    """
            It calls storage adapter to get minio client
    """

    def __init__(self, url, access_key, secret_key):
        self.url = url
        self.minio_client = Minio(endpoint=url, access_key=access_key,
                                  secret_key=secret_key, secure=False)

    def upload(self, file_path, bucket_name, file_name):
        try:
            if not self.minio_client.bucket_exists(bucket_name):
                self.minio_client.make_bucket(bucket_name)
            logger.info("Uploading file to bucket {} minio {}".format(bucket_name, self.url))
            self.minio_client.fput_object(bucket_name=bucket_name, file_path=file_path, object_name=file_name)
        except ClientError as e:
            logger.error(
                "Cannot connect to the minio {}. Please vefify the Credentials.".format(
                    self.url
                )
            )
        except Exception as e:
            logger.error(f'Minio_Service : upload : {e} ')

    def download_files(self, bucket_name, file_name, download_path):
        try:
            path = download_path + "/" + file_name
            self.minio_client.fget_object(bucket_name=bucket_name, object_name=file_name, file_path=path)

        except ClientError as e:
            logger.error(
                "Cannot connect to the minio {}. Please vefify the Credentials.".format(
                    self.url
                )
            )
        except Exception as e:
            logger.error(f'Minio_service: download_files : {e} ')

    def get_stat(self, bucket_name, file_name):
        stat = None
        try:
            stat = self.minio_client.stat_object(bucket_name=bucket_name, object_name=file_name)
        except ClientError as e:
            logger.error(
                "Cannot connect to the minio {}. Please vefify the Credentials.".format(
                    self.url
                )
            )
        except Exception as e:
            logger.error(f'Minio_Service : get_stat : {e} ')
            pass

        if stat:
            if not stat.metadata:
                stat = None
        return stat

