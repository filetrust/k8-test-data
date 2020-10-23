# -*- coding: utf-8 -*-
""" Scraper class for getting malicious files from tech defence portal """
import logging
from urllib.parse import urljoin

import scrapy
from scrapy.loader import ItemLoader
from src.items import MaliciousFileCrawlerItem
from src.spiders.scraper import Scraper
from src.utils.read_config import ConfigReader
logger = logging.getLogger(__name__)


class TekDefenceScraper(Scraper):
    """
        Crawler site https://das-malwerk.herokuapp.com/
        Getting the malware url from site and send it to storage pipeline
    """
    name = 'tekdefence'

    def __init__(self, config=None, data=None, *args, **kwargs):
        super(TekDefenceScraper, self).__init__(*args, **kwargs)
        self.cfg = ConfigReader(config.upper()).read_config()
        # self.cfg = config
        self.login_url = self.cfg.get('login_url')
        self.start_urls = [self.login_url]
        self.file_page_url = self.cfg.get("file_page_url")

    def start_requests(self):
        """ inbuilt start method called by scrapy when initializing crawler. """
        try:

            for url in self.start_urls:
                yield scrapy.Request(url,
                                     callback=self.navigate_to)
        except Exception as err:
            logger.error(f'TekDefenceScraper : start_requests : {err}')
            raise err

    def navigate_to(self, response):
        try:
            yield scrapy.Request(self.file_page_url,
                                 callback=self.download_files)
        except Exception as err:
            logger.error(f'TekDefenceScraper : navigate_to : {err}')
            raise err

    def download_files(self, response):
        # get download file link
        try:
            logger.info(f'TekDefenceScraper : parser : {response}')
            file_download_link_elements = response.xpath("//h3[@class='title']/a/@href")
            loader = ItemLoader(item=MaliciousFileCrawlerItem())
            for link_element in file_download_link_elements:
                link = link_element.get()
                absolute_path = urljoin(response.url, link)
                loader.add_value('file_urls', absolute_path)
                yield loader.load_item()

        except Exception as err:
            logger.error(f'TekDefenceScraper : download_files : {err}')
            raise err
