import os, json, yaml

from src.constants import Constants
from src.logger import Logger
from src.utils import Utils
from src.feed import Feed

logger = Logger.get_logger()

class Backup:

    def read():
        try:
            with open(Constants.backup_path, 'r') as yaml_file:
                backup = yaml.safe_load(yaml_file)['servers']
                logger.info('Backup loaded successfully')
                return backup
        except:
            return []

    def save(servers_context):
        if servers_context != []:
            servers_data_to_backup = servers_context[:]
            for server in servers_data_to_backup:
                for feed in server['feeds']:
                    logger.info(feed.get_feed_data())
                    feed = feed.get_feed_data()
            logger.info(servers_data_to_backup)
            yaml_text = yaml.dump({"servers": servers_data_to_backup})
            try:
                with open(Constants.backup_path, 'w') as yaml_file:
                    try:
                        yaml_file.write(yaml_text)
                    finally:
                        yaml_file.close()
            except Exception as e:
                logger.exception(str(e))
                os.mkdir(Constants.backup_dir_path)
                Backup.save(servers_context)