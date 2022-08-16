import discord, os, asyncio
from threading import Thread

from src.feed import Feed
from src.logger import Logger
from src.constants import Constants

logger = Logger.get_logger()

class FeedsManager:

    def __init__(self, client, config, parser, generator_exist) -> None:
        self.client = client
        self.parser = parser
        self.config = config
        self.generator_exist = generator_exist

    async def run(self):
        await self._display_bot_game()
        while "servers" in self.config and self.config['servers'] != []:
            while True:
                for server_config in self.config['servers']:
                    if server_config["feeds"] != []:
                        await self._start_feeds(server_config)
                    else:
                        logger.info(f"The server {server_config['id']} as no feeds set, skipping")
                self.parser.create_backup_servers_config()
                await self._sleep_before_refresh()
        logger.info('No servers config set yet')

    async def _start_feeds(self, server_config):
        try:
            for feed_config in server_config['feeds']:
                latest_post_in_feed = self._read_latest_post_file(feed_config['name'])
                channel = await self._get_current_channel(feed_config)
                rss_manager = Feed(feed_config, channel, latest_post_in_feed, self.generator_exist)
                if bool(feed_config['is_valid_url']):
                    thread = Thread(target=rss_manager.run, args=(self.client,))
                    thread.start()
                else:
                    logger.error(f"{feed_config['url']} is not a valid url, skipping")
        except Exception as e:
            if ("Unknown Channel" in str(e)):
                self.parser.delete_channel_from_config(feed_config['channel'], server_config['id'])
                logger.info(f"Channel {feed_config['channel']} does not exist. Deleting from config")
            else:
                logger.exception(str(e))
                logger.error(f'A network issue has occured')
                await self._sleep_before_refresh()
            await self._start_feeds(server_config)

    async def _get_current_channel(self, feed_config):
        return await self.client.fetch_channel(str(feed_config['channel']))

    async def _display_bot_game(self):
        game_displayed = self.config['game_displayed']
        await self.client.change_presence(activity=discord.Game(name=game_displayed))

    def _read_latest_post_file(self, feed_name):
        data_dir_path = Constants.feeds_data_dir
        file_path = data_dir_path + '/' + feed_name
        file_data = ''

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file_buff:
                file_data = file_buff.read()
        else:
            if not os.path.isdir(data_dir_path):
                os.mkdir(data_dir_path)
            with open(file_path, 'w') as file_buff:
                file_buff.write(file_data)
        return file_data

    async def _sleep_before_refresh(self) -> None:
        refresh_time = self.config['refresh_time']
        logger.info(f'Sleep for {refresh_time}s before the next refresh')
        await asyncio.sleep(refresh_time)
