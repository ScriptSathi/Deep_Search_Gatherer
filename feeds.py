from parser import Parser
from logger import Logger
from message import Message

logger = Logger(2).get_logger()

class Feeds:

    list = Parser().get_feeds()
    latest_feed_posted = []

    def __init__(self, handler) -> None:
        self.handler = handler   

    def get_status_of_feed(self, all_posts, index) -> int:

        index_exist = 0 <= index < len(self.latest_feed_posted)
        no_need_to_post, post_until_latest, add_all_post_until_time = (0, 1, 2)

        if index_exist:
            current_feed_is_registered = all_posts[0].title == self.latest_feed_posted[index]
            if current_feed_is_registered:
                return no_need_to_post
            else: 
                return post_until_latest
        else:
            return add_all_post_until_time
    
    def add_to_latest_post(self, new_post, index) -> None:           

        no_post_registered = len(self.latest_feed_posted) == 0
        current_feed_is_registered = 0 <= index < len(self.latest_feed_posted)

        if no_post_registered or not current_feed_is_registered:
            self.latest_feed_posted.append(new_post.title)
        else:
            self.latest_feed_posted[index] = new_post.title

    def add_events(self):
        self.handler.add_event('nothing_to_post', self._nothing_to_post)
        self.handler.add_event('post_until_latest', self._post_until_latest)
        self.handler.add_event('append_new_feed', self._append_new_feed)
        Message.add_events(self.handler)

    def _nothing_to_post(self, message):
        logger.info(message)
    
    def _post_until_latest(self, all_posts, index):
        logger.info(f'POST UNTIL')
        logger.info(index)
        for post in all_posts:
            self.handler.on('send_message', post)
        # logger.info(f'Here is all the logic for trigger an action when this event is triggered')

    def _append_new_feed(self, all_posts, index):
        logger.info(f'APPEND')
        logger.info(index)
        self.add_to_latest_post()
        # for post in all_posts:
        #     self.handler.on('send_message', post)
    
