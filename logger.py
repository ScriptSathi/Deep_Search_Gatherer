import logging

class Logger:
    def __init__(self, log_level: bool) -> None:
        self.log_level = log_level

    def get_logger(self) -> logging:
        logging.basicConfig(format='%(asctime)s [%(funcName)s:%(lineno)s] - %(levelname)s: %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=self.log_level)
        logger = logging.getLogger(__name__)
        logger.setLevel(self.log_level)
        return logging