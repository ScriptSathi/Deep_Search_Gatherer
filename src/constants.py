import os

class Constants:
    bot_name = "Information Gatherer"
    base_conf_path_dir = os.path.join('/config')
    home_dir = os.environ['HOME'] if os.environ['HOME'] else '/home/rssbot'
    feeds_data_dir = os.path.join(home_dir, 'feeds_data')
    default_config = {
        "token": "",
        "feeds": [],
        "published_since_default": 86000,
        "refresh_time": 900,
        'game_displayed': "Eating some RSS feeds",
    }
    api_url = "http://scrape2rss:9292"