from src.utils import Utils
from src.logger import Logger
from src.message import CommandMessage

logger = Logger.get_logger()

class BotCommands:

    def __init__(self, client, parser, message, generator_exist) -> None:
        self.client = client
        self.parser = parser
        self.generator_exist = generator_exist
        self.author = message.author
        self.channel = message.channel
        self.server = message.guild.id if "id" in dir(message.guild) else ""
        self.msg_content = message.content
        self.message = CommandMessage(self.client,
            msg_content=self.msg_content,
            author=self.author,
            channel=self.channel,
            server=self.server
        )

    async def handle_messages(self):
        help_triggered = Utils.is_include_in_string("help", self.msg_content)
        add_triggered = Utils.is_include_in_string("add", self.msg_content)
        delete_triggered = Utils.is_include_in_string("delete", self.msg_content)

        if add_triggered:
            await self._handle_adding_feed()
        elif delete_triggered:
            await self._handle_deletion_feed()
        elif not help_triggered:
            self.message.send_help(is_in_error=True)
        else:
            self.message.send_help()

    async def _handle_adding_feed(self):
        url_submited, channel_submited = self._get_message_data()
        url_is_valid = Utils.is_a_valid_url(url_submited)
        channel_name, channel_is_valid = await Utils.is_a_valid_channel(self.client, channel_submited, self.server)

        self.message.set_data_submited(url_submited, channel_name)
        self.message.send_add_waiting()
        
        if url_is_valid and channel_is_valid:
            try:
                self.parser.append_new_feed(
                    url_submited, 
                    channel_submited, 
                    channel_name, 
                    self.server,
                    self.generator_exist
                )
                self.message.send_add_success()
            except:
                self.message.send_add_error(url_in_error=True)
        elif url_is_valid and not channel_is_valid:
            self.message.send_add_error(channel_in_error=True)
        elif not url_is_valid and channel_is_valid:
            self.message.send_add_error(url_in_error=True)
        else:
            self.message.send_add_error()

    async def _handle_deletion_feed(self):
        url_submited, _ = self._get_message_data()
        url_is_valid = Utils.is_a_valid_url(url_submited)
        self.message.set_data_submited(url_submited,_)
        self.message.send_delete_waiting()

        if url_is_valid:
            self.message.send_delete_success()
        else:
            self.message.send_delete_error(url_in_error=True)

    def _get_message_data(self):
        url_submited = ""
        channel_submited = ""
        array_string = self.msg_content.split()
        for elem in array_string:
            if Utils.is_include_in_string("add", elem) \
                or Utils.is_include_in_string("delete", elem):
                try:
                    url_submited = elem.split('=')[1]
                except:
                    url_submited = ""
            elif "channel" in elem:
                try:
                    channel_submited = elem.split('=')[1]
                except:
                    channel_submited = ""
        return url_submited, channel_submited