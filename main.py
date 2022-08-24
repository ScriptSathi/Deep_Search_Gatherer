import discord
from src.logger import Logger
from src.context import Context
from src.rss_gen import RSSGenerator
from src.feeds_manager import FeedsManager
from src.bot_commands import BotCommands

logger = Logger.get_logger()

class Bot(discord.Client):
    def __init__(self, generator_exist, context, **discord_params) -> None:
        super().__init__(**discord_params)
        self.generator_exist = generator_exist
        self.context = context

    async def on_ready(self) -> None:
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')
        await context.load_servers_context(self.generator_exist)
        await self.loop.create_task(self._prepare_and_run())

    async def on_message(self, message):
        if message.author.id != self.user.id and self.user.mentioned_in(message):
            await BotCommands(self, self.context, message, self.generator_exist).handle_messages()

    async def _prepare_and_run(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Game(name=self.context.base_config['game_displayed']))
        await FeedsManager(self, self.context, self.generator_exist).run()

if __name__ == "__main__":
    generator_exist = RSSGenerator.generator_exist()
    context = Context()
    Bot(
        generator_exist,
        context,
        chunk_guilds_at_startup=False,
        member_cache_flags=discord.MemberCacheFlags.none(),
        max_messages=None,
        heartbeat_timeout=context.base_config['refresh_time']+5
    ).run(context.base_config['token']
)
