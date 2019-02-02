import asyncio
import sys

import discord
from discord.ext import commands
from mainconf import BOTDEVS

COLOR = 0x00ff00


class Testing:

    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def placeholder(self, ctx):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        embed = discord.Embed(
            title="Temporary", description="Coming Soon! :tools:", color=COLOR)
        embed.set_footer(text="Requested by {}".format(discord.utils.get(
            self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["rl"])
    @commands.is_owner()
    async def reload(self, ctx, extension: str):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        try:
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await ctx.send('Failed to reload extension {}\n{}'.format(extension, exc))
            return False

        embed = discord.Embed(
            title="Reloader", description="{} reloaded".format(extension), color=COLOR)
        await ctx.send(embed=embed)
        await ctx.invoke(self.clearconsole)
        print("Reloaded {}".format(extension))
        return True

    @commands.command(pass_context=True, aliases=["ll"])
    @commands.is_owner()
    async def load(self, ctx, extension: str):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        try:
            self.bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await ctx.send('Failed to load extension {}\n{}'.format(extension, exc))
            return False

        embed = discord.Embed(
            title="Reloader", description="{} loaded".format(extension), color=COLOR)
        await ctx.send(embed=embed)
        await ctx.invoke(self.clearconsole)
        print("Loaded {}".format(extension))
        return True

    @commands.command(pass_context=True, aliases=["ul"])
    @commands.is_owner()
    async def unload(self, ctx, extension: str):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        try:
            self.bot.unload_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await ctx.send('Failed to unload extension {}\n{}'.format(extension, exc))
            return False

        embed = discord.Embed(
            title="Reloader", description="{} unloaded".format(extension), color=COLOR)
        await ctx.send(embed=embed)
        await ctx.invoke(self.clearconsole)
        print("Unloaded {}".format(extension))
        return True

    @commands.command(pass_context=True, aliases=["cc"])
    @commands.is_owner()
    async def clearconsole(self, ctx):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        for i in range(50):
            print("")
        embed = discord.Embed(title="Console Cleaner",
                              description="Console cleared", color=COLOR)
        await ctx.send(embed=embed)
        print("Cleared console")
        return True

    @commands.command(pass_context=True, aliases=["sb"])
    @commands.is_owner()
    async def stopbot(self, ctx):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        await ctx.send("Stopping Bot")
        sys.exit(1)


def setup(bot):
    bot.add_cog(Testing(bot))
