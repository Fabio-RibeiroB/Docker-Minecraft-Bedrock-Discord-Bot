#!/home/fabio/.venv/bedrock/bin/python3
import discord
from discord.ext import tasks, commands
import asyncio
import subprocess
import os
import bot_config
import docker

TOKEN = bot_config.DISCORD_TOKEN
CHANNEL_ID = bot_config.DISCORD_CHANNEL_ID
CONTAINER_ID = bot_config.CONTAINER_ID


intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = "!bds ", intents = intents)

docker_client = docker.from_env()

def get_container_status(container_id):
    container = docker_client.containers.get(container_id)
    return container.status

async def send_discord_message(channel_id, message):
        channel = client.get_channel(channel_id)
        await channel.send(message)

# Define a task to periodically check the status of the Docker container
@tasks.loop(minutes=30)
async def check_container_status():
    container_status = get_container_status(CONTAINER_ID)
    if container_status == 'running':
        message = f"Bedrock server is up."
        await send_discord_message(CHANNEL_ID, message)
    elif container_status == 'exited':
        message = f"Bedrock server is down."
        await send_discord_message(CHANNEL_ID, message)

@client.command()
async def status(ctx):
    container_status = get_container_status(CONTAINER_ID)
    message = f"The Bedrock server is currently {container_status}."
    await ctx.send(message)

@tasks.loop(seconds=1)
async def login_check_loop():
    subprocess.call("./login_check.sh")
    if os.stat("./login_check_result").st_size != 0:
        f = open("./login_check_result", 'r')
        data = f.readline()
        channel = client.get_channel(int(CHANNEL_ID))
        await channel.send(data)
        f.close()


@client.event
async def on_ready():
	check_container_status.start()
	login_check_loop.start()
	print('Logged in done. Bot is ready...')

client.run(TOKEN)

