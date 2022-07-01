import os, json
from typing import List
from constants import Constants
from logger import Logger

logger = Logger(2).get_logger()

class Parser:
    def __init__(self) -> None:
        self.config = self._load_config()

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
            if "fields" not in feed:
                feed["fields"] = "**title**,author,_published_,link,summary"
                
            if "name" not in feed:
                current_index = config["feeds"].index(feed)
                feed["name"] = f"feed-n°-{str(current_index)}"
        
        return config

    def get_token(self) -> str:
        return self.config['token'] 
  
    def get_feeds(self) -> List:
        return self.config['feeds']