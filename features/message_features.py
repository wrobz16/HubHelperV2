import discord
from discord.ext import commands
import time

class MessageDeletion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.recent_p_user = None
        self.last_reply_time = 0
        self.cooldown_seconds = 3

    @commands.Cog.listener()
    async def on_message(self, message):
        # Set IDs for Bot reply
        BOT_ID = self.bot.config["bot_id"]
        MESSAGE_CHANNEL_ID = self.bot.config["message_channel_id"]
        SONG_REQUEST_CHANNEL_ID = self.bot.config["song_request_channel_id"]
        BOT_DELETE_PREFIX = self.bot.config["bot_delete_prefix"]

        # Check if pancake prefix
        if message.content.startswith(BOT_DELETE_PREFIX):
            self.recent_p_user = message.author

        # Reply to idiot who sent the song request in the wrong channel
        if message.author.id == BOT_ID and message.channel.id == MESSAGE_CHANNEL_ID:
            await message.delete()
            print(f'Deleted message from {message.author.name} in #{message.channel.name}')
            current_time = time.time()
            if current_time - self.last_reply_time > self.cooldown_seconds:
                self.last_reply_time = current_time
                if self.recent_p_user:
                    await message.channel.send(f'{self.recent_p_user.mention}, Pancake song requests go in {self.bot.get_channel(SONG_REQUEST_CHANNEL_ID).mention} dumb fuck.')
                else:
                    await message.channel.send(f'Pancake song requests go in {self.bot.get_channel(SONG_REQUEST_CHANNEL_ID).mention} dumb fuck.')

        # Log messages
        print(f'[{message.guild.name} - #{message.channel.name} - {message.author.name}]: {message.content}')
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(MessageDeletion(bot))
