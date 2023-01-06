require 'nokogiri'
require 'uri'

require_relative 'Utils'

class Scraper

    def initialize(url)
        @url = url
        raw_html = Utils.get_http_content(url)
        # raw_html = File.open('acceis.html').read
        @html_content = Nokogiri::HTML(raw_html)
    end
    public :initialize

    def render_news_data
        
        unparsed_divs_list = self._build_unparsed_divs_list
        html_articles = self._render_articles_list(unparsed_divs_list)
        items = []
        for html_article in html_articles
            item = {}
            item['title'] = self._extract_article_title(html_article)
            item['description'] = ""
            item['link'] = self._extract_article_link(html_article)
            item['author'] = ""
            item['pubDate'] = Time.now.to_s
            items.append(item)
        end
        items = self._remove_duplicates(items)
        rss_data = {}
        rss_data['title'] = self.method(:_extract_page_title).call
        rss_data['description'] = ''
        rss_data['url'] = @url
        rss_data['items'] = items
        return rss_data
    end
    public :render_news_data

    def _render_articles_list(unparsed_divs_list)
        def sort_biggest_array(arr, max_length)
            biggest_array = arr[0]       
            for i in 0..max_length-1
                if arr[i].length > biggest_array.length
                    biggest_array = arr[i]
                end
            end
            return biggest_array
        end

        headers = self._build_div_headers(unparsed_divs_list)
        big_array = []
        i = 0

        while i < unparsed_divs_list.length do
            mixed_divs = []
            headers.each_with_index do |div_head, index|
                if headers[i] == div_head
                    mixed_divs.append(unparsed_divs_list[index])
                end
            end
            big_array.append(mixed_divs)
            i += 1
        end
        return sort_biggest_array(big_array, big_array.length)
    end
    private :_render_articles_list

    def _build_div_headers(unparsed_divs_list)
        headers = []
        for div in unparsed_divs_list 
            headers.append(self._get_first_div(div))
        end
        return headers
    end
    private :_build_div_headers

    def _build_unparsed_divs_list
        unparsed_divs_list = []
        @html_content.css('div').each do |div|
            has_title, _ = self._has_title(div)
            res = self._has_link_in_div(div) + self._has_image(div) + has_title
            if res >= 3
                unparsed_divs_list.append(div)
            end
        end
        return unparsed_divs_list
    end
    private :_build_unparsed_divs_list

    def _get_first_div(div)
        return div.to_s.split("\n")[0]
    end

    def _has_link_in_div(div)
        link_exist = 0
        div.css('a').each do |link|
            link_exist = 1
        end
        return link_exist
    end
    private :_has_link_in_div

    def _has_image(div)
        image_exist = 0
        div.css('img').each do |img|
            image_exist = 1
        end
        return image_exist
    end
    private :_has_image

    def _has_title(div)
        title_exist = 0
        titles = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        title_type = ''
        titles.each do |title|
            div.css(title).each do |img|
                title_type = title
                title_exist = 1
            end
        end
        return title_exist, title_type
    end
    private :_has_title

    def _remove_duplicates(articles_list)
        def is_the_same(array_key, article_to_test, article)
            for key in array_key
                if (article_to_test[key] == article[key] &&
                    article_to_test[key] != "" &&
                    article[key] != "")
                    return true
                end
            end
            return false
        end

        first_article = articles_list[0]
        last_article = articles_list[articles_list.length - 1]
        articles_to_remove = []
        articles_list.each_with_index do |article, i|
            articles_list.each_with_index do |article_to_test, j|
                if is_the_same(['title', 'link', 'description'], article_to_test, article)
                    if i != j
                        articles_to_remove.append(j)
                    end
                end
            end
        end
        for index_to_delete in articles_to_remove
            articles_list.delete_at(index_to_delete)
        end
        return articles_list.uniq
    end
    private :_remove_duplicates

    def _extract_article_link(html_article)
        links = html_article.css('a').map { 
            |link| link['href'] 
        }
        link = links[0].to_s.delete("\n").strip
        
        is_not_http = ! link.include?('http')
        if is_not_http
            list_url = URI.split(@url).reject(&:nil?)
            base_url = list_url[0] + "://" + list_url[1]
            return URI.join(base_url + "/", link)
        end
        return URI.extract(link)[0]
    end
    private :_extract_article_link

    def _extract_article_title(html_article)
        _, title_type = self._has_title(html_article)
        title = html_article.css(title_type).map { 
            |title| title.content
        }
        return title[0].to_s.delete("\n").strip
    end
    private :_extract_article_title

    def _extract_page_title
        return @html_content.css('title').map{ |title| title.content}[0]
    end
end
