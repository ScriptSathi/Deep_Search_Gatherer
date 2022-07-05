from typing import List
import feedparser, datetime

from dateutil import parser
from time import sleep

from parser import Parser
from message import Message
from utils import Utils
from logger import Logger

logger = Logger(2).get_logger()

class RSSManager:

    latest_post_feed = None

    def __init__(self, feed_config, chan) -> None:
        self.feed_config = feed_config
        self.channels = chan
        self.all_posts = self._poll_feed(feed_config['url'])

    def run(self, client) -> None:
        self.message = Message(client, self.channels, self.feed_config)
        while True:
            case = self._get_status_of_feed()
            self._send_message_if_needed(case)
            self._sleep_before_refresh()

    def _sleep_before_refresh(self) -> None:
        logger.info(f'Sleep for {self.feed_config["refresh_time"]} before the next refresh')
        sleep(self.feed_config['refresh_time'])

    def _poll_feed(self, feed_url):
        return feedparser.parse(feed_url).entries

    def _send_message_if_needed(self, case) -> None:
        no_need_to_post, post_until_latest, add_all_post_until_time = (0, 1, 2)

        if no_need_to_post == case:
            self._nothing_to_post(f"There is no new post on {self.feed_config['name']}")
        elif post_until_latest == case:
            self._post_until_latest()
        elif add_all_post_until_time == case:
            self._append_new_feed()

    def _nothing_to_post(self, message) -> None:
        logger.info(message)

    def _post_until_latest(self) -> None:
        news_to_publish = self._get_unsended_news()

        for i, new_post in enumerate(reversed(news_to_publish)):
            self.message.send_message(new_post)

            is_last_news = i == len(news_to_publish) - 1
            if is_last_news:
                self.latest_post_feed = news_to_publish[0].title

    def _append_new_feed(self) -> None:
        news_to_publish = self._get_unsended_news()

        for i, new_post in enumerate(reversed(news_to_publish)):
            self.message.send_message(new_post)
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