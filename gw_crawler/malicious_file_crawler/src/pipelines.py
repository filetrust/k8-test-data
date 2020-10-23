# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import hashlib
import logging
import mimetypes
import os

from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.misc import md5sum
from scrapy.utils.python import to_bytes
from six import BytesIO

from .constants import DOWNLOAD_PATH
from .utils.minio_client import MinioClient

logger = logging.getLogger(__name__)
from itemadapter import ItemAdapter
from scrapy.http import Request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MaliciousFileCrawlerPipeline(FilesPipeline):

    def __init__(self, *a, **kw):
        super(MaliciousFileCrawlerPipeline, self).__init__(*a, **kw)
        self.extension = None
        self.hash_api_url = None
        self.url = None

    def file_downloaded(self, response, request, info, unzip_path=None):
        """
            Downloads file
            Check metadat of file and gets extension
            Store it in minio with spidername as bucketname
        """
        logger.info(f'MaliciousFileCrawlerPipeline:file_downloaded:: Spider Name {info.spider.name}')
        path = self.file_path(request, response=response, info=info)
        buf = BytesIO(response.body)
        try:
            logger.info(f'MaliciousFileCrawlerPipeline:file_downloaded:: Response status {response.status}')
            if (response.status == 200):
                checksum = md5sum(buf)
                buf.seek(0)
                self.store.persist_file(path, buf, info)
                downloaded_file_path = DOWNLOAD_PATH + path
                extension = path.split("/")[-1].split('.')[-1]
                if extension:
                    bucket_name = extension.lower()
                else:
                    bucket_name = 'hash'
                minio_path = path.split("/")[-1]
                file_stat = os.stat(downloaded_file_path)

                metadata = {"url": self.url}
                self.store_data_stream(bucket_name=bucket_name, minio_path=minio_path, data=response.body,
                                       length=file_stat.st_size, metadata=str(metadata))

                return checksum

        except Exception as err:
            logger.error(f'MaliciousFileCrawlerPipeline:file_downloaded: {err}')
            raise err

    def get_media_requests(self, item, info):
        try:
            urls = ItemAdapter(item).get(self.files_urls_field, [])
            ext = ItemAdapter(item).get('extension', [])
            self.hash_api_url = ItemAdapter(item).get('hash_api_url', [])
            if (ext):
                self.extension = "." + ext

            return [Request(u) for u in urls]
        except Exception as error:
            logger.error(f'MaliciousFileCrawlerPipeline : get_media_requests : {error}')
            raise error

    def file_path(self, request, response=None, info=None):
        self.url=request.url
        vs_key=os.environ.get('VIRUSSHARE_API_KEY')
        mal_key=os.environ.get('MALSHARE_API_KEY')

        self.url=self.url.replace(vs_key, "")
        self.url=self.url.replace(mal_key, "")

        logger.info(f'MaliciousFileCrawlerPipeline : file_path : malware url :  {self.url}')
        media_guid = hashlib.sha1(to_bytes(self.url)).hexdigest()
        media_ext = os.path.splitext(request.url)[1]
        # Handles empty and wild extensions by trying to guess the
        # mime type then extension or default to empty string otherwise
        if media_ext not in mimetypes.types_map:
            if (self.extension):
                media_ext = self.extension.lower()
            else:
                media_ext = ''
            media_type = mimetypes.guess_type(request.url)[0]
            if media_type:
                media_ext = mimetypes.guess_extension(media_type)
        return 'full/%s%s' % (media_guid, media_ext)

    def store_data_stream(self, bucket_name, minio_path, data, length, metadata):
        """
            Create bucket
            Store object in minio
        """
        try:
            MinioClient.upload_stream(bucket_name=bucket_name, name=minio_path, data=data, length=length,
                                      metadata=metadata)
        except Exception as error:
            logger.error(f'BundleZip:store:Error while processing file {error}')
            raise error
