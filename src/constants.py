import os

class Constants:
    bot_name = "Information Gatherer"
    source_code_url = "https://github.com/ScriptSathi/discord_information_gatherer"
    home_dir = os.environ['HOME'] if os.environ['HOME'] else '/home/rssbot'
    base_conf_path_dir = os.path.join('/config')
    backup_dir_path = os.path.join(home_dir, 'backups')
    backup_path = os.path.join(backup_dir_path, 'backup.yaml')
    feeds_data_dir = os.path.join(home_dir, 'feeds_data')
    base_config_default = {
        "token": "",
        "servers": [],
        "published_since_default": 0,
        "refresh_time": 900,
        'game_displayed': "Eating some RSS feeds",
    }
    api_url = "http://scrape2rss:9292"