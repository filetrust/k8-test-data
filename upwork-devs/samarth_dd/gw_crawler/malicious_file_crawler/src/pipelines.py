# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from contextlib import suppress
from os.path import isfile

from itemadapter import ItemAdapter

import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy.utils.misc import md5sum
from six import BytesIO
import sys

from src.virtual_total import Virustotal

from .utils.file_service import FileService
from .utils.malicious_check import MaliciousCheck

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MaliciousFileCrawlerPipeline(FilesPipeline):

    def file_downloaded(self, response, request, info):
        path = self.file_path(request, response=response, info=info)
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        buf.seek(0)

        self.store.persist_file(path, buf, info)

