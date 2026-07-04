import asyncio
import random
from typing import List
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discordLevelingSystem import DiscordLevelingSystem, RoleAward, LevelUpAnnouncement

load_dotenv()
intents = discord.Intents(messages=True, guilds=True, members=True, message_content=True)
bot = commands.Bot(command_prefix='!',intents=intents)


#Bot working test

@bot.event
async def on_ready():
  print(f'Systems Online as: {bot.user}')
  await bot.get_channel(1521809052555022369).send(f'```{bot.user} Is Online.```')

@bot.event
async def on_member_join(member):
  git_url = "https://github.com/themoon41/my-bot"
  embed = discord.Embed(
    title="Bot Stuff Server",
    description="Rules",
    color=discord.Color.purple(),
    url=git_url,
  )
  embed.add_field(name="1. Don't be a dick", value="\u200b", inline=False)
  embed.add_field(name="2. Have fun", value="\u200b", inline=False)
  embed.add_field(name="3. 20 minute coding adventures only", value="\u200b", inline=False)
  await member.send("Welcome {}! ".format(member.mention))
  await member.send(embed=embed)
  await bot.get_channel(1521809052555022369).send("Everyone Please Welcome {}!".format(member.mention))




#Basic bot commands

@bot.command(help='say hi.')
async def hello(ctx):
  await ctx.send("hi {0}".format(ctx.author.mention))

@bot.command(help='Github link')
async def git(ctx):
  await ctx.send("Find the code here: https://github.com/themoon41/my-bot")

@bot.command(help='For The Memes', aliases=['pppp'])
async def peepeepoopoo(ctx):
  await ctx.send("https://www.youtube.com/watch?v=PMNY8g0_wJA")
  
# Level Up system

try:
    loop = asyncio.get_event_loop()
except RuntimeError as e:
    if str(e).startswith('There is no current event loop in thread'):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    else:
        raise

# discord server id
Guild_ID = 1521809051867025529

#data set of roles and level requirements
My_Awards = {
  Guild_ID : [
    RoleAward(role_id=1521845456123203787, level_requirement=5, role_name=None),
    RoleAward(role_id=1521845755873198251, level_requirement=10, role_name=None),
    RoleAward(role_id=1521845797841403914, level_requirement=20, role_name=None),
  ]
}

#level up announcement settings
embed = discord.Embed()
embed.set_author(name=LevelUpAnnouncement.Member.name, icon_url=LevelUpAnnouncement.Member.avatar_url)
embed.description = f'{LevelUpAnnouncement.Member.mention} has leveled up! Current Level: {LevelUpAnnouncement.LEVEL}'

# the announcement
announcement = LevelUpAnnouncement(embed, level_up_channel_ids=[1522416390555045888])

# level up system set up then connecting to database
lvl = DiscordLevelingSystem(awards=My_Awards, level_up_announcement=announcement)
lvl.connect_to_database_file(r'/home/themoon40/PycharmProjects/my-bot/DiscordLevelingSystem.db')


#giving out xp on message excluding the bot
@bot.event
async def on_message(message):
  if message.author != bot.user:
    await bot.process_commands(message)
    await lvl.award_xp(amount=15, message=message)
  else:
    return

# command for level and xp check and leaderboard

@bot.command(help="Check your current level")
async def rank(ctx):
  data = await lvl.get_data_for(ctx.author)
  await ctx.send(f'You are level {data.level} with {data.xp} xp')

@bot.command(help="Show the top 10 users by rank", aliases=['lb'])
async def leaderboard(ctx):
  data = await lvl.each_member_data(ctx.guild, sort_by='rank', limit=10)
  leaderboard = "Top Members:\n"
  for rank, member in enumerate(data):
    leaderboard += f"{rank}. {member.name} - Level: {member.level} \n"

  await ctx.send(leaderboard)


#games



#RPS

@bot.command(help="Play rock paper scissors against the Bot")
async def rps(ctx, choice: str):
  choices = ['rock', 'paper', 'scissors']
  if choice not in choices:
      await ctx.send("Please choose rock, paper, or scissors.")
      return

  bot_choice = random.choice(choices)
  result = RPS_win(choice, bot_choice)

  await ctx.send(f"You picked {choice}, Moon bot picked {bot_choice}. {result}")

  if result == "Player wins! Awarded 15xp!":
    await lvl.add_xp(member=ctx.author, amount=15)


