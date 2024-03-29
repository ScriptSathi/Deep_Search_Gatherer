from tweepy import Client as Twitter_Client
from discord import TextChannel, Client
from typing import Dict, List, Union
from pydash import _
from praw import Reddit as Reddit_Client
from twitchAPI import Twitch as Twitch_Client

from src.core.feeds import Reddit, Twitter, Feed, RSS, Twitch
from src.utils import FeedUtils
from src.core.registered_data import RegisteredServer

class FeedsManager:

    feeds: List[List[Feed]] = [[],[],[],[]]

    def append_feed(self, type: int, feed: Feed) -> None:
        self.feeds[type].append(feed)

    def remove_feed(self, type: int, uid: int) -> None:
        _.pop(self.feeds[type], self._get_feed_index(type, "uid", uid))

    def create_feed(self,
        type: int,
        client: Client,
        channel: TextChannel,
        name: str,
        url: str,
        server_on: RegisteredServer,
        uid: int,
        generator_exist: bool,
        last_post: str,
        twitter_client: Twitter_Client,
        reddit_client: Reddit_Client,
        twitch_client: Union[Twitch_Client, None],
    ) -> Feed:
        rss, reddit, twitter, twitch = 0, 1, 2, 3
        feed: Feed
        if type == rss:
            if name == "":
                name = FeedUtils.find_rss_feed_name(url)
            feed = RSS(client, [channel], name, url, server_on, uid, generator_exist, last_post, type)
        elif type == reddit:
            if name == "":
                name = FeedUtils.find_reddit_feed_name(url)
            feed = Reddit(client, [channel], name, url, server_on, uid, generator_exist, last_post, type, reddit_client)
        elif type == twitter:
            if name == "":
                name = FeedUtils.find_twitter_feed_name(url, twitter_client)
            feed = Twitter(client, [channel], name, url, server_on, uid, generator_exist, last_post, type, twitter_client)
        elif type == twitch and twitch_client is not None:
            if name == "":
                name = FeedUtils.find_twitch_feed_name(url)
            feed = Twitch(client, [channel], name, url, server_on, uid, generator_exist, last_post, type, twitch_client)
        return feed

    def get_feed_backup(self, server_id: int, type: int, classvar_name: str, classvar_value: Union[str, int]) -> Dict[str, Union[str, int]]:
        return self.get_feed(type, classvar_name, classvar_value).get_feed_backup(server_id)

    def get_feed(self, type: int, classvar_name: str, classvar_value: Union[str, int]) -> Union[Feed, None]:
        index = self._get_feed_index(type, classvar_name, classvar_value)
        return self.feeds[type][index] if index != -1 else None

    def _get_feed_index(self, type: int, classvar_name: str, classvar_value: any) -> int:
        return _.find_index(self.feeds[type], lambda _, i, feed: getattr(feed[i], classvar_name) == classvar_value)