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
from .utils.rabbit_client import RabbitClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MaliciousFileCrawlerPipeline(FilesPipeline):
    def file_downloaded(self, response, request, info, unzip_path=None):

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
            json_response = {}  # MaliciousCheck.check_malicious(file_path)
            metadata = FileService.get_file_meta(path)
            integrated_data = metadata.update(json_response)
            zip_path = unzip_path + "/"
            with open(zip_path + "metadata.txt", "w") as outfile:
                json.dump(metadata, outfile)
            with open(zip_path + "report.txt", "w") as outfile:
                json.dump(json_response, outfile)

            zipped_file = FileService.zip_files(file_path, key=key)

            payload = {"file": zipped_file}

            # Connect to RabbitMQ client and put a job in Remote Queue
            client = RabbitClient()
            client.publish_job(payload)

        return checksum
