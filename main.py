import json
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

@bot.command(name='begin')
async def movieBegin(ctx,*,args):
    try:
        movie=''.join(args)
        movie=movie[1:-1]
        await ctx.send('HAVE FUN WATCHING {}'.format(movie))
        jsonDump=webScrape.getInfo(movie)
        await ctx.send("Runtime: {} minutes\nRatings: {}\nAspect Ratio: {}\nBox Office Gross: {}".format(jsonDump['runtime'],jsonDump['ratings'],jsonDump['aspect ratio'],jsonDump['gross']))
        await ctx.send("Genre:\n")
        for i in jsonDump['genre']:
            await ctx.send('\t-'+i)
    except:
        await ctx.send("Looks like something went wrong check back after a few mins :(")


@bot.command(name='compare')
async def compareBetween(ctx,*args):
    try:
        arg=''.join(args)
        movie1=arg[:arg.index('and')]
        movie2=arg[arg.index('and')+3:]
        await ctx.send('Comparing between {} and {}'.format(movie1,movie2))
        await ctx.send('Working on the ratings....')
        ratingsMovie1=webScrape.getMovieRatings(movie1)
        ratingsMovie2=webScrape.getMovieRatings(movie2)
        await ctx.send("Ratings for {}\nIMDb:{}\tRotten Tomatoes:{}\n".format(movie1,ratingsMovie1["IMDb"],ratingsMovie1["Rotten Tomatoes"]))
        await ctx.send("Ratings for {}\nIMDb:{}\tRotten Tomatoes:{}\n".format(movie2,ratingsMovie2["IMDb"],ratingsMovie2["Rotten Tomatoes"]))
    except:
        await ctx.send("Looks like something went wrong check back after a few mins :(")



@bot.command(name='summary')
async def getMovieInfo(ctx,*,args):
    try:
        movie=''.join(args)
        movie=movie[1:-1]
        await ctx.send("Working on getting the summary.....")
        Summary=webScrape.getMovieInfo(movie)
        await ctx.send("Summary for {}:\n{}".format(movie,Summary))
    except:
        await ctx.send("Looks like something went wrong check back after a few mins :(")


@bot.command(name='director')
async def getDir(ctx,*,args):
    try:
        movie=''.join(args)
        movie=movie[1:-1]
        await ctx.send("Working on getting the director.....")
        await ctx.send("Director of {}:{}".format(movie,webScrape.getDirector(movie)))
    except:
        await ctx.send("Looks like something went wrong check back after a few mins :(")

@bot.command(name='cast')
async def getCast(ctx,*,args):
    try:
        movie=''.join(args)
        movie=movie[1:-1]
        await ctx.send("Working on getting the cast........")
        cast=webScrape.getCast(movie)
        await ctx.send("Cast of {}:\n".format(movie))
        for i in range(12):
            await ctx.send("{} : {}".format(cast[i]['name'],cast[i].currentRole))
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
@bot.command(name='actor')
async def actorInfo(ctx,*,args):
    try:
        actor=''.join(args)
        actor=actor[1:-1]
        await ctx.send("Researching on {}......".format(actor))
        dump=webScrape.getActorDet(actor)
        await ctx.send("Films:")
        for i in range(5):
            await ctx.send(dump['films']['actor'][i]['title'])
        await ctx.send("Awards:")
        for i in range(10):
            await ctx.send('{} for {} from {} for the film {}'.format(dump['awards'][i]['result'],dump['awards'][i]['category'],dump['awards'][i]['award'],dump['awards'][i]['movies']['title']))
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
        print(e)
        pass

bot.run(discordToken)