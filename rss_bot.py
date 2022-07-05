from threading import Thread

from RSSManager import RSSManager
from logger import Logger

logger = Logger(2).get_logger()

class RSSBot:

    def __init__(self, client, config) -> None:
        self.client = client
        self.config = config

    async def run(self):
        for feed_config in self.config['feeds']:
            channels = await self.get_current_channel(feed_config)
            rss_manager = RSSManager(feed_config, channels)
            thread = Thread(target=rss_manager.run, args=(self.client,))
            thread.start()

    async def get_current_channel(self, feed_config):

        config_channels = feed_config['channels'].split(',')
        client_channels = []

        for chan in config_channels:
            channel_obj = await self.client.fetch_channel(chan)
            logger.info(channel_obj)
            client_channels.append(channel_obj)
        return client_channels