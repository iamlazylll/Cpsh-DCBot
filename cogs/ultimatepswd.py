import random
import discord
from discord.commands import Option
from discord.ext import commands
bot = discord.Bot(intents = discord.Intents.all())

class ultimatepswd(commands.Cog):
    # def __init__(self, bot):
    #     self.bot = bot


    class GameNumberView(discord.ui.View):
        def __init__(self, author, maxValue):
          super().__init__()
          self.answer = random.randint(1, maxValue)
          self.author = author
          self.playerList = []
          self.round = 0
          self.minVal = 1
          self.maxVal = maxValue
          self.playerList.append(author.id)

        class PlayerStart(discord.ui.View):
            def __init__(playerSelf, setting):
                super().__init__()
                playerSelf.setting = setting

            @discord.ui.button(label="輸入猜測數字", style=discord.ButtonStyle.success)
            async def player_start_callback(playerSelf, button:discord.ui.Button, interaction:discord.Interaction):
                await interaction.response.send_modal(playerSelf.setting.NumberGuess(title=f"<@{playerSelf.setting.playerList[playerSelf.setting.round]}> 開始猜，從 {playerSelf.setting.minVal}~{playerSelf.setting.maxVal} 選一個整數", setting=playerSelf.setting))
            

        class NumberGuess(discord.ui.Modal):
            def __init__(modalSelf, title, setting):
                print(setting)
                super().__init__(title=title)
                modalSelf.setting = setting
                modalSelf.add_item(discord.ui.InputText(label="整數數字", required=True))
  
            async def callback(modalSelf, interaction: discord.Interaction):
                playerInput = modalSelf.children[0].value
                try:
                    playerInput = int(playerInput)
                except:
                    return await interaction.response.send_message(f"請輸入 {modalSelf.setting.minVal + 1}～{modalSelf.setting.maxVal} 的整數", ephemeral=True)

                if playerInput < modalSelf.setting.minVal or playerInput > modalSelf.setting.maxVal:
                    return await interaction.response.send_message(f"請輸入 {modalSelf.setting.minVal + 1}～{modalSelf.setting.maxVal} 的整數", ephemeral=True)

                if playerInput != modalSelf.setting.answer:
                    if playerInput < modalSelf.setting.answer:
                        modalSelf.setting.minVal = playerInput + 1
                    elif playerInput > modalSelf.setting.answer:
                        modalSelf.setting.maxVal = playerInput - 1

                    if (modalSelf.setting.round + 1) >= len(modalSelf.setting.playerList):
                        modalSelf.setting.round = 0
                    else:
                        modalSelf.setting.round += 1
                      
                    await interaction.response.send_message(f"<@{modalSelf.setting.playerList[modalSelf.setting.round]}> 開始猜，從 {modalSelf.setting.minVal}~{modalSelf.setting.maxVal} 選一個整數", view=modalSelf.setting.PlayerStart(modalSelf.setting))
                else: 
                    await interaction.response.send_message(f"BOOM!!! <@{interaction.user.id}> 中獎囉WWW")
              

        @discord.ui.button(label="點擊參加", style=discord.ButtonStyle.primary)
        async def button_callback(self, button:discord.ui.Button, interaction:discord.Interaction):
            try:
                self.playerList.index(interaction.user.id)
            except:
                self.playerList.append(interaction.user.id)

            message = f"<@{self.author.id}>已開啟了一場「終極密碼」\n 已參加 : "
            for data in self.playerList:
                message += f"<@{data}> "

            message += f"\n確認好人數後，發起者按下開始w"
            await interaction.response.edit_message(content=message)
          

        @discord.ui.button(label="開始", style=discord.ButtonStyle.success)
        async def button_start_callback(self, button:discord.ui.Button, interaction:discord.Interaction):
            channel = bot.get_channel(interaction.channel_id)
            if interaction.user.id == self.author.id:
                await interaction.response.send_message(f"<@{self.playerList[self.round]}> 開始猜，從 {self.minVal}~{self.maxVal} 選一個整數", view=self.PlayerStart(self))
            else:
                await interaction.response.send_message("你不是發起者喔w", ephemeral=True)

  

    @discord.slash_command(description="建立一個猜數字遊戲")
    async def create_game(ctx, number: Option(int, "猜數字的最大範圍1~N", name="最大值", min_value=2, required=True)):
        await ctx.send_response(f"<@{ctx.author.id}>已開啟了一場「終極密碼」\n 已參加 : <@{ctx.author.id}> \n確認好人數後，發起者按下開始w", view=GameNumberView(ctx.author, number))
def setup(bot):
    bot.add_cog(ultimatepswd(bot))