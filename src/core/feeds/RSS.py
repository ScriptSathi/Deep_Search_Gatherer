from discord import Client, TextChannel
from typing import Any, List
import feedparser
from time import sleep
from html2text import HTML2Text
from re import sub

from src.core.messages.message_builders import PostMessage
from src.rss_gen import RSSGenerator
from . import Feed
from src.core.registered_data import RegisteredServer

class RSS(Feed):

    def __init__(self,
        client: Client,
        channels: List[TextChannel],
        name: str,
        url: str,
        server_on: RegisteredServer,
        uid: int,
        generator_exist: bool,
        last_post: str,
        type: int
    ) -> None:
        super().__init__(client, channels, name, url, server_on, uid, generator_exist, last_post, type)

    def run(self) -> None:
        self.news_to_publish = self._get_news()
        self._send_news()
        self._close_thread()

    def _send_news(self) -> None:
        if self.news_to_publish == []:
            self.message.send_no_news()
        else:
            for new_post in self.news_to_publish:
                self.message.send_news(PostMessage(
                    new_post.title,
                    self._parse_html(new_post) if not self._is_youtube_feed(new_post) else '',
                    new_post.link,
                    self._render_author(new_post),
                ), self.type)

    def _register_latest_post(self, news_to_save: List[Any]) -> None:
        if news_to_save != []:
            self.last_post = news_to_save[0].title

    def _get_news(self) -> List[Any]: # TODO Refacto this
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
                        if self._is_too_old_news(single_news['published'], True):
                            break
                        news_to_publish.append(single_news)
            self._register_latest_post(news_to_save)
            reversed_list_from_oldest_to_earliest = list(reversed(news_to_publish))
            return reversed_list_from_oldest_to_earliest
        return news_to_publish

    def _get_feed_data(self, feed_url: str) -> List[Any]: # TODO Refacto this with a "try again" behaviour for is_valid_url
        fail_status_code = 100
        retry_delay = 2
        def try_get_data():
            xml_entries = feedparser.parse(feed_url).entries
            if xml_entries != []:
                return xml_entries
            elif self.generator_exist:
                rss_feed = RSSGenerator(feed_url).render_xml_feed()
                feed_parsed = feedparser.parse(rss_feed).entries
                if feed_parsed != []:
                    return feed_parsed
            return fail_status_code
            
        for attempt in range(4):
            if attempt < 3:
                data = try_get_data()
                if data != fail_status_code:
                    break
                else:
                    self.message.send_error(f"Fail to read {feed_url}, attempt n°{attempt} in {retry_delay} seconds")
                    sleep(retry_delay)
            else:
                self.message.send_error(f"Error with url {feed_url} after {attempt} attempt. Deleting it ...")
                self.is_valid_url = False
                self._close_thread()
                return []
        return data

    def _render_author(self, new_post):
        if 'authors' or 'author' in new_post:
            if 'authors' in new_post:
                if new_post['authors'][0] == {}:
                    return "Unknow authors"
                else:
                    str_authors = 'Author: '
                    if len(new_post['authors']) == 1:
                        str_authors += (new_post['authors'][0]).name
                    else:
                        for author in new_post['authors']:
                            str_authors += author.name + ', '
                    return str_authors
            elif 'author' in new_post:
                return "Unknow author" if new_post['author'] == {} else new_post['author'].name
        return ''

    def _parse_html(self, new_post): 
        htmlfixer: HTML2Text = HTML2Text()
        htmlfixer.ignore_links = True
        htmlfixer.ignore_images = True
        htmlfixer.ignore_emphasis = False
        htmlfixer.body_width = 1000
        htmlfixer.ul_item_mark = "-" 
        markdownfield = htmlfixer.handle(new_post.summary)
        return sub("<[^<]+?>", "", markdownfield)

    def _is_youtube_feed(self, new_post):
        return 'yt_videoid' in new_post