import os

class Constants: 
    json_conf_path_dir = os.path.join('/config')
    default_config = {
            "token": "",
            "feeds": [],
            "published_since_default": 86000,
            "refresh_time": 300,
            'game_displayed': "Eating some RSS feeds",
        }