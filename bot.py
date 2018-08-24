# import asyncio
import logging
import os
import sys

import discord
from discord.ext import commands

from mainconf import TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


print("Starting bot...")
bot = commands.Bot(command_prefix='-')

initial_extensions = [
    "fun",
    "staff",
    "info",
    "gameinfo",
    "music",
    "testing",
]


@bot.event
async def on_ready():
    activity = discord.Activity(name="commands", type=2)
    await bot.change_presence(status=discord.Status.online, activity=activity)

    bot.remove_command("help")

    print(bot.user.name + " is running")


if __name__ == "__main__":
    # This allows the cogs in the commands folder to be loaded
    sys.path.insert(1, os.getcwd() + "/commands/")

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(TOKEN)
