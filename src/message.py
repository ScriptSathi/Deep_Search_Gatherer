from src.message_builders import NewsMessageBuilder, CommandMessageBuilder
from src.logger import Logger

logger = Logger.get_logger()

class Message:
    def __init__(self, client) -> None:
        self.client = client

    def _send_discord(self, message, channel, embed = False):
        if embed:
            self.client.loop.create_task(channel.send(embed=message))
        else:
            self.client.loop.create_task(channel.send(message))

    def _send_stdout(self, channel, **options):
        is_a_news = options.pop('is_a_news', False)
        news = options.pop('news', '')
        msg_content = options.pop('msg_content', '')
        server = options.pop('server', '')
        author = options.pop('author', '')
        channel = channel.name if "name" in dir(channel) else channel

        if is_a_news:
            logger.info(f'{self.feed_config["name"]} - Publishing on channel "{channel}" - "{news.title}"')
        else:
            logger.info(f'Author: {author} from server {server} on channel {channel} - "{msg_content}"')

class NewsMessage(Message):
    def __init__(self, client, channel, feed_config) -> None:
        super().__init__(client)
        self.channel = channel
        self.feed_config = feed_config

    def send_news(self, news):
        message = NewsMessageBuilder(news).build_message()
        self._send_stdout(self.channel, news=news, is_a_news=True)
        self._send_discord(message, self.channel)

class CommandMessage(Message):
    def __init__(self, client, author, channel, server, msg_content) -> None:
        super().__init__(client)
        self.msg_content = msg_content
        self.author = author
        self.channel = channel
        self.server = server
        self.builder = CommandMessageBuilder(
            client.user.id, 
            self.msg_content, 
            self.author, 
            self.channel, 
            self.server
        )

    def send_help(self, is_in_error=False):
        answer_to_user = self.builder.build_help_message(is_in_error)
        self._send_discord(answer_to_user, self.channel, True)

    def send_add_waiting(self):
        answer_to_user = self.builder.build_add_waiting_message()
        self._send_discord(answer_to_user, self.channel, True)

    def send_add_success(self):
        answer_to_user = self.builder.build_add_success_message()
        self._send_discord(answer_to_user, self.channel, True)

    def send_add_error(self, **props):
        answer_to_user = self.builder.build_add_error_message(**props)
        self._send_discord(answer_to_user, self.channel, True)

    def send_delete_waiting(self):
        answer_to_user = self.builder.build_delete_waiting_message()
        self._send_discord(answer_to_user, self.channel, True)

    def send_delete_success(self):
        answer_to_user = self.builder.build_delete_success_message()
        self._send_discord(answer_to_user, self.channel, True)

    def send_delete_error(self, **props):
        answer_to_user = self.builder.build_delete_error_message(**props)
        self._send_discord(answer_to_user, self.channel, True)

    def set_data_submited(self, url_submited, channel_submited):
        self.builder.set_data_submited(url_submited, channel_submited)
