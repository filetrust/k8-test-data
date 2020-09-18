# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import os

from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.misc import md5sum
from six import BytesIO

from .constants import base_unzip_path, zip_download_path
from .utils.file_service import FileService
from .utils.malicious_check import MaliciousCheck
from .utils.minio_client import MinioClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MaliciousFileCrawlerPipeline(FilesPipeline):

    def file_downloaded(self, response, request, info, unzip_path=None):
        bucket_name = os.environ['bucket_name']
        path = self.file_path(request, response=response, info=info)
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        buf.seek(0)
        self.store.persist_file(path, buf, info)

        file_path = zip_download_path + "/" + path
        key = path.split("/")[-1].split(".")[0]

        FileService.unzip_files(file_path, key)
        unzip_path = base_unzip_path + "/" + key

        for file in os.listdir(unzip_path):
            file_path = unzip_path + "/" + file
            json_response = MaliciousCheck.check_malicious(file_path)
            metadata = FileService.get_file_meta(path)
            integrated_data = metadata.update(json_response)
            zip_path = unzip_path + "/"
            with open(zip_path + 'metadata.txt', 'w') as outfile:
                json.dump(metadata, outfile)

            f = unzip_path + "/"
            zipped_file = FileService.zip_files(f, key=key)

            client = MinioClient.get_client()
            if not client.bucket_exists(bucket_name):
                client.create_bucket(bucket_name)
            client.upload_file(bucket_name, path.split("/")[-1], zipped_file)

        return checksum
