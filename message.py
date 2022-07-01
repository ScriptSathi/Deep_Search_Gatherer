from logger import Logger

logger = Logger(2).get_logger()

class Message:
    def add_events(handler):
        handler.add_event('send_message', Message.send_message)

    def send_message(current_post):
        logger.info(f'Sending message to discord')
        logger.info(f'Title: {current_post.title}')
        # logger.info(f'Published: {current_post.published}')
        # logger.info(f'Description: {current_post.summary}')
