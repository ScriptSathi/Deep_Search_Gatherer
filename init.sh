#!/bin/bash

build_docker_image(){
    # "--network host" to avoid possible network errors
    docker build --network host -t $1 $2
}

main(){
    mkdir -p config_file/
    git submodule update --init --recursive
    build_docker_image "rssbot" "externals/discord_information_gatherer"
    build_docker_image "scrape2rss" "externals/scrape2RSS"
}

main