import re, discord

from html2text import HTML2Text

from src.constants import Constants

class AnswerMessageBuilder:
    def __init__(self, bot_id, content, author, channel, server) -> None:
        self.bot_id = bot_id
        self.author = author
        self.content = content
        self.channel = channel
        self.server = server

    def build_message(self):
        return str(self.content)

    def build_help_message(self):
        description = \
            f"Hey <@{self.author.id}> ! You don't know me yet ?\n" +\
            f"I've been created to help you getting in touch with any websites you want !\n" +\
            f"Every time there will be a new article/video, i'll post it over discord on the channel you wanted\n" +\
            f"To help you using my services i'll tell you how i work."

        capabilites = \
            f"- `Add` a new feed to the list on a specific channel\n" +\
            f"- `Delete` a feed from the list on the current server"

        examples = \
            f"> **<@{self.bot_id}> add=<url_to_follow> submit_on=<channel_id>**\n" +\
            f"> **<@{self.bot_id}> delete=<url_to_delete>**"

        return discord.Embed(
            title=Constants.bot_name,
                url="https://github.com/ScriptSathi/discord_information_gatherer",
                description=description,
                color=discord.Color.orange()
            )\
            .add_field(name="__Capabilites:__", value=capabilites, inline=False)\
            .add_field(name="__Examples:__", value=examples, inline=False)\
            .set_footer(text="Made with 🧡")

    def _help_array(self):
        return [
            
            f"Few options are available. `Adding` a followed feed, or `deleting` a followed feed",
            f"For adding a feed, the key word is `add` and to delete is `delete`. But to make it work you need to tag me in the message.",
            f"Here is an example:",
            f"```",
            f"{self.bot_id} add=<url_to_follow> submit_on=<channel_id>"
            f"```",
        ]

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