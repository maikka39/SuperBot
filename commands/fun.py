import asyncio
import datetime
import random
import secrets
import sys

import discord
from discord.ext import commands

COLOR = 0xff6d00


class Fun:

    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        embed = discord.Embed(
            title="Ping Pong", description="Pong :ping_pong:", color=COLOR)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def roll(self, ctx):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        # Send a message with a pseudo-random number
        embed = discord.Embed(title="Roll a Dice", description=ctx.message.author.mention +
                              " rolled a **" + str(random.randint(1, 6)) + "**!", color=COLOR)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def troll(self, ctx):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        # Send a message with a "real" random number
        embed = discord.Embed(title="Roll a Dice", description=ctx.message.author.mention +
                              " rolled a **" + str(secrets.randbelow(6) + 1) + "**!", color=COLOR)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def time(self, ctx):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        # Send a message with a "real" random number
        embed = discord.Embed(title="Tell the Time", description="The current time is " +
                              str(datetime.datetime.utcnow().time())[:-7] + " UTC", color=COLOR)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
