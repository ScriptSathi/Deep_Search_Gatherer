import discord, asyncio
from threading import Thread

from src.feed import Feed
from src.logger import Logger
from src.constants import Constants

logger = Logger.get_logger()

class FeedsManager:

    def __init__(self, client, context, generator_exist) -> None:
        self.client = client
        self.context = context
        self.generator_exist = generator_exist

    async def run(self):
        while True:
            if self.context.servers_config != []:
                while True:
                    for server_config in self.context.servers_config:
                        if server_config["feeds"] != []:
                            await self._start_feeds(server_config)
                        else:
                            logger.info(f"The server {server_config['id']} as no feeds set, skipping")
                    # self.context.create_backup_servers_config()
                    await self._sleep_before_refresh()
            else:
                logger.info('No servers config set yet')
                await self._sleep_before_refresh(10)
                await self.run()

    async def _start_feeds(self, server_config):
        try:
            for feed in server_config['feeds']:
                if feed.is_valid_url:
                    thread = Thread(target=feed.run, args=(self.client,))
                    thread.start()
                else:
                    logger.error(f"{feed.url} is not a valid url, skipping")
        except:
            if ("Unknown Channel" in str(Exception)):
                self.context.delete_from_config('channel', feed.channel, server_config['id'])
                logger.info(f"Channel {feed.channel} does not exist. Deleting from config")
            else:
                logger.exception(str(Exception))
                logger.error(f'A network issue has occured')
                await self._sleep_before_refresh()
            await self._start_feeds(server_config)

    async def _sleep_before_refresh(self, time_to_sleep = 0) -> None:
        refresh_time = time_to_sleep if time_to_sleep != 0 else self.context.base_config['refresh_time']
        logger.info(f'Sleep for {refresh_time}s before the next refresh')
        await asyncio.sleep(refresh_time)
