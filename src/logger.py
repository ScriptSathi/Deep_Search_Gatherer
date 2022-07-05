import logging

class Logger:
    def get_logger(self) -> logging:
        logging.basicConfig(format='%(asctime)s [%(funcName)s:%(lineno)s] - %(levelname)s: %(message)s', datefmt='%d-%m-%y %H:%M:%S', level=self.log_level)
        logger = logging.getLogger(__name__)
        logger.setLevel(self.log_level)
        return logging