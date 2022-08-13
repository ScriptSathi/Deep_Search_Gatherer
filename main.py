import discord

from src.logger import Logger
from src.parser import Parser
from src.rss_gen import RSSGenerator
from src.rss_bot import RSSBot

logger = Logger.get_logger()

class Client(discord.Client):

    def __init__(self, generator_exist, **discord_params) -> None:
        super().__init__(**discord_params)
        self.config = config
        self.generator_exist = generator_exist

    async def on_ready(self) -> None:
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')
        await self.loop.create_task(self._prepare_and_run())

    async def _prepare_and_run(self):
        await self.wait_until_ready()
        await RSSBot(self, self.config, self.generator_exist).run()

if __name__ == "__main__":
    generator_exist = RSSGenerator.generator_exist()
    parser = Parser(generator_exist)
    config = parser.get_config()
    token = parser.get_token()

    Client(
        generator_exist,
        chunk_guilds_at_startup=False,
        member_cache_flags=discord.MemberCacheFlags.none(),
        max_messages=None,
        heartbeat_timeout=config['refresh_time']+5
    ).run(token)
