from cmath import exp
import os, json, yaml

from src.constants import Constants
from src.logger import Logger
from src.utils import Utils

logger = Logger.get_logger()

class Parser:
    def __init__(self, generator_exist) -> None:
        self._bootstrap_config(generator_exist)

    def get_token(self) -> str:
        return self.config['token']
    
    def get_server_config(self, server_id):
        for server in self.config['servers']:
            if server_id == server['id']:
                return server
        return []

    def append_new_feed(
        self,
        url_submited,
        channel_submited,
        channel_name,
        server_to_submit,
        generator_exist,
        name_submited
    ):
        feed = {
            "url": url_submited,
            "channel": channel_submited,
            "name": name_submited
        }
        self._build_feed(feed, generator_exist, channel_name)
        if self._is_server_already_registered(server_to_submit):
            for server in self.config['servers']:
                if server['id'] == server_to_submit:
                    server['feeds'].append(feed)
        else:
            new_server = {
                "id": server_to_submit,
                "feeds": [feed]
            }
            logger.info(f"Adding server: {server_to_submit} in the config")
            self.config['servers'].append(new_server)
        return feed['name']

    def create_backup_servers_config(self):
        if "servers" in self.config:
            yaml_text = yaml.dump({"servers": self.config["servers"]})
            with open(Constants.servers_conf_path, 'w') as yaml_file:
                try:
                    yaml_file.write(yaml_text)
                finally:
                    yaml_file.close()

    def delete_from_config(self, field_name_to_remove, field_value_to_remove, server_id):
        feed_is_removed = False
        for server in self.config['servers']:
            if server['id'] == server_id:
                for feed in server['feeds']:
                    if feed[field_name_to_remove] == field_value_to_remove:
                        server['feeds'].remove(feed)
                        feed_is_removed = True
        if not feed_is_removed:
            raise # for trigger Message.send_delete_error()
        logger.info(f"Successfully deleting {field_name_to_remove} from server {server_id}")

    def _bootstrap_config(self, generator_exist) -> str:
        self.config = Constants.default_config
        config_path = os.path.join(Constants.base_conf_path_dir, self._file_name())
        base_config, config_is_valid = self._validate_config_file(config_path)
        if config_is_valid:
            for key, value in base_config.items():
                self.config[key] = value
        self._load_server_config(generator_exist, self.config['servers'])

    def _build_feed(self, feed, generator_exist, channel_name = ''):
        if "name" not in feed or feed['name'] == '':
            channel_name = "feed" if channel_name == "" else channel_name
            feed["name"] = f"{channel_name}-{Utils.generate_random_string()}"
        if "published_since" not in feed:
            feed["published_since"] = Constants.default_config["published_since_default"]
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

    def _load_server_config(self, generator_exist, servers_config=[]):
        servers_config = self._read_backup_servers_config(servers_config)
        for server in servers_config:
            if "id" not in server:
                server["id"] = ""
            for feed in server["feeds"]:
                self._build_feed(feed, generator_exist)
        self.config['servers'] = servers_config

    def _read_backup_servers_config(self, servers_config):
        try:
            with open(Constants.servers_conf_path, 'r') as yaml_file:
                logger.info('Backup loaded successfully')
                return yaml.safe_load(yaml_file)['servers']
        except:
            return servers_config

    def _is_server_already_registered(self, server_to_submit):
        server_is_registered = False
        for server in self.config['servers']:
            if server['id'] == server_to_submit:
                server_is_registered = True
        return server_is_registered