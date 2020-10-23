import os
import sys
import time
import boto3
import logging
from botocore.client import Config
from botocore.exceptions import ClientError

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
        print("uploading", file_name, file_path)
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

    def download_files(self, bucket_name, num_files, file_download_path=None):

        try:
            file_path = file_download_path or ""
            # if not os.path.exists(Config.download_path):
            # # os.makedirs(Config.download_path)
            logger.info("Check if the Bucket {} exists".format(bucket_name))
            if self.s3.Bucket(bucket_name) not in self.s3.buckets.all():
                raise Exception(f"{bucket_name} bucket does not exist")
            bucket = self.s3.Bucket(bucket_name)
            files_list = []
            saved_files = 0
            for files in bucket.objects.all():
                try:
                    path, filename = os.path.split(files.key)
                    obj_file = file_path + filename
                    logger.info("Downloading file {}.".format(filename))
                    bucket.download_file(files.key, obj_file)
                    files_list.append(obj_file)
                    saved_files += 1
                    if saved_files == num_files:
                        break
                except Exception as ex:
                    continue
            return files_list
        except ClientError as e:
            logger.error(
                "Cannot Connect to the Minio {}. Please Verify your credentials.".format(
                    self.url
                )
            )
        except Exception as e:
            logger.error(e)

