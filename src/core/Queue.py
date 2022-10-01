from typing import List
from asyncio import sleep
from threading import Thread

from .feeds import Feed
from src.utils import Utils
from src.logger import Logger

logger = Logger.get_logger()

class Queue:

    unvalid_feeds: List[Feed] = []

    async def process(self, queue: List[List[Feed]]) -> None:
        for type, feeds_by_type in enumerate(queue):
            for feed in feeds_by_type:
                await self._process_current_feed(feed)
                if type != 0 :
                    await sleep(1) # sleep for don't overload twitter/reddit apis

    def _start_feeds(self, feed: Feed) -> None:
        thread = Thread(target=feed.run)
        thread.start()

    def exception_start_feeds(self, exception: Exception) -> None:
        logger.exception(str(exception))
        logger.error(f'An unknown error occured while starting the feeds')

    async def _process_current_feed(self, feed: Feed) -> None:
        if feed.is_valid_url:
            await Utils.try_again_if_fail(
                self._start_feeds,
                resolve_args=(feed,),
                reject=self.exception_start_feeds,
            )
        else:
            self.unvalid_feeds.append(feed)
