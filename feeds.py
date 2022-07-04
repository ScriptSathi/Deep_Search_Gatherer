import feedparser

from parser import Parser
from event import EventHandler
from logger import Logger
from RSSManager import RSSManager

logger = Logger(2).get_logger()

class Feeds:

    latest_feed_posted = []

    def __init__(self, handler: EventHandler) -> None:
        self.handler = handler

    def get_status_of_feed(self, all_posts, index_of_current_feed) -> int:

        index_exist = 0 <= index_of_current_feed < len(self.latest_feed_posted)
        no_need_to_post, post_until_latest, add_all_post_until_time = (0, 1, 2)

        if index_exist:
            current_feed_is_registered = all_posts[0].title == self.latest_feed_posted[index_of_current_feed]
            if current_feed_is_registered:
                return no_need_to_post
            else: 
                return post_until_latest
        else:
            return add_all_post_until_time
    
    def add_to_latest_post(self, new_post, index_of_current_feed) -> None:

        no_post_registered = len(self.latest_feed_posted) == 0
        current_feed_is_registered = 0 <= index_of_current_feed < len(self.latest_feed_posted)

        if no_post_registered or not current_feed_is_registered:
            self.latest_feed_posted.append(new_post.title)
        else:
            self.latest_feed_posted[index_of_current_feed] = new_post.title

    def update_feed_posts(self, latest_post_name, index_of_current_feed):
        self.latest_feed_posted[index_of_current_feed] = latest_post_name