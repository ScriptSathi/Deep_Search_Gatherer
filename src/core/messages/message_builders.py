from dataclasses import dataclass
from typing import List
from discord import User, Color, Embed
from datetime import datetime

from src.core.registered_data import RegisteredServer
from src.utils import FeedUtils
from src.constants import Constants

def build_embed(
    message, color = Color.orange(), title = Constants.bot_name, url = Constants.source_code_url,
    timestamp = datetime.utcnow()
    ) -> Embed:
    return Embed(
            title=title,
            url=url,
            description=message,
            color=color,
            timestamp=timestamp
        )

class CommandMessageBuilder:

    bot_id: int
    author: User
    link_submited: str = "Unknown"
    channel_submited: str = "Unknown"
    feed_name_submited: str = ""

    def __init__(self, bot_id: int, author: User) -> None:
        self.bot_id = bot_id
        self.author = author

    def set_data_submited(self, **options):
        self.link_submited = options.pop('link', '')
        self.channel_submited = options.pop('channel', '')
        self.feed_name_submited = options.pop('feed_name', '')

    def build_delete_waiting_message(self):
        description = CommandBuilderUtils.build_multiple_line_string([
            f"<@{self.author.id}> you asked for deleting `{self.feed_name_submited}`",
            f"I'm trying to delete the feed, please wait"
        ])
        return build_embed(description)

    def build_delete_success_message(self):
        description = f"The feed has been correctly deleted\n"
        return build_embed(description)\
            .set_footer(text="🪦 Rest in Peace little feed")

    def build_delete_error_message(self, **props):
        status = 1
        name_in_error = props.pop('url_in_error', False)
        if name_in_error: status = 0
        else: status = 1
        descriptions = [
            f"<@{self.author.id}> The submitted name `{self.feed_name_submited}` is invalid \n",
            f"<@{self.author.id}> There's no feed named: `{self.feed_name_submited}` registered\n"
        ]
        return build_embed(descriptions[status], Color.red())\
            .set_footer(text=f"🚨 Try again with a registered feed")

    def build_add_waiting_message(self):
        description = CommandBuilderUtils.build_multiple_line_string([
            f"<@{self.author.id}> you asked for adding `{self.link_submited}` in the channel `{self.channel_submited}`",
            f"I'm trying to add the feed, please wait",
        ])
        return build_embed(description)

    def build_add_success_message(self, feed_name):
        description = f"The feed as been correctly added with name `{feed_name}`\n" +\
            f"Next time there will be an article in the feed, it will be posted on the channel"
        return build_embed(description, Color.green())\
            .set_footer(text="📰 Now you just need to enjoy the news posted")

    def build_add_error_message(self, **props):
        status = 2
        url_in_error = props.pop('url_in_error', False)
        channel_in_error = props.pop('channel_in_error', False)
        if url_in_error: status = 0
        elif channel_in_error: status = 1
        else: status = 2
        descriptions = [
            f"<@{self.author.id}> an error occured with the link `{self.link_submited}` for the channel `{self.channel_submited}`\n",
            f"<@{self.author.id}> an error occured on the submited channel `{self.channel_submited}`\n",
            f"<@{self.author.id}> an error occured with the link `{self.link_submited}` and the channel `{self.channel_submited}`\n",
        ]
        footers = [
            "link",
            "channel id",
            "link and channel id"
        ]
        return build_embed(descriptions[status], Color.red())\
            .set_footer(text=f"🚨 Try again with a valid {footers[status]}")

    def build_help_message(self, is_in_error=False):
        desc_help = CommandBuilderUtils.build_multiple_line_string([
            f"Hey <@{self.author.id}> ! You don't know me yet ?",
            f"I've been created to help you getting in touch with any websites you want !",
            f"Every time there will be a new tweet/reddit/article/video, i'll post it over discord on the channel you wanted",
            f"To help you using my services i'll tell you how i work."
        ])
        desc_error = CommandBuilderUtils.build_multiple_line_string([
            f"Hey <@{self.author.id}>, i miss understood your command",
            f"I'll explain what i'm able to do"
        ])
        description = desc_error if is_in_error else desc_help

        capabilites = CommandBuilderUtils.build_multiple_line_string([
            f"- `Add` (cmd: add) a new feed to the list on a specific channel",
            f"- `Delete` (cmd: del/delete) a feed from the list on the current server",
            f"- `List` (cmd: ls/list) all the feeds registered in the server"
        ])

        features = CommandBuilderUtils.build_multiple_line_string([
            f"- `Twitter` account can be follow with **add @TwitterAcount**",
            f"- `Twitch` channels can be follow with **add tw/TwitchChannelName**",
            f"- `Youtube` channel can be followed using the channel url **add https://youtube.example/MyYoutubeChannel**",
            f"- `Reddit` with a subreddit using **add r/redditAccount**",
            f"- `RSS` feed simply by giving the url **add https://URL-OF-THE-FEED.com**",
            f"- `Static HTML pages` can be given as well to make it easily (may encounted weird behaviours)"
        ])

        examples = CommandBuilderUtils.build_multiple_line_string([
            f"> **<@{self.bot_id}> add <link_to_follow> channel <channel_id> (name <feed_name>)**",
            f"> **<@{self.bot_id}> delete <feed_name>**",
            f"> **<@{self.bot_id}> list**"
        ])

        troubleshoot = CommandBuilderUtils.build_multiple_line_string([
            'If you encounter weird behaviour with names due to the discord markdown parser, you can escape it using backticks "\`" around the name',
            f"> \`@My_Twitter_Account\`",
            f"> \`tw/My_Twitch_Channel\`",
        ])

        return build_embed(description)\
            .add_field(name="__Capabilites:__", value=capabilites, inline=False)\
            .add_field(name="__Features:__", value=features, inline=False)\
            .add_field(name="__Examples:__", value=examples, inline=False)\
            .add_field(name="__Troubleshoot:__", value=troubleshoot, inline=False)\
            .set_footer(text="Made with 🧡")

    def build_feeds_list_message(self, reg_server: RegisteredServer):
        description = \
            f"Here is the list of all the feeds registered on the server `{reg_server.name}`\n"
        feed_list = CommandBuilderUtils.get_feed_list_message(reg_server)
        return [build_embed(description + current_list) for current_list in feed_list]

    def build_feeds_list_empty_message(self, server_name):
        description = \
            f"There is no feeds registered in the server `{server_name}` yet\n"
        return build_embed(description)\
            .set_footer(text="Register first a feed, if you don't how to do, try the `help` command")

