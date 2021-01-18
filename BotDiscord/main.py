import discord
from configparser import ConfigParser
from discord.ext import commands

file= "settings.ini"
config=ConfigParser()
config.read(file)

bot=commands.Bot(command_prefix='>')

@bot.event
async def on_member_join(member):
    await member.send('Hola,Puto')

@bot.command()
async def definir_futuro(ctx):
    await ctx.send('David será un wen ingeniero')

@bot.command()
async def sumar(ctx,numOne:int, numTwo:int):
    await ctx.send("El resultado de la suma es:",numOne+numTwo)

bot.run(config['key']['public_key'])
