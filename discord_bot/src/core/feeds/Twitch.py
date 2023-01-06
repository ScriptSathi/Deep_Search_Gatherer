from datetime import datetime
from typing import List, TypedDict
from discord import Client, TextChannel
from twitchAPI import Twitch as Twitch_Client

from src.core.messages.message_builders import PostMessage
from src.core.registered_data import RegisteredServer
from . import Feed

Channel_Data = TypedDict(
    "Channel_Data",
    {
        'broadcaster_language': str,
        'broadcaster_login': str,
        'display_name': str,
        'game_id': int,
        'game_name': str,
        'id': str,
        'is_live': bool,
        'tag_ids': List[str],
        'thumbnail_url': str,
        'title': str,
        'started_at': str,
    }
)

class Twitch(Feed):

    tw_client: Twitch_Client
    user_id: int
    is_live: bool

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
        tw_client: Twitch_Client
    ) -> None:
        super().__init__(client, channels, name, url, server_on, uid, generator_exist, last_post, type)
        self.tw_client = tw_client
        self.user_display_name = self.tw_client.get_users(logins=[self.name])['data'][0]['display_name']
        self._use_backup_channel_status()

    def run(self) -> None:
        channel_data = self._get_data()
        if self._channel_changed_status(channel_data) and channel_data['is_live']:
            self.is_live = not self.is_live
            self.message.send_news(PostMessage(
                f"{channel_data['display_name']} is live",
                channel_data['title'],
                f"https://www.twitch.tv/{self.name}",
                channel_data['display_name'],
                channel_data['thumbnail_url'],
                channel_data['game_name'],
                datetime.strptime(channel_data['started_at'], "%Y-%m-%dT%H:%M:%SZ")
            ), self.type, True)
        else:
            self.message.send_no_news()
            if not channel_data['is_live']:
                self.is_live = False
        self._register_latest_post(channel_data['is_live'])

    def _get_data(self) -> Channel_Data:
        all_data = self.tw_client.search_channels(self.user_display_name)
        chan_data: Channel_Data
        for _chan_data in all_data['data']:
            if _chan_data['display_name'] == self.user_display_name:
                chan_data = _chan_data
        return chan_data

    def _channel_changed_status(self, channel_data: Channel_Data):
        return self.is_live != channel_data['is_live']

    def _register_latest_post(self, is_live: bool) -> None:
        self.last_post = is_live

    def _use_backup_channel_status(self) -> None:
        self.is_live = self.last_post if self.last_post != "" else False