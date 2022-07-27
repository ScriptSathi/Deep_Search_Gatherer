#!/bin/bash

banner(){
    echo "---"
    echo "Initializing the project"
    echo "---"
}

build_docker_image(){
    # "--network host" to avoid possible network errors
    docker build --network host -t $1 $2
}

main(){
    banner
    git submodule init
    build_docker_image "rssbot" "externals/discord_information_gatherer"
    build_docker_image "scrape2RSS" "externals/scrape2RSS"
}

main