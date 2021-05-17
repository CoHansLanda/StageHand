import os
import discord
from discord import channel
from discord import guild
from discord.ext import commands
from discord.ext.commands.core import bot_has_permissions
from discord.role import Role
import requests


response=requests.get("")



tmdbToken=os.environ.get('TMDN_API_KEY')
discordToken=os.environ.get('DISCORD_API_KEY')
client=discord.Client()
bot=commands.Bot(command_prefix="~")

@bot.command()
async def on_ready():
    print('ready')

@commands.has_permissions(manage_messages=True)
@bot.command(name='begin')
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
    
    
# @bot.command()
# async def test(ctx, *args):

# async def beginMovieMessage(ctx,* ,arg1):
#     await ctx.send("HEY THE MOVIE HAS BEGUN ENJOY {} @everyone".format(arg1))







bot.run(discordToken)