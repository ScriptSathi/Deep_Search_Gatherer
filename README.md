# [Youtube and RSS discord bot ](https://github.com/ScriptSathi/discord_rss)

This bot is used to follow a RSS feed or a youtube channel and post it over discord channels

## Features 

- Follow an RSS feed and post latests news
- Follow a Youtube channel and post latests videos

## Introduction

This file **is not** intended as an introduction to docker.

 If you are unfamiliar with Docker, check out the [Introduction to Docker](https://training.docker.com/introduction-to-docker) webinar, or consult your favorite search engine.

## Build the image

Simply run the following command from this project source directory to build your new image
```
docker build -t rssbot .
```

## Simple running command
The file don't need to be called `config.json` but need to be placed in `/config` folder. The file must be in a valid **JSON format**
```
docker run -d -v $(pwd)/config.json:/config/config.json --name=rssbot rssbot
```

## Minimal configuration needed 
```
{
    "token": "<TOKEN>",
    "feeds": [
                {
            "channel": "<CHANNEL>",
            "url": "<RSS_FEED_URL>",
        }
    ]
}
```
## Full configuration exemple
```
{
    "token": "OTg1MzgZE3cwNDQyMTF67TU5.GFl0nX.WeyI8vqX3yO6kqh8Oia6cDpgEkZ1zH6eNHN9w8",
    "feeds": [
                {
            "name": "MY-AMAZING-FEED",
            "channel": "984379931012256123",
            "url": "https://www.cert.ssi.gouv.fr/alerte/feed/",
        },
        {
            "name": "A-BETTER-FEED",
            "channel": "984379931012256123",
            "url": "https://www.youtube.com/c/LiveOverflow",
            "published_since": 60
        }
    ],
    "published_since_default": 86000,
    "refresh_time": 300,
    "game_displayed": "Eating some RSS feeds",
}
```

## Allow parameter
You can configurate the bot using [environnement variables](https://docs.docker.com/engine/reference/run/#env-environment-variables). 
You can avoid using json config file by simply adding token and feeds through environnement variables
| Command | Explanation | Default value |
|----|----| ----|
| `token` | Your bot token, it's **mandatory** variable. | "" |
| `feeds` | The feeds you want to be used by the bot. Each feeds in the list must be an object with at least a `url`and `channel` set. <ul><li>`name` Name of the feed (default: `feed-n°X`)<li>`url` **mandatory** Url of the feed (default: `''`)</li><li>`channel` **mandatory** Channel where to display the feed (default: `''`)</li><li>`published_since` Maximum age of latest news to be posted (default: is the value of `published_since_default`)</li>| [] |
| `refresh-time` | Time between refreshes of a feed, in second | 900 |
| `published_since_default` | Maximum age of news before it's discarded, in second. Used only when `published_since` of a feed is not set | 86400 |
| `gameplayed` | Change the game displayed in bot profile | "Eating some RSS feeds" |

You should then see your bot online on discord 

**Note:** If you've previously run a container with the same name, this command will fail. In that instance, you can use:
```
docker rm rssbot
```

## Youtube Feature

To follow a youtube channel just put the youtube url in the `url` field.

Format tested: `https://www.youtube.com/c/<Channel-Name>`