# -*- coding: utf-8 -*-
""" Scraper class for getting malicious files from tech defence portal """
import logging

import requests
import scrapy
from itemloaders import ItemLoader
from lxml import html as html_xml
from src.items import MaliciousFileCrawlerItem
from src.spiders.scraper import Scraper
from src.utils.read_config import ConfigReader
logger = logging.getLogger(__name__)


class ZooScraper(Scraper):
    """
        base_url=https://github.com
        zoo_url= https://github.com/ytisf/theZoo/tree/master/malwares/Binaries
        Getting the malware url from site and send it to storage pipeline
    """
    name = 'zoo'

    def __init__(self, config=None, data=None, *args, **kwargs):
        super(ZooScraper, self).__init__(*args, **kwargs)
        self.cfg = ConfigReader(config.upper()).read_config()
        # self.cfg = config
        self.file_urls = self.cfg.get('zoo_url')
        self.base_url = self.cfg.get('base_url')

    def start_requests(self):
        """ inbuilt start method called by scrapy when initializing crawler. """
        try:
            logger.info(f'crawling url : {self.file_urls}')
            yield scrapy.Request(self.file_urls, callback=self.navigate_to)
        except Exception as err:
            logger.error(f'ZooScraper : start_requests : {err}')
            raise err

    def navigate_to(self, response):
        try:
            yield scrapy.Request(self.file_urls,
                                 callback=self.download_files)
        except Exception as err:
            logger.error(f'ZooScraper : navigate_to : {err}')
            raise err

    def download_files(self, response):
        try:
            logger.info(f'ZooScraper : download_files : {response}')
            zip_urls = []
            # get download file link
            html = html_xml.fromstring(response.text)

            links = html.xpath("//a[@class='js-navigation-open link-gray-dark']/@href")
            print('jjdd')
            print(len(links))
            # url=self.base_url+links[3]
            for url in links:
                git_url = self.base_url + url
                response = requests.get(git_url)
                html = html_xml.fromstring(response.text)
                zip_links = html.xpath("//a[@class='js-navigation-open link-gray-dark']/@href")

                zip_url = self.base_url + zip_links[3]
                zip_urls.append(zip_url)
                loader = ItemLoader(item=MaliciousFileCrawlerItem())
                loader.add_value('file_urls', zip_url)
                yield loader.load_item()

        except Exception as err:
            logger.error(f'ZooScraper : download_files : {err}')
            raise err
