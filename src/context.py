from typing_extensions import Literal
from discord import TextChannel, Client
from pydash import _
from random import randint
from typing import List, Union

from src.generic_types import Feed
from src.feeds_manager import FeedsManager
from src.registered_data import RegisteredServer, RegisteredFeed

class Context:
    client: Client
    registered_data: List[RegisteredServer] = []
    manager: FeedsManager = FeedsManager()
    generator_exist: bool

    def __init__(self, client: Client, generator_exist: bool) -> None:
        self.client = client
        self.generator_exist = generator_exist

    def add(self, url: str, channel: TextChannel, name: str, last_post: str = "") -> Feed:
        type = ContextUtils.get_type(url)
        server = ContextUtils.get_registered_server(channel.guild.id, self.registered_data)
        feed: Feed = self.manager.get_feed(type, "url", url)
        if server == None:
            server = RegisteredServer(channel.guild.id, channel.guild.name)
            self.registered_data.append(server)
        if feed == None:
            uid = ContextUtils.create_uid(10)
            feed = self.manager.create_feed(type, self.client, channel, name, url, server, uid, self.generator_exist, last_post)
            self.manager.append_feed(type, feed)
            server.feeds.append(RegisteredFeed(uid, type, feed.name, url, channel.id))
        else:
            feed.channels.append(channel)
            (reg_feed.registered_channels.append(channel.id) for reg_feed in server.feeds if reg_feed.name == name)
        return feed

    def remove(self, **options) -> None:
        if "with_feed" in options:
            feed, type = options.get('with_feed')
            server_id = feed.server_on.id
        else:
            feed_name, server_id = options.get('without_feed')
            feed = ContextUtils.get_registered_feed(feed_name,
                ContextUtils.get_registered_server(server_id, self.registered_data))
            type = feed.type
        self.manager.remove_feed(type, feed.uid)
        for server in self.registered_data:
            if server.id == server_id:
                _.remove(server.feeds, lambda feed_to_delete: feed_to_delete.uid == feed.uid)

class ContextUtils:
    def get_registered_server(server_id: int, registered_data: List[RegisteredServer]) -> RegisteredServer:
        server = None
        for registered_server in registered_data:
            if registered_server.id == server_id:
                server = registered_server
        return server

    def get_registered_feed(feed_name, registered_server: RegisteredServer) -> RegisteredFeed:
        feed = None
        for registered_feed in registered_server.feeds:
            if registered_feed.name == feed_name:
                feed = registered_feed
        return feed

    def create_uid(n) -> int:
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)        

    def get_type(url) -> Union[Literal[0], Literal[1], Literal[2]]:
        rss, reddit, twitter = 0, 1, 2
        if url.startswith("https://www.reddit.com"):
            return reddit
        elif url.startswith("https://www.twitter.com"):
            return twitter
        else:
            return rss