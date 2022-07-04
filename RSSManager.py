import feedparser
from logger import Logger

logger = Logger(2).get_logger()

class RSSManager:
    def __init__(self, feed_url: str, index_of_current_feed: int, latest_post_feed: str, handler) -> None:
        self.all_posts = self.poll_feed(feed_url)
        self.handler = handler
        self.index_of_current_feed = index_of_current_feed
        self.latest_post_feed = latest_post_feed

    def poll_feed(self, feed_url):
        return feedparser.parse(feed_url).entries

    def update_and_return_latest_rss(self, case):
        self._send_message_if_needed(case)
        return 

    def _send_message_if_needed(self, case):
        no_need_to_post, post_until_latest, add_all_post_until_time = (0, 1, 2)

        if no_need_to_post == case:
            self._nothing_to_post('There is no new post on this feed')
        elif post_until_latest == case:
            self._post_until_latest()
        elif add_all_post_until_time == case:
            self._append_new_feed()
    
    def _nothing_to_post(self, message):
        logger.info(message)
    
    def _post_until_latest(self):
        logger.info(f'POST UNTIL')
        logger.info(self.index_of_current_feed)
        
        news_to_post = self._get_unsended_news()
        
        for news in news_to_post:
            # logger.info('Posted !!')
            logger.info(f'News: {news.title} posted !')
            # self.handler.do('send_message', post)


    def _append_new_feed(self):
        logger.info(f'APPEND')
        logger.info(self.index_of_current_feed)
        # self.add_to_latest_post()
        # for post in all_posts:
        #     self.handler.on('send_message', post)
    
    def _get_unsended_news(self):
        news_to_post = []

        for new in self.all_posts:
            if new.title != self.latest_post_feed:
                news_to_post.append(new)
            elif new.title == self.latest_post_feed:
                break
        return news_to_post