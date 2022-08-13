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
