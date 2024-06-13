import os
from dotenv import load_dotenv
import discord
import random
import datetime
from typing import List
from discord.ext import commands
from discord.commands import Option
load_dotenv()
bot = discord.Bot(intents = discord.Intents.all())
class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used.
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed.
    # This is part of the "meat" of the game logic.
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View.
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons.
    # This is not required.
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons.
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner and is used by the TicTacToeButton.
    def check_board_winner(self):
        # Check horizontal
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X
        elif diag == 3:
            return self.O

        # If we're here, we need to check if a tie has been reached.
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

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
                return await interaction.response.send_message(f"請輸入 {modalSelf.setting.minVal}～{modalSelf.setting.maxVal} 的整數", ephemeral=True)

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



@bot.slash_command(name="終極密碼", description="建立一個猜數字遊戲")
async def create_game(ctx, number: Option(int, "猜數字的最大範圍1~N", name="最大值", min_value=2, required=True)):
    await ctx.send_response(f"<@{ctx.author.id}>已開啟了一場「終極密碼」\n 已參加 : <@{ctx.author.id}> \n確認好人數後，發起者按下開始w", view=GameNumberView(ctx.author, number))

@bot.slash_command(name = "圈圈叉叉", description = "孤兒版")
async def tic(ctx: commands.Context):
    """Starts a tic-tac-toe game with yourself."""
    # Setting the reference message to ctx.message makes the bot reply to the member's message.
    await ctx.send("Tic Tac Toe: X goes first", view=TicTacToe(), reference=ctx.message)

@bot.listen()
async def on_ready():
    print("你好 我是")
    print(f"{bot.user}啟動！")
    print("------")

@bot.listen('on_message')
async def rutomboy(message):
    if message.author.id == bot.user.id:
        return
    if message.content.startswith("潘宇軒"):
        await message.channel.send("是打藝之神")

@bot.listen('on_message')
async def ruchangprince(message):
    if message.author.id == bot.user.id:
        return
    if message.content.startswith("張祐睿"):
        await message.channel.send("拜見張氏太子")

@bot.listen('on_message')
async def goodmorning(message):
    if message.author.id == bot.user.id:
        return
    if message.content == "早安":
        await message.channel.send("午安")

@bot.listen('on_message')
async def goodafter(message):
    if message.author.id == bot.user.id:
        return
    if message.content == "午安":
        await message.channel.send("晚安")

@bot.listen('on_message')
async def goodnight(message):
    if message.author.id == bot.user.id:
        return
    if message.content == "晚安":
        await message.channel.send("瑪卡巴卡")

@bot.listen('on_member_join')
async def ppljoin(member):
    await member.send(f"{member.mentions} 你好")    

@bot.slash_command(name = "你好", description="回覆訊息")
async def hello(ctx):
    await ctx.respond("hi")

@bot.slash_command(name = "現在時間", description="就是現在時間")
async def nowtime(ctx):
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    await ctx.respond(f"現在時間: `{current_time_str}`")

@bot.slash_command(name = "好欸", description="好欸")
async def oyes(ctx,st:str):
    await ctx.respond(f"好欸, {st}")

TOKN = os.getenv('TOKEN')
bot.run(TOKN)