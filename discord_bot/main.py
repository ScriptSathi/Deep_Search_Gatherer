from discord import Client, Game, Intents, MemberCacheFlags, Message
from pydash import _

from src import Utils, Logger, Crawler, Context, BotCommands, Backup, RSSGenerator, UserConfig

logger = Logger.get_logger()

class Bot(Client):

    generator_exist: bool = RSSGenerator.generator_exist()
    context: Context

    def __init__(self, **discord_params) -> None:
        super().__init__(**discord_params)

    async def on_ready(self) -> None:
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')
        self.context = await Backup.load(self, self.generator_exist, user_config)
        self.loop.create_task(self._start_crawler())

    async def on_message(self, message: Message) -> None:
        is_private_message = not getattr(message, "guild")
        if (message.author.id != self.user.id \
            and self.user.mentioned_in(message)\
            and Utils.everyone_tag_is_not_used(message.content)):
            if not is_private_message:
                await BotCommands(self, self.context, message, self.generator_exist).handle_messages()
        elif is_private_message:
            logger.info(f"Private message received from {message.author.id}: {message.content}")
            # TODO send a private message disclaimer

    async def _start_crawler(self) -> None:
        await self.wait_until_ready()
        await self.change_presence(activity=Game(name=user_config['game_displayed']))
        await Crawler(self.context, user_config['refresh_time']).run()

if __name__ == "__main__":
    user_config = UserConfig.load_user_config()
    Bot(
        intents=Intents.default(),
        chunk_guilds_at_startup=False,
        member_cache_flags=MemberCacheFlags.none(),
        max_messages=None,
        heartbeat_timeout=user_config['refresh_time']+5
    ).run(user_config['token']
)
