import asyncio

from logger import Logger
from feeds import Feeds
from RSSManager import RSSManager
from event import EventHandler
from parser import Parser

logger = Logger(2).get_logger()

class RSSBot:

    handler = EventHandler()
    parser = Parser()

    def __init__(self) -> None:
        self.feeds = Feeds(self.handler)
        self.config = self.parser.get_config()

    def crawl_feeds(self):

        # for index_of_current_feed, feed_config in enumerate(self.feeds.list_data):

        index_of_current_feed = 0
        feed_config = self.config['feeds'][index_of_current_feed]
        latest_post_feed = None if len(self.feeds.latest_feed_posted) == 0 else self.feeds.latest_feed_posted[index_of_current_feed]

        rss_manager = RSSManager(feed_config, index_of_current_feed, latest_post_feed, self.handler, self.parser)

        feed_status_code = self.feeds.get_status_of_feed(rss_manager.all_posts, index_of_current_feed)

        latest_post_name = rss_manager.update_and_return_latest_rss(feed_status_code)
        # self.feeds.update_feed_posts(latest_post_name, index_of_current_feed)





        #         # for index_of_current_feed, feed_config in enumerate(self.feeds.list_data):

        #         rss_manager = RSSManager(feed_config['url'], index_of_current_feed, self.handler)

        #         feed_status_code = self.feeds.get_status_of_feed(rss_manager.all_posts, index_of_current_feed)

        #         latest_post_name = rss_manager.update_and_return_latest_rss(feed_status_code)
        #         self.feeds.update_feed_posts(latest_post_name, index_of_current_feed)

    async def run(self):
        while True:
            self.crawl_feeds()
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(
        RSSBot().run()
    )
