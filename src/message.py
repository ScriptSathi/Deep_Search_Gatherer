from src.message_builders import NewsMessageBuilder, AnswerMessageBuilder
from src.logger import Logger

logger = Logger.get_logger()

class Message:

    def __init__(self, client, channels = [], feed_config = []) -> None:
        self.client = client
        self.channels = channels
        self.feed_config = feed_config

    def send_news(self, news):
        message = NewsMessageBuilder(news).build_message()
        for chan in self.channels:
            self._send_stdout(chan, news=news, is_a_news=True)
            self._send_discord(message, chan)
    
    def send_answer(self, msg_content, author, chan, server):
        answer_to_user = AnswerMessageBuilder(msg_content, author, chan, server).build_message()
        self._send_stdout(chan, msg_content=msg_content, author=author, server=server)
        self._send_discord(answer_to_user, chan)

    def _send_discord(self, message, channel):
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
