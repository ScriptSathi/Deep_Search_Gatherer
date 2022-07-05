import discord, asyncio
from logger import Logger

logger = Logger(2).get_logger()

class Message:
    def add_events(handler, client, channels):
        message = Message(client, channels)
        handler.add_event('send_stdout', Message.send_stdout)
        handler.add_event('send_discord', message._send_discord)

    def send_stdout(current_post):
        logger.info(f'New article published on discord: {current_post.title}')

    def __init__(self, client, channels) -> None:
        self.client = client
        self.channels = channels

    def _send_discord(self, news):
        logger.info('Notification received for sending a new message')
        for chan in self.channels:
            message = self._build_message(news)
            self.client.loop.create_task(chan.send(message))

    def _build_message(self, news):
        message = ''
        wanted_fields = ['title', 'author', 'published', 'link', 'summary']

        title = f'**{news.title}**'
        published = news.published
        link = news.link
        summary = news.summary

        for field in (title, published, link, summary):
            message += field + '\n'

        return message
