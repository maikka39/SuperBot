import asyncio
import sys
from typing import Optional

import discord
from discord.ext import commands

COLOR = 0x616161


class Staff(commands.Cog):

    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot

    @commands.command(pass_context=True, aliases=["c"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, number: str = "250"):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        # Set the title for the messages in this function
        Title = "Clear Messages"

        # Make sure the send message is an interger
        if not number.isdigit() or number == "0":
            # If not, report that
            embed = discord.Embed(
                title=Title, description="Please enter a valid number of messages to delete", color=COLOR)
            embed.set_footer(text="Requested by {}".format(discord.utils.get(
                self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        # Make the number and interger and make it positive
        number = max(0, int(number))

        # Initialize the message counter
        deletemessages = 0
        # Get the last set amount of messages
        messages = await ctx.message.channel.history(limit=number).flatten()

        while True:
            if len(messages) >= 2 and len(messages) <= 100:
                await ctx.message.channel.delete_messages(messages)
                deletemessages += len(messages)
                break
            if len(messages) == 1:
                await messages[0].delete()
                deletemessages += len(messages)
                break
            else:
                break

        # Send a message in the channel
        embed = discord.Embed(title=Title, description=ctx.message.author.mention +
                              " has removed the last **" + str(deletemessages) + "** messages!", color=COLOR)
        embed.set_footer(
            text=f"Requested by {ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member = None, time="30"):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        print("FIX THE MUTE COMMAND!!!")

        Title = "Mute Member"
        role = discord.utils.get(ctx.message.guild.roles, name="Muted")

        if not time.isdigit():
            embed = discord.Embed(
                title=Title, description="Please enter a valid mute length", color=COLOR)
            embed.set_footer(text="Requested by {}".format(discord.utils.get(
                self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        if member is None:
            embed = discord.Embed(
                title=Title, description="Please provide a valid member to mute", color=COLOR)
            embed.set_footer(text="Requested by {}".format(discord.utils.get(
                self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        if time != "-1":
            time = abs(int(time))
            await member.add_roles(role)
            embed = discord.Embed(title=Title, description="Member " + member.mention + " has been muted for **" +
                                  str(time) + "** minutes by " + ctx.message.author.mention, color=COLOR)
            embed.set_footer(text="Requested by {}".format(discord.utils.get(
                self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await member.add_roles(role)
            embed = discord.Embed(title=Title, description="Member " + member.mention +
                                  " has been muted by " + ctx.message.author.mention, color=COLOR)
            embed.set_footer(text="Requested by {}".format(discord.utils.get(
                self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member = None):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        Title = "Mute Member"

        if member is None:
            embed = discord.Embed(
                title=Title, description="Please provide a valid member to unmute", color=COLOR)
            embed.set_footer(text="Requested by {}".format(discord.utils.get(
                self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        await member.remove_roles(discord.utils.get(ctx.message.guild.roles, name="Muted"))
        embed = discord.Embed(title=Title, description="Member " + member.mention +
                              " has been unmuted by " + ctx.message.author.mention, color=COLOR)
        embed.set_footer(
            text=f"Requested by {ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: Optional[str] = None):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        Title = "Kick Member"

        embed = discord.Embed(title=Title, description="Member " + member.mention +
                              " has been kicked by " + ctx.message.author.mention, color=COLOR)

        try:
            await member.kick(reason=reason)
        except Exception as e:
            print(e)
            embed = discord.Embed(title=Title, description="Could not kick " +
                                  member.mention + ", An error occured", color=COLOR)
        embed.set_footer(
            text=f"Requested by {ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Staff(bot))
