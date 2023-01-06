import logging

class Logger:
    def get_logger() -> logging:
        log_level = logging.INFO
        logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)s] - %(levelname)s: %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=log_level)
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        return logging