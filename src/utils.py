import pytz, requests, re, feedparser, random

from src.logger import Logger
from src.constants import Constants

logger = Logger.get_logger()

class Utils:
    def get_timezone():
        tz = 'Europe/Paris'
        try:
            timezone = pytz.timezone(tz)
        except Exception:
            timezone = pytz.utc

        return timezone

    def get_youtube_feed_url(url):
        consent_cookie = {"CONSENT": "YES+"}
        html_content = requests.get(url, cookies=consent_cookie).text
        line_str = re.findall(r"channel_id=([A-Za-z0-9\-\_]+)", html_content)
        return f'https://www.youtube.com/feeds/videos.xml?channel_id={line_str[0]}'
    
    def get_youtube_channel_url(feed_url):
        return feedparser.parse(feed_url).feed['link']

    def is_youtube_url(url) -> bool:
        return 'youtu' in url

    def is_include_in_string(include_to_test, string):
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

    def _message_is_empty(message_txt):
        msg = message_txt.split()
        if len(msg) == 1:
            return True
        return False

    def sanitize_check(url, generator_exist):
        def try_to_reach():
            is_valid = False
            try:
                feed_data = feedparser.parse(url).entries
                if feed_data == [] and generator_exist:
                    api_gen_url = Constants.api_url + "/create?url=" + url
                    status = requests.get(api_gen_url, timeout=5).status_code
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

    def is_a_valid_url(url):
        is_valid = False
        regexp = re.compile(
            r'^(?:http)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        try:
            is_url_format_valid = re.match(regexp, url) is not None
            if is_url_format_valid:
                status = requests.get(url, timeout=5).status_code
                is_valid = status == 200 and is_url_format_valid
        except:
            logger.warning(f"The submited url: {url} does not answer")
        return is_valid

    async def is_a_valid_channel(client, channel_submited, server_id):
        is_valid = False
        channel_name = channel_submited
        try:
            channel_obj = await client.fetch_channel(channel_submited)
            if channel_obj.guild.id == server_id:
                is_valid = True
                channel_name = channel_obj.name
        except:
            logger.warning(f"The submited channel: {channel_submited} is not valid")
        return channel_name, is_valid
    
    def generate_random_string():
        random_string = ""
        for _ in range(5):
            random_integer = random.randint(97, 97 + 26 - 1)
            flip_bit = random.randint(0, 1)
            random_integer = random_integer - 32 if flip_bit == 1 else random_integer
            random_string += (chr(random_integer))
        return random_string