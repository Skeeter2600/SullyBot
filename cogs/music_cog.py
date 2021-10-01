import asyncio
import random
from random import Random

import discord
from discord.ext import commands

from youtube_dl import YoutubeDL


class music_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # all the music related stuff
        self.is_playing = False
        self.title_sent = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = ""

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog is online")

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            if self.vc == "" or not self.vc.is_connected() or self.vc is None:
                self.vc = await self.music_queue[0][1].connect()
            else:

                await self.vc.move_to(self.music_queue[0][1])

            await self.tc.send("**Now Playing:** " + self.music_queue[0][0]['title'], delete_after=30)
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            self.title_sent = False

    @commands.command(name="join")
    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel, dummy!")
        await voice_channel.connect()

    @commands.command(name="leave")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name="play")
    async def p(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel, dummy!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send(
                    "This song couldn't be played, try another version")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])

                if not self.is_playing:
                    self.tc = ctx.message.channel
                    await self.play_music()

    @commands.command(name="queue")
    async def q(self, ctx):
        retval = ""
        q_length = len(self.music_queue)
        if q_length > 10:
            q_length = 9
        for i in range(0, q_length):
            retval += "**" + self.music_queue[i][0]['title'] + "**\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="skip_song")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            # try to play next in the queue if it exists
            await self.play_music()

    @commands.command()
    async def pause(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.pause()
            await ctx.send("Song paused")

    @commands.command()
    async def resume(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.resume()
            await ctx.send("Song resumed")

    @commands.command(name="shuffle_queue")
    async def shuffle_q(self, ctx):
        random.shuffle(self.music_queue)
        await ctx.send("The queue has been shuffled")

    @commands.command(name="clear_queue")
    async def clear_q(self, ctx):
        self.music_queue = []
        self.vc.stop()
        await ctx.send("The queue has been cleared")



def setup(client):
    client.add_cog(music_cog(client))
