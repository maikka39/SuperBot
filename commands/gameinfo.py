import asyncio
import datetime
import json
import re
import sys
import urllib.request

import discord
import pycountry
from discord.ext import commands
from mainconf import STEAMAPIKEY

COLOR = 0x0288d1


class Gameinfo:

    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot
        try:
            with urllib.request.urlopen("https://api.steampowered.com/ISteamApps/GetAppList/v2/") as url:
                self.steamtitles = safe_get_list(safe_get_list(
                    json.loads(url.read().decode()), "applist"), "apps")
        except:
            self.steamtitles = None

    def get_steam_id(self, user):
        match = re.match(
            r'((http|https):\/\/steamcommunity.com\/(profiles|id)\/(?P<steamid>\w+))', user)

        if match:
            user = match.group("steamid")

        with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + STEAMAPIKEY + "&steamids=" + user) as url:
            data = json.loads(url.read().decode())
        if safe_get_list(safe_get_list(data, "response"), "players", []) == []:
            with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key=" + STEAMAPIKEY + "&vanityurl=" + user) as url:
                data = json.loads(url.read().decode())
            if safe_get_list(safe_get_list(data, "response"), "success") == 1:
                user = safe_get_list(
                    safe_get_list(data, "response"), "steamid")
            else:
                user = None
        return user

    def get_steam_title(self, appid):
        for title in self.steamtitles:
            if str(safe_get_list(title, "appid")) == str(appid):
                return safe_get_list(title, "name")

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

        steamuserid = self.get_steam_id(user)

        try:
            with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + STEAMAPIKEY + "&steamids=" + steamuserid) as url:
                data = json.loads(url.read().decode())
        except:
            embed = discord.Embed(
                title="Steam Accounts", description="Please provide a valid steam id or url", color=COLOR)
            await ctx.send(embed=embed)
            return

        if safe_get_list(safe_get_list(data, "response"), "players", []) == []:
            embed = discord.Embed(
                title="Steam Accounts", description="Please provide a valid steam id or url", color=COLOR)
            await ctx.send(embed=embed)
            return

        # steamsummary = data["response"]["players"][0]
        steamsummary = safe_get_list(safe_get_list(
            safe_get_list(data, "response"), "players"), 0)

        embed = discord.Embed(title="Steam Account", description="Here's what I could find about " +
                              str(safe_get_list(steamsummary, "personaname")) + ".", color=COLOR)

        try:
            embed.add_field(name="Name (Real Name)", value=str(
                safe_get_list(steamsummary, "personaname") + " (" + safe_get_list(steamsummary, "realname") + ")"))
        except:
            embed.add_field(name="Name (Real Name)", value=str(
                safe_get_list(steamsummary, "personaname") + " (" + "Private" + ")"))

        embed.add_field(name="ID", value=str(
            safe_get_list(steamsummary, "steamid")))

        try:
            embed.add_field(name="Country", value=str(
                pycountry.countries.get(alpha_2=safe_get_list(steamsummary, "loccountrycode")).name))
        except:
            embed.add_field(name="Country", value=str("Private"))

        embed.add_field(name="Status", value=str(
            safe_get_list(["Offline", "Online", "Busy", "Away", "Snooze", "Looking to Trade"], safe_get_list(steamsummary, "personastate", "Unknown"))))

        try:
            embed.add_field(name="Joined", value=str(datetime.datetime.fromtimestamp(
                int(safe_get_list(steamsummary, "timecreated"))).strftime('%Y-%m-%d')))
        except ValueError:
            embed.add_field(name="Joined", value=str("Unknown"))

        with urllib.request.urlopen("https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key=" + STEAMAPIKEY + "&steamid=" + steamuserid) as url:
            leveldata = safe_get_list(json.loads(
                url.read().decode()), "response")
        embed.add_field(name="Level", value=str(
            safe_get_list(leveldata, "player_level")))

        embed.add_field(name="Profile", value=str(
            safe_get_list(steamsummary, "profileurl")))
        embed.set_thumbnail(url=safe_get_list(steamsummary, "avatarfull"))
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["addicted", "addiction"])
    async def addict(self, ctx, user=None):
        # Remove the message send by the author
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        if user is None:
            embed = discord.Embed(
                title="Addiction Checker", description="Please provide a valid Steam ID or Profile URL", color=COLOR)
            await ctx.send(embed=embed)
            return

        steamuserid = self.get_steam_id(user)

        try:
            with urllib.request.urlopen("https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=" + STEAMAPIKEY + "&steamid=" + steamuserid) as url:
                data = json.loads(url.read().decode())
        except:
            embed = discord.Embed(
                title="Addiction Checker", description="Please provide a valid steam id or url", color=COLOR)
            await ctx.send(embed=embed)
            return

        if safe_get_list(safe_get_list(data, "response"), "game_count", None) == None:
            embed = discord.Embed(
                title="Addiction Checker", description="Sorry, this account seems to be private", color=COLOR)
            await ctx.send(embed=embed)
            return

        mostplayed = [0, 0]
        for game in safe_get_list(safe_get_list(data, "response"), "games"):
            if safe_get_list(game, "playtime_forever", 0) > mostplayed[1]:
                mostplayed[0] = safe_get_list(game, "appid")
                mostplayed[1] = safe_get_list(game, "playtime_forever")

        try:
            with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + STEAMAPIKEY + "&steamids=" + steamuserid) as url:
                steamsummary = safe_get_list(safe_get_list(safe_get_list(
                    json.loads(url.read().decode()), "response"), "players"), 0)
        except:
            return

        embed = discord.Embed(title="Addiction Checker", description="Here's what I could find about " +
                              str(safe_get_list(steamsummary, "personaname")) + "." + "\nThey seem to be addicted to:", color=COLOR)

        embed.add_field(name="Game", value=str(
            self.get_steam_title(mostplayed[0])))
        embed.add_field(name="Playtime", value=str(
            int(mostplayed[1] / 60)) + "h")
        embed.add_field(name="Profile", value=str(
            safe_get_list(steamsummary, "profileurl")), inline=False)
        embed.set_thumbnail(url=safe_get_list(steamsummary, "avatarfull"))
        await ctx.send(embed=embed)


def safe_get_list(l, item, default="Unknown"):
    try:
        return l[item]
    except:
        return default


def setup(bot):
    bot.add_cog(Gameinfo(bot))
