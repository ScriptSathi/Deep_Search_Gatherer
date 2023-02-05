import asyncio
from typing import List
from discord import Client, TextChannel
from twitchAPI import Twitch as Twitch_Client
from twitchAPI.helper import first
from twitchAPI.object import SearchChannelResult, TwitchUser

from src.core.messages.message_builders import PostMessage
from src.core.registered_data import RegisteredServer
from . import Feed

class Twitch(Feed):

    tw_client: Twitch_Client
    user_id: int
    is_live: bool
    tw_user: TwitchUser

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
        self._use_backup_channel_status()

    def run(self) -> None:
        asyncio.run(self.async_run())

    async def async_run(self) -> None:
        self.tw_user =(await first(self.tw_client.get_users(logins=self.name)))
        channel_data = await self._get_data()
        if self._channel_changed_status(channel_data) and channel_data.is_live:
            self.is_live = not self.is_live
            self.message.send_news(PostMessage(
                f"{self.tw_user.display_name} is live",
                channel_data.title,
                f"https://www.twitch.tv/{self.name}",
                self.tw_user.display_name,
                self.tw_user.profile_image_url,
                channel_data.game_name,
                channel_data.started_at
            ), self.type, True)
        else:
            self.message.send_no_news()
            if not channel_data.is_live:
                self.is_live = False
        self._register_latest_post(channel_data.is_live)

    async def _get_data(self) -> SearchChannelResult:
        return await first(self.tw_client.search_channels(self.tw_user.display_name))

    def _channel_changed_status(self, channel_data: SearchChannelResult):
        return self.is_live != channel_data.is_live

    def _register_latest_post(self, is_live: bool) -> None:
        self.last_post = is_live

    def _use_backup_channel_status(self) -> None:
        self.is_live = self.last_post if self.last_post != "" else False