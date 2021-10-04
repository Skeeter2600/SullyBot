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

            if self.vc == "" or self.vc is None:
                self.vc = await self.music_queue[0][1].connect()

            await self.tc.send("**Now Playing:** " + self.music_queue[0][0]['title'])
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
        else:
            self.tc = ctx.message.channel
            self.music_queue.append([{'source': 'https://r4---sn-ab5sznl7.googlevideo.com/videoplayback?expire=163340887'
                                                '1&ei=B4NbYaPBH-PhgwOgjI_oDg&ip=129.21.130.204&id=o-AHuL7G512M2Yw8HHIOM'
                                                'dkL5Q_-YfOddW7e7lRFTfunHM&itag=249&source=youtube&requiressl=yes&mh=VK'
                                                '&mm=31%2C26&mn=sn-ab5sznl7%2Csn-p5qs7ned&ms=au%2Conr&mv=m&mvi=4&pl=16&'
                                                'pcm2=yes&initcwndbps=3465000&vprv=1&mime=audio%2Fwebm&ns=HqZP9HAwkUOjN'
                                                'WE6-Amy5FsG&gir=yes&clen=494&dur=0.381&lmt=1496327315141176&mt=1633386'
                                                '777&fvip=4&keepalive=yes&fexp=24001373%2C24007246&c=WEB&n=uhd_MjsnqdNe'
                                                'oPoZ&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cpcm2'
                                                '%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhALppERor4'
                                                'vlL29_dxTO27fIV1D97rs1u5dSRMjgg-y6KAiEArOYkY3tz8VvnFWqM7RwTQQcB6NBZjq'
                                                '-Rwh1qEnI0WBU%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwn'
                                                'dbps&lsig=AG3C_xAwRQIhAL7qe_LQRSadQCFdhgU4Y7xR-78Ry6rKL5lo2FLRvER1AiB'
                                                'rDUEkzedTWNQ_nvMu39a0apIPjfv9puahNBy6-1d0HQ%3D%3D', 'title': 'Shortest'
                                                ' Video on Youtube EVER! 0 seconds nearly 1 (fastest)'}, voice_channel])
            self.is_playing = True

            self.vc = await self.music_queue[0][1].connect()
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            if self.vc == "" or self.vc is None:
                self.vc = await self.music_queue[0][1].connect()

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

    @commands.command(name="leave")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.message.send("Hasta luego")

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
                await ctx.send("Song added to the queue", delete_after=30)
                self.music_queue.append([song, voice_channel])

                if not self.is_playing:
                    self.tc = ctx.message.channel
                    await self.play_music()

    @commands.command(alias="queue, q")
    async def queue(self, ctx):
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

    @commands.command(name="skip", alias="skip_song")
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

    @commands.command(alias="shuffle, shuffle_q")
    async def shuffle_queue(self, ctx):
        random.shuffle(self.music_queue)
        await ctx.send("The queue has been shuffled")

    @commands.command(name="clear_q")
    async def clear_queue(self, ctx):
        self.music_queue = []
        self.vc.stop()
        await ctx.send("The queue has been cleared")


def setup(client):
    client.add_cog(music_cog(client))
