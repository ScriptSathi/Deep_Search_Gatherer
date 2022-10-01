from random import randint
from typing import Literal

from .FeedUtils import FeedUtils

class ContextUtils:

    def create_uid(n: int) -> int:
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)        

    def get_type(link: str) -> Literal[0, 1, 2]:
        rss, reddit, twitter = 0, 1, 2
        if FeedUtils.is_twitter_link(link):
            return twitter
        elif FeedUtils.is_reddit_url(link) :
            return reddit
        else:
            return rss
