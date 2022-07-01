import feedparser, asyncio
from event import EventHandler

from logger import Logger
from feeds import Feeds

logger = Logger(2).get_logger()

class RSSBot:
    def __init__(self) -> None:
        self.handle = EventHandler()
        self.feeds = Feeds(self.handle)

        self.feeds.add_events()

    def trigger_post_event(self, all_posts, index):
        no_need_to_post, post_until_latest, add_all_post_until_time = (0, 1, 2)
        case = self.feeds.get_status_of_feed(all_posts, index)

        if no_need_to_post == case:
            self.handle.on('nothing_to_post', 'There is no new post on this feed')
        elif post_until_latest == case:
            self.handle.on('post_until_latest', all_posts, index)
        if add_all_post_until_time == case:
            self.handle.on('append_new_feed', all_posts, index)

    async def poll_feed(self):
        for index, feed in enumerate(self.feeds.list):

            all_posts = feedparser.parse(feed['url']).entries

            self.trigger_post_event(all_posts, index)

            for new_post in reversed(all_posts):
                pass

    async def call_data(self):
        while True:
            await self.poll_feed()
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(
        RSSBot().call_data()
    )
