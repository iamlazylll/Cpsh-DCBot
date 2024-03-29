from dotenv import load_dotenv
import os
import discord
import time
load_dotenv()
bot = discord.Bot(intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("你好 我是")
    print(f"{bot.user}啟動！")
    print("------")

@bot.slash_command(description="回覆訊息")
async def hello(ctx):
    await ctx.respond("hi")


@bot.slash_command(description="現在時間")
async def nowtime(ctx):
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    await ctx.respond(f"現在時間: `{current_time_str}`")

@bot.slash_command(description="好欸")
async def nowtime(ctx,st:str):
    await ctx.respond(f"好欸, {st}")

@bot.slash_command(description="現在時間")
async def nowtime(ctx):
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    await ctx.respond(f"現在時間: '{current_time_str}'")

bot.run(os.getenv("TOKEN"))