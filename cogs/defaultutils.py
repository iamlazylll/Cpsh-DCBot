
import discord
import datetime
from discord.ext import commands
bot = discord.Bot(intents = discord.Intents.all())
class DefaultUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @discord.slash_command()
    async def hello(self, ctx):
        await ctx.respond('你好')
    # @discord.listen(once = True)
    # async def on_ready(self):
    #     print("你好 我是")
    #     print(f"{self.user}啟動！")
    #     print("------")

# @bot.listen('on_message')
# async def rutomboy(message):
#     if message.author.id == bot.user.id:
#         return
#     if message.content.startswith("潘宇軒"):
#         await message.channel.send("是男娘")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        ch_id = 1248216296663814166
        chan_readonly = bot.get_channel(ch_id)
        await chan_readonly.send(f"{member.mentions} 你好")    

    @discord.slash_command(name = "hihi", description="回覆訊息")
    async def hello(self, ctx):
        await ctx.respond("hi")


    @discord.slash_command(description="現在時間")
    async def nowtime(self, ctx):
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        await ctx.respond(f"現在時間: `{current_time_str}`")

    @discord.slash_command(description="好欸")
    async def oyes(self, ctx,st:str):
        await ctx.respond(f"好欸, {st}")
def setup(bot):
    bot.add_cog(DefaultUtils(bot))

