# [Twitter/Twitch/Youtube/Reddit/RSS discord bot](https://github.com/ScriptSathi/Deep_Search_Gatherer)

## <a name="introduction">Introduction</a>

This bot is a multi server content tracker. It can follow twitter accounts/twitch channels/youtube channels/subreddit/rss feeds and static web pages with articles (when using the [full project](https://github.com/ScriptSathi/Deep_Search_Gatherer)) or RSS feeds and post it on the discord channels you want. To configure part of it you just need to use the available [commands](#bot-cmds)
<br/>
This is part of a full featured discord bot, the [Deep Search Gatherer bot](https://github.com/ScriptSathi/Deep_Search_Gatherer). It can be run on it's own or with the [Scrape2RSS project](../scrape2RSS/README.md) for tracking any websites that don't have rss feed and you wish to follow.

## <a name="features">Features</a>

- Follow a Twitter account
- Follow a Twitch channel
- Follow a subreddit
- Follow an RSS feed and post latests news
- Follow a Youtube channel and post latests videos
- Follow a static web page with comparing the diff

To interact with the bot, simply tag at the beggining of the message(`@Information Gatherer` for example)
- `help` Command to display all the commands available
- `add` Register a new feed to your server
- `delete` Delete a registered feed from your server
- `list` List all registered feeds

## <a name="bot-cmds">Bot Commands</a>

| Commands | Explanations 
|----|----|
| `add` | No Aliases <br/> __Parameters__: <br/>- just give the desired url after specifying the "add" command <br/> - `channel`: the channel ID where you want to post news on (you need to enable dev mode in your discord settings) <br/> - `name`: (optional) Chose a name for the registered feed|
| `delete` |  Aliases: `del` / `dl` <br/> Take the name of the feed to delete as parameter|
| `help` | Aliases: `-h` / `` (no params) <br/> Display the help menu |
| `list` | List all the registered feeds in your server |

### Examples
####  Add Youtube channel or an RSS feed
```bash
@Information Gatherer add https://www.youtube.com/c/LiveOverflow channel 1009496824605843607
```
```bash
@Information Gatherer add https://www.youtube.com/c/LiveOverflow channel 1009496824605843607 name LiveOverflow
```
####  Add Twitter
```bash
@Information Gatherer add @LiveOverflow channel 1009496824605843607
```
####  Add Reddit
```bash
@Information Gatherer add r/netsec channel 1009496824605843607
```
####  Delete a feed
```bash
@Information Gatherer del LiveOverflow
```
####  List feeds
```bash
@Information Gatherer ls
```

## Troubleshooting

If the name of you channel/account is parsed by the discord markdown (for exemple: \_my\_channel\_) you can use backticks arround the name to escape it 
```
@Information Gatherer add `@LiveOverflow` channel 1009496824605843607
```

## <a name="disclaimer">Disclaimer</a>

If you are unfamiliar with Docker, check out the [Introduction to Docker](https://training.docker.com/introduction-to-docker) webinar, or consult your favorite search engine.

## <a name="build">Build the image</a> 

Simply run the following command from this project source directory to build your new image
```
docker build -t rssbot .
```
## <a name="start">Start the container</a> 

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

## <a name="min-config">Minimal configuration needed</a> 

```
token: <TOKEN>
```

## <a name="allow-parameters">Configuration parameters</a> 

| Parameters | Explanation | Default value |
|----|----| ----|
| `token` | Your bot token, it's **mandatory** variable. | "" |
| `refresh-time` | Time between refreshes of a feed, in second | 900 |
| `published_since_default` | Maximum age of news before it's discarded, in second. Used only when `published_since` of a feed is not set. <br/>If `published_since_default` or `published_since` are equal to `0`, only posts published after the initialization of this bot will be sent (usefull in case you use [Scrape2RSS feature](../scrape2RSS/README.md)) | 0 |
| `gameplayed` | Change the game displayed in bot profile | "Eating some RSS feeds" |
| `twitter` |<li>`enabled` (default: False) - Enable the feature<li>`bearer_token` (default: "") Needed to auth the Twitter API | [] |
| `reddit` |<li>`enabled` (default: False) - Enable the feature<li>`client_id` (default: "") Needed to auth the Reddit API<li>`client_secret` (default: "") Needed to auth the Reddit API<li>`password` (default: "") Needed to auth the Reddit account for accessing reddit data<li>`username` (default: "") Needed to auth the Reddit account for accessing reddit data | [] |
| `twitch` |<li>`enabled` (default: False) - Enable the feature<li>`client_id` (default: "") Needed to auth the [Twitch API](https://dev.twitch.tv/docs/authentication)<li>`client_secret` (default: "") Needed to auth the [Twitch API](https://dev.twitch.tv/docs/authentication)| [] |

## [Scrape2RSS feature](../scrape2RSS/README.md)

If you want to follow a website that doesn't have an RSS feed, submit the URL of the page in the `url` parameter like a normal feed.
To be used, you need to set the [full bot project](https://github.com/ScriptSathi/Deep_Search_Gatherer)

## <a name="youtube-feature">Youtube Feature</a> 

To follow a youtube channel just put the youtube url in the `url` field.

Format tested: 
- `https://www.youtube.com/c/<Channel-Name>`
- `https://www.youtube.com/user/<Channel-Name>`