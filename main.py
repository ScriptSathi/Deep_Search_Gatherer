import discord
from src.logger import Logger
from src.parser import Parser
from src.rss_gen import RSSGenerator
from src.feeds_manager import FeedsManager
from src.bot_commands import BotCommands

logger = Logger.get_logger()

class Bot(discord.Client):

    def __init__(self, generator_exist, **discord_params) -> None:
        super().__init__(**discord_params)
        self.config = config
        self.parser = parser
        self.generator_exist = generator_exist

    async def on_ready(self) -> None:
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')
        await self.loop.create_task(self._prepare_and_run())

    async def _prepare_and_run(self):
        await self.wait_until_ready()
        await FeedsManager(self, self.config, self.parser, self.generator_exist).run()

    async def on_message(self, message):
        if message.author.id != self.user.id and self.user.mentioned_in(message):
            await BotCommands(self, self.parser, message, self.generator_exist).handle_messages()

if __name__ == "__main__":
    generator_exist = RSSGenerator.generator_exist()
    parser = Parser(generator_exist)
    config = parser.config
    token = parser.get_token()

    Bot(
        generator_exist,
        chunk_guilds_at_startup=False,
        member_cache_flags=discord.MemberCacheFlags.none(),
        max_messages=None,
        heartbeat_timeout=config['refresh_time']+5
    ).run(token)
