import os
import sys
import time
import boto3
import logging
from botocore.client import Config
from botocore.exceptions import ClientError
from flask import send_from_directory


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

    def list_s3_bucket_files(self, bucket_name, sub_dir):

        file_list = []
        if self.s3.Bucket(bucket_name) not in self.s3.buckets.all():
            raise Exception(f"{bucket_name} bucket does not exist")
        bucket = self.s3.Bucket(bucket_name)

        bucket_file_list = bucket.objects.all() if sub_dir == "" else bucket.objects.filter(Prefix=sub_dir)

        for file in bucket_file_list:
            file_list.append(file.key)

        return file_list

    def download_single_s3_file(self, bucket_name, file_key, file_name):

        bucket = self.s3.Bucket(bucket_name)
        try:
            file_download_obj = bucket.download_file(file_key,
                                                     os.path.join(AppConfig.s3_download_path,
                                                                  file_name))
            logger.info(file_download_obj)

        except Exception as e:
            logger.error(e)
            raise e

        return 1

    def upload_file(self, file, file_name, bucket,folder=None):
        try:
            if (self.s3.Bucket(bucket) in self.s3.buckets.all()) == False:
                self.s3.create_bucket(
                    Bucket=bucket,
                    CreateBucketConfiguration={
                        'LocationConstraint': os.environ['S3_REGION']
                    }
                )
            logger.info(
                "Uploading file to bucket {} s3 {}".format(bucket, self.url)
            )
            if folder:
                self.s3.Bucket(bucket).upload_file(file, folder + "/" + file_name)
            else:
                self.s3.Bucket(bucket).upload_file(file, file_name)

            return bucket + "/" + folder + "/" + file_name

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
                    obj_file = file_path +"/"+filename
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
                "Cannot Connect to the s3 {}. Please Verify your credentials.".format(
                    self.url
                )
            )
        except Exception as e:
            logger.error(e)

    def download_subdirectory_files(self, bucket_name, subdir, num_files, file_download_path=None):
        logger.info("S3ClientUpdated::download_subdirectory_files "
                    "Received request to download files from subdirectory {} "
                    "with file download path {}".format(subdir, file_download_path))
        try:
            file_path = file_download_path or ""
            logger.info("Check if the Bucket {} exists".format(bucket_name))
            if self.s3.Bucket(bucket_name) not in self.s3.buckets.all():
                raise Exception(f"{bucket_name} bucket does not exist")
            bucket = self.s3.Bucket(bucket_name)
            files_list = []
            saved_files = 0
            for files in bucket.objects.filter(Prefix=subdir):
                # print(files)
                try:
                    path, filename = os.path.split(files.key)
                    obj_file = file_path +"/"+ filename

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

