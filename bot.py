import os
from dotenv import load_dotenv
import discord
import datetime
load_dotenv()
bot = discord.Bot(intents = discord.Intents.all())

@bot.listen(once = True)
async def on_ready():
    print("你好 我是")
    print(f"{bot.user}啟動！")
    print("------")

# @bot.listen('on_message')
# async def rutomboy(message):
#     if message.author.id == bot.user.id:
#         return
#     if message.content.startswith("潘宇軒"):
#         await message.channel.send("是男娘")

# @bot.listen('on_member_join')
# async def ppljoin(member):
#     ch_id = 1248216296663814166
#     chan_readonly = bot.get_channel(ch_id)
#     await chan_readonly.send(f"{member.mentions} 你好")    

# @bot.slash_command(name = "hihi", description="回覆訊息")
# async def hello(ctx):
#     await ctx.respond("hi")


# @bot.slash_command(description="現在時間")
# async def nowtime(ctx):
#     current_time = datetime.datetime.now()
#     current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
#     await ctx.respond(f"現在時間: `{current_time_str}`")

# @bot.slash_command(description="好欸")
# async def oyes(ctx,st:str):
#     await ctx.respond(f"好欸, {st}")
cogs_list = [
    'defaultutils',
    'defaultevents',
    'ultimatepswd'
]
for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')
TOKN = os.getenv('TOKEN')
bot.run(TOKN)