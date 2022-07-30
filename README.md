# [Deep search gatherer](https://github.com/ScriptSathi/Deep_Search_Gatherer)

## Introduction

This project is a full featured RSS **discord bot** using 2 services over a docker compose. It is used to track RSS feeds / youtube channels or common websites and post it over discord channels
-  The [discord information gatherer bot](https://github.com/ScriptSathi/discord_information_gatherer) who track RSS feeds and youtube channel latest videos and publish it on discord 
- The [scrape2RSS](https://github.com/ScriptSathi/scrape2RSS/) who generate an RSS feed based on a simple url

## Features 

example url that can be tracked (you can put this in your config file to try it)
- A very common RSS feed url `https://www.cert.ssi.gouv.fr/alerte/feed/`
- A youtube channel `https://www.youtube.com/c/LiveOverflow`
- A static webpage `https://www.synacktiv.com/publications`

## Disclaimer

This project need docker to be installed and this **is not** intended as an introduction to docker.

 If you are unfamiliar with Docker, check out the [Introduction to Docker](https://training.docker.com/introduction-to-docker) webinar, or consult your favorite search engine.

## Prepare the project

Before starting the project you need to pull git submodules and build the docker images.
```
bash init.sh
```

## Usage

After you added your configuration file in `config_file` (view next section for this part), just run the below command
```
docker compose -d up
```

## Create the config file

The configuration file is compatible with either `json` and `yaml` (or `yml`) format.
View the documentation [here](https://github.com/ScriptSathi/discord_information_gatherer) for json usage.
<br/>
**Put your configuration file in the `config_file/` directory**

### Minimal configuration needed 
```
token: <TOKEN>
feeds:
    - channel: <CHANNEL>
      url: <RSS_FEED_URL>
```

### Configuration example

```
token: OTg1MzgZE3cwNDQyMTF67TU5.GFl0nX.WeyI8vqX3yO6kqh8Oia6cDpgEkZ1zH6eNHN9w8
feeds:
    - name: MY-AMAZING-FEED
      channel: 984379931012256123,98437993101227456
      url: https://www.cert.ssi.gouv.fr/alerte/feed/
    - name: A-BETTER-FEED
      channel: 984379931012256123
      url: https://www.youtube.com/c/LiveOverflow
      published_since: 6000
published_since_default: 86000
refresh_time: 900
game_displayed: Eating some RSS feeds
```

## Allow parameters


| Command | Explanation | Default value |
|----|----| ----|
| `token` | Your bot token, it's **mandatory** variable. | "" |
| `feeds` | The feeds you want to be used by the bot. Each feeds in the list must be an object with at least a `url`and `channel` set. <ul><li>`name` Name of the feed (default: `feed-n°X`)<li>`url` **mandatory** Url of the feed (default: `''`)</li><li>`channel` **mandatory** Channel where to display the feed. For multiple channels for a single feed, just seperate the channels with a comma (`,`) (default: `''`)</li><li>`published_since` Maximum age of latest news to be posted (default: is the value of `published_since_default`)</li>| [] |
| `refresh-time` | Time between refreshes of a feed, in second | 900 |
| `published_since_default` | Maximum age of news before it's discarded, in second. Used only when `published_since` of a feed is not set | 86400 |
| `gameplayed` | Change the game displayed in bot profile | "Eating some RSS feeds" |
