import discord
from discord.ext import commands
import io
import openai
from PIL import Image
import requests 


class PhotoAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="photo")
    async def photo(self, ctx, description: str, variations: int = 1):
        def generate(text, num_variations): 
            res = openai.Image.create( 
                prompt=text, 
                n=num_variations,
                size="256x256", 
            ) 
            return [image["url"] for image in res["data"]]
        
        if 1 <= variations <= 10:
            urls = generate(description, variations) 

            for url in urls:
                response = requests.get(url) 
                image_stream = io.BytesIO(response.content)

                await ctx.send(file=discord.File(fp=image_stream, filename="photo.jpg"))
        else:
            await ctx.send("Please provide a number of variations between 1 and 10.")


async def setup(bot):
    await bot.add_cog(PhotoAI(bot))
