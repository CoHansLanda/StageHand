from asyncio.tasks import sleep
import os
import discord
from discord.ext import commands
import supportApi
from tmdb import getMovieSummary
import tmdb

discordToken=os.environ.get('DISCORD_API_KEY')
client=discord.Client()
bot=commands.Bot(command_prefix="~")
bot.remove_command('help')

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
        print(type(react))
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
@bot.command()
async def fetchMessage(ctx,msgID):
    msg=await ctx.fetch_message(msgID)
    return msg

bot.run(discordToken)