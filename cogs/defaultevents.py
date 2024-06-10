
import discord
from discord.ext import commands
bot = discord.Bot(intents = discord.Intents.all())
class DefaultEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # @commands.Cog.listener(once = True)
    # async def on_ready(self):
    #     print("你好 我是")
    #     print(f"{self.user}啟動！")
    #     print("------")

    @commands.Cog.listener('on_message')
    async def rutomboy(self, message):
        if message.author.id == self.bot.user.id:
            return
        if message.content.startswith("潘宇軒"):
            await message.channel.send("是男娘")

def setup(bot):
    bot.add_cog(DefaultEvents(bot))

