import feedparser, datetime, sys

from dateutil import parser

from src.message import NewsMessage
from src.utils import Utils
from src.logger import Logger
from src.constants import Constants
from src.rss_gen import RSSGenerator

logger = Logger.get_logger()

class Feed:

    def __init__(self, feed_config, chan, latest_post, generator_exist = False) -> None:
        self.latest_post = latest_post
        self.feed_config = feed_config
        self.channel = chan
        self.generator_exist = generator_exist
        
        all_posts = self._get_feed_data(self.feed_config['url'])
        self.news_to_publish = self._get_unsended_news(all_posts)

    def run(self, client) -> None:
        self.message = NewsMessage(client, channel=self.channel, feed_config=self.feed_config)
        self._send_message_if_needed()
        self._close_thread()

    def _register_latest_post(self, news_to_save):
        if news_to_save != []:
            self.latest_post = news_to_save[0].title
            self.feed_config['last_post'] = self.latest_post

    def _close_thread(self) -> None:
        sys.exit()

    def _send_message_if_needed(self) -> None:
        if self.news_to_publish == []:
            logger.info(f"{self.feed_config['name']}: No news to share")
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
        return not time_since_published.total_seconds() <= self.feed_config['published_since']

    def _get_unsended_news(self, all_posts):
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
                if int(self.feed_config['published_since']) == 0:
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

    def _get_feed_data(self, feed_url):
        xml_entries = feedparser.parse(feed_url).entries
        if xml_entries != []:
            return xml_entries
        elif self.generator_exist:
            rss_feed = RSSGenerator(feed_url).render_xml_feed()
            feed_parsed = feedparser.parse(rss_feed).entries
            if feed_parsed == []:
                logger.error(f"The RSS Generator can't generate a feed based on the URL {feed_url}")
                self.feed_config['is_valid_url'] = False
            return feed_parsed
        else:
            raise Exception(f"URL: {feed_url} is not a valid url")