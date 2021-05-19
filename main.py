import os
import discord
from discord import channel
from discord import guild
from discord.ext import commands
from discord.ext.commands.core import bot_has_permissions
from discord.role import Role
import webScrape

discordToken=os.environ.get('DISCORD_API_KEY')
client=discord.Client()
bot=commands.Bot(command_prefix="~")

@bot.command()
async def on_ready():
    print('ready')

@commands.has_permissions(manage_messages=True)
@bot.command(name='Movie begin')
async def join(ctx,member:discord.Member):
    channel=ctx.author.voice.channel
    await channel.connect()
    Guild=ctx.guild
    mutedRole=discord.utils.get(Role.name,name="MUTED")

    if not mutedRole:
        mutedRole=await guild.create_role(name="MUTED")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole,speak=False, send_messages=True,read_message_history=True, read_messages=True)
    await member.add_roles(mutedRole,reason=None)
    await ctx.send("you have been muted {}".format(member))

@bot.command(name='compare')
async def compareBetween(ctx,*args):
    arg=''.join(args)
    movie1=arg[:arg.index('and')]
    movie2=arg[arg.index('and')+3:]
    await ctx.send('Comparing between {} and {}'.format(movie1,movie2))
    await ctx.send('Working on the ratings....')
    ratingsMovie1=webScrape.getMovieRatings(movie1)
    ratingsMovie2=webScrape.getMovieRatings(movie2)
    await ctx.send("Ratings for {}\nIMDb:{}\tRotten Tomatoes:{}\n".format(movie1,ratingsMovie1["IMDb"],ratingsMovie1["Rotten Tomatoes"]))
    await ctx.send("Ratings for {}\nIMDb:{}\tRotten Tomatoes:{}\n".format(movie2,ratingsMovie2["IMDb"],ratingsMovie2["Rotten Tomatoes"]))

@bot.command(name='Begin Movie')
async def beginMovieMessage(ctx,* ,arg1):
    await ctx.send("HEY THE MOVIE HAS BEGUN ENJOY {} @everyone".format(arg1))

@bot.command(name='summary')
async def getMovieInfo(ctx,*,args):
    movie=''.join(args)
    movie=movie[1:len(movie)-1]
    await ctx.send("Working on getting the summary.....")
    Summary=webScrape.getMovieInfo(movie)
    await ctx.send("Summary for {}:\n{}".format(movie,Summary))

@bot.command(name='director')
async def getDir(ctx,*,args):
    movie=''.join(args)
    movie=movie[1:len(movie)-1]
    await ctx.send("Working on getting the director.....")
    await ctx.send("Director of {}:{}".format(movie,webScrape.getDirector(movie)))





bot.run(discordToken)