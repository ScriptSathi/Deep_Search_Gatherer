import os, json
from typing import List

from src.constants import Constants
from src.logger import Logger
from src.utils import Utils

logger = Logger.get_logger()

class Parser:
    def __init__(self) -> None:
        self.config = self._load_config()

    def get_token(self) -> str:
        return self.config['token']

    def get_feeds(self) -> List['str']:
        return self.config['feeds']

    def get_config(self):
        return self.config

    def _is_valid_json_file(self, file_path) -> bool:
        try:
            if os.path.isfile(file_path):
                json_config_content = open(file_path,'r').read()
                self.config = json.loads(json_config_content)
                return True
        except Exception:
            logger.info(f'You must submit a valid file in path: {Constants.json_conf_path_dir} file dir')
            return False

    def _file_name(self) -> str:
        file_list = os.listdir(Constants.json_conf_path_dir)
        for file in file_list:
            if ".json" in file:
                return file

    def _load_config(self) -> str:
        config = Constants.default_config
        json_config_path = os.path.join(Constants.json_conf_path_dir, self._file_name())

        if self._is_valid_json_file(json_config_path):

            for key, value in self.config.items():
                config[key] = value

        for feed in config["feeds"]:
            if "name" not in feed:
                current_index = config["feeds"].index(feed)
                feed["name"] = f"feed-{str(current_index)}"

            if "published_since" not in feed:
                feed["published_since"] = config["published_since_default"]
            
            if "refresh_time" not in feed:
                feed["refresh_time"] = config["refresh_time"]

            if 'youtu' in feed['url']:
                feed['url'] = Utils.get_youtube_feed_url(feed['url'])

        return config
