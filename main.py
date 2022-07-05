import asyncio
from threading import Thread

from logger import Logger
from RSSManager import RSSManager
from event import EventHandler
from parser import Parser

logger = Logger(2).get_logger()

class RSSBot:

    handler = EventHandler()
    parser = Parser()

    def __init__(self) -> None:
        self.config = self.parser.get_config()

    def run(self):
        threads = []
        for feed_config in self.config['feeds']:
            rss_manager = RSSManager(feed_config, self.handler, self.parser)
            current_thread = Thread(target=rss_manager.run)
            threads.append(current_thread)
            current_thread.start()

if __name__ == "__main__":
    RSSBot().run()

