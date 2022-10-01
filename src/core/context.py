from tweepy import Client as Twitter_Client
from praw import Reddit as Reddit_Client
from discord import TextChannel, Client
from pydash import _
from typing import  List, Tuple, Union

from src.user_config import User_config_dict
from src.core.feeds import Feed
from src.utils import ContextUtils, Utils
from .feeds_manager import FeedsManager
from .registered_data import RegisteredServer, RegisteredFeed

class Context:

    client: Client
    registered_data: List[RegisteredServer] = []
    manager: FeedsManager = FeedsManager()
    user_config: User_config_dict
    generator_exist: bool
    twitter_client: Twitter_Client
    reddit_client: Reddit_Client

    def __init__(self, client: Client, generator_exist: bool, user_config: User_config_dict) -> None:
        self.client = client
        self.generator_exist = generator_exist
        self.user_config = user_config
        self.twitter_client = Twitter_Client(bearer_token=user_config["twitter"]["bearer_token"])
        self.reddit_client = Reddit_Client(
                client_id=user_config["reddit"]["client_id"],
                client_secret=user_config["reddit"]["client_secret"],
                password=user_config["reddit"]["password"],
                user_agent=Utils.get_user_agent(),
                username=user_config["reddit"]["username"],
            )

    def add(self, link: str, channel: TextChannel, name: str, type, last_post: str = "") -> Feed:
        reg_server = self.get_registered_server(channel.guild.id)
        feed: Union[Feed, None] = self.manager.get_feed(type, "url", link)
        uid = feed.uid if feed is not None else ContextUtils.create_uid(10)
        if reg_server is None:
            reg_server = RegisteredServer(channel.guild.id, channel.guild.name)
            self.registered_data.append(reg_server)
        if feed is None:
            feed = self.manager.create_feed(
                type, self.client, channel, name, link, reg_server, uid, self.generator_exist, last_post,
                self.twitter_client, self.reddit_client
                )
            self.manager.append_feed(type, feed)
        else:
            if not _.includes(feed.channels, channel):
                feed.channels.append(channel)
            for reg_feed in reg_server.feeds:
                if reg_feed.name == name and not _.includes(reg_feed.registered_channels, channel):
                    reg_feed.registered_channels.append(channel.id)
        reg = RegisteredFeed(uid, type, feed.name, link, channel.id)
        reg_server.feeds.append(reg)
        return feed

    def remove(self, **options: Union[Tuple[Feed, int], Tuple[str, int]]) -> None:
        if "with_feed" in options:
            feed, type = options.get('with_feed')
            server_id = feed.server_on.id
        else:
            feed_name, server_id = options.get('without_feed')
            feed = self._get_registered_feed(feed_name,
                self.get_registered_server(server_id))
            type = feed.type
        self.manager.remove_feed(type, feed.uid)
        for server in self.registered_data:
            if server.id == server_id:
                _.remove(server.feeds, lambda feed_to_delete: feed_to_delete.uid == feed.uid)

    def get_registered_server(self, server_id: int) -> Union[RegisteredServer, None]:
        return _.find(self.registered_data, lambda server: server.id == server_id)

    def _get_registered_feed(self, feed_name, registered_server: RegisteredServer) -> Union[RegisteredFeed, None]:
        return _.find(registered_server.feeds, lambda reg_feed: reg_feed.name == feed_name)