import datetime, pytz, sys

from dateutil import parser
from typing_extensions import TypedDict
from discord import Client, TextChannel
from abc import ABCMeta, abstractclassmethod
from typing import Any, List

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

class AFeed(metaclass=ABCMeta):

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
    type: int
    is_valid_url: bool = True
    published_since: int = 0

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
        self.name = name
        self.client = client
        self.url = url
        self.uid = uid
        self.channels = channels
        self.server_on = server_on
        self.generator_exist = generator_exist
        self.news_to_publish = []
        self.last_post = last_post
        self.type = type
        self.message = NewsMessage(client, channels, name)

    @abstractclassmethod
    def run(self) -> None:
        pass

    @abstractclassmethod
    def _send_news(self) -> None:
        pass

    @abstractclassmethod
    def _close_thread(self) -> None:
        pass

class Feed(AFeed):

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

    def get_feed_backup(self, server_id: int) -> Feed_backup_dict:
        return {
            "name": self.name,
            "url": self.url,
            "last_post": self.last_post,
            "channels": [channel.id for channel in self.channels if channel.guild.id == server_id],
            "type": self.type   ,
        }

    def _is_too_old_news(self, date_time: datetime.datetime, to_parse=False) -> bool:
        def get_timezone() -> pytz.timezone:
            tz = 'Europe/Paris'
            try:
                timezone = pytz.timezone(tz)
            except Exception:
                timezone = pytz.utc
            return timezone
        if to_parse:
            date_time = parser.parse(date_time)
        timezone = get_timezone()
        time_since_published = timezone.localize(
            datetime.datetime.now()
        ) - date_time.astimezone(timezone)
        return not time_since_published.total_seconds() <= self.published_since
    
    def _close_thread(self) -> None:
        sys.exit()