import os, yaml
from typing import List
from discord import Client, TextChannel
from src.user_config import User_config_dict
from src.core.messages.message import Message

from .constants import Constants
from .core import Context
from .logger import Logger

logger = Logger.get_logger()

class Backup:

    async def load(client: Client, generator_exist: bool, user_config: User_config_dict) -> Context:
        context = Context(client, generator_exist, user_config)
        try:
            with open(Constants.backup_path, 'r') as yaml_file:
                backup_data = yaml.safe_load(yaml_file)['servers']
                for server_data in backup_data:
                    for feed_data in server_data['feeds']:
                        feed_channels: List[TextChannel] = []
                        for channel_id in feed_data['channels']:
                            try:
                                feed_channels.append(await client.fetch_channel(str(channel_id)))
                            except:
                                base_message = Message.standard_output(server_data["name"], server_data['id'])
                                logger.warning(f"{base_message} - Channel {str(channel_id)} does not exist, skipping")
                        for channel in feed_channels:
                            context.add(feed_data['url'], channel, feed_data['name'], feed_data['type'], feed_data['last_post'])
            logger.info('Backup loaded successfully')
            return context
        except:
            logger.error('Fail to load backup')
            return context

    context: Context

    def __init__(self, context: Context) -> None:
        self.context = context

    def save(self) -> None:
        backup_data = []
        for server in self.context.registered_data:
            backup_data.append({
                "id": server.id,
                "name": server.name,
                "feeds": [
                    self.context.manager.get_feed_backup(server.id, feed.type, "uid", feed.uid) for feed in server.feeds
                ],
            })
        try:
            with open(Constants.backup_path, 'w') as yaml_file:
                yaml_text = yaml.dump({"servers": backup_data})
                try:
                    yaml_file.write(yaml_text)
                finally:
                    yaml_file.close()
        except Exception as e:
            logger.exception(str(e))
            os.mkdir(Constants.backup_dir_path)
            self.save()
