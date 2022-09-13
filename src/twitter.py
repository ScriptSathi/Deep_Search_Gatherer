from dataclasses import dataclass
from typing import Any, List
from discord import Client, TextChannel
from tweepy import Client as Twitter_Client, User, Tweet
from src.message_builders import PostMessage

from src.registered_data import RegisteredServer
from src.Feed import Feed

@dataclass(frozen=True)
class PublishableTweet:
    is_retweed: bool
    is_reply: bool
    tweet: Tweet

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
        self.news_to_publish: List[PublishableTweet] = self._get_news()
        self._send_news()
        self._close_thread()

    def _get_recent_tweets(self) -> List[Tweet]:
        return self.tw_client.get_users_tweets(
            self.user.id,
            tweet_fields=['created_at', "referenced_tweets", "in_reply_to_user_id"]
        ).data

    def _send_news(self) -> None:
        if self.news_to_publish == []:
            self.message.send_no_news()
        else:
            for pub_tweet in self.news_to_publish:
                if not pub_tweet.is_reply:
                    tweet_id = pub_tweet.tweet.id
                    tweet_status = "tweeted"
                    if pub_tweet.is_retweed:
                        tweet_id = pub_tweet.tweet.referenced_tweets[-1].id
                        tweet_status = "retweeted from"
                    link = f"https://twitter.com/{self.url}/status/{tweet_id}"
                    author = f"@{self.url}"
                    msg = f"{tweet_status} this {link}"
                    self.message.send_news(
                        PostMessage(pub_tweet.tweet.text, msg, link, author),
                        self.type
                    )

    def _get_news(self) -> List[PublishableTweet]:
        all_tweets = self._get_recent_tweets()
        publishable_tweets: List[PublishableTweet] = []
        news_to_save = publishable_tweets
        is_not_in_error = all_tweets != []

        if is_not_in_error:
            if self.last_post != '':
                for tweet in all_tweets:
                    if str(tweet.created_at) == self.last_post:
                        break
                    publishable_tweets.append(PublishableTweet(
                        True if tweet.referenced_tweets != [] and str(tweet.text).startswith('RT') else False,
                        True if tweet.in_reply_to_user_id != None else False,
                        tweet
                    ))
            else:
                if int(self.published_since) == 0:
                    news_to_save = [
                        PublishableTweet(
                            True if all_tweets[0].referenced_tweets != [] and str(all_tweets[0].text).startswith('RT') else False,
                            True if all_tweets[0].in_reply_to_user_id != None else False,
                            all_tweets[0]
                        )
                    ]
                else:
                    for tweet in all_tweets:
                        if self._is_too_old_news(tweet.created_at):
                            break
                        publishable_tweets.append(PublishableTweet(
                            True if tweet.referenced_tweets != [] and str(tweet.text).startswith('RT') else False,
                            True if tweet.in_reply_to_user_id != None and str(tweet.text).startswith('@') else False,
                            tweet
                        ))
            self._register_latest_post(news_to_save)
            reversed_list_from_oldest_to_earliest = list(reversed(publishable_tweets))
            return reversed_list_from_oldest_to_earliest
        return publishable_tweets

    def _register_latest_post(self, pub_tweet: List[PublishableTweet]) -> None:
        if pub_tweet != []:
            self.last_post = str(pub_tweet[0].tweet.created_at)
