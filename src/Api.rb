require "roda"

require_relative 'Extractor'
require_relative 'RSSBuilder'

class App < Roda

  fail_output = "Please submit an url at /create?url=\"YOUR_URL\""

  route do |req|
    # GET / req
    req.root do
      fail_output.to_s
    end
    req.on 'create' do
      req.get do
        if req.params.has_key?('url')
          extractor = Extractor.new(req.params['url'])
          rss_data = extractor.render_rss_data
          rss_builder = RSSBuilder.new(rss_data)
          "#{rss_builder.render_rss_feed}"
        else
          fail_output.to_s
        end
      end
    end
  end
end
