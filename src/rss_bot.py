import discord
from threading import Thread

from src.RSSManager import RSSManager
from src.logger import Logger

logger = Logger.get_logger()

class RSSBot:

    def __init__(self, client, config) -> None:
        self.client = client
        self.config = config

    async def run(self):
        await self._display_bot_game()

        for feed_config in self.config['feeds']:
            channels = await self._get_current_channel(feed_config)
            rss_manager = RSSManager(feed_config, channels)
            thread = Thread(target=rss_manager.run, args=(self.client,))
            thread.start()

    async def _get_current_channel(self, feed_config):

        config_channels = feed_config['channels'].split(',')
        client_channels = []

        for chan in config_channels:
            channel_obj = await self.client.fetch_channel(chan)
            client_channels.append(channel_obj)
        return client_channels

    async def _display_bot_game(self):
        game_displayed = self.config['game_displayed']
        await self.client.change_presence(activity=discord.Game(name=game_displayed))