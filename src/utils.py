import tweepy

from pydash import _
from typing import Literal, Tuple, Union
import requests, re, feedparser, random
from asyncio import sleep
from src.logger import Logger

from src.constants import Constants

logger = Logger.get_logger()

class Utils:

    def is_include_in_string(include_to_test, string) -> bool:
        if isinstance(include_to_test, str) or isinstance(include_to_test, int):
            return str(include_to_test).upper() in string \
                or str(include_to_test).lower() in string
        else:
            is_include = False
            for to_test_str in include_to_test:
                if str(to_test_str).upper() in string \
                    or str(to_test_str).lower() in string:
                    is_include = True
            return is_include

    def sanitize_check(url, generator_exist) -> bool:
        def try_to_reach():
            is_valid = False
            try:
                feed_data = feedparser.parse(url).entries
                if feed_data == [] and generator_exist:
                    api_gen_url = Constants.api_url + "/create?url=" + url
                    status = Utils.get_request(api_gen_url).status_code
                    is_valid = status == 200
                elif feed_data != []:
                    is_valid = True
            except:
                logger.error(f"An error occured. No answer from host {url}. "
                    + f"Please verify if the submitted URL is valid"
                )
            return is_valid
        is_valid = try_to_reach()
        if not is_valid: # try to reach a second time
            is_valid = try_to_reach()
        return is_valid

    def generate_random_string() -> str:
        random_string = ""
        for _ in range(5):
            random_integer = random.randint(97, 97 + 26 - 1)
            flip_bit = random.randint(0, 1)
            random_integer = random_integer - 32 if flip_bit == 1 else random_integer
            random_string += (chr(random_integer))
        return random_string

    def everyone_tag_is_not_used(message) -> bool:
        return not Utils.is_include_in_string('everyone', message)

    def get_request(url, **options) -> requests.Response:
        extra_cookies = options.pop('cookies', {})
        extra_headers = options.pop('headers', {})
        timeout = options.pop('timeout', 5)
        headers = {
            "User-Agent": f"Mozilla/5.0 - This is a bot from this project {Constants.source_code_url}."
                + "Please do not ban me. It has been build to help following content using RSS feeds."
                + f"The purpose is only to gather informations every {Constants.base_config_default['refresh_time']} seconds",
            "Retry-After": "5",
            }
        for key, value in extra_headers.items():
            headers[key] = value
        return requests.get(url, timeout=timeout, headers=headers, cookies=extra_cookies)

    async def try_again_if_fail(resolve, max_retry=3, **args) -> None:
        for attempt in range(max_retry):
            try:
                resolve(*args["resolve_args"]) if "resolve_args" in args else resolve()
                break
            except Exception:
                if "reject" in args:
                    args["reject"](Exception, *args["resolve_args"]) if "reject_args" not in args else args["reject"]()
                if attempt < max_retry:
                    retry_delay = 2
                    logger.error(f"Fail, retry in {retry_delay} seconds")
                    await sleep(retry_delay)
                resolve(*args["resolve_args"]) if "resolve_args" in args else resolve()

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
        return link.startswith("https://www.youtube.com") and "feeds" not in link

    def is_reddit_url(link: str) -> bool:
        return link.startswith("/r/") or link.startswith("/u/")

    def is_twitter_link(link: str) -> bool:
        return link.startswith("@")

    def is_twitter_user_exist(user: str, bearer_token: str) -> bool:
        try:
            return tweepy.Client(bearer_token=bearer_token).get_user(username=user).data.username == user
        except Exception:
            return False

    def find_rss_feed_name(url: str) -> str:
        data = feedparser.parse(url)
        name = data.feed['title'] if "title" in data.feed else f"feed-{Utils.generate_random_string()}"
        return name.replace(" ", "-")

    def find_twitter_feed_name(user: str, bearer_token: str) -> str:
        name = tweepy.Client(bearer_token=bearer_token).get_user(username=user).data.name
        return name.replace(" ", "-")

class ContextUtils:

    def create_uid(n: int) -> int:
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start, range_end)        

    def get_type(link: str) -> Literal[0, 1, 2]:
        rss, reddit, twitter = 0, 1, 2
        if FeedUtils.is_twitter_link(link):
            return twitter
        elif FeedUtils.is_reddit_url(link) :
            return reddit
        else:
            return rss

class BotCommandsUtils:

    def get_command_name(full_message_str) -> Literal[0, 1, 2, 3, 100]:
        help_trigger, add_trigger, delete_trigger, list_trigger = (0,1,2,3)
        msg = full_message_str.split()
        if len(msg) == 1 or Utils.is_include_in_string('help', msg[1]) or Utils.is_include_in_string('-h', msg[1]):
            return help_trigger
        elif Utils.is_include_in_string('add', msg[1]):
            return add_trigger
        elif Utils.is_include_in_string('delete', msg[1]) or Utils.is_include_in_string('del', msg[1]):
            return delete_trigger
        elif Utils.is_include_in_string('list', msg[1]) or Utils.is_include_in_string('ls', msg[1]):
            return list_trigger
        else:
            return 100
    
    def check_link_and_return(link_submited: str, bearer_token: str) -> Tuple[Literal[0, 1, 2, 100], Union[str, None]]:
        rss, reddit, twitter = 0, 1, 2
        type = ContextUtils.get_type(link_submited)
        is_valid = False
        if reddit == type:
            logger.info("Reddit asked, skip")
        elif twitter == type:
            link_submited = _.replace_start(link_submited, "@", "")
            is_valid = FeedUtils.is_twitter_user_exist(link_submited, bearer_token)
        elif rss == type:
            is_valid = FeedUtils.is_a_valid_url(link_submited)
            if is_valid:
                if FeedUtils.is_youtube_url(link_submited):
                    link_submited = FeedUtils.get_youtube_feed_url(link_submited)
        if is_valid:
            return type, link_submited
        else:
            return type, None