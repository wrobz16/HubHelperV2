import asyncio
import discord
from discord.ext import commands
import json
import openai
import os

# Load configs
with open("config.json", "r") as file:
    config = json.load(file)
PREFIX = config["prefix"]
TOKEN = config["token"]
BOT_ID = config["bot_id"]
MESSAGE_CHANNEL_ID = config["message_channel_id"]
SONG_REQUEST_CHANNEL_ID = config["song_request_channel_id"]


# Initialize bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, case_insensitive=True)

# On ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord.')

# Load commands
async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"commands.{filename[:-3]}")

# For messages
@bot.event
async def on_message(message):
    # Bot message deletion
    if message.author.id == BOT_ID and message.channel.id == MESSAGE_CHANNEL_ID:
        await message.delete()
        print(f'Deleted message from {message.author.name} in #{message.channel.name}')
        await message.channel.send(f'Pancake song requests go in {bot.get_channel(SONG_REQUEST_CHANNEL_ID).mention} dumb fuck.')

    print(f'[{message.guild.name} - #{message.channel.name} - {message.author.name}]: {message.content}')
    await bot.process_commands(message)

# Load bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Start bot
asyncio.run(main())

