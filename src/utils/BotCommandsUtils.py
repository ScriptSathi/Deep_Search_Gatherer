from typing import Literal, Tuple, Union
from pydash import _

from src.user_config import User_config_dict
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

    def check_link_and_return(link_submited: str, user_config: User_config_dict) -> Tuple[Literal[0, 1, 2, 100], Union[str, None]]:
        rss, reddit, twitter, twitch = 0, 1, 2, 3
        link_submited = link_submited.replace("`", "")
        type_of_feed = ContextUtils.get_type(link_submited)
        is_valid = False
        name = ''
        if reddit == type_of_feed:
            name = FeedUtils.find_reddit_feed_name(link_submited)
            is_valid = FeedUtils.is_subreddit_exist(link_submited)
        elif twitter == type_of_feed:
            if '@' in link_submited:
                name = _.replace_start(link_submited, "@", "")
            elif 'www' in link_submited: 
                name = _.replace_start(link_submited, "https://www.twitter.com/", "")
            else:
                name = _.replace_start(link_submited, "https://twitter.com/", "")
            is_valid = FeedUtils.is_twitter_user_exist(name, user_config["twitter"]["bearer_token"])
        elif twitch == type_of_feed:
            if 'tw/' in link_submited:
                name = _.replace_start(link_submited, "tw/", "")
            elif 'www' in link_submited: 
                name = _.replace_start(link_submited, "https://www.twitch.tv/", "")
            else:
                name = _.replace_start(link_submited, "https://twitch.tv/", "")
            is_valid = FeedUtils.is_twitch_channel_exist(
                name,
                user_config["twitch"]["client_id"],
                user_config["twitch"]["client_secret"]
            )
        elif rss == type_of_feed:
            is_valid = FeedUtils.is_a_valid_url(link_submited)
            if is_valid:
                if FeedUtils.is_youtube_url(link_submited) and not "feeds" in link_submited:
                    link_submited = FeedUtils.get_youtube_feed_url(link_submited)
        if is_valid:
            return type_of_feed, name
        else:
            return type_of_feed, None