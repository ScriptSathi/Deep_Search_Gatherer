import datetime, pytz, sys

from sys import exit
from datetime import datetime
from pytz import timezone, utc
from dateutil import parser
from typing_extensions import TypedDict
from discord import Client, TextChannel
from typing import Any, List

from src.core.registered_data import RegisteredServer
from src.core.messages.message import NewsMessage

Feed_backup_dict = TypedDict(
        'Feed',
        {
            "name": str,
            "url": str,
            "last_post": str,
            "channels": List[int]
        }
    )

class Feed:

    client: Client
    channels: List[TextChannel]
    last_post: str
    name: str
    server_on: RegisteredServer
    url: str
    news_to_publish: List[Any]
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

    def __repr__(self) -> str:
        vars_in_str = ' '.join(f'{key}={value}' for key, value in vars(self).items())
        return f'<Feed {vars_in_str}>'

    def run(self) -> None:
        pass

    def _get_news(self) -> None:
        pass

    def _send_news(self) -> None:
        pass

    def get_feed_backup(self, server_id: int) -> Feed_backup_dict:
        return {
            "name": self.name,
            "url": self.url,
            "last_post": self.last_post,
            "channels": [channel.id for channel in self.channels if channel.guild.id == server_id],
            "type": self.type,
        }

    def _is_too_old_news(self, date_time: datetime, last_publication_in_sec = 0, to_parse=False) -> bool:
        def get_timezone() -> timezone:
            str_tz = 'Europe/Paris'
            try:
                tz = timezone(str_tz)
            except Exception:
                tz = utc
            return tz
        if to_parse:
            date_time = parser.parse(date_time)
        tz = get_timezone()
        time_since_published = tz.localize(
            datetime.now()
        ) - date_time.astimezone(tz)
        return not time_since_published.total_seconds() <= last_publication_in_sec

    def _close_thread(self) -> None:
        exit()
