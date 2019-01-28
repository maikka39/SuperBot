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

    async def get_steam_id(self, ctx, user):
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

        steamuserid = await self.get_steam_id(ctx, user)

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


def safe_get_list(l, item, default="Unknown"):
    try:
        return l[item]
    except:
        return default


def setup(bot):
    bot.add_cog(Gameinfo(bot))
