require "roda"

class App < Roda
  route do |r|
    # GET / request
    r.root do
      r.redirect "/create"
    end
    r.on 'create' do
      r.get do
        if r.params.has_key?("url")
          "#{r.params['url']}"
        end
        "#{r.params['url']}:#{r.params.has_key?("url")}"
        # "Please submit an url at /create?url=<YOUR URL>"
      end
    end
  end
end
