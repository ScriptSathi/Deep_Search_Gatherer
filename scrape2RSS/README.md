# [Scrape2RSS](./README.md)

This project take an url as entry with articles you wanted to follow, and return an RSS feed

## Disclaimer

This file **is not** intended as an introduction to docker.

 If you are unfamiliar with Docker, check out the [Introduction to Docker](https://training.docker.com/introduction-to-docker) webinar, or consult your favorite search engine.

## Build the image

Simply run the following command from this project source directory to build your new image
```
docker build -t scrape2rss .
```

## Start the application
To start the api simply run the following command
```
docker run -d -p 9292:9292 --name=scrape2rss scrape2rss
```

## Generate the RSS feed
After the application is correctly initialized, just submit a url like this 
```
curl http://localhost:9292/create?url=<YOUR_URL>
```
And it will return the RSS feed

Or you can simply use the browser and the `ctrl+u` to view the source and have the xml output