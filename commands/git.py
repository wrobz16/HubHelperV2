from discord.ext import commands


class INFO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="git",
                      help="Displays the link to the GIT Repo of this discord bot.")
    async def git_command(self, ctx):
        await ctx.send("Here is the link to John's GIT Repo for this project: https://github.com/wrobz16/HubHelperV2")


async def setup(bot):
    await bot.add_cog(INFO(bot))