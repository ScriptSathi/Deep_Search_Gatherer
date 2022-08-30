import re
from discord import TextChannel, User, Color, Embed
from src.registered_data import RegisteredServer
from src.utils import Utils

from html2text import HTML2Text

from src.constants import Constants

class CommandMessageBuilder:

    bot_id: int
    author: User
    url_submited: str = "Unknown"
    channel_submited: str = "Unknown"
    feed_name_submited: str = ""

    def __init__(self, bot_id: int, author: User) -> None:
        self.bot_id = bot_id
        self.author = author

    def set_data_submited(self, **options):
        self.url_submited = options.pop('url', '')
        self.channel_submited = options.pop('channel', '')
        self.feed_name_submited = options.pop('feed_name', '')

    def build_delete_waiting_message(self):
        description = CommandBuilderUtils.build_multiple_line_string([
            f"<@{self.author.id}> you asked for deleting `{self.feed_name_submited}`",
            f"I'm trying to delete the feed, please wait"
        ])
        return Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=Color.orange()
            )

    def build_delete_success_message(self):
        description = f"The feed has been correctly deleted\n"
        return Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=Color.green()
            )\
            .set_footer(text="Rest in Peace little feed 🪦")

    def build_delete_error_message(self, **props):
        status = 1
        name_in_error = props.pop('url_in_error', False)
        if name_in_error: status = 0
        else: status = 1
        descriptions = [
            f"<@{self.author.id}> The submitted name `{self.feed_name_submited}` is invalid \n",
            f"<@{self.author.id}> There's no feed named: `{self.feed_name_submited}` registered\n"
        ]
        return Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=descriptions[status],
                color=Color.red()
            )\
            .set_footer(text=f"Try again with a registered feed 🚨")

    def build_add_waiting_message(self):
        description = CommandBuilderUtils.build_multiple_line_string([
            f"<@{self.author.id}> you asked for adding `{self.url_submited}` in the channel `{self.channel_submited}`",
            f"I'm trying to add the feed, please wait",
        ])
        return Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=Color.orange()
            )

    def build_add_success_message(self, feed_name):
        description = f"The feed as been correctly added with name `{feed_name}`\n" +\
            f"Next time there will be an article in the feed, it will be posted on the channel"
        return Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=Color.green()
            )\
            .set_footer(text="Now you just need to enjoy the news posted 📰")

    def build_add_error_message(self, **props):
        status = 2
        url_in_error = props.pop('url_in_error', False)
        channel_in_error = props.pop('channel_in_error', False)
        if url_in_error: status = 0
        elif channel_in_error: status = 1
        else: status = 2
        descriptions = [
            f"<@{self.author.id}> an error occured with the url `{self.url_submited}` for the channel `{self.channel_submited}`\n",
            f"<@{self.author.id}> an error occured on the submited channel `{self.channel_submited}`\n",
            f"<@{self.author.id}> an error occured with the url `{self.url_submited}` and the channel `{self.channel_submited}`\n",
        ]
        footers = [
            "url",
            "channel id",
            "url and channel id"
        ]
        return Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=descriptions[status],
                color=Color.red()
            )\
            .set_footer(text=f"Try again with a valid {footers[status]} 🚨")

    def build_help_message(self, is_in_error=False):
        desc_help = CommandBuilderUtils.build_multiple_line_string([
            f"Hey <@{self.author.id}> ! You don't know me yet ?",
            f"I've been created to help you getting in touch with any websites you want !",
            f"Every time there will be a new article/video, i'll post it over discord on the channel you wanted",
            f"To help you using my services i'll tell you how i work."
        ])
        desc_error = CommandBuilderUtils.build_multiple_line_string([
            f"Hey <@{self.author.id}>, i miss understood your command",
            f"I'll explain what i'm able to do"
        ])
        description = desc_error if is_in_error else desc_help

        capabilites = CommandBuilderUtils.build_multiple_line_string([
            f"- `Add` a new feed to the list on a specific channel",
            f"- `Delete` a feed from the list on the current server",
            f"- `List` all the feeds registered in the server"
        ])

        examples = CommandBuilderUtils.build_multiple_line_string([
            f"> **<@{self.bot_id}> add <url_to_follow> channel <channel_id> (name <feed_name>)**",
            f"> **<@{self.bot_id}> delete <feed_name>**",
            f"> **<@{self.bot_id}> list**"
        ])

        return Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=Color.orange()
            )\
            .add_field(name="__Capabilites:__", value=capabilites, inline=False)\
            .add_field(name="__Examples:__", value=examples, inline=False)\
            .set_footer(text="Made with 🧡")

    def build_feeds_list_message(self, reg_server: RegisteredServer):
        description = \
            f"Here is the list of all the feeds registered on the server `{reg_server.name}`\n"
        feed_list = CommandBuilderUtils.get_feed_list_message(reg_server)
        return Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description + "\n" + feed_list,
                color=Color.orange()
                )

    def build_feeds_list_empty_message(self, server_name):
        description = \
            f"There is no feeds registered in the server `{server_name}` yet\n"
        return Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=Color.orange()
            )\
            .set_footer(text="Register first a feed, if you don't how to do, try the `help` command")

class CommandBuilderUtils:
    def get_feed_list_message(server_config: RegisteredServer):
        feeds_list = ["**__Feeds:__**"]
        for feed in server_config.feeds:
            feed_url = feed.url
            if Utils.is_youtube_url(feed.url):
                feed_url = Utils.get_youtube_channel_url(feed.url)
            feeds_list.append(f"**- Name: `{feed.name}` with url: {feed_url}**")
        return CommandBuilderUtils.build_multiple_line_string(feeds_list)

    def build_multiple_line_string(array_of_messages):
        output_msg = ""
        for i, msg in enumerate(array_of_messages):
            output_msg += msg
            if i <  len(array_of_messages) - 1:
                output_msg += "\n"
        return output_msg

class NewsMessageBuilder:
    
    def __init__(self, single_news) -> None:
        self.single_news = single_news
    
    def build_message(self):
        auth = self._render_author()
        message = ''
        title = f'***{self.single_news.title}***'
        author = f'*{auth}*' if auth != '' else ''
        link = self.single_news.link
        summary = self._parse_html() if not self._is_youtube_feed() and not Utils.is_reddit_url(link) else ''
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