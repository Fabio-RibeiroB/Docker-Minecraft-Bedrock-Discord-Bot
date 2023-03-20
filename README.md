# Minecraft Bedrock Discord Bot

Discord bot plugin for [Minecraft bedrock edition on Docker](https://github.com/itzg/docker-minecraft-bedrock-server)

Fabio-RibeiroB's edit: Work in progress. Containerising the bot to read from logs in shared volume as bedrock server and send messages to discord. 

Note to self: solve file not found issues.

## Overview

I built a Minecraft bedrock edition server with Docker, but there was no proper plugin for that environment, so I created a Bot plugin for Discord. It currently supports the following features.

- Send a message when a specific command is entered.
- Notify when someone log in and log out of the Minecraft server.

![mcdbot00](https://kosukelab.com/share/minecraft-discord-bot.png)

## Preparation

- Require Python 3.5.3 or higher
- Require pip3
- Require `discord.py`

  ```(text)
  $ pip3 install -U "discord.py[voice]"
  ```

- Edit `bot_config.py`
  - Get Discord token at developer site.
  - Enter your Discord channel id.
  - Enter your minecraft container full id.
    - You can search it with below command.
      ```
      docker inspect <container_name> | grep Id
      ```

- Add execute permission to `login_check.sh`

  ```
  $ chmod +x login_check.sh
  ```

- It is recommended that you add the following entry in visudo.

  ```(text)
  $ sudo visudo

  <your_user_name>  ALL=NOPASSWD:  /bin/tail
  ```

## How to use

- I recommend to start a separate session using screen command etc.
  
  ```(text)
  $ screen -S <session_name>
  ```

- Just execute the following command.

  ```(text)
  $ python3 discordbot.py
  ```

- The bot program will be left running, so detach it with Ctrl+A → D.
