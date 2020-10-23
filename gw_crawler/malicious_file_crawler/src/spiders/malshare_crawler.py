# coding: utf-8
# !/usr/bin/env python
import logging
import os

import requests
import scrapy
from scrapy.loader import ItemLoader
from src.items import MaliciousFileCrawlerItem
from src.spiders.scraper import Scraper
from src.utils.read_config import ConfigReader
logger = logging.getLogger(__name__)


class MalShareScraper(Scraper):
    """
            malhare url http://www.malshare.com
            api url http://www.malshare.com/api.php
            Get the malware url using hashes and api and send it to storage
    """
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    name = 'malshare'

    # Allow duplicate url request (we will be crawling "page 1" twice)
    # custom_settings will only apply these settings in this spider

    def __init__(self, config=None, data=None, *args, **kwargs):
        super(MalShareScraper, self).__init__( *args, **kwargs)
        self.cfg = ConfigReader(config.upper()).read_config()
        #self.cfg = config
        self.API_KEY = self.cfg.get('api_key',vars=os.environ)
        self.API_URL = self.cfg.get('api_base_url')
        self.base_url = self.cfg.get('base_url')
        self.url = self.cfg.get('api_url')

    def start_requests(self):
        try:
            logger.info(f'Site url : {self.base_url}')
            yield scrapy.Request(url="http://google.com", callback=self.parser)
        except Exception as err:
            logger.error(f'MalShareScraper : start_requests : {err}')
            raise err

    def parser(self, response):
        try:
            logger.info(f'MalShareScraper : response : {response}')
            hashes = self.get_hases()
            for _hash in hashes:
                logger.info(f'MalShareScraper : parser : {_hash}')
                details = self.getfiledetails(file_hash=_hash)
                logger.info(f'details of file {details}')
                logger.info(f'F type {details["F_TYPE"]}')
                url = self.url.format(self.API_KEY, _hash)
                loader = ItemLoader(item=MaliciousFileCrawlerItem())
                loader.add_value('file_urls', url)
                loader.add_value('extension', details["F_TYPE"])
                loader.add_value('hash_api_url', self.url.format(None, _hash))
                yield loader.load_item()

        except Exception as err:
            logger.error(f'MalShareScraper : parser : {err}')
            raise err

    def get_response(self, payload, output='json'):
        """
        Base Method to query to Malshare API server for different options.
        :param payload: API Request Parameters
        :param output: Output Format - JSON or RAW
        :return: Response
        """
        try:
            resp = requests.get(self.API_URL, params=payload)
            if resp is not None:
                if output == 'json':
                    return resp.json()
                elif output == 'raw':
                    return resp.text
        except Exception as error:
            raise error
        else:
            return False

    def get_hases(self):
        try:
            json_hash = self.getlist()
            raw_hash = self.getlistraw()
            hashes = []
            response = raw_hash.split('\n')
            for each in response:
                try:
                    hashes.append(each.split(" ")[0])
                except Exception as error:
                    continue
            return hashes
        except Exception as error:
            raise error

    def getlist(self):
        """
        List hashes from the past 24 hours
        :return: Response as JSON
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getlist'})

    def getlistraw(self):
        """
        List hashes from the past 24 hours
        :return: Response as RAW Text
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'getlistraw'}, 'raw')

    def getfiledetails(self, file_hash, output='json'):
        """
        GET stored sample file details
        :param file_hash: Sample Hash
        :param output: Type of Output - JSON or RAW
        :return: Response as JSON
        """
        return self.get_response({'api_key': self.API_KEY, 'action': 'details', 'hash': file_hash}, output)
