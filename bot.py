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
OPENAI_KEY = config["openai_key"]

# Initialize bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, case_insensitive=True)

# Set some other things
openai.api_key = OPENAI_KEY

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
    print(f'[{message.guild.name} - #{message.channel.name} - {message.author.name}]: {message.content}')
    await bot.process_commands(message)

# Load bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())