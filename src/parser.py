import os, json, yaml

from src.constants import Constants
from src.logger import Logger
from src.utils import Utils

logger = Logger.get_logger()

class Parser:
    def __init__(self, generator_exist) -> None:
        self._bootstrap_config(generator_exist)
        self._generate_servers_config()

    def get_token(self) -> str:
        return self.config['token']
    
    def load_server_config(self, generator_exist, config=[]):
        if config == []:
            config['servers'] = self._read_and_render_server_configs()
        for server in config["servers"]:
            if "id" not in server:
                server["id"] = ""
            for feed in server["feeds"]:
                self._build_feed(feed, generator_exist)
        self.config['servers'] = config["servers"]

    def append_new_feed(
        self, 
        url_submited,
        channel_submited, 
        channel_name, 
        server_to_submit,
        generator_exist
    ):
        for server in self.config['servers']:
            if server['id'] == server_to_submit:
                feed = {
                    "url": url_submited,
                    "channels": channel_submited,
                }
                self._build_feed(feed, generator_exist, channel_name)
                logger.info(feed)
                server['feeds'].append(feed)
                logger.info("---")
                logger.info(self.config)
                logger.info("---")


    def _build_feed(self, feed, generator_exist, channel_name = ''):
        if "name" not in feed:
            channel_name = "feed" if channel_name == "" else channel_name
            feed["name"] = f"{channel_name}-{Utils.generate_random_string()}"
        if "published_since" not in feed:
            feed["published_since"] = Constants.default_config["published_since_default"]
        if "refresh_time" not in feed:
            feed["refresh_time"] = Constants.default_config["refresh_time"]
        if 'youtu' in feed['url'] and "feeds" not in feed['url']:
            feed['url'] = Utils.get_youtube_feed_url(feed['url'])
        feed['is_valid_url'] = Utils.sanitize_check(feed['url'], generator_exist)

    def _validate_config_file(self, file_path) -> bool:
        config = []
        try:
            if os.path.isfile(file_path):
                config_file_content = open(file_path,'r').read()
                try:
                    config = json.loads(config_file_content)
                except:
                    config = yaml.safe_load(config_file_content)
                return config, True
        except Exception:
            logger.info(f'You must submit a valid file in path: {Constants.base_conf_path_dir} file dir')
            return config, False

    def _file_name(self) -> str:
        file_list = os.listdir(Constants.base_conf_path_dir)
        for file in file_list:
            if ".json" or ".yaml" or ".yml" in file and file != Constants.servers_conf_path:
                return file

    def _bootstrap_config(self, generator_exist) -> str:
        self.config = Constants.default_config
        config_path = os.path.join(Constants.base_conf_path_dir, self._file_name())
        base_config, config_is_valid = self._validate_config_file(config_path)
        if config_is_valid:
            for key, value in base_config.items():
                self.config[key] = value
        self.load_server_config(generator_exist, self.config)

    def _generate_servers_config(self):
        if "servers" in self.config:
            yaml_text = yaml.dump({"servers": self.config["servers"]})
            with open(Constants.servers_conf_path, 'w') as yaml_file:
                try:
                    yaml_file.write(yaml_text)
                finally:
                    yaml_file.close()

    def _read_and_render_server_configs(self):
        with open(Constants.servers_conf_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file.readlines())['servers']
