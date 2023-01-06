from random import randint
from typing import Literal

from .FeedUtils import FeedUtils

class ContextUtils:

    def create_uid(n: int) -> int:
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)        

    def get_type(link: str) -> Literal[0, 1, 2, 3]:
        rss, reddit, twitter, twitch = 0, 1, 2, 3
        if FeedUtils.is_twitter_link(link):
            return twitter
        elif FeedUtils.is_reddit_url(link) :
            return reddit
        elif FeedUtils.is_twitch_link(link) :
            return twitch
        else:
            return rss
