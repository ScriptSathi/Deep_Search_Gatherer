from discord import Client, Message, Guild, TextChannel, User, Member
from typing import Tuple, Union

from src.utils import BotCommandsUtils, Utils
from src.core.messages.message import CommandMessage
from .context import Context

class BotCommands:

    client: Client
    context: Context
    generator_exist: bool
    author: Union[User, Member]
    channel: TextChannel
    server = Union[Guild, str]
    msg_content: str 
    message: CommandMessage

    def __init__(self, client: Client, context: Context, message: Message, generator_exist: bool) -> None:
        self.client = client
        self.context: Context = context
        self.generator_exist = generator_exist
        self.author = message.author
        self.channel = message.channel
        self.server = message.guild if "guild" in dir(message) else ""
        self.msg_content = message.content
        self.message = CommandMessage(
            self.client,
            msg_content=self.msg_content,
            author=self.author,
            channel=self.channel,
            server_name=self.server.name
        )

    async def handle_messages(self) -> None:
        help_trigger, add_trigger, delete_trigger, list_trigger = (0,1,2,3)
        is_trigger = BotCommandsUtils.get_command_name(self.msg_content)
        if list_trigger == is_trigger:
            self._handle_feeds_list()
        elif help_trigger == is_trigger:
            self.message.send_help()
        elif add_trigger == is_trigger or delete_trigger == is_trigger:
            url_submited, channel_submited, name_submited = self._get_message_data()
            if url_submited == "" and name_submited == "":
                self.message.send_help(is_in_error=True)
            else:
                if add_trigger == is_trigger:
                    await self._handle_adding_feed(url_submited, channel_submited, name_submited)
                else:
                    await self._handle_deletion_feed(self.server.id, name_submited)
        else:
            self.message.send_help(is_in_error=True)

    def _handle_feeds_list(self) -> None:
        reg_server = self.context.get_registered_server(self.server.id)
        if reg_server is None or reg_server.feeds == []:
            self.message.send_feeds_list_empty(self.server.name)
        else:
            self.message.send_feeds_list(reg_server)

    async def _handle_adding_feed(self, link_submited: str, channel_submited: str, name_submited: str) -> None:
        type, link = BotCommandsUtils.check_link_and_return(
            link_submited, 
            self.context.user_config
        )
        try:
            channel_obj = await self.client.fetch_channel(str(channel_submited))
        except:
            channel_obj = None
        chan_name = channel_obj.name if channel_obj != None else channel_submited
        self.message.set_data_submited(channel=chan_name, link=link)
        self.message.send_add_waiting()
        if link != None and channel_obj != None:
            try:
                feed=""
                feed = self.context.add(link, channel_obj, name_submited, type)
                self.message.send_add_success(feed.name, feed.url)
            except:
                self.message.send_add_error(url_in_error=True)
        elif link != None and not channel_obj != None:
            self.message.set_data_submited(channel=channel_submited, link=link)
            self.message.send_add_error(channel_in_error=True)
        elif link is None and channel_obj != None:
            self.message.set_data_submited(channel=channel_obj.name, link=link)
            self.message.send_add_error(url_in_error=True)
        else:
            self.message.send_add_error()

    async def _handle_deletion_feed(self, server_id: int, feed_name: str) -> None:
        self.message.set_data_submited(feed_name=feed_name)
        self.message.send_delete_waiting()
        if feed_name != '':
            try:
                self.context.remove(without_feed=(feed_name, server_id))
                self.message.send_delete_success(feed_name)
            except:

                self.message.send_delete_error()
        else:
            self.message.send_delete_error()

    def _get_message_data(self) -> Tuple[str, str, str]:
        url_submited = ""
        channel_submited = ""
        name_submitted = ""
        array_string = self.msg_content.split()
        user_cmd = list(filter(None, array_string))
        for i, elem in enumerate(user_cmd):
            is_not_last_elem_in_list = elem !=  user_cmd[-1]
            if is_not_last_elem_in_list: 
                add_trigger = 1
                is_trigger = BotCommandsUtils.get_command_name(self.msg_content)
                if add_trigger == is_trigger:
                    if Utils.is_include_in_string("add", elem):
                        url_submited = user_cmd[i+1]
                    if Utils.is_include_in_string(["channel", "chan"], elem):
                        channel_submited = user_cmd[i+1]
                    if Utils.is_include_in_string("name", elem):
                        name_submitted = user_cmd[i+1]
                elif Utils.is_include_in_string(["delete", "dl", "del"], elem):
                    name_submitted = user_cmd[i+1]
        return url_submited, channel_submited, name_submitted
