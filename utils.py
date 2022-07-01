from logger import Logger
from pprint import pprint

logger = Logger(2).get_logger()

class Utils:

    def add_to_latest_post(self, new_post, index) -> None:           

        no_post_registered = len(self.latest_feed_posted) == 0
        current_feed_is_registered = 0 <= index < len(self.latest_feed_posted)

        if no_post_registered or not current_feed_is_registered:
            self.latest_feed_posted.append(new_post.title)
        else:
            self.latest_feed_posted[index] = new_post.title
