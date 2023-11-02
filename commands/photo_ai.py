import datetime
import discord
from discord.ext import commands
import io
import openai
import requests 

LIMIT = 25

class PhotoAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.images_generated_today = 0
        self.current_date = datetime.date.today()


    @commands.command(name="photo",
                      help=f"Generates an image based on the provided prompt ({LIMIT} per day). Usage: !photo <description (in quotes)> <variations (3 max)>.",
                      brief="Generate an image with AI based on a given prompt.")
    async def photo(self, ctx, 
                    description:str=commands.parameter(description="Prompt for the AI to use."), 
                    variations:int=commands.parameter(default=1, description="The number of photos to be generated (max: 3)")):
        def generate(text, num_variations): 
            res = openai.Image.create( 
                prompt=text, 
                n=num_variations,
                size="256x256")
            return [image["url"] for image in res["data"]]
        
        if self.current_date != datetime.date.today():
            self.current_date = datetime.date.today()
            self.images_generated_today = 0

        if self.images_generated_today + variations > LIMIT:
            await ctx.send("Sorry, the limit of 25 images per day has been reached.")
            return
        
        if 1 <= variations <= 3:
            urls = generate(description, variations) 

            for url in urls:
                response = requests.get(url) 
                image_stream = io.BytesIO(response.content)

                await ctx.send(file=discord.File(fp=image_stream, filename="photo.jpg"))

            self.images_generated_today += variations
        else:
            await ctx.send("Please provide a number of variations between 1 and 10.")


    @commands.command(name="photos_left",
                      help=f"Sends the remaining amount of photos that are able to be generated for the day ({LIMIT} per day).",
                      brief="Amount of photos left to be generated.")
    async def photos_left(self, ctx):
        if self.current_date != datetime.date.today():
            self.current_date = datetime.date.today()
            self.images_generated_today = 0

        remaining = LIMIT - self.images_generated_today
        await ctx.send(f"You can generate {remaining} more images today.")


async def setup(bot):
    await bot.add_cog(PhotoAI(bot))