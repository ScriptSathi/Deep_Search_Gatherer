require "rss"

class RSSBuilder
    def initialize(rss_data)
        @title = rss_data['title']
        @description = rss_data['description']
        @url = rss_data['url']
        @items = rss_data['items']
    end

    def render_rss_feed
        return RSS::Maker.make("2.0") do |maker|
            maker.channel.author = @title
            maker.channel.updated = Time.now.to_s
            maker.channel.link = @url
            maker.channel.title = @title
            maker.channel.description = @description
            
            for item_data in @items
                maker.items.new_item do |item|
                    item.link = item_data['link']
                    item.title = item_data['title']
                    item.description = item_data['description']
                    item.author = item_data['author']
                    item.pubDate = Time.now.to_s
                end
            end
        end
    end
end
