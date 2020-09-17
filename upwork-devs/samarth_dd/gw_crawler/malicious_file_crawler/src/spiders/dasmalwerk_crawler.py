# -*- coding: utf-8 -*-
""" Scraper class for getting malicious files from tech defence portal """
import requests
import scrapy
from urllib.parse import urljoin

from scrapy.http import TextResponse
from scrapy.loader import ItemLoader
from malicious_file_crawler.src.items import MaliciousFileCrawlerItem
from malicious_file_crawler.src.spiders.scraper import Scraper
from lxml import html as html_xml

class DasMalwerkScraper(Scraper):
    name = 'das_malwerk_scraper'
    # Allow duplicate url request (we will be crawling "page 1" twice)
    # custom_settings will only apply these settings in this spider
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self, config=None, data=None):
        super(DasMalwerkScraper, self).__init__()
        self.cfg = config
        self.file_urls = self.cfg.get('url')

    def start_requests(self):
        """ inbuilt start method called by scrapy when initializing crawler. """
        yield scrapy.Request(self.file_urls,callback=self.navigate_to)

    def navigate_to(self, response):
        yield scrapy.Request(self.file_urls,
                             callback=self.download_files)

    def download_files(self, response):
        # get download file link
        html= html_xml.fromstring(response.text)
        file_download_link_elements = html.xpath("//tr//td[2]/a/@href")

        loader = ItemLoader(item=MaliciousFileCrawlerItem())

        for link in file_download_link_elements:
            loader.add_value('file_urls', link)
            yield loader.load_item()






