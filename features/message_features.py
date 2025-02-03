import discord
from discord.ext import commands

class MessageDeletion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        BOT_ID = self.bot.config["bot_id"]
        MESSAGE_CHANNEL_ID = self.bot.config["message_channel_id"]
        SONG_REQUEST_CHANNEL_ID = self.bot.config["song_request_channel_id"]

        if message.author.id == BOT_ID and message.channel.id == MESSAGE_CHANNEL_ID:
            await message.delete()
            print(f'Deleted message from {message.author.name} in #{message.channel.name}')
            await message.channel.send(f'Pancake song requests go in {self.bot.get_channel(SONG_REQUEST_CHANNEL_ID).mention} dumb fuck.')

        print(f'[{message.guild.name} - #{message.channel.name} - {message.author.name}]: {message.content}')
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(MessageDeletion(bot))
