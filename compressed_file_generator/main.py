import json
import logging as logger
import os
import shutil

import requests
from src.config import Config
from src.utils.compress import Compress

logger.basicConfig(level=logger.INFO)


class Process:
    def __init__(self):

        self.num_of_files = Config.NUM_OF_FILES
        self.target = Config.upload_path
        self.server_base_url = os.environ.get('server_base_url')
        self.not_allowed_types = ["zip", "7z", "rar", "tar", "gz"]

    def compress_file(self):
        try:
            target = self.target
            _files = os.listdir(Config.download_path)
            if not _files:
                logger.error("file of required file type not present inside the bucket")
            for f in _files:
                if os.path.isfile(Config.download_path + f):
                    file_path = Config.download_path + f
                    file_name = f.split(".")[0]
                    logger.info(f'zipping file {file_path}')

                    Compress.zip_compresstion(target, file_name, file_path)
                    Compress.seven_z_compresstion(target, file_name, file_path)
                    Compress.tar_compresstion(target, file_name, file_path)
                    Compress.gz_compresstion(target, file_name, file_path)
                    Compress.rar_compresstion(target, file_name, file_path)

        except Exception as err:
            logger.info(f"Process : compress : {err}")

    def upload_to_s3(self):
        try:
            _files = os.listdir(Config.upload_path)
            for file_name in _files:
                file = Config.upload_path + file_name
                folder_name = file_name.split(".")[-1]
                payload = {'bucket_name': os.environ["TARGET_S3_BUCKET"], 'folder_name': folder_name}
                files = {"file": (file_name, open(file, "rb")), }

                requests.post(self.server_base_url + "upload_to_s3", files=files, params=payload)
        except Exception as e:
            logger.info(f"Process : upload_to_s3 : {e}")
            raise e

    def list_files_from_minio(self, bucket_name):
        try:
            json = {'bucket_name': bucket_name}
            return requests.post(self.server_base_url + "list_files", json=json)
        except Exception as e:
            logger.error(f'MinioClient : list_files_from_minio : {e} ')

    def list_buckets_from_minio(self):
        try:
            return requests.post(self.server_base_url + "list_buckets")
        except Exception as e:
            logger.error(f'MinioClient : upload_stream : {e} ')

    def download_file_from_minio(self, bucket, file_name):
        try:
            json = {'bucket_name': bucket, "object_name": file_name}
            response = requests.get(self.server_base_url + "download_from_minio", json=json)
            logger.info(f'Response : {response.status_code}')

            if response.status_code == 200:
                f = open(Config.download_path + file_name, "wb")
                f.write(response.content)
                f.close()
                return True
            else:
                return False
        except Exception as e:
            logger.error(f'MinioClient : download_file_from_minio : {e} ')
            return False

    def download_n_files_from_minio(self, num_of_files):
        count = 0
        bucket_list = self.list_buckets_from_minio()
        if bucket_list.status_code == 200:
            bucket_list = json.loads(bucket_list.content)
            for bucket in bucket_list["list"]:
                files = self.list_files_from_minio(bucket_name=bucket)
                file_response = json.loads(files.content)
                for f in file_response['list']:
                    if count == num_of_files:
                        break
                    else:
                        if not bucket in self.not_allowed_types:
                            logger.info("download_file_from_minio")
                            status = self.download_file_from_minio(bucket=bucket, file_name=f)
                            if status:
                                count = count + 1


if __name__ == "__main__":

    try:
        if not os.path.exists(Config.download_path):
            os.makedirs(Config.download_path)
        if not os.path.exists(Config.upload_path):
            os.makedirs(Config.upload_path)

        process = Process()
        logger.info("main : Downloading malware files from minio")
        process.download_n_files_from_minio(Config.NUM_OF_FILES)

    except Exception as err:
        logger.error(f'Main : downlaod error : {err}')
        raise Exception(f'Main:Error while downloading files {err}')

    try:
        logger.info(f'Main :Sending file for zipping')
        process.compress_file()
        logger.info(f'Main : compression is done')
        logger.info(f'Main : Uploading compressed files to s3')
        process.upload_to_s3()
        logger.info(f'Main : Uploading is done')
    except Exception as err:
        logger.error(f'main: compress and upload file error : {err}')
        raise err

    try:
        shutil.rmtree(Config.download_path)
        shutil.rmtree(Config.upload_path)
    except Exception as err:
        logger.error((f'Error while deleted download upload path'))
        raise err