def RPS_win(player_choice, bot_choice):
  if player_choice == bot_choice:
    return "It's a Tie!"
  elif (player_choice == 'rock' and bot_choice == 'scissors') or (player_choice == 'paper' and bot_choice == 'rock') or (player_choice == 'scissors' and bot_choice == 'paper'):
    return "Player wins! Awarded 15xp!"
  else:
    return "Moon Bot Wins"








#Tic Tac Toe

#button logic

class TicTacToeButton(discord.ui.Button['TicTacToe']):
  def __init__(self, x: int, y: int):
    super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
    self.x = x
    self.y = y

# Game logic
  async def callback(self, interaction: discord.Interaction):
    assert self.view is not None
    view: TicTacToe = self.view


    if interaction.user not in (view.players_x, view.players_o):
      return await interaction.response.send_message("Your not in this game!", ephemeral=True)

    if view.current_player == view.X and interaction.user != view.players_x:
      return await interaction.response.send_message("It's not your turn!", ephemeral=True)

    if view.current_player == view.O and interaction.user != view.players_o:
      return await interaction.response.send_message("It's your turn!", ephemeral=True)




    state = view.board[self.y][self.x]
    if state in (view.X, view.O):
      return

    if view.current_player == view.X:
      self.style = discord.ButtonStyle.danger
      self.label = 'X'
      self.disabled = True
      view.board[self.y][self.x] = view.X
      view.current_player = view.O
      content = "It's now O's Turn"

    else:
      self.style = discord.ButtonStyle.success
      self.label = 'O'
      self.disabled = True
      view.board[self.y][self.x] = view.O
      view.current_player = view.X
      content = "It's now X's Turn"

    winner = view.check_board_winner()
    if winner is not None:
      if winner == view.X:
        content = "X won!"
      elif winner == view.O:
        content = "O won!"
      else:
        content = "Tie!"

      for child in view.children:
        child.disabled = True


      view.stop()

    await interaction.response.edit_message(content=content, view=view)

#board

class TicTacToe(discord.ui.View):
  children: List[TicTacToeButton]
  X = -1
  O = 1
  def __init__(self,player_x: discord.Member, player_o: discord.Member):
    super().__init__()
    self.Tie = 0
    self.players_x = player_x
    self.players_o = player_o

    self.current_player = self.X
    self.board =[
        [0,0,0],
        [0,0,0],
        [0,0,0],
      ]

    for x in range(3):
      for y in range(3):
        self.add_item(TicTacToeButton(x, y))

  def check_board_winner(self):
    for across in self.board:
      value = sum(across)
      if value == 3:
        return self.O
      elif value == -3:
        return self.X
      elif all(i != 0 for row in self.board for i in row):
        return self.Tie

    #vertical lines

    for line in range(3):
      value = self.board[0][line] + self.board[1][line] + self.board[2][line]
      if value == 3:
        return self.O
      elif value == -3:
        return self.X


    #diagonal lines

    diag = self.board[0][2] + self.board[1][1] + self.board[2][2]
    if diag == 3:
      return self.O
    elif diag == -3:
      return self.X

    diag = self.board[0][0] + self.board[1][1] + self.board[2][0]
    if diag == 3:
      return self.O
    elif diag == -3:
      return self.X



    return None

#game command
@bot.command()
async def tic(ctx: commands.Context, opponent: discord.Member):
  if opponent == bot.user:
    return await ctx.send("The Bot can't play")

  player_x = ctx.author
  player_o = opponent

  if random.choice([True, False]):
    player_x, player_o = player_o, player_x

  starter = player_x
  view = TicTacToe(player_x=player_x, player_o=player_o)

  await ctx.send(f"Tic Tac Toe: {starter.mention} goes first!", view=view)


@tic.error
async def tic_error(ctx: commands.Context, error:commands.CommandError):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please @ the other player")
    return

#end of tic tac toe






#bot key and run
Discord_token = os.getenv('D_TOKEN')

bot.run(Discord_token)
