from asyncio.tasks import sleep
import os
import discord
from discord.colour import Color
from discord.ext import commands
from dotenv import load_dotenv
import supportApi
from tmdb import getMovieSummary
import tmdb

discordToken = os.getenv("discordToken")
load_dotenv()
bot=commands.Bot(command_prefix="~")
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='help')
async def help(ctx):
    await ctx.send('help')
    embed=discord.Embed(
        title='StageHand Help Page',
        color=discord.Color.blue(),
        description="ALWAYS PUT NAMES OF ANY TYPE IN QUOTATION MARKS"
    )
    embed.add_field(name="~begin '{movie name}'",value='This command will give you a small list of data right before your movie starts It also puts everyone on mute so as to prevent any disturbance during your movie watching experience',inline=False)
    embed.add_field(name="~interval ",value='This command will unmute everyone in the middle of the movie so as to allow a small break',inline=False)
    embed.add_field(name="~end",value='This command is similar to the interval command',inline=False)
    embed.add_field(name="~compare '{movie name 1}' and '{movie name 2}'",value='Compares and throws back ratings for the two mentioned movies',inline=False)
    embed.add_field(name="~summary '{movie name}'",value="Provides summary for the movie",inline=False)
    embed.add_field(name="~director '{movie name}'",value="Get director of movie",inline=False)
    embed.add_field(name="~cast '{movie name}'",value='Shows the top 12 cast members from the film',inline=False)
    embed.add_field(name="~actor '{actor name}'",value='Shows the awards, films starred in and a small paragraph about the actor',inline=False)
    embed.add_field(name="~choose",value="Can't decide which movie to watch pop in your three top options and let the people decide. Watch a movie that is for the people, by the people and with the people. Pass in the three top choices comma seperated",inline=False)
    embed.add_field(name="~timetravel",value='Unmutes the author so as to request skipping forward or rewinding It then sends a poll asking everyone if they would like to "time travel" through the movie. ',inline=False)
    embed.add_field(name="~info",value="Get github repo and publish issues",inline=False)
    await ctx.send(embed=embed)

@bot.command(name='info')
async def info(ctx):
    embedInfo=discord.Embed(
        title='StageHand Info',
        color=discord.Color.orange(),
        description='[Github Repo](https://github.com/CoHansLanda/discord-bot-main)\n[Issues](https://github.com/CoHansLanda/discord-bot-main/issues)'
    )
    await ctx.send(embed=embedInfo)

@bot.command(name='mute')
async def mute(ctx,member: discord.Member):
    print('mute')
    try:
        await member.edit(mute=True)
    except Exception as e:
        await ctx.send('Looks like something went wrong :[')
        print(e)

@bot.command(name='unmute')
async def unmute(ctx,member: discord.Member):
    try:
        print('unmute')
        await member.edit(mute=False)
    except Exception as e:
        await ctx.send('Looks like something went wrong :[')
        print(e)

@bot.command(name='begin')
async def movieBegin(ctx,*,args):
    try:
        print("beginning movie")
        guild=ctx.guild
        memberList=guild.members
        for i in memberList:
            if(i.bot):
                pass
            else:
                print(i)
                await mute(ctx,i)
        movie=''.join(args)
        movie=movie[1:-1]
        dump=tmdb.getMovieInfo(movie)
        movieInfo=discord.Embed(
            title=movie,
            color=discord.Color.blue()
        )
        tagline=dump['tagline']
        popularity=dump['popularity']
        ratings=dump['ratings']
        movieInfo.add_field(name='Tagline',value=tagline,inline=False)
        for i in dump['genres']:
            genre=i['name']
            movieInfo.add_field(name='Genre',value=genre)
        movieInfo.add_field(name='Popularity:',value=popularity)
        movieInfo.add_field(name='Ratings',value=ratings)
        await ctx.send(embed=movieInfo)
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
        print('Exception:'+e)
        pass

@bot.command(name='interval')
async def endMovie(ctx):
    try:
        print('interval')
        guild=ctx.guild
        memberList=guild.members
        memberList.append(ctx.message.author)
        for i in memberList:
            print(i)
            if(i.bot):
                pass
            else:
                await unmute(ctx,i)
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
        print(e)
        pass

@bot.command(name='end')
async def endMovie(ctx):
    try:
        print('end')
        guild=ctx.guild
        memberList=guild.members
        memberList.append(ctx.message.author)
        for i in memberList:
            if(i.bot):
                pass
            else:
                await unmute(ctx,i)
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
        print(e)
        pass


@bot.command(name='compare')
async def compareBetween(ctx,*args):
    try:
        print('compare')
        arg=''.join(args)
        movie1=arg[:arg.index('and')]
        movie2=arg[arg.index('and')+3:]
        await ctx.send('Comparing between {} and {}'.format(movie1,movie2))
        await ctx.send('Working on the ratings....')
        ratingsMovie1=supportApi.getMovieRatings(movie1)
        ratingsMovie2=supportApi.getMovieRatings(movie2)
        await ctx.send("Ratings for {}\nIMDb:{}\tRotten Tomatoes:{}\n".format(movie1,ratingsMovie1["IMDb"],ratingsMovie1["Rotten Tomatoes"]))
        await ctx.send("Ratings for {}\nIMDb:{}\tRotten Tomatoes:{}\n".format(movie2,ratingsMovie2["IMDb"],ratingsMovie2["Rotten Tomatoes"]))
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
        print(e)
        pass

