from typing import Any, List, Union
import discord

from src.core.registered_data import RegisteredServer
from .message_builders import NewsMessageBuilder, CommandMessageBuilder, PostMessage
from src.logger import Logger

logger = Logger.get_logger()

class Message:

    def standard_output(server_name: str, server_id: str) -> str:
        return f"On {server_name}({server_id})"

    def __init__(self,
        client: discord.Client,
        channels: List[discord.TextChannel],
        feed_name: str,
        **props: Union[str, bool]
    ) -> None:
        self.client: discord.Client = client
        self.feed_name: str = feed_name
        self.channels: discord.TextChannel = channels
        self.is_a_news = props.pop('is_a_news', False)
        
    def _send_discord(self, message, embed = False) -> None:
        for channel in self.channels:
            if embed:
                self.client.loop.create_task(channel.send(embed=message))
            else:
                self.client.loop.create_task(channel.send(message))

    def _send_stdout(self, **options) -> None:
        no_news = options.pop('no_news', False)
        add = options.pop('add', {})
        delete = options.pop('delete', {})
        news = options.pop('news', '')
        msg_content = options.pop('msg_content', '')
        author = options.pop('author', '')
        for channel in self.channels:
            server_name: str = channel.guild.name
            server_id: int = channel.guild.id
            base_message = Message.standard_output(server_name, server_id)
            if self.is_a_news:
                if no_news:
                    logger.info(f"{base_message} - {self.feed_name} - No news to share")
                else:
                    logger.info(f'{base_message} - {self.feed_name} - Publishing on channel "{channel.name}" - "{news}"')
            elif add != {}:
                logger.info(f"{base_message} - Successfully adding {add['name']} with url {add['url']}")
            elif delete != {}:
                logger.info(f"{base_message} - Successfully deleting {delete['name']}")
            else:
                logger.info(f'{base_message} - Author: {author} on channel {channel.name} - "{msg_content}"')

class NewsMessage(Message):
    def __init__(self, client: discord.Client, channels: List[discord.TextChannel], feed_name: str) -> None:
        super().__init__(client, channels, feed_name, is_a_news=True)

    def send_news(self, news: PostMessage, type: int):
        message = NewsMessageBuilder(news).build_message(type)
        self._send_stdout(news=news.title)
        self._send_discord(message)

    def send_no_news(self):
        self._send_stdout(no_news=True)

    def send_error(self, error) -> None:
        logger.error(error)

class CommandMessage(Message):
    def __init__(self, 
        client: discord.Client,
        author: str,
        channel: discord.TextChannel,
        msg_content: str,
        server_name: str
    ) -> None:
        super().__init__(client, [channel], "")
        self.msg_content = msg_content
        self.author = author
        self.server_name = server_name
        self.builder = CommandMessageBuilder(
            client.user.id, 
            self.author
        )

    def send_simple_message_stdout(self):
        self._send_stdout(msg_content=self.msg_content)

    def send_help(self, is_in_error=False):
        answer_to_user = self.builder.build_help_message(is_in_error)
        self._send_discord(answer_to_user, True)

    def send_feeds_list(self, reg_server: RegisteredServer):
        answer_to_user = self.builder.build_feeds_list_message(reg_server)
        self._send_discord(answer_to_user, True)

    def send_feeds_list_empty(self, server_name):
        answer_to_user = self.builder.build_feeds_list_empty_message(server_name)
        self._send_discord(answer_to_user, True)

    def send_add_waiting(self):
        answer_to_user = self.builder.build_add_waiting_message()
        self._send_discord(answer_to_user, True)

    def send_add_success(self, feed_name, feed_url):
        answer_to_user = self.builder.build_add_success_message(feed_name)
        self._send_discord(answer_to_user, True)
        self._send_stdout(add={"name":feed_name,"url":feed_url})

    def send_add_error(self, **props):
        answer_to_user = self.builder.build_add_error_message(**props)
        self._send_discord(answer_to_user, True)

    def send_delete_waiting(self):
        answer_to_user = self.builder.build_delete_waiting_message()
        self._send_discord(answer_to_user, True)

    def send_delete_success(self, feed_name):
        answer_to_user = self.builder.build_delete_success_message()
        self._send_discord(answer_to_user, True)
        self._send_stdout(delete={"name":feed_name})

    def send_delete_error(self, **props):
        answer_to_user = self.builder.build_delete_error_message(**props)
        self._send_discord(answer_to_user, True)

    def set_data_submited(self, **options):
        self.builder.set_data_submited(**options)
