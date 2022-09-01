from typing import Any, List
from discord import Client, TextChannel
from tweepy import Client as Twitter_Client, User, Tweet

from src.registered_data import RegisteredServer
from src.generic_types import Feed

class Twitter(Feed):

    tw_client: Twitter_Client
    user: User

    def __init__(self,
        client: Client,
        channels: List[TextChannel],
        name: str,
        url: str,
        server_on: RegisteredServer,
        uid: int,
        generator_exist: bool,
        last_post: str,
        type: int,
        tw_client: Twitter_Client
    ) -> None:
        super().__init__(client, channels, name, url, server_on, uid, generator_exist, last_post, type)
        self.tw_client = tw_client
        self.user = self.tw_client.get_user(username=self.url).data

    def run(self) -> None:
        self.news_to_publish: List[Tweet] = self._get_news()
        self._send_news()
        self._close_thread()

    def _get_recent_tweets(self) -> List[Tweet]:
        return self.tw_client.get_users_tweets(
            self.user.id,
            tweet_fields=['created_at'] # ['context_annotations','created_at','geo']
        ).data

    def _send_news(self) -> None:
        if self.news_to_publish == []:
            self.message.send_no_news()
        else:
            for tweet in self.news_to_publish:
                tweet_url = f"https://twitter.com/{self.url}/status/{tweet.id}"
                message = f"**Author: @{self.url}**" + "\n" + tweet_url
                self.message.send_news(message, self.type)

    def _get_news(self) -> List[Tweet]:
        all_tweets = self._get_recent_tweets()
        tweets_to_publish: List[Any] = []
        news_to_save = tweets_to_publish
        is_not_in_error = all_tweets != []
        
        if is_not_in_error:
            if self.last_post != '':
                for tweet in all_tweets:
                    if str(tweet.created_at) == self.last_post:
                        break
                    tweets_to_publish.append(tweet)
            else:
                if int(self.published_since) == 0:
                    news_to_save = [all_tweets[0]]
                else:
                    for tweet in all_tweets:
                        if self._is_too_old_news(tweet.created_at):
                            break
                        tweets_to_publish.append(tweet)
            self._register_latest_post(news_to_save)
            reversed_list_from_oldest_to_earliest = list(reversed(tweets_to_publish))
            return reversed_list_from_oldest_to_earliest
        return tweets_to_publish
    
    def _register_latest_post(self, tweet: List[Tweet]) -> None:
        if tweet != []:
            self.last_post = str(tweet[0].created_at)