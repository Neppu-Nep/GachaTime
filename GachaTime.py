import os
import json

import discord
from discord.ext import commands
    
with open("config.json", "r") as infile:
    config = json.load(infile)

def get_prefix(bot, message):

    prefixes = config['prefix']
    return commands.when_mentioned_or(*prefixes)(bot, message)

module_list = os.listdir(str(os.getcwd()) + "\\modules")
modules = ["modules." + module.split(".py")[0] for module in module_list if ".py" in module]

bot = commands.Bot(command_prefix=get_prefix, description='Plutia Bot')

@bot.event
async def on_ready():

    print(f'\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    bot.remove_command("help")
    for module in modules:
        bot.load_extension(module)

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Gacha Games"))
    print(f'Successfully logged in and booted...!')

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments. Try again.")

    elif isinstance(error, commands.BadArgument):
        await ctx.send("Wrong Usage. Use help to check usage.") 

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Permission Missing.") 

    else:
        print("Error")
        print(error)

bot.run(config['token'], bot=True, reconnect=True)
