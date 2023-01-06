from typing import List
from time import sleep
from threading import Thread
from sys import exit

from .feeds import Feed
from src.utils import Utils
from src.logger import Logger

logger = Logger.get_logger()

class Queue:

    unvalid_feeds: List[Feed] = []

    def process(self, queue: List[List[Feed]]) -> None:
        for type, feeds_by_type in enumerate(queue):
            for feed in feeds_by_type:
                self._process_current_feed(feed)
                if type != 0 :
                    sleep(1) # sleep for don't overload twitter/reddit apis
        self._close_thread()

    def _start_feeds(self, feed: Feed) -> None:
        thread = Thread(target=feed.run)
        thread.start()

    def exception_start_feeds(self, exception: Exception) -> None:
        logger.exception(str(exception))
        logger.error(f'An unknown error occured while starting the feeds')

    def _process_current_feed(self, feed: Feed) -> None:
        if feed.is_valid_url:
            Utils.try_again_if_fail(
                self._start_feeds,
                resolve_args=(feed,),
                reject=self.exception_start_feeds,
            )
        else:
            self.unvalid_feeds.append(feed)

    def _close_thread(self) -> None:
        exit()