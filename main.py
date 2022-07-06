import discord

from src.logger import Logger
from src.parser import Parser

from src.rss_bot import RSSBot

logger = Logger.get_logger()

class Client(discord.Client):

    def __init__(self, **discord_params) -> None:
        super().__init__(**discord_params)
        config = parser.get_config()

        self.config = config

    async def on_ready(self) -> None:
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')
        await self.loop.create_task(self.my_background_task())

    async def my_background_task(self):
        await self.wait_until_ready()
        await RSSBot(self, self.config).run()

if __name__ == "__main__":
    parser = Parser()
    token = parser.get_token()

    Client(
        chunk_guilds_at_startup=False,
        member_cache_flags=discord.MemberCacheFlags.none(),
        max_messages=None,
    ).run(token)
