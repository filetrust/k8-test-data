# Scrapy settings for malicious_file_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

from src.constants import DOWNLOAD_PATH
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
from dotenv import load_dotenv
env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

PROJECT_NAME = 'malicious_file_crawler'
# Define JOBDIR path for pausing and resuming crawls
#JOB_DIR = 'crawlers/spider-1'

date = datetime.strftime(datetime.now(), '%Y%m%d')

EXTENSIONS = {
   'scrapy_dotpersistence.DotScrapyPersistence': 0,
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Get the path to the directory this file is in
CURR_DIR = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'src'

SPIDER_MODULES = ['src.spiders']
NEWSPIDER_MODULE = 'src.spiders'

# Config file path
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.ini')

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'malicious_file_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32
REACTOR_THREADPOOL_MAXSIZE = 20

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "src.pipelines.MaliciousFileCrawlerPipeline": 1,
    'src.middlewares.MaliciousFileCrawlerDownloaderMiddleware': 543,

}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "src.pipelines.MaliciousFileCrawlerPipeline": 300,
}

DOWNLOAD_TIMEOUT = 12000

MEDIA_ALLOW_REDIRECTS = True
FILES_STORE = DOWNLOAD_PATH

# Uncomment this when MINIO service is running
# max download size of 5gb
DOWNLOAD_MAXSIZE = 5368709120

# scrapyd endpoint
SCRAPYD_ENDPOINT =  os.environ.get('scrapyd_endpoint','http:0.0.0.0:6800/')

XTENSIONS = {

    'scrapy_dotpersistence.DotScrapyPersistence': 0
}

DOTSCRAPY_ENABLED = True

ADDONS_AWS_ACCESS_KEY_ID = os.environ.get("ADDONS_AWS_ACCESS_KEY_ID")
ADDONS_AWS_SECRET_ACCESS_KEY = os.environ.get("ADDONS_AWS_SECRET_ACCESS_KEY")
ADDONS_AWS_USERNAME =  os.environ.get("ADDONS_AWS_USERNAME")
ADDONS_S3_BUCKET = os.environ.get("ADDONS_S3_BUCKET")


HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 60 * 60 * 24 * 7
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


