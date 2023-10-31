import discord
from discord.ext import commands
import json

# Load the JSON file
with open("config.json", "r") as file:
    config = json.load(file)

PREFIX = config["prefix"]
TOKEN = config["token"]


# Initialize bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, case_insensitive=True)

# When bot is loaded
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord.')
    print("THIS IS A TEST")

# For messages
@bot.event
async def on_message(message):
    print(f'[{message.guild.name} - #{message.channel.name} - {message.author.name}]: {message.content}')

    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
