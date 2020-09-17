from unittest import TestCase

from malicious_file_crawler.src.utils.read_config import ConfigReader


class TestUtil(TestCase):
    def test_config_reader(self):
        site = 'corvus'
        config = ConfigReader(site.upper()).read_config()
        self.assertIn('corvus',str(config).lower())
        self.assertIsNotNone(config)

