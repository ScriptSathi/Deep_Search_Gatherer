import discord
from src.message_builders import NewsMessageBuilder, CommandMessageBuilder
from src.logger import Logger

logger = Logger.get_logger()

class Message:
    def __init__(self, client, channel) -> None:
        self.client = client
        self.channel = channel

    def _send_discord(self, message, embed = False):
        if embed:
            self.client.loop.create_task(self.channel.send(embed=message))
        else:
            self.client.loop.create_task(self.channel.send(message))

    def _send_stdout(self, **options):
        is_a_news = options.pop('is_a_news', False)
        news = options.pop('news', '')
        msg_content = options.pop('msg_content', '')
        server = options.pop('server', '')
        author = options.pop('author', '')

        if is_a_news:
            logger.info(f'{author} - Publishing on channel "{self.channel.name}" - "{news.title}"')
        else:
            logger.info(f'Author: {author} from server {server} on channel {self.channel.name} - "{msg_content}"')

class NewsMessage(Message):
    def __init__(self, client, channel: discord.TextChannel, feed_name) -> None:
        super().__init__(client, channel)
        self.feed_name = feed_name

    def send_news(self, news):
        message = NewsMessageBuilder(news).build_message()
        self._send_stdout(news=news, author=self.feed_name, is_a_news=True)
        self._send_discord(message)

class CommandMessage(Message):
    def __init__(self, client, author, channel: discord.TextChannel, msg_content, server_name) -> None:
        super().__init__(client, channel)
        self.msg_content = msg_content
        self.author = author
        self.server_name = server_name
        self.builder = CommandMessageBuilder(
            client.user.id, 
            self.msg_content, 
            self.author, 
            self.channel, 
            self.server_name
        )

    def send_help(self, is_in_error=False):
        answer_to_user = self.builder.build_help_message(is_in_error)
        self._send_discord(answer_to_user, True)

    def send_feeds_list(self, server_name, server_config):
        answer_to_user = self.builder.build_feeds_list_message(server_name, server_config)
        self._send_discord(answer_to_user, True)

    def send_feeds_list_empty(self, server_name):
        answer_to_user = self.builder.build_feeds_list_empty_message(server_name)
        self._send_discord(answer_to_user, True)

    def send_add_waiting(self):
        answer_to_user = self.builder.build_add_waiting_message()
        self._send_discord(answer_to_user, True)

    def send_add_success(self, feed_name):
        answer_to_user = self.builder.build_add_success_message(feed_name)
        self._send_discord(answer_to_user, True)

    def send_add_error(self, **props):
        answer_to_user = self.builder.build_add_error_message(**props)
        self._send_discord(answer_to_user, True)

    def send_delete_waiting(self):
        answer_to_user = self.builder.build_delete_waiting_message()
        self._send_discord(answer_to_user, True)

    def send_delete_success(self):
        answer_to_user = self.builder.build_delete_success_message()
        self._send_discord(answer_to_user, True)

    def send_delete_error(self, **props):
        answer_to_user = self.builder.build_delete_error_message(**props)
        self._send_discord(answer_to_user, True)

    def set_data_submited(self, **options):
        self.builder.set_data_submited(**options)
