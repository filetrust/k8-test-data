import os
import time
import boto3
import logging
from botocore.client import Config
from botocore.exceptions import ClientError
from src.config import Config as AppConfig

logger = logging.getLogger("GW:s3")


class S3Client:
    def __init__(self, url, access_key, secret_key):
        self.url = url
        self.s3 = boto3.resource(
            "s3",
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4", s3={'addressing_style': 'virtual'}),
        )

    def upload_file(self, file_path, file_name, bucket):
        try:
            if (self.s3.Bucket(AppConfig.S3_BUCKET) in self.s3.buckets.all()) == False:
                self.s3.create_bucket(
                    Bucket=AppConfig.S3_BUCKET,
                    CreateBucketConfiguration={
                        'LocationConstraint': AppConfig.S3_REGION
                        }
                    )
            logger.info(
                "Uploading file to bucket {} minio {}".format(AppConfig.S3_BUCKET, self.url)
            )
            self.s3.Bucket(AppConfig.S3_BUCKET).upload_file(file_path, bucket + "/" + file_name)
            return AppConfig.S3_BUCKET + "/" + bucket + "/" + file_name
        except ClientError as e:
            logger.error(
                "Cannot connect to the S3 {}. Please vefify the Credentials.".format(
                    self.url
                )
            )
            logger.error(e)
        except Exception as e:
            logger.error("ex : {}".format(e))

    def upload_folder(self, file_path, file_name, bucket):
        try:
            if (self.s3.Bucket(AppConfig.S3_BUCKET) in self.s3.buckets.all()) == False:
                self.s3.create_bucket(
                    Bucket=AppConfig.S3_BUCKET,
                    CreateBucketConfiguration={
                        'LocationConstraint': AppConfig.S3_REGION
                        }
                    )
            logger.info(
                "Uploading file to bucket {} minio {}".format(AppConfig.S3_BUCKET, self.url)
            )
            self.s3.Bucket(AppConfig.S3_BUCKET).upload_file(file_path, bucket + "/" + file_name)
            return AppConfig.S3_BUCKET + "/" + bucket + "/" + file_name
        except ClientError as e:
            logger.error(
                "Cannot connect to the S3 {}. Please vefify the Credentials.".format(
                    self.url
                )
            )
            logger.error(e)
        except Exception as e:
            logger.error("ex : {}".format(e))

    def get_files(self, folder_name):
        try:
            bucket = self.s3.Bucket(AppConfig.S3_BUCKET)
            files = bucket.meta.client.list_objects(
                        Bucket=bucket.name,
                        Prefix=folder_name + "/",
                        )
            return files
        except Exception as ex:
            logger.error("error getting files from s3 {}".format(str(ex)))