@bot.command(name='summary')
async def getMovieInfo(ctx,*,args):
    try:
        print('summary')
        movie=''.join(args)
        movie=movie[1:-1]
        await ctx.send("Working on getting the summary.....")
        Summary=getMovieSummary(movie)
        await ctx.send("Summary for {}:\n{}".format(movie,Summary))
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
        print(e)
        pass

@bot.command(name='director')
async def getDir(ctx,*,args):
    try:
        print('director')
        movie=''.join(args)
        movie=movie[1:-1]
        await ctx.send("Working on getting the director.....")
        await ctx.send("Director of {}:{}".format(movie,supportApi.getDirector(movie)))
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
        print(e)
        pass

@bot.command(name='cast')
async def getCast(ctx,*,args):
    try:
        print('cast')
        movie=''.join(args)
        movie=movie[1:-1]
        await ctx.send("Working on getting the cast........")
        cast=supportApi.getCast(movie)
        await ctx.send("Cast of {}:\n".format(movie))
        for i in range(12):
            await ctx.send("{} : {}".format(cast[i]['name'],cast[i].currentRole))
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
        print(e)
        pass
@bot.command(name='actor')
async def actorInfo(ctx,*,args):
    try:
        print('actor')
        actor=''.join(args)
        actor=actor[1:-1]
        await ctx.send("Researching on {}......".format(actor))
        dump=supportApi.getActorDet(actor)
        await ctx.send("Biography:\n{}".format(dump['bio']))
        await ctx.send("Films:")
        for i in dump['films']:
            await ctx.send(i)
        await ctx.send("Awards:")
        for i in range(10):
            await ctx.send('{} for {} from {} for the film {}'.format(dump['awards'][i]['result'],dump['awards'][i]['category'],dump['awards'][i]['award'],dump['awards'][i]['movies']['title']))
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
        print('Exception')
        print(e)
    except (ImportError,ImportWarning) as e:
        print('Import error')
        print(e)
    except (KeyError) as e:
        print('key error')
        print(e)

@bot.command(name='timetravel')
async def timeTravel(ctx):
    try:
        print('time travel')
        await unmute(ctx,ctx.message.author)
        msg=await ctx.send('Time Travel?')
        reactionYes="✅"
        reactionNo="❎"
        await msg.add_reaction(reactionYes)
        await msg.add_reaction(reactionNo)
        print("Sleeping")
        await sleep(10)
        newMsg=await fetchMessage(ctx,msg.id)
        react=newMsg.reactions
        print(react)
        reactionYesCount=react[0].count
        reactionNoCount=react[1].count
        await mute(ctx,ctx.message.author)
        if(reactionYesCount>reactionNoCount):
            await ctx.send('Time travel confirmed @everyone')
        else:
            await ctx.send('Time travel ignored @everyone\n@{} better ask someone what just happened'.format(ctx.message.author))
    except Exception as e:
        await ctx.send("Looks like something went wrong check back after a few mins :(")
        print(e)
        pass

@bot.command(name='choose')
async def choosePoll(ctx,*,args):
    try:
        print('Choosing')
        movies=''.join(args)[1:-1].split(',')
        chooseEmbed=discord.Embed(
            title='Choose Movie',
            color=discord.Color.purple(),
            description="Let's choose between the two movies"
        )
        for movie in movies:
            chooseEmbed.add_field(name=movie,value=getMovieSummary(movie),inline=True)
        msg=await ctx.send(embed=chooseEmbed)
        reaction1="1️⃣"
        reaction2="2️⃣"
        reaction3="3️⃣"
        await msg.add_reaction(reaction1)
        await msg.add_reaction(reaction2)
        await msg.add_reaction(reaction3)
        print('Sleeping')
        await sleep(10)
        newMsg=await fetchMessage(ctx,msg.id)
        react=newMsg.reactions
        reactCount=[[movies[0],react[0].count],[movies[1],react[1].count],[movies[2],react[2].count]]
        reactCount.sort(key=lambda x:x[1])
        await ctx.send('Looks like the public vote is to watch {}'.format(reactCount[2][0]))
        print(reactCount)
        dump=tmdb.getMovieInfo(reactCount[2][0])
        movieInfo=discord.Embed(
            title=reactCount[2][0],
            color=discord.Color.blue()
        )
        tagline=dump['tagline']
        popularity=dump['popularity']
        ratings=dump['ratings']
        movieInfo.add_field(name='Tagline',value=tagline,inline=False)
        for i in dump['genres']:
            genre=i['name']
            movieInfo.add_field(name='Genre',value=genre)
        movieInfo.add_field(name='Popularity:',value=popularity)
        movieInfo.add_field(name='Ratings',value=ratings)
        await ctx.send(embed=movieInfo)
    except Exception as e:
        print('Exception')
        print(e)

@bot.command()
async def fetchMessage(ctx,msgID):
    msg=await ctx.fetch_message(msgID)
    return msg

bot.run("ODQzNzYxNzY4MzcxMDYwNzU2.Guc0Rz.hOn42LUMBg60ZYx_b4Tgj6WLYnzXU6D-yRSBBg")