class CommandBuilderUtils:
    def get_feed_list_message(server_config: RegisteredServer) -> List[str]:
        rss, reddit, twitter, twitch = 0, 1, 2, 3
        feeds_list = ["**__RSS and Youtube:__**"]
        twitter_list = ["**__Twitter:__**"]
        reddit_list = ["**__Reddit:__**"]
        twitch_list = ["**__Twitch:__**"]
        for feed in server_config.feeds:
            feed_link = feed.link
            if feed.type == rss:
                if FeedUtils.is_youtube_url(feed.link):
                    feed_link = FeedUtils.get_youtube_channel_url(feed.link)
                feeds_list.append(f"- Name: `{feed.name}` with url: **{feed_link}**")
            elif feed.type == reddit:
                reddit_list.append(f"- Name: `{feed.name}` for account **r/{feed_link}**")
            elif feed.type == twitter:
                twitter_list.append(f"- Name: `{feed.name}` for the user **@{feed_link}**")
            elif feed.type == twitch:
                twitch_list.append(f"- Name: `{feed.name}` for the twitch channel **{feed_link}**")
        feeds_list_arr = [list for list in [feeds_list, twitter_list, reddit_list, twitch_list] if len(list) > 1]
        complete_feed_list = CommandBuilderUtils.build_multiple_line_string(*feeds_list_arr)
        list_is_too_long_for_discord = len(complete_feed_list) >= 4096
        return (
            [complete_feed_list],
            ["\n".join(list) for list in feeds_list_arr]
        )[list_is_too_long_for_discord]

    def build_multiple_line_string(*args) -> str:
        return "".join('\n'.join(array_of_messages) + '\n' for array_of_messages in args)

@dataclass(frozen=True)
class PostMessage:
    title: str
    content: str
    link: str
    author: str = 'Unknow Author'
    sec_link: str = ""
    activity_title: str = ""

class NewsMessageBuilder:

    single_news: PostMessage

    def __init__(self, single_news: PostMessage) -> None:
        self.single_news = single_news

    def build_message(self, type: int, embed: bool) -> str:
        rss, reddit, twitter, twitch = 0, 1, 2, 3
        if type == rss:
            return self._render_rss_message() if not embed else self._render_rss_embed_message()
        if type == reddit:
            return self._render_reddit_message()
        elif type == twitter:
            return self._render_twitter_message()
        elif type == twitch:
            return self._render_twitch_message()

    def _render_twitter_message(self) -> str:
        return f"**{self.single_news.author}** {self.single_news.content}"

    def _render_reddit_message(self) -> str:
        link = "" if self.single_news.link == "" else f"\n- The submitted link by the user -\n{self.single_news.link}"
        return (f"**{self.single_news.title}**" + link
            + "\n" + f"- View the reddit post -\n{self.single_news.sec_link}")

    def _render_rss_message(self) -> str:
        message = ''
        for field in (
            f'***{self.single_news.title}***',
            f'*{self.single_news.author}*' if self.single_news.author != '' else '',
            self.single_news.link, self.single_news.content):
            if field != '' :
                message += field + '\n'
        return message

    def _render_rss_embed_message(self) -> Embed:
        youtube_logo = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/YouTube_social_white_squircle.svg/2048px-YouTube_social_white_squircle.svg.png'
        return build_embed(f"{self.single_news.author} release a new video", Color.red(), self.single_news.title, 
            self.single_news.link, timestamp=datetime.fromisoformat(self.single_news.activity_title))\
            .set_author(name=self.single_news.author, icon_url= youtube_logo)\
            .set_image(url=self.single_news.sec_link)\
            .add_field(name="__Description:__", value=self.single_news.content, inline=False)\
            .set_footer(text='Youtube \u200b', icon_url=youtube_logo)


    def _render_twitch_message(self) -> Embed:
        twitch_logo = 'https://assets.stickpng.com/thumbs/580b57fcd9996e24bc43c540.png'
        return build_embed(f"On {self.single_news.activity_title}", Color.purple(), f"**{self.single_news.title}**", self.single_news.link)\
            .set_author(name=self.single_news.author, icon_url=twitch_logo)\
            .set_image(url=self.single_news.sec_link)\
            .add_field(name="__Description:__", value=self.single_news.content, inline=False)\
            .set_footer(text='Twitch \u200b', icon_url=twitch_logo)
