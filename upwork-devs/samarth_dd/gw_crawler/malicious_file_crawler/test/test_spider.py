import os
from unittest import TestCase
from unittest.mock import Mock

from malicious_file_crawler.src.utils.read_config import ConfigReader

from gw_crawler.malicious_file_crawler.src.spiders.glasswall_crawler import GlasswallScraper


class TestGlasswallCrawler(TestCase):
    def setUp(self):
        site = 'corvus'
        config = ConfigReader(site.upper()).read_config()
        self.cfg = config
        self.scrapper = GlasswallScraper(self.cfg)

    def test_start_requests(self):
        self.url = os.environ['login_url']
        response = self.scrapper.start_requests()
        self.assertIsNotNone(response)

    def test_download_files(self):
        content = self.scrapper.download_files(os.getenv('login_url'))
        self.assertIsNotNone(content)

    def test_navigate_to(self):
        url = os.environ['file_page_url']
        response = self.scrapper.navigate_to(Mock())
        self.assertIsNotNone(response)


class TestDasMalwerkScraper:

    def test_start_requests(self):
        pass
