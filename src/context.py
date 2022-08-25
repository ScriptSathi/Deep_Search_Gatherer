import os, json, yaml, discord

from src.backup import Backup
from src.constants import Constants
from src.logger import Logger
from src.utils import Utils
from src.feed import Feed

logger = Logger.get_logger()

class Context:

    base_config = Constants.base_config_default
    servers_config = []

    def __init__(self) -> None:
        self._load_base_context()

    def get_server_config(self, server_id):
        for server in self.servers_config:
            if server_id == server['id']:
                return server
        return []

    def append_new_feed(
        self,
        url_submited,
        channel_obj,
        server_to_submit,
        generator_exist,
        name_submited
    ):
        last_post = ''
        feed = self._create_feed(
            name_submited,
            url_submited,
            channel_obj,
            last_post,
            Constants.base_config_default["published_since_default"],
            generator_exist
        )
        if self._is_server_already_registered(server_to_submit):
            for server in self.servers_config:
                if server['id'] == server_to_submit:
                    server['feeds'].append(feed)
        else:
            new_server = {
                "id": server_to_submit,
                "feeds": [feed]
            }
            logger.info(f"Adding server: {server_to_submit} in the config")
            self.servers_config.append(new_server)
        return feed.name

    def delete_from_config(self, field_name_to_remove, field_value_to_remove, server_id):
        feed_is_removed = False
        for server in self.servers_config:
            if server['id'] == server_id:
                for feed in server['feeds']:
                    if getattr(feed, field_name_to_remove) == field_value_to_remove:
                        server['feeds'].remove(feed)
                        feed_is_removed = True
        if not feed_is_removed:
            raise # for trigger Message.send_delete_error()

    async def load_context_from_backup(self, generator_exist, client):
        full_backup = Backup.read()
        if full_backup != []:
            for server_backup in full_backup:
                server = {
                    "id": server_backup['id'],
                    "feeds": []
                }
                for feed_config in server_backup["feeds"]:
                    channel_obj = await ContextUtils.get_channel_object(client, feed_config['channel'])
                    if channel_obj != None:
                        server['feeds'].append(self._create_feed(
                            feed_config['name'],
                            feed_config['url'],
                            channel_obj,
                            feed_config['last_post'],
                            feed_config["published_since"],
                            generator_exist
                            )
                        )
                self.servers_config.append(server)

    def _create_feed(self,
        name,
        url,
        channel_obj,
        latest_post_in_feed,
        published_since,
        generator_exist
     ):
        url = Utils.get_youtube_feed_url(url) \
            if 'youtu' in url and "feeds" not in url \
            else url
        is_valid_url = Utils.sanitize_check(url, generator_exist)
        name = name if name != "" else f"{channel_obj.name}-{Utils.generate_random_string()}"
        return Feed(name, url, channel_obj, latest_post_in_feed, is_valid_url, published_since, generator_exist)

    def _is_server_already_registered(self, server_to_submit):
        server_is_registered = False
        for server in self.servers_config:
            if server['id'] == server_to_submit:
                server_is_registered = True
        return server_is_registered

    def _load_base_context(self):
        config_path = os.path.join(Constants.base_conf_path_dir, ContextUtils.file_name())
        base_config = ContextUtils.read_config_file(config_path)
        if base_config != []:
            for key, value in base_config.items():
                self.base_config[key] = value

class ContextUtils:
    async def get_channel_object(client: discord.Client, channel_id):
        channel_obj = None
        try:
            channel_obj = await client.fetch_channel(str(channel_id))
        except:
            logger.warning(f"The submited channel: {channel_id} is not valid")
        return channel_obj

    def read_config_file(file_path) -> bool:
        config = []
        try:
            if os.path.isfile(file_path):
                config_file_content = open(file_path,'r').read()
                try:
                    config = json.loads(config_file_content)
                except:
                    config = yaml.safe_load(config_file_content)
                return config
        except Exception:
            logger.info(f'You must submit a valid file in path: {Constants.base_conf_path_dir} file dir')
            return config

    def file_name() -> str:
        file_list = os.listdir(Constants.base_conf_path_dir)
        for file in file_list:
            if ".json" in file or ".yaml" in file or ".yml" in file and file != Constants.backup_path:
                return file