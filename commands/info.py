import asyncio
import sys

import discord
from discord.ext import commands

COLOR = 0x64dd17


class Info:

    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot

    @commands.command(pass_context=True)
    async def info(self, ctx, user: discord.Member = None):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        if user is None:
            user = ctx.message.author

        embed = discord.Embed(title="{}'s info".format(
            user.name), description="Here's what I could find about " + user.mention + ".", color=COLOR)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=str(
            user.status).title(), inline=True)
        embed.add_field(name="Highest role", value=user.top_role)
        # embed.add_field(name="Joined", value=str(user.joined_at)[:-7])
        embed.add_field(name="Joined", value=str(user.joined_at)[:-16])
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        embed = discord.Embed(name="{}'s info".format(
            ctx.message.guild.name), description="Here's what I could find.", color=COLOR)
        embed.set_author(name=ctx.message.guild.name)
        embed.add_field(name="Name", value=ctx.message.guild.name, inline=True)
        embed.add_field(name="ID", value=ctx.message.guild.id, inline=True)
        embed.add_field(name="Roles", value=len(
            ctx.message.guild.roles), inline=True)
        embed.add_field(name="Members", value=len(ctx.message.guild.members))
        embed.set_thumbnail(url=ctx.message.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["bot"])
    async def botinfo(self, ctx):
        bot_id = 459079947219107860

        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        embed = discord.Embed(
            name="My info", description="Here's what I could find about myself.", color=COLOR)
        embed.add_field(name="Name", value="<@{}>".format(bot_id), inline=True)
        embed.add_field(
            name="Creator", value="<@273161070103887872>", inline=True)
        embed.add_field(name="Aviable Since", value="2018-02-12", inline=True)
        embed.add_field(name="Written In", value="Python", inline=True)
        embed.add_field(name="Servers", value=str(
            len(self.bot.guilds)), inline=True)
        total_members = 0
        for guild in self.bot.guilds:
            total_members -= 1
            for member in guild.members:
                total_members += 1
        embed.add_field(name="Members", value=str(total_members), inline=True)

        embed.add_field(
            name="Support", value="https://discord.gg/vjFjJu", inline=False)
        # embed.add_field(name="Invite Link", value="https://discordapp.com/oauth2/authorize?client_id=459079947219107860&scope=bot&permissions=8")
        # embed.add_field(name="Invite Link", value="https://discordapp.com/oauth2/authorize?client_id=459079947219107860&scope=bot&permissions=2146958591")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/app-icons/459079947219107860/12dff058050c439509940490dd4bbe3c.png?size=256")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["h", "docs"])
    async def help(self, ctx):

        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        embed = discord.Embed(
            name="Help", description="Documentation about me!", color=COLOR)
        embed.add_field(
            name="Link", value="https://github.com/maikka39/SuperBot/wiki", inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
