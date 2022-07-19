This project is a WIP. The scraper is working and make an RSS feed, but the api isn't build yet.
If you want to use it, check the code below

```
extractor = Extractor.new('<Your_URL>')
rss_data = extractor.render_rss_data
rss_builder = RSSBuilder.new(rss_data)
puts rss_builder.render_rss_feed # output you RSS feed
```