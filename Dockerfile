FROM ruby:3.1.2-alpine3.16

COPY config.ru Gemfile /opt/
COPY src/*.rb /opt/src/

WORKDIR /opt

RUN apk update && \
    apk add make g++ && \
    bundle install

RUN adduser -D -u 1000 scrap2rss
USER scrap2rss

CMD rackup
