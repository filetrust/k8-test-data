import json
import logging
import os
import time

import requests

# -*- coding: utf-8 -*-
""" Scraper class for getting malicious files from virus share portal """
import scrapy

from src.spiders.scraper import Scraper
from scrapy.loader import ItemLoader
from src.items import MaliciousFileCrawlerItem
from src.utils.read_config import ConfigReader
logger = logging.getLogger(__name__)

class VirusShareScraper(Scraper):
    """
        virus share api https://virusshare.com/apiv2/
        hash url https://virusshare.com/hashfiles/unpacked_hashes.md5
        Get the virus share url using hashes and api and send it to storage
    """
    name = 'virusshare'
    # Allow duplicate url request (we will be crawling "page 1" twice)
    # custom_settings will only apply these settings in this spider
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 1,
        'DOWNLOAD_DELAY': 16,

    }

    def __init__(self, config=None, data=None, *args, **kwargs):
        super(VirusShareScraper, self).__init__(*args, **kwargs)
        self.cfg = ConfigReader(config.upper()).read_config()
        # self.cfg = config
        self.base_url = self.cfg.get('base_url')
        self.url = self.cfg.get('virusshare_url')
        self.hash_url = self.cfg.get('virusshare_hash_url')
        self.request_mode = "download"
        self.api_key = self.cfg.get('vs_api_key', vars=os.environ)

    def start_requests(self):
        """
            start_requests get hashes and send it to parser
        """
        try:
            logger.info(f'Site url : {self.base_url}')
            hashes = self.scrape_hashes()
            for _hash in hashes:
                yield scrapy.Request(url=self.base_url, callback=self.parser, meta={'hash': _hash})
        except Exception as error:
            logger.error(f"VirusShareScraper:start_requests: {error}")
            raise error

    def parser(self, response):
        """
            Retrieves api url and get file type and load it to loader
        """
        try:
            logger.info(f"VirusShareScraper : parser : hash : {response.meta['hash']}")
            if response.status == 200:
                url = self.url.format(self.request_mode, self.api_key, response.meta['hash'])
                file_details_url = self.url.format("file", self.api_key, response.meta['hash'])
                details = VirusShareScraper.get(file_details_url)
                time.sleep(16)
                loader = ItemLoader(item=MaliciousFileCrawlerItem())
                if details.status_code==200 :
                    json_str = details.content
                    try:
                        if json_str :
                            json_details = json.loads(json_str)
                            loader.add_value('extension', json_details['exif']['FileTypeExtension'])
                    except:
                        pass
                loader.add_value('file_urls', url)
                loader.add_value('hash_api_url', self.url.format(self.request_mode, None, response.meta['hash']))
                yield loader.load_item()

        except Exception as err:
            logger.error(f'VirusShareScraper : parser : {err}')
            raise err

    def scrape_hashes(self):
        """
        Retrieve all hashes from  VS and save to csv file
        """
        response = VirusShareScraper.get(self.hash_url)

        hashes = []
        response = response.content.split(b'\n')

        for each in response[1:-2]:
            try:
                hashes.append(each.split(b"  ")[1].decode("utf-8"))
            except Exception as error:
                continue
        return hashes

    @staticmethod
    def get(url):
        headers = {
            "Accept": "text/html, application/xhtml+xml, application/xml",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US, en",
            "User-Agent": "Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        }
        """
        Fetch url
        """
        try:
            response = requests.get(url, headers=headers)
            return response
        except Exception:
            return False