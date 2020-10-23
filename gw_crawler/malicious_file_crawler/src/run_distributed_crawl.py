""" Main class for initializing and running crawlers. """
import logging
import os
import sys

from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from scrapyd_api import ScrapydAPI
from src.utils.read_config import ConfigReader

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

logger = logging.getLogger(__name__)
class DistributedCrawlRunner(object):
    """ Initialize crawler with project settings """

    def __init__(self, *spidercfg):
        self.settings = get_project_settings()  # Scrapy settings
        self.spidercfg = spidercfg
        self.scrapyd = ScrapydAPI(self.settings.get('SCRAPYD_ENDPOINT'))
        self.project_name = self.settings.get('PROJECT_NAME')
        self.extra_settings = {'JOBDIR': self.settings.get('JOB_DIR')}
        logger.info(f"Initialized ScrapydAPI object: {self.scrapyd} for Project: {self.project_name} with settings: {self.extra_settings}")


    """ Get all the sites to crawl from config file """

    def get_sites_and_config(self, scrape_site=None):

        if scrape_site is None:
            section = "SCRAPE_SITE"
            section = os.environ['SCRAPE_SITES']
            try:
                sites_arr = section.split(',')
                #config_obj = ConfigReader(section).read_config()
                #sites_arr = config_obj['scrape_sites'].split(',')
            except KeyError as ke:
                logger.error(f'DistributedCrawlRunner : get_sites_and_config : key error {ke} ')
                raise CloseSpider(reason="Error while getting site list from config.")

        else:
            sites_arr = scrape_site.split(",")

        site_cfg = {}

        # construct site_cfg dictionary: {site_name: site_cfg}
        for site in sites_arr:
            try:
                cfg = ConfigReader(site.upper()).read_config()
                site_cfg[site] = cfg
            except KeyError as ke:
                logger.error(f'DistributedCrawlRunner : get_sites_and_config : key error {ke}')
                raise CloseSpider

        logger.info(f'DistributedCrawlRunner: get_sites_and_config: site_cfg {site_cfg}')
        return site_cfg

    def schedule_job(self, site_arr):

        for site, cfg in site_arr.items():
            """ run crawler for every site and get response list """
            logger.info("Starting to schedule scrapyd process.")
            try:
                self.scrapyd.schedule(project=self.settings.get('PROJECT_NAME'),
                                      spider=cfg.get('name'),
                                      settings=self.extra_settings,
                                      config=site)
            except Exception as error:
                logger.error(f'DistributedCrawlRunner : schedule_job : error {error} ')
                raise Exception(f'error {error}')


if __name__ == '__main__':

    scraper = DistributedCrawlRunner()

    """ get site list and corresponding config into a dictionary """
    if len(sys.argv) == 2:
        scrape_site = sys.argv[1]
        site_list = scraper.get_sites_and_config(scrape_site=scrape_site)
    else:
        site_list = scraper.get_sites_and_config()

    scraper.schedule_job(site_list)
