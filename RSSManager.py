import feedparser, datetime

from dateutil import parser

from parser import Parser
from utils import Utils
from event import EventHandler
from logger import Logger

logger = Logger(2).get_logger()

class RSSManager:
    def __init__(self, feed_config, index_of_current_feed: int, latest_post_feed: str, handler: EventHandler, parser: Parser) -> None:
        self.feed_config = feed_config
        self.all_posts = self.poll_feed(feed_config['url'])
        self.handler = handler
        self.index_of_current_feed = index_of_current_feed
        self.latest_post_feed = latest_post_feed
        self.parser = parser

    def poll_feed(self, feed_url):
        return feedparser.parse(feed_url).entries

    def update_and_return_latest_rss(self, case):
        self._send_message_if_needed(case)
        return 

    def _send_message_if_needed(self, case):
        no_need_to_post, post_until_latest, add_all_post_until_time = (0, 1, 2)

        if no_need_to_post == case:
            self._nothing_to_post('There is no new post on this feed')
        elif post_until_latest == case:
            self._post_until_latest()
        elif add_all_post_until_time == case:
            self._append_new_feed()
    
    def _nothing_to_post(self, message):
        logger.info(message)

    def _post_until_latest(self):
        news_to_publish = self._get_unsended_news()

        for new_post in news_to_publish:
            self.handler.do('send_message', new_post)

    def _append_new_feed(self):
        news_to_publish = self._get_unsended_news()

        for new_post in news_to_publish:
            self.handler.do('send_message', new_post)

    def _get_unsended_news(self):
        news_to_publish = []

        if self.latest_post_feed != None: 
            for new in self.all_posts:
                if new.title != self.latest_post_feed:
                    news_to_publish.append(new)
                elif new.title == self.latest_post_feed:
                    break
            return news_to_publish
        else:
            for new in self.all_posts:
                date_time = parser.parse(new['published'])
                timezone = Utils.get_timezone()
                time_since_published = timezone.localize(
                    datetime.datetime.now()
                ) - date_time.astimezone(timezone)
                
                is_not_to_old_news = time_since_published.total_seconds() <= self.feed_config['published_since']
                
                if is_not_to_old_news:
                    news_to_publish.append(new)
                else:
                    logger.info('No news to publish')
                    break

            return news_to_publish