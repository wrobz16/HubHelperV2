import json
from discord.ext import commands

class SWEAR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.swear_words_file = "swear_words.json"
        self.swear_word_counter = self.load_swear_words(self.swear_words_file)

    def load_swear_words(self, file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {file_path} not found. Initializing with an empty dictionary.")
            return {}
        except json.JSONDecodeError:
            print(f"Error reading {file_path}. Initializing with an empty dictionary.")
            return {}

    def update_swear_counts(self):
        with open(self.swear_words_file, "w") as file:
            json.dump(self.swear_word_counter, file, indent=4)

    @commands.command(name="swear",
                      help="Displays the total count of all curse words that have been said in a text chat.")
    async def swear_command(self, ctx):
        total_count = sum(self.swear_word_counter.values())
        message = f"Total Swear Words Said: {total_count}"
        await ctx.send(message)

    @commands.command(name="swear_search",
                      help="Searches for a specific word and returns the amount of times it was said.")
    async def swear_search(self, ctx, word: str):
        word = word.lower()
        word_count = self.swear_word_counter.get(word, 0)
        similar_words = [w for w in self.swear_word_counter if word in w or w in word]

        message = f"The word '{word}' was said {word_count} time(s)."
        if similar_words:
            message += "\nSimilar words: " + ", ".join(similar_words)
        await ctx.send(message)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        message_words = message.content.lower().split()
        updated = False
        for word in message_words:
            if word in self.swear_word_counter:
                self.swear_word_counter[word] += 1
                updated = True

        if updated:
            self.update_swear_counts()


async def setup(bot):
    await bot.add_cog(SWEAR(bot))
