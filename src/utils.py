from src.logger import Logger
import pytz

logger = Logger.get_logger()

class Utils:
    def get_timezone():
        tz = 'Europe/Paris'
        try:
            timezone = pytz.timezone(tz)
        except Exception:
            timezone = pytz.utc

        return timezone