from unicodedata import name
import feedparser, datetime, sys

from dateutil import parser

from src.message import NewsMessage
from src.utils import Utils
from src.logger import Logger
from src.rss_gen import RSSGenerator

logger = Logger.get_logger()

class Feed:

    def __init__(self, name, url, channel_obj, latest_post, is_valid_url, published_since, generator_exist = False) -> None:
        self.name = name
        self.url = url
        self.latest_post = latest_post
        self.channel_obj = channel_obj
        self.is_valid_url = is_valid_url
        self.published_since = published_since
        self.generator_exist = generator_exist
        self.news_to_publish = []

    def run(self, client) -> None:
        self.news_to_publish = self._get_unsended_news()
        self.message = NewsMessage(client, self.channel_obj, self.name)
        self._send_message_if_needed()
        self._close_thread()

    def get_feed_data(self):
        return {
            "name": self.name,
            "url": self.url,
            "last_post": self.latest_post,
            "channel": self.channel.id,
            "is_valid_url": self.is_valid_url,
            "published_since": self.published_since,
        }

    def _register_latest_post(self, news_to_save):
        if news_to_save != []:
            self.latest_post = news_to_save[0].title

    def _close_thread(self) -> None:
        sys.exit()

    def _send_message_if_needed(self) -> None:
        if self.news_to_publish == []:
            logger.info(f"{self.name}: No news to share")
        else:
           self._post_news_on_discord(self.news_to_publish)

    def _post_news_on_discord(self, news_to_publish) -> None:
        for new_post in news_to_publish:
            self.message.send_news(new_post)

    def _is_too_old_news(self, single_news):
        date_time = parser.parse(single_news['published'])
        timezone = Utils.get_timezone()
        time_since_published = timezone.localize(
            datetime.datetime.now()
        ) - date_time.astimezone(timezone)
        return not time_since_published.total_seconds() <= self.published_since

    def _get_unsended_news(self): # TODO Refacto this
        all_posts = self._get_feed_data(self.url)
        news_to_publish = []
        news_to_save = news_to_publish
        is_not_in_error = all_posts != []
        if is_not_in_error:
            if self.latest_post != '':
                for single_news in all_posts:
                    if single_news.title == self.latest_post:
                        break
                    news_to_publish.append(single_news)
            else:
                if int(self.published_since) == 0:
                    news_to_save = [all_posts[0]]
                else:
                    for single_news in all_posts:
                        if self._is_too_old_news(single_news):
                            break
                        news_to_publish.append(single_news)
            self._register_latest_post(news_to_save)
            reversed_list_from_oldest_to_earliest = list(reversed(news_to_publish))
            return reversed_list_from_oldest_to_earliest
        return news_to_publish

    def _get_feed_data(self, feed_url): # TODO Refacto this with a "try again" behaviour for is_valid_url
        xml_entries = feedparser.parse(feed_url).entries
        if xml_entries != []:
            return xml_entries
        elif self.generator_exist:
            rss_feed = RSSGenerator(feed_url).render_xml_feed()
            feed_parsed = feedparser.parse(rss_feed).entries
            if feed_parsed == []:
                logger.error(f"The RSS Generator can't generate a feed based on the URL {feed_url}")
                self.is_valid_url = False
            return feed_parsed
        else:
            raise Exception(f"URL: {feed_url} is not a valid url")