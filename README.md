# haruyq's Utility Bot

A lightweight Discord utility bot for support servers.

> [!IMPORTANT]
> This project is currently in development. Please use at own risks!  

## Features
  - Webhook message sender
  - Ticket panel

## Docker
### Run with Docker Compose

> [!WARNING]
> This bot uses Privileged Gateway Intents.  
> You must enable the **Message Content Intent** in the Developer Portal.

**compose.yml Example:**
```yaml
services:
  haruyq-util-bot:
    image: ghcr.io/haruyq/haruyq-utility-bot:latest
    container_name: haruyq-util-bot

    env_file:
      - ./config/.env
    
    working_dir: /haruyq-util-bot
    volumes:
      - ./config:/haruyq-util-bot/config
      - ./db:/haruyq-util-bot/db

    restart: always
```

The `./config` and `./db` directory is mounted into the container.  
so you can edit `./config/webhooks.json` on the host and it will be used by the running container.

**Folder structure Example**
```
haruyq-utility-bot/
|-- compose.yml
|-- config/
|   |-- .env
|   |-- webhooks.json
|-- db/
|   |-- main.db
```

Set the environment variable `TOKEN` in your `./config/.env` file.  
See **[example.env](./config/example.env)** for more details.


## Copyright and License
Copyright [haruyq](https://haruyq.org) under the [MIT License](./LICENSE).
