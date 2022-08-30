from discord import Client, TextChannel
from typing import Any, Dict, List, Union
import feedparser, datetime, sys

from dateutil import parser

from src.rss_gen import RSSGenerator
from src.message import NewsMessage
from src.utils import Utils
from src.generic_types import Feed, Feed_backup_dict
from src.registered_data import RegisteredServer

from src.logger import Logger
logger = Logger.get_logger()

class RSS(Feed):

    def find_feed_name(url: str):
        data = feedparser.parse(url)
        name = data.feed['title'] if "title" in data.feed else f"feed-{Utils.generate_random_string()}"
        return name.replace(" ", "-")

    def __init__(self,
        client: Client,
        channels: List[TextChannel],
        name: str,
        url: str,
        server_on: RegisteredServer,
        uid: int,
        generator_exist: bool,
        last_post: str
    ) -> None:
        super().__init__(client, channels, name, url, server_on, uid, generator_exist, last_post)
        self.published_since = 16000 # FOR TEST ONLY

    def run(self) -> None:
        self.news_to_publish = self._get_news()
        self._send_news()
        self._close_thread()

    def get_feed_backup(self, server_id: int) -> Feed_backup_dict:
        return {
            "name": self.name,
            "url": self.url,
            "last_post": self.last_post,
            "channels": [channel.id for channel in self.channels if channel.guild.id == server_id],
        }

    def _send_news(self) -> None:
        if self.news_to_publish == []:
            self.message.send_no_news()
        else:
            for new_post in self.news_to_publish: 
                self.message.send_news(new_post)

    def _register_latest_post(self, news_to_save):
        if news_to_save != []:
            self.last_post = news_to_save[0].title

    def _close_thread(self) -> None:
        sys.exit()

    def _is_too_old_news(self, single_news) -> bool:
        date_time = parser.parse(single_news['published'])
        timezone = Utils.get_timezone()
        time_since_published = timezone.localize(
            datetime.datetime.now()
        ) - date_time.astimezone(timezone)
        return not time_since_published.total_seconds() <= self.published_since

    def _get_news(self) -> List[Any]: # TODO Refacto this
        all_posts = Utils.sync_try_again_if_fail(
                        self._get_feed_data,
                        resolve_args=(self.url, 0),
                        reject=self._exception_get_data,
                    )
        all_posts = self._get_feed_data(self.url)
        news_to_publish: List[Any] = []
        news_to_save = news_to_publish
        is_not_in_error = all_posts != []
        if is_not_in_error:
            if self.last_post != '':
                for single_news in all_posts:
                    if single_news.title == self.last_post:
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

    def _get_feed_data(self, feed_url: str, retry_attempt: int = 0) -> List[Any]: # TODO Refacto this with a "try again" behaviour for is_valid_url
        if retry_attempt <= 3:
            xml_entries = feedparser.parse(feed_url).entries
            if xml_entries != []:
                return xml_entries
            elif self.generator_exist:
                rss_feed = RSSGenerator(feed_url).render_xml_feed()
                feed_parsed = feedparser.parse(rss_feed).entries
                if feed_parsed == []:
                    self.message.send_error(f"The RSS Generator can't generate a feed based on the URL {feed_url}")
                return feed_parsed
            else:
                raise Exception(f"URL: {feed_url} is not a valid url")
        else:
            self.is_valid_url = False
    
    def _exception_get_data(self, _: Exception, feed_url: str, attempt: int) -> None:
        logger.error(f"Fail to read {feed_url}, attempt n°{attempt}")
