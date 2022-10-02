from dataclasses import dataclass
from typing import Any, List
from discord import Client, TextChannel
from twitchAPI import Twitch as Twitch_Client

from src.core.messages.message_builders import PostMessage
from src.core.registered_data import RegisteredServer
from . import Feed

from src.logger import Logger
logger = Logger.get_logger()

class Twitch(Feed):

    tw_client: Twitch_Client
    user_id: int
    is_live = False

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

    def run(self) -> None:

        user_data = self.tw_client.search_channels(self.user_display_name)
        for user in user_data['data']:
            if user['display_name'] == self.user_display_name:
                logger.info(user)
        # self.message.send_news(
        #     PostMessage("AAAAA", "This is a test", self.url, self.name),
        #     self.type
        # )

    def _register_latest_post(self, pub_tweet: List[Any]) -> None:
        if pub_tweet != []:
            ...
