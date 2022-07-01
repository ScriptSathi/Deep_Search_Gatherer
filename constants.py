import os

class Constants: 
    home_dir = os.environ["HOME"] if "HOME" in os.environ else '/home/feedbot'
    # json_conf_path_dir = os.path.join('/config')
    json_conf_path_dir = os.path.join('.')
    default_config = {
            "token": "",
            "feeds": []
        }