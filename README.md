# haruyq's Utility Bot

A lightweight Discord utility bot for support servers.

> [!IMPORTANT]
> This project is currently in development. Please use at own risks!  

## Features
***Coming soon***

## Docker

### Run with Docker Compose

Set `IMAGE_REPOSITORY` to `ghcr.io/haruyq/haruyq-utility-bot:latest`  

**Example:**
```yaml
services:
  haruyq-util-bot:
    image: ghcr.io/haruyq/haruyq-utility-bot:latest
    container_name: haruyq-util-bot

    environment:
      - TOKEN=YOUR_BOT_TOKEN
    
    working_dir: /haruyq-util-bot
    volumes:
      - ./config:/haruyq-util-bot/config

    restart: always
```

The `./config` directory is mounted into the container, so you can edit `config/webhooks.json` on the host and it will be used by the running container.

## Copyright and License
Copyright [haruyq](https://haruyq.org) under the [MIT License](./LICENSE).
