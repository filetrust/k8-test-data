import os
import sys
from unittest import TestCase, mock
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from malicious_file_crawler.src.glasswall_crawler_runner import GlassWallRunner


class TestGlassWallCrawlerRunner(TestCase):
    def setUp(self):
        settings = get_project_settings()  # Scrapy settings
        self.process = CrawlerProcess(settings)
        self.runner = GlassWallRunner()

    def test_get_sites_to_run_single(self):
        sites = GlassWallRunner.get_sites_to_run(self, None)
        self.assertEquals(len(sites), 1)

    def test_get_sites_to_run_multiple(self):
        sites = GlassWallRunner.get_sites_to_run(self, scrape_site='SCRAPE_SITE,CORVUS')
        self.assertEquals(len(sites), 2)

    @mock.patch('scrapy.crawler.CrawlerProcess.crawl')
    @mock.patch('scrapy.crawler.CrawlerProcess.start')
    def test_run_spiders(self, mock_start, mock_crawl):
        sites = GlassWallRunner.get_sites_to_run(self, scrape_site='SCRAPE_SITE,CORVUS')
        cfg = sites['CORVUS']
        runner = GlassWallRunner.run_spiders(self, cfg)
        mock_crawl.assert_called_with('glasswall_spider', config=cfg, data=None)
        mock_start.assert_called_with()

    @mock.patch('malicious_file_crawler.src.glasswall_crawler_runner.GlassWallRunner.main')
    def test_main(self, mock_run_spider):
        self.runner.main("Spider")
        mock_run_spider.assert_called_with("Spider")
