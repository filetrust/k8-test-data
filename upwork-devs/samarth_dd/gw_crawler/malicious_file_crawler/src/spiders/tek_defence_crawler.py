# -*- coding: utf-8 -*-
""" Scraper class for getting malicious files from tech defence portal """
from urllib.parse import urljoin

import scrapy
from malicious_file_crawler.src.items import MaliciousFileCrawlerItem
from malicious_file_crawler.src.spiders.scraper import Scraper
from scrapy.loader import ItemLoader


class TekDefenceScraper(Scraper):
    name = 'tek_defence_spider'

    # Allow duplicate url request (we will be crawling "page 1" twice)
    # custom_settings will only apply these settings in this spider
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self, config=None, data=None):
        super(TekDefenceScraper, self).__init__()
        self.cfg = config
        self.login_url = self.cfg.get('login_url')
        self.start_urls = [self.login_url]
        self.file_page_url = self.cfg.get("file_page_url")

    def start_requests(self):
        """ inbuilt start method called by scrapy when initializing crawler. """

        for url in self.start_urls:
            yield scrapy.Request(url,
                                 callback=self.navigate_to)

    def navigate_to(self, response):
        yield scrapy.Request(self.file_page_url,
                             callback=self.download_files)

    def download_files(self, response):

        # get download file link
        file_download_link_elements = response.xpath("//h3[@class='title']/a/@href")
        loader = ItemLoader(item=MaliciousFileCrawlerItem())
        for link_element in file_download_link_elements:
            link = link_element.get()
            absolute_path = urljoin(response.url, link)
            loader.add_value('file_urls', absolute_path)
            yield loader.load_item()
