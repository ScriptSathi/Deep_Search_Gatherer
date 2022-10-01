from datetime import datetime
from praw import Reddit as Reddit_Client, models as Rd_models
from discord import Client, TextChannel
from typing import Any, List

from src.core.messages.message_builders import PostMessage
from . import Feed
from src.core.registered_data import RegisteredServer

from src.logger import Logger
logger = Logger.get_logger()

class Reddit(Feed):

    rd_client: Reddit_Client

    def __init__(self,
        client: Client,
        channels: List[TextChannel],
        name: str,
        url: str,
        server_on: RegisteredServer,
        uid: int,
        generator_exist: bool,
        last_post: str,
        type: int,
        reddit_client: Reddit_Client,
    ) -> None:
        super().__init__(client, channels, name, url, server_on, uid, generator_exist, last_post, type)
        self.rd_client = reddit_client

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
                    "",
                    "" if "url" in vars(new_post).values() and new_post.url != "" else new_post.url,
                    self.url,
                    f"https://www.reddit.com{new_post.permalink}"
                ), self.type)

    def _register_latest_post(self, news_to_save: List[Any]) -> None:
        if news_to_save != []:
            self.last_post = news_to_save[0].title

    def _get_news(self) -> List[Rd_models.Submission]:
        all_posts = self._get_feed_data()
        news_to_publish: List[Any] = []
        news_to_save = news_to_publish
        is_not_in_error = all_posts != []
        if is_not_in_error:
            if self.last_post != '':
                for single_news in all_posts:
                    if single_news.created_utc == self.last_post:
                        break
                    news_to_publish.append(single_news)
            else:
                if int(self.published_since) == 0:
                    news_to_save = [post for i, post in enumerate(all_posts) if i == 0]
                else:
                    for single_news in all_posts:
                        if self._is_too_old_news(datetime.fromtimestamp(single_news.created_utc)):
                            break
                        news_to_publish.append(single_news)
            self._register_latest_post(news_to_save)
            return_list: List[Rd_models.Submission] = []
            for elem in news_to_publish:
                return_list.append(elem)
            return return_list
        return news_to_publish

    def _get_feed_data(self) -> Rd_models.ListingGenerator:
        return self.rd_client.subreddit(self.url).top(time_filter="day", limit=25)

    def _register_latest_post(self, news_to_save: List[Rd_models.Submission]):
        if news_to_save != []:
            self.last_post = news_to_save[0].created_utc