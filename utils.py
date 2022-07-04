from logger import Logger
import pytz

logger = Logger(2).get_logger()

class Utils:
    def get_timezone():
        tz = 'utc+2'
        try:
            timezone = pytz.timezone(tz)
        except Exception:
            timezone = pytz.utc

        return timezone