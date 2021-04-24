import logging
import os
import sys
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


print("Starting bot...")
bot = commands.Bot(command_prefix=os.environ["COMMAND_PREFIX"])

initial_extensions = [
    "fun",
    "staff",
    "info",
    "gameinfo",
    "music",
    "testing",
    "dictionary",
]


@bot.event
async def on_ready():
    activity = discord.Activity(name="commands", type=2)
    await bot.change_presence(status=discord.Status.online, activity=activity)

    print(bot.user.name + " is running")


if __name__ == "__main__":
    # This allows the cogs in the commands folder to be loaded
    sys.path.insert(1, os.getcwd() + "/commands/")

    bot.remove_command("help")

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(os.environ["TOKEN"])
