from typing_extensions import TypedDict
from discord import Client, TextChannel
from abc import ABCMeta, abstractclassmethod
from typing import Any, ClassVar, List
from src.registered_data import RegisteredServer

from src.message import NewsMessage

Feed_backup_dict = TypedDict(
        'Feed',
        {
            "name": str,
            "url": str,
            "last_post": str,
            "channels": List[int]
        }
    )

class Feed(metaclass=ABCMeta):

    def find_feed_name(url: str):
        pass

    client: Client
    channels: List[TextChannel]
    last_post: str
    name: str
    server_on: RegisteredServer
    url: str
    news_to_publish: List[any]
    uid: int
    generator_exist: bool
    message: NewsMessage
    is_valid_url: bool = True

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
        self.name = name
        self.client = client
        self.url = url
        self.uid = uid
        self.channels = channels
        self.server_on = server_on
        self.generator_exist = generator_exist
        self.news_to_publish = []
        self.last_post = last_post
        self.message = NewsMessage(client, channels, name)

    @abstractclassmethod
    def run(self, client: Client) -> None:
        pass

    @abstractclassmethod
    def get_feed_backup(self, server_id: int) -> Feed_backup_dict:
        pass

    @abstractclassmethod
    def _send_news(self) -> None:
        pass

    @abstractclassmethod
    def _close_thread(self) -> None:
        pass

