import pytz, requests, re, feedparser

from src.logger import Logger

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

    def is_youtube_url(url) -> bool:
        return 'youtu' in url

    def is_include_in_string(is_include_string, string):
        return str(is_include_string).upper() in string \
            or str(is_include_string).lower() in string

    def sanitize_check(feed, generator_exist):
        is_valid = False
        try:
            status = requests.get(feed['url'], timeout=5).status_code
            if generator_exist:
                is_valid = status == 200
            else:
                feed_data = feedparser.parse(feed['url']).entries
                is_valid = feed_data != []
        except:
            logger.error(f"An error occured. No answer from host {feed['url']}. "
                + f"Please verify if the submitted URL is valid"
            )
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
        is_url_format_valid = re.match(regexp, url) is not None
        try:
            status = requests.get(url, timeout=5).status_code
            is_valid = status == 200 and is_url_format_valid
        except:
            logger.error(f"The submited url: {url} does not answer")
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
            logger.error(f"The submited channel: {channel_submited} is not valid")
        return channel_name, is_valid