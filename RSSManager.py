import feedparser, datetime

from dateutil import parser

from parser import Parser
from utils import Utils
from event import EventHandler
from logger import Logger

logger = Logger(2).get_logger()

class RSSManager:

    latest_post_feed = None

    def __init__(self, feed_config, index_of_current_feed: int, handler: EventHandler, parser: Parser) -> None:
        self.feed_config = feed_config
        self.all_posts = self.poll_feed(feed_config['url'])
        self.handler = handler
        self.index_of_current_feed = index_of_current_feed
        self.parser = parser

    def poll_feed(self, feed_url):
        return feedparser.parse(feed_url).entries

    def update_and_return_latest_rss(self):
        case = self._get_status_of_feed()
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

        for i, new_post in enumerate(news_to_publish):
            self.handler.do('send_message', new_post)

            is_last_news = i == len(news_to_publish) - 1
            if is_last_news:
                self.latest_post_feed = news_to_publish[0].title

    def _append_new_feed(self):
        news_to_publish = self._get_unsended_news()

        for i, new_post in enumerate(news_to_publish):
            self.handler.do('send_message', new_post)

            is_last_news = i == len(news_to_publish) - 1
            if is_last_news:
                self.latest_post_feed = news_to_publish[0].title

    def _get_unsended_news(self):
        news_to_publish = []

        if self.latest_post_feed != None: 
            for single_news in self.all_posts:
                if single_news.title != self.latest_post_feed:
                    news_to_publish.append(single_news)
                elif single_news.title == self.latest_post_feed:
                    break
        else:
            for single_news in self.all_posts:
                date_time = parser.parse(single_news['published'])
                timezone = Utils.get_timezone()
                time_since_published = timezone.localize(
                    datetime.datetime.now()
                ) - date_time.astimezone(timezone)
                
                is_not_to_old_news = time_since_published.total_seconds() <= self.feed_config['published_since']
                
                if is_not_to_old_news:
                    news_to_publish.append(single_news)
                else:
                    break

        if news_to_publish == []:
            logger.info('No news to publish')

        return news_to_publish

    def _get_status_of_feed(self) -> int:

        no_need_to_post, post_until_latest, add_all_post_until_time = (0, 1, 2)

        if self.latest_post_feed != None:
            current_feed_is_registered = self.all_posts[0].title == self.latest_post_feed
            if current_feed_is_registered:
                return no_need_to_post
            else: 
                return post_until_latest
        else:
            return add_all_post_until_time