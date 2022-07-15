import discord, functools
from threading import Thread
from time import sleep

from src.feed import Feed
from src.logger import Logger

logger = Logger.get_logger()

class RSSBot:

    def __init__(self, client, config) -> None:
        self.client = client
        self.config = config

    async def run(self):
        await self._display_bot_game()
        while True:
            for feed_config in self.config['feeds']:
                channels = await self._get_current_channel(feed_config)
                rss_manager = Feed(feed_config, channels)
                thread = Thread(target=rss_manager.run, args=(self.client,))
                thread.start()
            await self._sleep_until_refresh()

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
    
    
    async def _sleep_until_refresh(self, *args, **kwargs):
        def do_sleep(config):
            refresh_time = config['refresh_time']
            logger.info(f"Sleep until the next refresh in {refresh_time}s")
            sleep(refresh_time)
        """Runs a blocking function in a non-blocking way"""
        func = functools.partial(do_sleep(self.config), *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
        return await self.client.loop.run_in_executor(None, func)