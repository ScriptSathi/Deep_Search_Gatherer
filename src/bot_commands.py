from src.logger import Logger
from src.message import Message

logger = Logger.get_logger()

class BotCommands:

    def __init__(self, client, message) -> None:
        self.client = client
        self.author = message.author
        self.channel = message.channel
        self.server = message.guild.id if "id" in dir(message.guild) else ""
        self.msg_content = message.content
        self.message = Message(self.client)
        
    def do_smth(self):
        self.message.send_help(
            self.msg_content, 
            self.author, 
            self.channel, 
            self.server
        )