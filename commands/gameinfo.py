import asyncio
import datetime
import os
from commands.lib.other import safe_get_list
from commands.lib.steamapi import SteamAPI as steam_api

import discord
import pycountry
from discord.ext import commands

COLOR = 0x0288d1

SteamAPI = steam_api(os.environ["STEAMAPIKEY"])


class Gameinfo(commands.Cog):
    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot
        SteamAPI.get_game_titles()

    @commands.command(pass_context=True, aliases=["st"])
    async def steam(self, ctx, user=None):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        if user is None:
            embed = discord.Embed(
                title="Steam Accounts", description="Please provide a valid Steam ID or Profile URL", color=COLOR)
            embed.set_footer(text="Requested by {}".format(discord.utils.get(
                self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        steamid = SteamAPI.get_steam_id(user)

        steamsummary = SteamAPI.get_player_summary(steamid)
        if not steamsummary:
            embed = discord.Embed(
                title="Steam Accounts", description="Please provide a valid steam id or url", color=COLOR)
            embed.set_footer(text="Requested by {}".format(discord.utils.get(
                self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Steam Account", description="Here's what I could find about " +
                              str(safe_get_list(steamsummary, "personaname", steamid)) + ".", color=COLOR)

        embed.add_field(name="Name (Real Name)", value=str(
            safe_get_list(steamsummary, "personaname", "Unknown") + " (" + safe_get_list(steamsummary, "realname", "Private") + ")"))

        embed.add_field(name="ID", value=str(
            safe_get_list(steamsummary, "steamid", "Unknown")))

        try:
            embed.add_field(name="Country", value=str(
                pycountry.countries.get(alpha_2=safe_get_list(steamsummary, "loccountrycode")).name))
        except AttributeError:
            embed.add_field(name="Country", value=str("Private"))

        embed.add_field(name="Status", value=str(
            safe_get_list(["Offline", "Online", "Busy", "Away", "Snooze", "Looking to Trade"], safe_get_list(steamsummary, "personastate"), "Unknown")))

        try:
            embed.add_field(name="Joined", value=str(datetime.datetime.fromtimestamp(
                int(safe_get_list(steamsummary, "timecreated", None))).strftime('%Y-%m-%d')))
        except TypeError:
            embed.add_field(name="Joined", value=str("Unknown"))

        embed.add_field(name="Level", value=str(
            SteamAPI.get_steam_level(steamid)))

        embed.add_field(name="Profile", value=str(
            safe_get_list(steamsummary, "profileurl", "Unknown")))
        embed.set_thumbnail(url=safe_get_list(steamsummary, "avatarfull",
                                              "https://steamuserimages-a.akamaihd.net/ugc/868480752636433334/1D2881C5C9B3AD28A1D8852903A8F9E1FF45C2C8/"))

        embed.set_footer(
            text=f"Requested by {ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        embed.set_footer(
            text=f"Requested by {ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["addicted", "addict"])
    async def addiction(self, ctx, user=None, amount: int = 3):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        if user is None:
            embed = discord.Embed(
                title="Addiction Checker", description="Please provide a valid Steam ID or Profile URL", color=COLOR)
            embed.set_footer(text="Requested by {}".format(discord.utils.get(
                self.bot.get_all_members(), id=ctx.message.author.id)), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return

        steamid = SteamAPI.get_steam_id(user)
        mostplayed = SteamAPI.get_most_played_games(steamid, amount=amount)
        steamsummary = SteamAPI.get_player_summary(steamid)

        embed = discord.Embed(title="Addiction Checker", description="Here's what I could find about " +
                              str(safe_get_list(steamsummary, "personaname")) + "." + "\nThey seem to be addicted to:", color=COLOR)

        embed.add_field(name="Game", value=str(
            '\n '.join([SteamAPI.get_game_title(mostplayed[i][0]) for i in range(amount)])))
        embed.add_field(name="Playtime", value=str(
            '\n '.join([(str(int(mostplayed[i][1] / 60)) + "h") for i in range(amount)])))
        embed.add_field(name="Profile", value=str(
            safe_get_list(steamsummary, "profileurl")), inline=False)
        embed.set_thumbnail(url=str(
            "https://steamcdn-a.akamaihd.net/steam/apps/{0}/header.jpg".format(mostplayed[0][0])))
        embed.set_footer(
            text=f"Requested by {ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def csgo(self, ctx):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        embed = discord.Embed(
            title="Counter-Strike: Global Offensive", description="Coming Soon! :tools:", color=COLOR)
        embed.set_footer(
            text=f"Requested by {ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Gameinfo(bot))
