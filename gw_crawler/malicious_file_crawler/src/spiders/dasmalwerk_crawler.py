# -*- coding: utf-8 -*-
""" Scraper class for getting malicious files from tech defence portal """
import logging

import scrapy
from lxml import html as html_xml
from scrapy.loader import ItemLoader
from src.items import MaliciousFileCrawlerItem
from src.spiders.scraper import Scraper
from src.utils.read_config import ConfigReader
logger = logging.getLogger(__name__)


class DasMalwerkScraper(Scraper):
    """
        Crawler site http://www.tekdefense.com/downloads/malware-samples/
        Getting the malware url from site and send it to storage pipeline
    """
    name = 'dasmalwerk'

    def __init__(self, config=None, data=None, *args, **kwargs):
        super(DasMalwerkScraper, self).__init__( *args, **kwargs)
        self.cfg = ConfigReader(config.upper()).read_config()
        #self.cfg = config
        self.file_urls = self.cfg.get('url')

    def start_requests(self):
        """ inbuilt start method called by scrapy when initializing crawler. """
        try:
            yield scrapy.Request(self.file_urls, callback=self.navigate_to)
        except Exception as err:
            logger.error(f"DasMalwerkScraper:start_requests {err}")
            raise err

    def navigate_to(self, response):
        try:
            yield scrapy.Request(self.file_urls,
                                 callback=self.download_files)
        except Exception as err:
            logger.error(f"DasMalwerkScraper:navigate_to {err}")
            raise err

    def download_files(self, response):
        # get download file link
        try:
            logger.info(f'DasMalwerkScraper : download_files : {response}')
            html = html_xml.fromstring(response.text)
            file_download_link_elements = html.xpath("//tr//td[2]/a/@href")
            loader = ItemLoader(item=MaliciousFileCrawlerItem())
            print('kks')
            print(len(file_download_link_elements))
            for link in file_download_link_elements:
                # self.state['items_count'] = self.state.get('items_count', 0) + 1
                loader.add_value('file_urls', link)
                yield loader.load_item()
        except Exception as err:
            logger.error(f"DasMalwerkScraper:download_files {err}")
            raise err
