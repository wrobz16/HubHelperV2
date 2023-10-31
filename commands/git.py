from discord.ext import commands


class GIT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="git")
    async def git_command(self, ctx):
        await ctx.send("Here is the link to John's GIT Repo for this project: https://github.com/wrobz16/HubHelperV2")


async def setup(bot):
    await bot.add_cog(GIT(bot))