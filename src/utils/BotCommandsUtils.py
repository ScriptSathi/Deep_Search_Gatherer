from typing import Literal, Tuple, Union
from pydash import _

from .utils import Utils
from .ContextUtils import ContextUtils
from .FeedUtils import FeedUtils

class BotCommandsUtils:

    def get_command_name(full_message_str) -> Literal[0, 1, 2, 3, 100]:
        help_trigger, add_trigger, delete_trigger, list_trigger = (0,1,2,3)
        msg = full_message_str.split()
        if len(msg) == 1 or Utils.is_include_in_string('help', msg[1]) or Utils.is_include_in_string('-h', msg[1]):
            return help_trigger
        elif Utils.is_include_in_string('add', msg[1]):
            return add_trigger
        elif Utils.is_include_in_string('delete', msg[1]) or Utils.is_include_in_string('del', msg[1]):
            return delete_trigger
        elif Utils.is_include_in_string('list', msg[1]) or Utils.is_include_in_string('ls', msg[1]):
            return list_trigger
        else:
            return 100
    
    def check_link_and_return(link_submited: str, bearer_token: str) -> Tuple[Literal[0, 1, 2, 100], Union[str, None]]:
        rss, reddit, twitter = 0, 1, 2
        type = ContextUtils.get_type(link_submited)
        is_valid = False
        if reddit == type:
            link_submited = FeedUtils.find_reddit_feed_name(link_submited)
            is_valid = FeedUtils.is_subreddit_exist(link_submited)
        elif twitter == type:
            link_submited = _.replace_start(link_submited, "@", "")
            is_valid = FeedUtils.is_twitter_user_exist(link_submited, bearer_token)
        elif rss == type:
            is_valid = FeedUtils.is_a_valid_url(link_submited)
            if is_valid:
                if FeedUtils.is_youtube_url(link_submited) and not "feeds" in link_submited:
                    link_submited = FeedUtils.get_youtube_feed_url(link_submited)
        if is_valid:
            return type, link_submited
        else:
            return type, None