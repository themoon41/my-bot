import asyncio
import json
import random
import discord
import requests
from discord.ext import commands
import os
from dotenv import load_dotenv


intents = discord.Intents.default()
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!',intents=intents)
client = discord.Client(intents=intents)



#Bot working test

@bot.event
async def on_ready():
  print(f'Systems Online as: {bot.user}')
  await bot.get_channel(1521809052555022369).send(f'{bot.user} Is Online.')

@bot.event
async def on_member_join(member):
  await member.send("Welcome!".format(member.mention))




#Basic bot commands

@bot.command(help='say hi.')
async def hello(ctx):
  await ctx.send("hi {0}".format(ctx.author.mention))

@bot.command(help='test')
async def test(ctx):
  await ctx.send('test worked')


  
  # Level Up system






# Tic Tac Toe

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


@bot.command(help= "Play tic tac toe with someone")
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

    # pirnt the board
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
      await bot.get_channel.send("It is <@" + str(player1.id) + ">'s turn.")
    elif num == 2:
      turn = player2
      await bot.get_channel.send("It is <@" + str(player2.id) + ">'s turn.")
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
    await ctx.send("Make should you put a number.")

#end of tic-tac-toe



Discord_token = os.getenv('D_TOKEN')

bot.run(Discord_token)
