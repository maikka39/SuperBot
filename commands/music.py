import asyncio
import datetime
import functools
import sys
import time

import discord
import youtube_dl
from discord.ext import commands

COLOR = 0xf44336

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')


class Music(commands.Cog):
    def __init__(self, bot):  # This allows the cog to access the bot, and its functions
        self.bot = bot
        self.message_title = "Music Player"
        self.voice_client = None
        self.song_queue = []

    def __unload(self):
        self.voice_client.stop()
        # await self.voice_client.disconnect()

    async def create_voice_client(self, channel):
        voice_client = await channel.connect()
        self.voice_client = voice_client

    @commands.command(pass_context=True, no_pm=True, aliases=["summon", "j", "follow", "f"])
    async def join(self, ctx, channel: discord.VoiceChannel = None):
        """Joins a voice channel."""
        # Try to remove the message by the sender
        try:
            await asyncio.sleep(0.05)
            await ctx.message.delete()
        # If not found, it's already gone so pass
        except discord.errors.NotFound:
            pass

        # If the user didn't include a channel, set the user's channel as the channel
        if channel is None:
            if ctx.message.author.voice:
                channel = ctx.message.author.voice.channel
            # If the user isn't in a channel, exit
            else:
                embed = discord.Embed(
                    title=self.message_title,
                    description="You are not in a voice channel.",
                    color=COLOR)
                await ctx.send(embed=embed)
                return False

        # Try to create a voice channel
        try:
            await self.create_voice_client(channel)
        # If there already is a client, move to it
        except discord.errors.ClientException:
            embed = discord.Embed(
                title=self.message_title,
                description="Moving to your current voice channel...",
                color=COLOR)
            await ctx.send(embed=embed)
            await self.voice_client.move_to(channel)
        # If the voice channel the user provided is not valid, tell the user
        except discord.errors.InvalidArgument:
            embed = discord.Embed(
                title=self.message_title,
                description="This is not a voice channel...",
                color=COLOR)
            await ctx.send(embed=embed)
        # If everything succeeded without incidents, tell the user
        else:
            embed = discord.Embed(
                title=self.message_title,
                description="Ready to play audio in " + channel.name,
                color=COLOR)
            await ctx.send(embed=embed)
            return True
        return False

    @commands.command(pass_context=True, no_pm=True, aliases=["leave", "l", "quit"])
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel"""
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        if not self.voice_client:
            return

        embed = discord.Embed(
            title=self.message_title,
            description="Leaving...",
            color=COLOR)
        await ctx.send(embed=embed)
        self.voice_client.stop()
        await self.voice_client.disconnect()
        self.song_queue = []

    @commands.command(pass_context=True, no_pm=True, aliases=["p"])
    async def play(self, ctx, song: str):
        """Plays a song"""
        await asyncio.sleep(0.05)
        await ctx.message.delete()

        if self.voice_client is None:
            success = await ctx.invoke(self.join)
            if not success:
                return

        song = self.add_to_queue(song, ctx.message.author.mention)
        if not self.voice_client.is_playing():
            self.play_next_song()

        embed = discord.Embed(
            title=self.message_title,
            description="Added the following song to the queue:",
            color=COLOR)
        embed.add_field(name="Title", value=song.title, inline=False)
        embed.add_field(name="Uploader",
                        value=song.uploader, inline=True)
        duration = song.duration
        if duration:
            embed.add_field(name="Duration", value="{0[0]}m {0[1]}s".format(
                divmod(duration, 60)), inline=True)
        if len(self.song_queue) > 0:
            embed.add_field(name="Position in Queue", value=str(
                self.song_queue.index(song) + 1), inline=True)
        else:
            embed.add_field(name="Position in Queue", value="0", inline=True)

        embed.add_field(name="Requested By",
                        value=song.requester, inline=False)
        embed.set_thumbnail(url=song.thumbnail_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, no_pm=True, aliases=["vol", "v"])
    async def volume(self, ctx, value: int = 60):
        """Sets the volume of the bot."""
        if not self.voice_client:
            return
        if self.voice_client.is_playing():
            value = abs(value)
            if value > 200:
                value = 200
            self.voice_client.source.volume = value / 100
            embed = discord.Embed(
                title=self.message_title,
                description="Set the volume to {:.0%}".format(
                    self.voice_client.source.volume),
                color=COLOR)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(
                title=self.message_title,
                description="I'm not playing any music right now...",
                color=COLOR)
            await ctx.send(embed=embed)
            return

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        if not self.voice_client:
            return
        if self.voice_client.is_paused():
            embed = discord.Embed(
                title=self.message_title,
                description="I already paused the song!",
                color=COLOR)
            await ctx.send(embed=embed)
            return
        if self.voice_client.is_playing():
            self.voice_client.pause()
            embed = discord.Embed(
                title=self.message_title,
                description="Paused!",
                color=COLOR)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(
                title=self.message_title,
                description="I'm not playing any music right now...",
                color=COLOR)
            await ctx.send(embed=embed)
            return

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        if not self.voice_client:
            return
        if self.voice_client.is_playing():
            if self.voice_client.is_paused():
                self.voice_client.resume()
                embed = discord.Embed(
                    title=self.message_title,
                    description="Resumed!",
                    color=COLOR)
                await ctx.send(embed=embed)
                return
            else:
                embed = discord.Embed(
                    title=self.message_title,
                    description="I'm already playing!",
                    color=COLOR)
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(
                title=self.message_title,
                description="I'm not playing any music right now...",
                color=COLOR)
            await ctx.send(embed=embed)
            return

    @commands.command(pass_context=True, no_pm=True, aliases=["s"])
    async def skip(self, ctx):
        """Skips the song if it had enough votes"""
        if not self.voice_client:
            return
        if not self.voice_client.is_playing():
            embed = discord.Embed(
                title=self.message_title, description="I'm not playing any music right now...", color=COLOR)
            await ctx.send(embed=embed)
            return

        voter = ctx.message.author
        if voter == self.voice_client.song.requester:
            embed = discord.Embed(
                title=self.message_title, description="Requester skipped song...", color=COLOR)
            await ctx.send(embed=embed)
            self.play_next_song()
        elif voter.id not in self.voice_client.song.skip_votes:
            self.voice_client.song.skip_votes.append(voter.id)
            total_votes = len(self.voice_client.song.skip_votes)
            min_votes = int(len(self.voice_client.channel.members) / 2 + 0.5)
            if total_votes >= min_votes:
                embed = discord.Embed(
                    title=self.message_title, description="Skip vote passed, skipping song...", color=COLOR)
                await ctx.send(embed=embed)
                self.voice_client.stop()
                self.play_next_song()
            else:
                embed = discord.Embed(
                    title=self.message_title, description="Skip vote added, currently at [{}/{}]".format(total_votes, min_votes), color=COLOR)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=self.message_title, description="You have already voted to skip this song.", color=COLOR)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, no_pm=True, aliases=["q"])
    async def queue(self, ctx):
        """Prints out the queue to the user"""
        if not self.voice_client:
            return
        embed = discord.Embed(
            title=self.message_title,
            description="Queue: \n",
            color=COLOR)

        if self.voice_client.is_playing():
            embed.add_field(name="Now Playing", value=self.voice_client.song.title +
                            ', requester: ' + self.voice_client.song.requester + "\n", inline=False)
        else:
            embed.add_field(name="Now Playing", value="None \n", inline=False)

        upcoming = ""
        for song in self.song_queue:
            upcoming += str(self.song_queue.index(song) + 1) + ". " + \
                song.title + ", requester: " + song.requester + "\n"
        if upcoming == "":
            embed.add_field(name="Upcoming", value="None \n", inline=False)
        else:
            embed.add_field(name="Upcoming", value=upcoming +
                            "\n", inline=False)
        await ctx.send(embed=embed)

    def play_next_song(self):
        if self.voice_client.is_playing():
            self.voice_client.stop()

        if len(self.song_queue) == 0:
            return

        song = self.song_queue[0]
        self.song_queue.pop(0)
        self.voice_client.song = song
        self.voice_client.play(discord.FFmpegPCMAudio(
            song.download_url), after=self.play_next_song)
        self.voice_client.source = discord.PCMVolumeTransformer(
            self.voice_client.source)
        self.voice_client.source.volume = 0.6

    def add_to_queue(self, url, requester):
        song = self.get_ytdl_info(url)
        song.requester = requester
        self.song_queue.append(song)
        return song

    def get_ytdl_info(self, url):
        """Gets all the info from youtube-dl"""
        opts = {
            'format': 'webm[abr>0]/bestaudio/best',
            'prefer_ffmpeg': True,
            'default_search': 'ytsearch',
            'quiet': True,
            'audio-quality': '0'
        }

        ytdl = youtube_dl.YoutubeDL(opts)
        func = functools.partial(ytdl.extract_info, url, download=False)
        info = func()
        if "entries" in info:
            info = info['entries'][0]

        download_url = info['url']
        song = self.Song()

        # set the dynamic attributes from the info extraction
        song.download_url = download_url
        song.url = url
        song.ytdl = ytdl
        song.views = info.get('view_count')
        song.is_live = bool(info.get('is_live'))
        song.likes = info.get('like_count')
        song.dislikes = info.get('dislike_count')
        song.duration = info.get('duration', '')
        song.uploader = info.get('uploader', 'Unknown')
        song.thumbnail_url = info.get('thumbnail', '')

        if 'twitch' in url:
            # twitch has 'title' and 'description' sort of mixed up.
            song.title = info.get('description')
            song.description = None
        else:
            song.title = info.get('title')
            song.description = info.get('description')

        # upload date handling
        date = info.get('upload_date')
        if date:
            try:
                date = datetime.datetime.strptime(date, '%Y%M%d').date()
            except ValueError:
                date = None

        song.upload_date = date
        return song

    class Song:
        """Song class"""

        def __init__(self):
            self.download_url = ""
            self.url = ""
            self.ytdl = ""
            self.views = ""
            self.is_live = ""
            self.likes = ""
            self.dislikes = ""
            self.duration = ""
            self.uploader = ""
            self.title = ""
            self.description = ""
            self.upload_date = ""
            self.requester = ""
            self.skip_votes = []


def setup(bot):
    bot.add_cog(Music(bot))
