import discord
from discord.ext import commands
import openai
import requests 
from PIL import Image
import io


class PhotoAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="photo")
    async def photo(self, ctx, *, description: str):
        def generate(text): 
            res = openai.Image.create( 
                prompt=text, 
                n=1, 
                size="256x256", 
            ) 
            return res["data"][0]["url"]
        
        url1 = generate(description) 
        
        response = requests.get(url1) 
        image_stream = io.BytesIO(response.content)

        await ctx.send(file=discord.File(fp=image_stream, filename="photo.jpg"))


async def setup(bot):
    await bot.add_cog(PhotoAI(bot))
