import requests

from src.constants import Constants
from src.logger import Logger
from src.utils import Utils

logger = Logger.get_logger()

class RSSGenerator:
    
    def generator_exist():
        status_code = 0
        try:
            status_code = Utils.get_request(Constants.api_url).status_code
        except:
            logger.info("The Scrape2RSS feature is disable")
        return status_code == 200

    def __init__(self, url) -> None:
        self.url = url

    def render_xml_feed(self):
        api_gen_url = Constants.api_url + "/create?url=" + self.url
        return Utils.get_request(api_gen_url).text