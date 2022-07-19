require 'net/http'

class Utils

    def self.get_http_content(url)
        response = Net::HTTP.get_response(URI(url))
        if response.code.to_i != 200
            raise Exception "Error while reading url #{url}. Getting http error code #{response.code}"
        else
            return response.body
        end
    end
end