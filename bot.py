import asyncio
import random
from encodings.aliases import aliases

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
  embed = discord.Embed(
    title="Bot Stuff Server",
    description="Rules",
    color=discord.Color.purple()
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
async def rps(ctx, choice: str, message):
  choices = ['rock', 'paper', 'scissors']
  if choice not in choices:
      await ctx.send("Please choose rock, paper, or scissors.")
      return

  bot_choice = random.choice(choices)
  result = RPS_win(choice, bot_choice)

  if result != "Player wins! Awarded 15xp!":
    await ctx.send(f"You picked {choice}, Moon bot picked {bot_choice}. {result}")
  elif result == "Player wins! Awarded 15xp!":
    await ctx.send(f"You picked {choice}, Moon bot picked {bot_choice}. {result}")


def RPS_win(player_choice, bot_choice):
  if player_choice == bot_choice:
    return "It's a Tie!"
  elif (player_choice == 'rock' and bot_choice == 'scissors') or (player_choice == 'paper' and bot_choice == 'rock') or (player_choice == 'scissors' and bot_choice == 'paper'):
    return "Player wins! Awarded 15xp!"
  else:
    return "Moon Bot Wins"











#Tic Tac Toe

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []


winningConditions = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [8, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6]
]


@bot.command(help= "Play tic tac toe with someone", aliases=['ttt'])
async def tictac(ctx, p1 : discord.Member, p2 : discord.Member):
  global player1
  global player2
  global turn
  global gameOver
  global count

  if gameOver:
    global board
    board = [":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:"]
    turn = ""
    gameOver = False
    count = 0

    player1 = p1
    player2 = p2

    # print the board
    line = ""
    for x in range(len(board)):
      if x == 2 or x ==  5 or x == 8:
        line += " " + board[x]
        await bot.get_channel(1521809344121933875).send(line)
        line = ""

      else:
        line += " " + board[x]

    # who goes first
    num = random.randint(1, 2)
    if num == 1:
      turn = player1
      await bot.get_channel(1521809344121933875).send("It is <@" + str(player1.id) + ">'s turn.")
    elif num == 2:
      turn = player2
      await bot.get_channel(1521809344121933875).send("It is <@" + str(player2.id) + ">'s turn.")
    else:
      await ctx.send("There is already a game in progress! Please wait until it is finished")


@bot.command(help="Used to place marker tic tac toe.")
async def p(ctx, pos : int):
  global turn
  global player1
  global player2
  global board
  global count
  
  if not gameOver:
    mark = ""
    if turn == ctx.author:
      if turn == player1:
       mark = ":regional_indicator_x:"
      elif turn == player2:
        mark = ":o2:"
      if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
        board[pos - 1] = mark
        count += 1

        #print board again
        line = ""
        for x in range(len(board)):
          if x == 2 or x ==  5 or x == 8:
           line += " " + board[x]
           await bot.get_channel(1521809344121933875).send(line)
           line = ""
          else:
            line += " " + board[x]

        checkWinner(winningConditions, mark)
        print(count)
        if count >= 9:
          await bot.get_channel(1521809344121933875).send("It's a tie")
        elif gameOver == True:
          await ctx.send(mark + "wins!")
        

        # switching turns
        elif turn == player1:
          turn = player2
          await bot.get_channel(1521809344121933875).send("It's now <@" + str(player2.id) + ">'s turn.")
        elif turn == player2:
          turn = player1
          await bot.get_channel(1521809344121933875).send("It's now <@" + str(player1.id) + ">'s turn.")
    


      else:
        await bot.get_channel(1521809344121933875).send("Pick a number between 1 and 9 (inclusive) and a unmarked title.")
    else:
      await bot.get_channel(1521809344121933875).send("Please wait for your turn.")
  else:
    await bot.get_channel(1521809344121933875).send("Start a game using !tictac.")




  
def checkWinner(winningConditions, mark):
  global gameOver
  for condition in winningConditions:
   if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark or count >= 9:
     gameOver = True


@tictac.error
async def tictac_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Mention 2 players for this game.")
  elif isinstance(error, commands.BadArgument):
    await ctx.send("Make sure you @ message another player.")

@p.error
async def place_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Enter position you would like to place a marker.")
  elif isinstance(error, commands.BadArgument):
    await ctx.send("Make sure you put a number.")

#end of tic-tac-toe



Discord_token = os.getenv('D_TOKEN')

bot.run(Discord_token)
