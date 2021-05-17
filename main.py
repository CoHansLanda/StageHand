import os
import discord
from discord import channel
from discord.ext import commands
from discord.ext.commands.core import bot_has_permissions
token=os.environ.get('DISCORD_API_KEY')
client=discord.Client()
bot=commands.Bot(command_prefix="~")
@bot.command()
async def on_ready():
    print('ready')
@bot.command(name='begin')
async def beginMovieMessage(ctx,* ,arg1):
    await ctx.send("HEY THE MOVIE HAS BEGUN ENJOY {} @everyone".format(arg1))


bot.run(token)