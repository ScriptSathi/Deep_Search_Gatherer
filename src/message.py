from src.logger import Logger

logger = Logger.get_logger()

class Message:
    def __init__(self, client, channels, feed_config) -> None:
        self.client = client
        self.channels = channels
        self.feed_config = feed_config

    def send_message(self, news):
        message = self._build_message(news)
        for chan in self.channels:
            self._send_stdout(news, chan)
            self._send_discord(message, chan)

    def _send_discord(self, message, channel):
        self.client.loop.create_task(channel.send(message))

    def _send_stdout(self, news, channel):
        logger.info(f'{self.feed_config["name"]} - Publishing on channel "{channel.name}" - "{news.title}"')

    def _build_message(self, news):
        message = ''

        title = f'**{news.title}**'
        published = news.published
        link = news.link
        summary = news.summary

        for field in (title, published, link, summary):
            message += field + '\n'

        return message
