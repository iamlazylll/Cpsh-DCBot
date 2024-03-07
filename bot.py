from dotenv import load_dotenv
import os
import discord
load_dotenv()
bot = discord.bot()

@bot.event
async def on_ready():
    print("你好 我是")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
bot.run(os.getenv("TOKEN"))