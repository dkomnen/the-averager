# The Averager

## Installation
Run `pip install -r requirements`

Run Mongo with docker

`docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:latest`

Add `mongo_host` and `mongo_port` env vars

Add your slack API token to `rtmbot.conf`

## Running

Run the bot from root of the project with `rtmbot`

Run the server from the root of the project with `flask run`