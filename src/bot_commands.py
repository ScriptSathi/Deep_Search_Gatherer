import discord

from src.utils import Utils
from src.logger import Logger
from src.message import CommandMessage
from src.context import ContextUtils, Context

logger = Logger.get_logger()

class BotCommands:

    def __init__(self, client, context, message, generator_exist) -> None:
        self.client: discord.Client = client
        self.context: Context = context
        self.generator_exist = generator_exist
        self.author = message.author
        self.channel = message.channel
        self.server = message.guild if "guild" in dir(message) else ""
        self.msg_content = message.content
        self.message = CommandMessage(self.client,
            msg_content=self.msg_content,
            author=self.author,
            channel=self.channel,
            server_name=self.server.name
        )

    async def handle_messages(self):
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

    def _handle_feeds_list(self):
        server_config = self.context.get_server_config(self.server.id)
        if server_config == [] or server_config['feeds'] == []:
            self.message.send_feeds_list_empty(self.server.name)
        else:
            self.message.send_feeds_list(self.server.name, server_config)

    async def _handle_adding_feed(self, url_submited, channel_submited, name_submited):
        url_is_valid = Utils.is_a_valid_url(url_submited)
        channel_obj = await ContextUtils.get_channel_object(self.client, channel_submited)
        if url_is_valid and channel_obj != None:
            self.message.set_data_submited(channel=channel_obj.name, url=url_submited)
            self.message.send_add_waiting()
            try:
                feed_name = self.context.append_new_feed(
                    url_submited,
                    channel_obj,
                    self.server.id,
                    self.generator_exist,
                    name_submited
                )
                self.message.send_add_success(feed_name)
            except:
                self.message.send_add_error(url_in_error=True)
        elif url_is_valid and not channel_obj != None:
            self.message.send_add_error(channel_in_error=True)
        elif not url_is_valid and channel_obj != None:
            self.message.send_add_error(url_in_error=True)
        else:
            self.message.send_add_error()

    async def _handle_deletion_feed(self, server_id, feed_name):
        logger.info(feed_name)
        self.message.set_data_submited(feed_name=feed_name)
        self.message.send_delete_waiting()
        if feed_name != '':
            try:
                self.context.delete_from_config('name', feed_name, server_id)
                self.message.send_delete_success()
            except:
                self.message.send_delete_error()
        else:
            self.message.send_delete_error()

    def _get_message_data(self):
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

class BotCommandsUtils:
    def get_command_name(full_message_str):
        help_trigger, add_trigger, delete_trigger, list_trigger = (0,1,2,3)
        msg = full_message_str.split()
        if Utils.is_include_in_string('help', msg[1]) or Utils.is_include_in_string('-h', msg[1]):
            return help_trigger
        elif Utils.is_include_in_string('add', msg[1]):
            return add_trigger
        elif Utils.is_include_in_string('delete', msg[1]) or Utils.is_include_in_string('del', msg[1]):
            return delete_trigger
        elif Utils.is_include_in_string('list', msg[1]) or Utils.is_include_in_string('ls', msg[1]):
            return list_trigger
        else:
            return 100