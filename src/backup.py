import os, yaml

from src.constants import Constants
from src.logger import Logger

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
            full_backup = []
            for server in servers_context:
                backup_feeds = []
                for feed in server['feeds']:
                    backup_feeds.append(feed.get_feed_data())
                backup_server = {
                    "id": server['id'],
                    "feeds": backup_feeds,
                }
                full_backup.append(backup_server)
            yaml_text = yaml.dump({"servers": full_backup})
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