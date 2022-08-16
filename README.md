# [Youtube and RSS discord bot](https://github.com/ScriptSathi/discord_rss)


***UNDER MAINTAINANCE FOR BIG REFORGE, THE DOC BELLOW IS NOT UP TO DATE***

## Introduction 

This bot is used to follow a RSS feed or a youtube channel and post it over discord channels
<br/>
This is part of a full featured discord bot, the [Deep Search Gatherer bot](https://github.com/ScriptSathi/Deep_Search_Gatherer). It can be run on it's own or with the [Scrape2RSS project](https://github.com/ScriptSathi/scrape2RSS) for tracking any websites that don't have rss feed and you wish to follow.

## Features 

- Follow an RSS feed and post latests news
- Follow a Youtube channel and post latests videos

## Disclaimer

If you are unfamiliar with Docker, check out the [Introduction to Docker](https://training.docker.com/introduction-to-docker) webinar, or consult your favorite search engine.

## Build the image

Simply run the following command from this project source directory to build your new image
```
docker build -t rssbot .
```
## Usage

The configuration file is compatible with either `json` and `yaml` (or `yml`) format.
To understand how this project must be run, we will take the example with a valid yaml configuration file
The file don't need to be called `config.yaml` but need to be placed in `/config` folder. The file must be in a valid **JSON format**
```
docker run -d -v $(pwd)/config.yaml:/config/config.yaml --name=rssbot rssbot
```
You should then see your bot online on discord 

**Note:** If you've previously run a container with the same name, this command will fail. In that instance, you can use:
```
docker rm rssbot
```

## Minimal configuration needed

```
token: <TOKEN>
feeds:
    - channel: <CHANNEL>
      url: <RSS_FEED_URL>
```

## YAML configuration example

```
token: OTg1MzgZE3cwNDQyMTF67TU5.GFl0nX.WeyI8vqX3yO6kqh8Oia6cDpgEkZ1zH6eNHN9w8
feeds:
    - name: MY-AMAZING-FEED
      channel: 984379931012256123,98437993101227456
      url: https://www.cert.ssi.gouv.fr/alerte/feed/
    - name: A-BETTER-FEED
      channel: 984379931012256123
      url: https://www.youtube.com/c/LiveOverflow
      published_since: 6
published_since_default: 86000
refresh_time: 900
game_displayed: Eating some RSS feeds
```

## JSON configuration example

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
    "refresh_time": 900,
    "game_displayed": "Eating some RSS feeds",
}
```

## Allow parameters

| Command | Explanation | Default value |
|----|----| ----|
| `token` | Your bot token, it's **mandatory** variable. | "" |
| `feeds` | The feeds you want to be used by the bot. Each feeds in the list must be an object with at least a `url`and `channel` set. <ul><li>`name` Name of the feed (default: `feed-n°X`)<li>`url` **mandatory** Url of the feed (default: `''`)</li><li>`channel` **mandatory** Channel where to display the feed. For multiple channels for a single feed, just seperate the channels with a comma (`,`) (default: `''`)</li><li>`published_since` Maximum age of latest news to be posted (default: is the value of `published_since_default`)</li>| [] |
| `refresh-time` | Time between refreshes of a feed, in second | 900 |
| `published_since_default` | Maximum age of news before it's discarded, in second. Used only when `published_since` of a feed is not set. <br/>If `published_since_default` or `published_since` are equal to `0`, only posts published after the initialization of this bot will be sent (usefull in case you use [Scrape2RSS feature](https://github.com/ScriptSathi/scrape2RSS)) | 86400 |
| `gameplayed` | Change the game displayed in bot profile | "Eating some RSS feeds" |

## [Scrape2RSS feature](https://github.com/ScriptSathi/scrape2RSS)

If you want to follow a website that doesn't have an RSS feed, submit the URL of the page in the `url` parameter like a normal feed.
To be used, you need to set the [full bot project](https://github.com/ScriptSathi/Deep_Search_Gatherer)

## Youtube Feature

To follow a youtube channel just put the youtube url in the `url` field.

Format tested: 
- `https://www.youtube.com/c/<Channel-Name>`
- `https://www.youtube.com/user/<Channel-Name>`