from discord.ext import commands
import openai


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="ai",
                      help="Responds to a given prompt using GPT-4.")
    async def ai_command(self, ctx, *, 
                         question=commands.parameter(description="Prompt for the AI.")):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                temperature=0.5,
                max_tokens=150
            )
            assistant_reply = response.choices[0].message['content']
            await ctx.send(assistant_reply)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(AI(bot))