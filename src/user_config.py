import os, json, yaml
from typing import Any, TypedDict

from src.constants import Constants
from src.logger import Logger

logger = Logger.get_logger()

User_config_dict = TypedDict(
        'UserConfig',
        {
            "token": str,
            "published_since_default": int,
            "refresh_time": int,
            'game_displayed': str,
            'twitter': TypedDict('twitter',{
                "enabled": bool,
                "bearer_token": str,
            })
        }
    )

class UserConfig:
    def load_user_config() -> User_config_dict:
        config_path = os.path.join(Constants.base_conf_path_dir, UserConfig.file_name())
        base_config = UserConfig.read_config_file(config_path)
        config = Constants.base_config_default
        if base_config != []:
            for key, value in base_config.items():
                config[key] = value
        return config

    def read_config_file(file_path) -> bool:
        config = []
        try:
            if os.path.isfile(file_path):
                config_file_content = open(file_path,'r').read()
                try:
                    config = json.loads(config_file_content)
                except:
                    config = yaml.safe_load(config_file_content)
                return config
        except Exception:
            logger.info(f'You must submit a valid file in path: {Constants.base_conf_path_dir} file dir')
            return config

    def file_name() -> str:
        file_list = os.listdir(Constants.base_conf_path_dir)
        for file in file_list:
            if ".json" in file or ".yaml" in file or ".yml" in file and file != Constants.backup_path:
                return file