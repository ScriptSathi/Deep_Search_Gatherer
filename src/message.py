import re

from html2text import HTML2Text

from src.logger import Logger

logger = Logger.get_logger()

class Message:

    def parse_html(html_content): 
        htmlfixer = HTML2Text()
        htmlfixer.ignore_links = True
        htmlfixer.ignore_images = True
        htmlfixer.ignore_emphasis = False
        htmlfixer.body_width = 1000
        htmlfixer.unicode_snob = True
        htmlfixer.ul_item_mark = "-" 
        markdownfield = htmlfixer.handle(html_content)
        return re.sub("<[^<]+?>", "", markdownfield)

    def render_author(news):
        if 'authors' or 'author' in news:
            if (news['authors'][0]) == {}:
                (news['authors'][0]).name = "Unknow author"
            elif news['author'] == {}:
                news['author'].name = "Unknow author"
            if 'authors' in news:
                str_authors = 'Author: '
                if len(news['authors']) == 1:
                    str_authors += (news['authors'][0]).name
                else: 
                    for author in news['authors']:
                        str_authors += author.name + ', '
                return str_authors
            elif 'author' in news: 
                return news['author'].name
        return ''

    def is_youtube_feed(news):
        return 'yt_videoid' in news

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

        auth = Message.render_author(news)
        message = ''

        title = f'***{news.title}***'
        author = f'*{auth}*' if auth != '' else ''
        published = news.published if not Message.is_youtube_feed(news) else ''
        link = news.link
        summary = Message.parse_html(news.summary) if not Message.is_youtube_feed(news) else ''

        for field in (title, author, published, link, summary):
            if field != '' :
                message += field + '\n'                

        return message
