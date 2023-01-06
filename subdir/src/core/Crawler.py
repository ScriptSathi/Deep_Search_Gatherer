from asyncio import sleep
from threading import Thread
from pydash import _

from .context import Context
from .Queue import Queue
from src.logger import Logger
from src.backup import Backup

logger = Logger.get_logger()

class Crawler:

    context: Context
    queue: Queue = Queue()
    _refresh_timer: int

    def __init__(self, context: Context, refresh_timer: int) -> None:
        self.context = context
        self._refresh_timer = refresh_timer

    async def run(self) -> None:
        feeds_to_poll = self.context.manager.feeds
        feeds_to_poll_are_set = len(_.without(feeds_to_poll, [])) > 0
        while feeds_to_poll_are_set:
            for feed in self.queue.unvalid_feeds:
                self.context.remove(with_feed=(feed, feed.type))
            Thread(target=self.queue.process, args=(self.context.manager.feeds,)).start()
            Backup(self.context).save()
            await self._sleep_before_refresh()
        else:
            logger.info('No servers config set yet')
            await self._sleep_before_refresh(10)
            await self.run()

    async def _sleep_before_refresh(self, time_to_sleep = 0) -> None:
        refresh_time = time_to_sleep if time_to_sleep != 0 else self._refresh_timer
        logger.info(f'Sleep for {refresh_time}s before the next refresh')
        await sleep(refresh_time)
