import asyncio
from commands.lib.other import safe_get_list

import discord
from discord.ext import commands
from PyDictionary import PyDictionary

COLOR = 0xbb33ee


class Dictionary:

    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot

    @commands.command(pass_context=True, aliases=["dict", "define", "def", "meaning"])
    async def dictionary(self, ctx, word):
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        embed = discord.Embed(
            title="Dictionary", description="Here is what I found for `{}`: \n\n___".format(word), color=COLOR)

        meaning = safe_get_list(PyDictionary(word).getMeanings(), word)

        if safe_get_list(meaning, "Noun", False):
            embed.add_field(name="Noun", value=str(
                '`1.` ' + safe_get_list(safe_get_list(meaning, "Noun"), 0, "").capitalize() +
                '\n`2.` ' + safe_get_list(safe_get_list(meaning, "Noun"), 1, "").capitalize()), inline=False)

        if safe_get_list(meaning, "Verb", False):
            embed.add_field(name="Verb", value=str(
                '`1.` ' + safe_get_list(safe_get_list(meaning, "Verb"), 0, "").capitalize() +
                '\n`2.` ' + safe_get_list(safe_get_list(meaning, "Verb"), 1, "").capitalize()), inline=False)

        if safe_get_list(meaning, "Adjective", False):
            embed.add_field(name="Adjective", value=str(
                '`1.` ' + safe_get_list(safe_get_list(meaning, "Adjective"), 0, "").capitalize() +
                '\n`2.` ' + safe_get_list(safe_get_list(meaning, "Adjective"), 1, "").capitalize()), inline=False)

        if safe_get_list(meaning, "Adverb", False):
            embed.add_field(name="Adverb", value=str(
                '`1.` ' + safe_get_list(safe_get_list(meaning, "Adverb"), 0, "").capitalize() +
                '\n`2.` ' + safe_get_list(safe_get_list(meaning, "Adverb"), 1, "").capitalize()), inline=False)

        # embed.add_field(name="ID", value=user.id, inline=True)

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def translate(self, ctx, word):
        await asyncio.sleep(0.05)
        await ctx.message.delete()
        embed = discord.Embed(
            title="Translator", description="Coming Soon! :tools:", color=COLOR)
        await ctx.send(embed=embed)

    # TODO: Synonyms
    # TODO: Antonyms


def setup(bot):
    bot.add_cog(Dictionary(bot))
