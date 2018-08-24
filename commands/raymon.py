import asyncio

import discord
from discord.ext import commands


class Raymon:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def raymon(self, ctx):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        ctx.send("Raymon is n00b")


def setup(bot):
    bot.add_cog(Raymon(bot))
