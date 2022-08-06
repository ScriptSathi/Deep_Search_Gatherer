import feedparser, datetime, sys

from dateutil import parser

from src.message import Message
from src.utils import Utils
from src.logger import Logger
from src.constants import Constants
from src.rss_gen import RSSGenerator

logger = Logger.get_logger()

class Feed:

    def __init__(self, feed_config, chan, latest_post, generator_exist = False) -> None:
        self.latest_post = latest_post
        self.feed_config = feed_config
        self.channels = chan

        self.all_posts = self._get_xml_feed(feed_config['url'], generator_exist)

    def run(self, client) -> None:
        self.message = Message(client, self.channels, self.feed_config)
        while True:
            case = self._get_status_of_feed()
            self._send_message_if_needed(case)
            self._close_thread_after_usage()

    def _register_latest_post_file(self):
        file_path = Constants.feeds_data_dir + '/' + self.feed_config['name']

        with open(file_path, 'w') as file_buff:
            file_buff.write(self.latest_post)

    def _update_latest_post_data(self, news_content):
        self.latest_post = news_content

    def _close_thread_after_usage(self) -> None:
        sys.exit()

    def _get_xml_feed(self, feed_url, generator_exist):
        xml_entries = feedparser.parse(feed_url).entries
        if xml_entries != []:
            return xml_entries
        elif generator_exist:
            rss_feed = RSSGenerator(feed_url).render_xml_feed()
            return feedparser.parse(rss_feed).entries
        else:
            raise Exception(f"URL: {feed_url} is not a valid url")

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
                self._update_latest_post_data(news_to_publish[0].title)
        self._register_latest_post_file()

    def _append_new_feed(self) -> None:
        news_to_publish = self._get_unsended_news()

        for i, new_post in enumerate(reversed(news_to_publish)):
            self.message.send_message(new_post)
            is_last_news = i == len(news_to_publish) - 1
            if is_last_news:
                self._update_latest_post_data(news_to_publish[0].title)
        self._register_latest_post_file()

    def _get_unsended_news(self):
        news_to_publish = []
        feed_already_registered = self.latest_post != ''

        if feed_already_registered:
            for single_news in self.all_posts:
                if single_news.title != self.latest_post:
                    news_to_publish.append(single_news)
                elif single_news.title == self.latest_post or not self._is_too_old_news(single_news):
                    break
        else:
            for single_news in self.all_posts:
                if not self._is_too_old_news(single_news):
                    news_to_publish.append(single_news)
                else:
                    break

        if news_to_publish == []:
            logger.info(f"{self.feed_config['name']}: No news to share")

        return news_to_publish

    def _is_too_old_news(self, single_news):
        date_time = parser.parse(single_news['published'])
        timezone = Utils.get_timezone()
        time_since_published = timezone.localize(
            datetime.datetime.now()
        ) - date_time.astimezone(timezone)
        return not time_since_published.total_seconds() <= self.feed_config['published_since']

    def _get_status_of_feed(self) -> int:

        no_need_to_post, post_until_latest, add_all_post_until_time = (0, 1, 2)
        feed_already_registered = self.latest_post != ''

        if feed_already_registered:
            current_feed_is_registered = self.all_posts[0].title == self.latest_post
            if current_feed_is_registered:
                return no_need_to_post
            else: 
                return post_until_latest
        else:
            return add_all_post_until_time