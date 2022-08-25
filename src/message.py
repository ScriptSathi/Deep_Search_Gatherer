import discord
from src.message_builders import NewsMessageBuilder, CommandMessageBuilder
from src.logger import Logger

logger = Logger.get_logger()

class Message:
    def __init__(self, client, channel_obj, feed_name) -> None:
        self.client = client
        self.feed_name = feed_name
        self.channel_obj = channel_obj
        self.server_name = channel_obj.guild.name
        self.server_id = channel_obj.guild.id

    def _send_discord(self, message, embed = False):
        if embed:
            self.client.loop.create_task(self.channel_obj.send(embed=message))
        else:
            self.client.loop.create_task(self.channel_obj.send(message))

    def _send_stdout(self, **options):
        is_a_news = options.pop('is_a_news', False)
        no_news = options.pop('no_news', False)
        add = options.pop('add', {})
        delete = options.pop('delete', {})
        news = options.pop('news', '')
        msg_content = options.pop('msg_content', '')
        server = options.pop('server', '')
        author = options.pop('author', '')
        
        base_message = f"On {self.server_name}({self.server_id})"

        if is_a_news:
            logger.info(f'{base_message} - {self.feed_name} - Publishing on channel "{self.channel_obj.name}" - "{news.title}"')
        elif no_news:
            logger.info(f"{base_message} - {self.feed_name} - No news to share")
        elif add != {}:
            logger.info(f"{base_message} - Successfully adding {add['name']} with url {add['url']}")
        elif delete != {}:
            logger.info(f"{base_message} - Successfully deleting {delete['name']}")
        else:
            logger.info(f'{base_message} - Author: {author} from server {server} on channel {self.channel_obj.name} - "{msg_content}"')

class NewsMessage(Message):
    def __init__(self, client, channel_obj: discord.TextChannel, feed_name) -> None:
        super().__init__(client, channel_obj, feed_name)

    def send_news(self, news):
        message = NewsMessageBuilder(news).build_message()
        self._send_stdout(news=news, author=self.feed_name, is_a_news=True)
        self._send_discord(message)
    
    def send_no_news(self):
        self._send_stdout(no_news=True)

class CommandMessage(Message):
    def __init__(self, client, author, channel_obj: discord.TextChannel, msg_content, server_name) -> None:
        super().__init__(client, channel_obj, "")
        self.msg_content = msg_content
        self.author = author
        self.server_name = server_name
        self.builder = CommandMessageBuilder(
            client.user.id, 
            self.msg_content, 
            self.author, 
            self.channel_obj, 
            self.server_name
        )

    def send_help(self, is_in_error=False):
        answer_to_user = self.builder.build_help_message(is_in_error)
        self._send_discord(answer_to_user, True)

    def send_feeds_list(self, server_name, server_config):
        answer_to_user = self.builder.build_feeds_list_message(server_name, server_config)
        self._send_discord(answer_to_user, True)

    def send_feeds_list_empty(self, server_name):
        answer_to_user = self.builder.build_feeds_list_empty_message(server_name)
        self._send_discord(answer_to_user, True)

    def send_add_waiting(self):
        answer_to_user = self.builder.build_add_waiting_message()
        self._send_discord(answer_to_user, True)

    def send_add_success(self, feed_name, url):
        answer_to_user = self.builder.build_add_success_message(feed_name)
        self._send_discord(answer_to_user, True)
        self._send_stdout(add={"name":feed_name,"url":url})

    def send_add_error(self, **props):
        answer_to_user = self.builder.build_add_error_message(**props)
        self._send_discord(answer_to_user, True)

    def send_delete_waiting(self):
        answer_to_user = self.builder.build_delete_waiting_message()
        self._send_discord(answer_to_user, True)

    def send_delete_success(self, feed_name):
        answer_to_user = self.builder.build_delete_success_message()
        self._send_discord(answer_to_user, True)
        self._send_stdout(delete={"name":feed_name})

    def send_delete_error(self, **props):
        answer_to_user = self.builder.build_delete_error_message(**props)
        self._send_discord(answer_to_user, True)

    def set_data_submited(self, **options):
        self.builder.set_data_submited(**options)
