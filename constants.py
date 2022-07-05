import os, discord

class Constants: 
    home_dir = os.environ["HOME"] if "HOME" in os.environ else '/home/rssbot'
    json_conf_path_dir = os.path.join('.')
    default_config = {
            "token": "",
            "feeds": [],
            "published_since_default": 86000,
            "refresh_time": 300,
        }