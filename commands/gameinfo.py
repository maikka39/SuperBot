import asyncio
import datetime
import json
import sys
import urllib.request

import discord
from discord.ext import commands
from mainconf import STEAMAPIKEY

COLOR = 0x0288d1


class Gameinfo:

    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot

    @commands.command(pass_context=True)
    async def steam(self, ctx, user=None):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        if user is None:
            embed = discord.Embed(
                title="Steam Accounts", description="Please provide a valid Steam ID or Profile URL", color=COLOR)
            await ctx.send(embed=embed)
            return

        # steamsummary = get_steam_player_summary(user)

        steamuserid = user
        with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + STEAMAPIKEY + "&steamids=" + steamuserid) as url:
            data = json.loads(url.read().decode())
        if data["response"]["players"] == []:
            with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key=" + STEAMAPIKEY + "&vanityurl=" + user) as url:
                data = json.loads(url.read().decode())
            if data["response"]["success"] == 1:
                steamuserid = data["response"]["steamid"]
            else:
                steamuserid = None

            try:
                with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + STEAMAPIKEY + "&steamids=" + steamuserid) as url:
                    data = json.loads(url.read().decode())
            except:
                embed = discord.Embed(
                    title="Steam Accounts", description="Please provide a valid steam id or url", color=COLOR)
                await ctx.send(embed=embed)
                return
        if data["response"]["players"] == []:
            embed = discord.Embed(
                title="Steam Accounts", description="Please provide a valid steam id or url", color=COLOR)
            await ctx.send(embed=embed)
            return
        steamsummary = data["response"]["players"][0]

        embed = discord.Embed(title="Steam Account", description="Here's what I could find about " +
                              str(steamsummary["personaname"]) + ".", color=COLOR)

        try:
            embed.add_field(name="Name (Real Name)", value=str(
                steamsummary["personaname"] + " (" + steamsummary["realname"] + ")"))
        except:
            embed.add_field(name="Name (Real Name)", value=str(
                steamsummary["personaname"] + " (" + "Private" + ")"))

        embed.add_field(name="ID", value=str(steamsummary["steamid"]))

        try:
            embed.add_field(name="Country", value=str(
                pycountry.countries.get(alpha_2=steamsummary["loccountrycode"]).name))
        except:
            embed.add_field(name="Country", value=str("Private"))

        embed.add_field(name="Status", value=str(
            ["Offline", "Online", "Busy", "Away", "Snooze", "Looking to Trade"][steamsummary["personastate"]]))
        embed.add_field(name="Joined", value=str(datetime.datetime.fromtimestamp(
            int(steamsummary["timecreated"])).strftime('%Y-%m-%d')))
        embed.add_field(name="Level", value=str(
            steamsummary["communityvisibilitystate"]))
        embed.add_field(name="Profile", value=str(steamsummary["profileurl"]))
        embed.set_thumbnail(url=steamsummary["avatarfull"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Gameinfo(bot))
