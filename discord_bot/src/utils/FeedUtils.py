import tweepy

from pydash import _
import re, feedparser
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first


from src.logger import Logger
from .utils import Utils

logger = Logger.get_logger()

class FeedUtils:
    def is_a_valid_url(url: str) -> bool:
        is_valid = False
        regexp = re.compile(
            r'^(?:http)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/.?]\S+)$', re.IGNORECASE
        )
        try:
            is_url_format_valid = re.match(regexp, url) is not None
            if is_url_format_valid:
                status = Utils.get_request(url).status_code
                is_valid = status == 200 and is_url_format_valid
        except:
            logger.exception(Exception)
            logger.warning(f"The submited url: {url} does not answer")
        return is_valid

    def get_youtube_feed_url(url: str) -> str:
        consent_cookie = {"CONSENT": "YES+"}
        html_content = Utils.get_request(url, cookies=consent_cookie).text
        line_str = re.findall(r"channel_id=([A-Za-z0-9\-\_]+)", html_content)
        return f'https://www.youtube.com/feeds/videos.xml?channel_id={line_str[0]}'

    def get_youtube_channel_url(feed_url: str) -> str:
        return feedparser.parse(feed_url).feed['link']

    def is_youtube_url(link: str) -> bool:
        return link.startswith("https://www.youtube.com")

    def is_reddit_url(link: str) -> bool:
        return link.startswith("/r/") or link.startswith("r/")

    def is_twitter_link(link: str) -> bool:
        return link.startswith("@") or link.startswith("https://www.twitter.com") or link.startswith("https://twitter.com")

    def is_twitch_link(link: str) -> bool:
        return link.startswith("tw/") or link.startswith("https://twitch.tv") or link.startswith("https://www.twitch.tv")

    def is_twitter_user_exist(user: str, bearer_token: str) -> bool:
        try:
            return tweepy.Client(bearer_token=bearer_token).get_user(username=user).data.username == user
        except Exception:
            return False

    async def is_twitch_channel_exist(user: str, client_id: str, client_secret: str) -> bool:
        try:
            return (await first((await Twitch(client_id, client_secret)).get_users(logins=user))).login == user
        except:
            return False

    def is_subreddit_exist(subreddit_name: str, ) -> bool:
        try:
            return Utils.get_request(f'https://www.reddit.com/r/{subreddit_name}').status_code == 200
        except Exception:
            return False

    def find_rss_feed_name(url: str) -> str:
        data = feedparser.parse(url)
        name = data.feed['title'] if "title" in data.feed else f"feed-{Utils.generate_random_string()}"
        return name.replace(" ", "-")

    def find_twitter_feed_name(user: str, client: tweepy.Client) -> str:
        name = client.get_user(username=user).data.name
        return name.replace(" ", "-")

    def find_reddit_feed_name(subreddit_name: str) -> str:
        subreddit_name = _.replace_start(subreddit_name, "/", "")
        subreddit_name = _.replace_start(subreddit_name, "r/", "")
        return subreddit_name

    def find_twitch_feed_name(subreddit_name: str) -> str:
        subreddit_name = _.replace_start(subreddit_name, "tw/", "")
        return subreddit_name
