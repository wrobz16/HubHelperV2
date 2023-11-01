import discord
from discord.ext import commands
import yt_dlp as ytdl


class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
            }],
            'quiet': False,
            'source_address': '0.0.0.0',
        }


    @commands.command(name='play')
    async def play(self, ctx, *, search: str):
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return
        
        channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)
        
        with ytdl.YoutubeDL(self.ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch1:{search}", download=False)
            if 'entries' not in search_results:
                await ctx.send("No suitable format found. Please try another video.")
                return
    
            video_url = search_results['entries'][0]['url']
            voice = ctx.voice_client
            try:
                source = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=video_url,
                            options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5')
                voice.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
            except Exception as e:
                print(f"Error while trying to play audio: {e}")
            await ctx.send(f"Playing: {search_results['entries'][0]['title']}")


    @commands.command(name='leave')
    async def leave(self, ctx):
        if not ctx.voice_client:
            await ctx.send("I am not connected to a voice channel.")
            return
        await ctx.voice_client.disconnect()


async def setup(bot):
    await bot.add_cog(YouTube(bot))