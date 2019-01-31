import asyncio

import discord
from discord.ext import commands

COLOR = 0xffffff


class Dictionary:

    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot

    @commands.command(pass_context=True, aliases=["dictionary", "define", "def", "meaning"])
    async def dict(self, ctx, word):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        embed = discord.Embed(
            title="Dictionary", description="Coming Soon! :tools:", color=COLOR)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Dictionary(bot))
