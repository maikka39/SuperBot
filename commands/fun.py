import asyncio
import datetime
import random
import secrets
import sys
from commands.lib.other import safe_get_list

import discord
import praw
from discord.ext import commands
from mainconf import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from pythonping import ping

COLOR = 0xff6d00


class Fun:

    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        embed = discord.Embed(
            title="Ping Pong", description=str("Pong :ping_pong: \n\n Response took `{0}ms`".format(round(self.bot.latency * 1000, 1))), color=COLOR)
        embed.set_footer(text="Requested by {}".format(discord.utils.get(
            self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def roll(self, ctx):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        # Send a message with a pseudo-random number
        embed = discord.Embed(title="Roll a Dice", description=ctx.message.author.mention +
                              " rolled a **" + str(random.randint(1, 6)) + "**!", color=COLOR)
        embed.set_footer(text="Requested by {}".format(discord.utils.get(
            self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def troll(self, ctx):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        # Send a message with a "real" random number
        embed = discord.Embed(title="Roll a Dice", description=ctx.message.author.mention +
                              " rolled a **" + str(secrets.randbelow(6) + 1) + "**!", color=COLOR)
        embed.set_footer(text="Requested by {}".format(discord.utils.get(
            self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def time(self, ctx):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        embed = discord.Embed(title="Tell the Time", description="The current time is " +
                              str(datetime.datetime.utcnow().time())[:-7] + " UTC", color=COLOR)
        embed.set_footer(text="Requested by {}".format(discord.utils.get(
            self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["memes"])
    async def meme(self, ctx):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        embed = discord.Embed(
            title="Memes", description="Best memes of today:", color=COLOR)
        await ctx.send(embed=embed)

        subreddit = self.reddit.subreddit("memes")
        for submission in subreddit.top(time_filter="day", limit=5):
            await ctx.send(embed=discord.Embed(color=COLOR).set_image(url=submission.url))

        embed = discord.Embed(description="Check back tomorrow!", color=COLOR)
        embed.set_footer(text="Requested by {}".format(discord.utils.get(
            self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
