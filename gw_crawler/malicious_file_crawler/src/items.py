# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class MaliciousFileCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    file_urls = scrapy.Field()
    extension = scrapy.Field(output_processor=TakeFirst())
    files = scrapy.Field()
    hash_api_url=scrapy.Field(output_processor=TakeFirst())
