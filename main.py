from discord import Client, Game, MemberCacheFlags, Message
from asyncio import sleep
from threading import Thread
from pydash import _

from src.user_config import UserConfig
from src.logger import Logger
from src.context import Context
from src.rss_gen import RSSGenerator
from src.backup import Backup
from src.Feed import Feed
from src.bot_commands import BotCommands
from src.utils import Utils

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
        self.loop.create_task(self._prepare_and_run())

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

    async def _prepare_and_run(self) -> None:
        await self.wait_until_ready()
        await self.change_presence(activity=Game(name=user_config['game_displayed']))
        await self._run()

    async def _run(self) -> None:
        while True:
            feeds_to_poll = self.context.manager.feeds
            feeds_to_poll_are_set = len(_.without(feeds_to_poll, [])) > 0
            if feeds_to_poll_are_set:
                while True:
                    for type, all_feeds_type in enumerate(feeds_to_poll):
                        for feed in all_feeds_type:
                            if feed.is_valid_url:
                                await Utils.try_again_if_fail(
                                    self._start_feeds,
                                    resolve_args=(feed,),
                                    reject=self.exception_start_feeds,
                                )
                            else:
                                self.context.remove(with_feed=(feed, type))
                    Backup(self.context).save()
                    await self._sleep_before_refresh()
            else:
                logger.info('No servers config set yet')
                await self._sleep_before_refresh(10)
                await self._run()

    def _start_feeds(self, feed: Feed) -> None:
        thread = Thread(target=feed.run)
        thread.start()

    def exception_start_feeds(self, exception: Exception) -> None:
        logger.exception(str(exception))
        logger.error(f'An unknown error occured while starting the feeds')
    
    async def _sleep_before_refresh(self, time_to_sleep = 0) -> None:
        refresh_time = time_to_sleep if time_to_sleep != 0 else user_config['refresh_time']
        logger.info(f'Sleep for {refresh_time}s before the next refresh')
        await sleep(refresh_time)

if __name__ == "__main__":
    user_config = UserConfig.load_user_config()
    Bot(
        chunk_guilds_at_startup=False,
        member_cache_flags=MemberCacheFlags.none(),
        max_messages=None,
        heartbeat_timeout=user_config['refresh_time']+5
    ).run(user_config['token']
)
