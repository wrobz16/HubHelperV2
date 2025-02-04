import asyncio
import discord
from discord.ext import commands
import json
import os

#######################################
# Load configs
#######################################
with open("config.json", "r") as file:
    config = json.load(file)
PREFIX = config["prefix"]
TOKEN = config["token"]

#######################################
# Initialize bot
#######################################
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, case_insensitive=True)
bot.config = config

#######################################
# Override default on_message
#######################################
@bot.event
async def on_message(message):
    pass

#######################################
# On ready
#######################################
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord.')

#######################################
# Load commands
#######################################
async def load_extensions():
    for filename in os.listdir("./features"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"features.{filename[:-3]}")

#######################################
# Load bot
#######################################
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

#######################################
# Start bot
#######################################
asyncio.run(main())
