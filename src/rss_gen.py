import requests

from src.constants import Constants

class RSSGenerator:
    
    def generator_exist():
        status_code = requests.get(Constants.api_url).status_code
        return status_code == 200

    def __init__(self, url) -> None:
        self.url = url

    def render_xml_feed(self):
        api_gen_url = Constants.api_url + "/create?url=" + self.url
        return requests.get(api_gen_url).text