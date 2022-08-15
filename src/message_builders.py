import re

from html2text import HTML2Text

class AnswerMessageBuilder:
    def __init__(self, content, author, channel, server) -> None:
        self.author = author
        self.content = content
        self.channel = channel
        self.server = server

    def build_message(self):
        return str(self.content)

class NewsMessageBuilder:
    
    def __init__(self, single_news) -> None:
        self.single_news = single_news
    
    def build_message(self):

        auth = self._render_author()
        message = ''

        title = f'***{self.single_news.title}***'
        author = f'*{auth}*' if auth != '' else ''
        # published = single_news.published if not Message.is_youtube_feed(single_news) else ''
        link = self.single_news.link
        summary = self._parse_html() if not self._is_youtube_feed() else ''

        for field in (title, author, link, summary):
            if field != '' :
                message += field + '\n'                

        return message

    def _parse_html(self): 
        htmlfixer = HTML2Text()
        htmlfixer.ignore_links = True
        htmlfixer.ignore_images = True
        htmlfixer.ignore_emphasis = False
        htmlfixer.body_width = 1000
        htmlfixer.unicode_snob = True
        htmlfixer.ul_item_mark = "-" 
        markdownfield = htmlfixer.handle(self.single_news.summary)
        return re.sub("<[^<]+?>", "", markdownfield)

    def _render_author(self):
        if 'authors' or 'author' in self.single_news:
            if 'authors' in self.single_news:
                if self.single_news['authors'][0] == {}:
                    return "Unknow authors"
                else:
                    str_authors = 'Author: '
                    if len(self.single_news['authors']) == 1:
                        str_authors += (self.single_news['authors'][0]).name
                    else:
                        for author in self.single_news['authors']:
                            str_authors += author.name + ', '
                    return str_authors
            elif 'author' in self.single_news:
                return "Unknow author" if self.single_news['author'] == {} else self.single_news['author'].name
        return ''
    
    def _is_youtube_feed(self):
        return 'yt_videoid' in self.single_news