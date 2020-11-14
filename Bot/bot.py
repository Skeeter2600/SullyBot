import asyncio

import discord
import os
import random
import youtube_dl
from discord.ext import commands

TOKEN = "NzExNjc2MzE5NjcwNDY4NzQw.XsGeOA.HTvkWb2n4QEZtr9XFKJ85227vpM"
client = commands.Bot(command_prefix="*")
players = {}
smashers = []
smash_queue = []
smash_queue_pointer = 0

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

youtube_dl.utils.bug_reports_message = lambda: ''
# 🥺🥺🥺🥺🥺🥺
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
#test
#hi josh
ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


@client.event
async def on_ready():
    print("I'm back, bitches")


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server. Get the chalice ready, NotSoBot.')


@client.event
async def on_member_remove(member):
    print("Hasta la vista, " + f'{member}')


@client.command()
async def ping(ctx):
    if client.latency * 1000 > 500:
        await ctx.send(f' Dayum, yo internet slow as fuck "( {round(client.latency * 1000)} ms )"')
    else:
        await ctx.send(f' You good ( {round(client.latency * 1000)} ms )')


@client.command()
async def pong(ctx):
    await ctx.send("Ping!!!!!!!!!")


@client.command()
async def advise(ctx, *, question):
    outcomes = ["I don't know man, I'm just a machine in a basement",
                "Abso-fucking-lutely",
                "Nah",
                "Uhhhhh, sure",
                "Who cares?",
                "Not this time champ",
                "If you watch yourself, then maybe",
                "Slip me a 20, then we'll see"]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(outcomes)}')


@client.command(aliases=['hi'])
async def hello(ctx):
    hellos = ["Sup",
              "It's great to be here!",
              "What do you want me to say, ''Its great to be here!'' or something?"]
    await ctx.send(random.choice(hellos))


@client.command()
async def smash(ctx, condition, person):
    global smashers
    global smash_queue
    if condition == "add":
        smashers.append(person)
        await ctx.send(person + ' was added to the roster!')
    elif condition == "clear":
        smashers = []
        smash_queue = []
        await ctx.send("The roster was cleared")
    elif condition == "drop" or condition == "remove":
        if person not in smashers:
            await ctx.send(person + " isn't in the queue stupid!")
        else:
            smashers.remove(person)
            await ctx.send(person + ' was dropped to the roster. Please make a new fight queue to see the update.')


@client.command()
async def fight(ctx, fight_type):
    global smash_queue
    global smashers
    create = False
    if len(smashers) == 0:
        await ctx.send("Gotta add people to the roster in order to fight, retard (if we used the word)!")
    elif len(smashers) == 1:
        await ctx.send("It's not good to play with yourself. Add others to the roster.")
    else:
        smashers_total = len(smashers)

        # 1 on 1 fights
        if fight_type == "singles":
            # mix up the queue
            random.shuffle(smashers)

            if smashers_total < 3:
                await ctx.send("Do you really need my help with this? Either fight by yourselves or rotate.")
            # 4 people want to fight
            elif smashers_total == 4:
                smash_queue.append(["singles", smashers[0], smashers[1]])
                smash_queue.append(["singles", smashers[2], smashers[3]])

                smash_queue.append(["singles", smashers[0], smashers[3]])
                smash_queue.append(["singles", smashers[1], smashers[2]])

                smash_queue.append(["singles", smashers[1], smashers[3]])
                smash_queue.append(["singles", smashers[0], smashers[2]])
                create = True
            # 5 people want to fight
            elif smashers_total == 5:
                smash_queue.append(["singles", smashers[0], smashers[1]])
                smash_queue.append(["singles", smashers[2], smashers[3]])

                smash_queue.append(["singles", smashers[4], smashers[0]])
                smash_queue.append(["singles", smashers[1], smashers[2]])

                smash_queue.append(["singles", smashers[3], smashers[4]])
                smash_queue.append(["singles", smashers[0], smashers[2]])

                smash_queue.append(["singles", smashers[4], smashers[2]])
                smash_queue.append(["singles", smashers[3], smashers[1]])

                smash_queue.append(["singles", smashers[3], smashers[0]])
                smash_queue.append(["singles", smashers[1], smashers[4]])
                create = True
            # 6 people want to fight
            elif smashers_total == 6:
                smash_queue.append(["singles", smashers[0], smashers[1]])
                smash_queue.append(["singles", smashers[2], smashers[5]])
                smash_queue.append(["singles", smashers[4], smashers[3]])

                smash_queue.append(["singles", smashers[2], smashers[3]])
                smash_queue.append(["singles", smashers[5], smashers[0]])
                smash_queue.append(["singles", smashers[1], smashers[4]])

                smash_queue.append(["singles", smashers[5], smashers[3]])
                smash_queue.append(["singles", smashers[1], smashers[2]])
                smash_queue.append(["singles", smashers[0], smashers[4]])

                smash_queue.append(["singles", smashers[3], smashers[0]])
                smash_queue.append(["singles", smashers[2], smashers[4]])
                smash_queue.append(["singles", smashers[1], smashers[5]])

                smash_queue.append(["singles", smashers[4], smashers[5]])
                smash_queue.append(["singles", smashers[0], smashers[2]])
                smash_queue.append(["singles", smashers[3], smashers[1]])
                create = True
            # 7 people want to fight
            elif smashers_total == 7:
                smash_queue.append(["singles", smashers[0], smashers[5]])
                smash_queue.append(["singles", smashers[1], smashers[4]])
                smash_queue.append(["singles", smashers[2], smashers[3]])
                smash_queue.append(["singles", smashers[3], smashers[1]])

                smash_queue.append(["singles", smashers[4], smashers[0]])
                smash_queue.append(["singles", smashers[5], smashers[6]])
                smash_queue.append(["singles", smashers[1], smashers[6]])
                smash_queue.append(["singles", smashers[2], smashers[5]])

                smash_queue.append(["singles", smashers[3], smashers[4]])
                smash_queue.append(["singles", smashers[4], smashers[2]])
                smash_queue.append(["singles", smashers[5], smashers[1]])
                smash_queue.append(["singles", smashers[6], smashers[0]])

                smash_queue.append(["singles", smashers[2], smashers[1]])
                smash_queue.append(["singles", smashers[3], smashers[6]])
                smash_queue.append(["singles", smashers[4], smashers[5]])
                smash_queue.append(["singles", smashers[5], smashers[3]])

                smash_queue.append(["singles", smashers[6], smashers[2]])
                smash_queue.append(["singles", smashers[0], smashers[1]])
                smash_queue.append(["singles", smashers[6], smashers[3]])
                smash_queue.append(["singles", smashers[0], smashers[3]])
                smash_queue.append(["singles", smashers[1], smashers[2]])
                create = True
            # 8 people want to fight
            elif smashers_total == 8:
                # good
                smash_queue.append(["singles", smashers[0], smashers[7]])
                smash_queue.append(["singles", smashers[1], smashers[6]])
                smash_queue.append(["singles", smashers[2], smashers[5]])
                smash_queue.append(["singles", smashers[3], smashers[4]])
                # good
                smash_queue.append(["singles", smashers[0], smashers[6]])
                smash_queue.append(["singles", smashers[5], smashers[7]])
                smash_queue.append(["singles", smashers[1], smashers[4]])
                smash_queue.append(["singles", smashers[2], smashers[3]])
                # good
                smash_queue.append(["singles", smashers[0], smashers[5]])
                smash_queue.append(["singles", smashers[4], smashers[6]])
                smash_queue.append(["singles", smashers[3], smashers[7]])
                smash_queue.append(["singles", smashers[1], smashers[2]])
                # good
                smash_queue.append(["singles", smashers[0], smashers[4]])
                smash_queue.append(["singles", smashers[3], smashers[5]])
                smash_queue.append(["singles", smashers[2], smashers[6]])
                smash_queue.append(["singles", smashers[1], smashers[7]])
                # good
                smash_queue.append(["singles", smashers[0], smashers[3]])
                smash_queue.append(["singles", smashers[2], smashers[4]])
                smash_queue.append(["singles", smashers[1], smashers[5]])
                smash_queue.append(["singles", smashers[6], smashers[7]])
                # good
                smash_queue.append(["singles", smashers[0], smashers[2]])
                smash_queue.append(["singles", smashers[1], smashers[3]])
                smash_queue.append(["singles", smashers[4], smashers[7]])
                smash_queue.append(["singles", smashers[5], smashers[6]])
                # good
                smash_queue.append(["singles", smashers[0], smashers[1]])
                smash_queue.append(["singles", smashers[2], smashers[7]])
                smash_queue.append(["singles", smashers[3], smashers[6]])
                smash_queue.append(["singles", smashers[4], smashers[5]])
                create = True

        # 2 on 2 fights
        elif fight_type == "doubles":
            if len(smashers) < 4:
                await ctx.send("You can't do doubles with less than 4 people!")
            else:
                # mix up the queue
                random.shuffle(smashers)
                # 4 people want to fight
                if smashers_total == 4:
                    smash_queue.append(["doubles", smashers[0], smashers[1], smashers[2], smashers[3]])
                    smash_queue.append(["doubles", smashers[0], smashers[3], smashers[1], smashers[2]])
                    smash_queue.append(["doubles", smashers[1], smashers[3], smashers[0], smashers[2]])
                    create = True
                # 5 people want to fight
                elif smashers_total == 5:
                    smash_queue.append(["doubles", smashers[0], smashers[1], smashers[2], smashers[3]])
                    smash_queue.append(["doubles", smashers[4], smashers[0], smashers[1], smashers[2]])
                    smash_queue.append(["doubles", smashers[3], smashers[4], smashers[0], smashers[2]])
                    smash_queue.append(["doubles", smashers[4], smashers[2], smashers[3], smashers[1]])
                    smash_queue.append(["doubles", smashers[3], smashers[0], smashers[1], smashers[4]])
                    create = True
                # 6 people want to fight
                elif smashers_total == 6:
                    smash_queue.append(["doubles", smashers[0], smashers[1], smashers[2], smashers[5]])
                    smash_queue.append(["doubles", smashers[4], smashers[3], smashers[2], smashers[3]])
                    smash_queue.append(["doubles", smashers[5], smashers[0], smashers[1], smashers[4]])
                    smash_queue.append(["doubles", smashers[5], smashers[3], smashers[1], smashers[2]])
                    smash_queue.append(["doubles", smashers[0], smashers[4], smashers[3], smashers[0]])
                    smash_queue.append(["doubles", smashers[2], smashers[4], smashers[1], smashers[5]])
                    smash_queue.append(["doubles", smashers[4], smashers[5], smashers[0], smashers[2]])
                    smash_queue.append(["doubles", smashers[3], smashers[1], smashers[0], smashers[1]])
                    smash_queue.append(["doubles", smashers[2], smashers[5], smashers[4], smashers[3]])
                    smash_queue.append(["doubles", smashers[2], smashers[3], smashers[5], smashers[0]])
                    smash_queue.append(["doubles", smashers[1], smashers[4], smashers[5], smashers[3]])
                    smash_queue.append(["doubles", smashers[1], smashers[2], smashers[0], smashers[4]])
                    smash_queue.append(["doubles", smashers[3], smashers[0], smashers[2], smashers[4]])
                    smash_queue.append(["doubles", smashers[1], smashers[5], smashers[4], smashers[5]])
                    smash_queue.append(["doubles", smashers[0], smashers[2], smashers[3], smashers[1]])
                    create = True

                # 7 people want to fight
                elif smashers_total == 7:
                    smash_queue.append(["doubles", smashers[0], smashers[5], smashers[1], smashers[4]])
                    smash_queue.append(["doubles", smashers[2], smashers[3], smashers[3], smashers[1]])
                    smash_queue.append(["doubles", smashers[4], smashers[0], smashers[5], smashers[6]])
                    smash_queue.append(["doubles", smashers[1], smashers[6], smashers[2], smashers[5]])
                    smash_queue.append(["doubles", smashers[3], smashers[4], smashers[4], smashers[2]])
                    smash_queue.append(["doubles", smashers[5], smashers[1], smashers[6], smashers[0]])
                    smash_queue.append(["doubles", smashers[2], smashers[1], smashers[3], smashers[6]])
                    smash_queue.append(["doubles", smashers[4], smashers[5], smashers[5], smashers[3]])
                    smash_queue.append(["doubles", smashers[6], smashers[2], smashers[0], smashers[1]])
                    smash_queue.append(["doubles", smashers[6], smashers[3], smashers[0], smashers[3]])
                    smash_queue.append(["doubles", smashers[1], smashers[2], smashers[0], smashers[5]])
                    smash_queue.append(["doubles", smashers[1], smashers[4], smashers[2], smashers[3]])
                    smash_queue.append(["doubles", smashers[3], smashers[1], smashers[4], smashers[0]])
                    smash_queue.append(["doubles", smashers[5], smashers[6], smashers[1], smashers[6]])
                    smash_queue.append(["doubles", smashers[2], smashers[5], smashers[3], smashers[4]])
                    smash_queue.append(["doubles", smashers[4], smashers[2], smashers[5], smashers[1]])
                    smash_queue.append(["doubles", smashers[6], smashers[0], smashers[2], smashers[1]])
                    smash_queue.append(["doubles", smashers[3], smashers[6], smashers[4], smashers[5]])
                    smash_queue.append(["doubles", smashers[5], smashers[3], smashers[6], smashers[2]])
                    smash_queue.append(["doubles", smashers[0], smashers[1], smashers[6], smashers[3]])
                    smash_queue.append(["doubles", smashers[0], smashers[3], smashers[1], smashers[2]])
                    create = True

                # 8 people want to fight
                elif smashers_total == 8:
                    smash_queue.append(["doubles", smashers[0], smashers[7], smashers[1], smashers[6]])
                    smash_queue.append(["doubles", smashers[2], smashers[5], smashers[3], smashers[4]])
                    smash_queue.append(["doubles", smashers[0], smashers[6], smashers[5], smashers[7]])
                    smash_queue.append(["doubles", smashers[1], smashers[4], smashers[2], smashers[3]])
                    smash_queue.append(["doubles", smashers[0], smashers[5], smashers[4], smashers[6]])
                    smash_queue.append(["doubles", smashers[3], smashers[7], smashers[1], smashers[2]])
                    smash_queue.append(["doubles", smashers[0], smashers[4], smashers[3], smashers[5]])
                    smash_queue.append(["singles", smashers[2], smashers[6], smashers[1], smashers[7]])
                    smash_queue.append(["singles", smashers[0], smashers[3], smashers[2], smashers[4]])
                    smash_queue.append(["singles", smashers[1], smashers[5], smashers[6], smashers[7]])
                    smash_queue.append(["singles", smashers[0], smashers[2], smashers[1], smashers[3]])
                    smash_queue.append(["singles", smashers[4], smashers[7], smashers[5], smashers[6]])
                    smash_queue.append(["singles", smashers[0], smashers[1], smashers[2], smashers[7]])
                    smash_queue.append(["singles", smashers[3], smashers[6], smashers[4], smashers[5]])
                    create = True
        if create:
            await ctx.send("The queue is ready!")
            await next_fight(ctx)
            global smash_queue_pointer
            smash_queue_pointer += 1
        else:
            await ctx.send("Either remove or add people so its between 4 and 8 people for singles or doubles.")


@client.command()
async def next_fight(ctx):
    fight_flares = ["! I heard that ",
                    " , watch out for the uppercuts!",
                    "! 5 brownie points if ",
                    "! This'll be boring. Let me know when it's over",
                    "! Who cares?",
                    "! This should be interesting",
                    "! Maybe the match up will be better for ",
                    "! Imagine thinking "]
    global smash_queue_pointer
    flare = random.randint(0, 7)
    player = random.randint(0, 1)
    read = smash_queue[smash_queue_pointer]
    if smash_queue_pointer == len(smash_queue):
        smash_queue_pointer = 0
    if not smash_queue:
        await ctx.send("Make sure the smash queue exists. Can't fight without one!")
    else:
        if flare == 0:
            if read[0] == "singles":
                await ctx.send("Next up: " + read[1] + " VS " + read[2] + fight_flares[0] +
                               read[player + 1] + " fights dirty!")
            else:
                if player == 1:
                    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                                   " and " + read[4] + fight_flares[0] + read[1] + " and " + read[2] + " fight dirty!")
                else:
                    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                                   " and " + read[4] + fight_flares[0] + read[3] + " and " + read[4] + " fight dirty!")
        elif flare == 1:
            if read[0] == "singles":
                await ctx.send("Next up: " + read[1] + " VS " + read[2] + " ! " + read[player + 1] + fight_flares[1])
            else:
                if player == 1:
                    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                                   " and " + read[4] + " ! " + + read[1] + " and " + read[2] + fight_flares[1])
                else:
                    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                                   " and " + read[4] + " ! " + read[3] + " and " + read[4] + fight_flares[1])
        elif flare == 2:
            if read[0] == "singles":
                await ctx.send("Next up: " + read[1] + " VS " + read[2] + fight_flares[2] +
                               read[player + 1] + " wins.")
            else:
                if player == 1:
                    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                                   " and " + read[4] + fight_flares[2] + read[1] + " and " + read[2] + " win.")
                else:
                    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                                   " and " + read[4] + fight_flares[2] + read[3] + " and " + read[4] + " win.")
        elif flare == 6:
            if read[0] == "singles":
                await ctx.send("Next up: " + read[1] + " VS " + read[2] + fight_flares[6] +
                               read[player + 1] + " next time.")
            else:
                if player == 1:
                    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                                   " and " + read[4] + fight_flares[6] + read[1] + " and " + read[2] + " next time.")
                else:
                    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                                   " and " + read[4] + fight_flares[6] + read[3] + " and " + read[4] + " next time.")
        elif flare == 7:
            if read[0] == "singles":
                await ctx.send("Next up: " + read[1] + " VS " + read[2] + fight_flares[7] +
                               read[player + 1] + " will win this one.")
            else:
                if player == 1:
                    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                                   " and " + read[4] + fight_flares[7] + read[1] + " and " + read[2] +
                                   "  will win this one.")
                else:
                    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                                   " and " + read[4] + fight_flares[7] + read[3] + " and " + read[
                                       4] + "  will win this one.")
        else:
            if read[0] == "singles":
                await ctx.send("Next up: " + read[1] + " VS " + read[2] + fight_flares[flare])
            else:
                await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
                               " and " + read[4] + fight_flares[flare])
        smash_queue_pointer += 1


@client.command()
async def image(ctx, message):
    if message == "🥺":
        await ctx.send("🥺🥺🥺🥺🥺🥺")
    if message == "jerkoff":
        await ctx.send(":middle_finger:         :weary:\n   :bug::zzz::necktie::bug:\n               ⛽️       :boot:\n "
                       "              ⚡️8=:punch:=D:sweat_drops:\n          :guitar: "
                       ":closed_umbrella:\n          ⛽️      ⛽️\n          :boot:      :boot:")
    if message == "daffy":
        await ctx.send("--------┈┈╱╱╱▔ --------┈╱╭┈▔▔╲ \n--------▕▏┊╱╲┈╱▏  \n--------▕▏▕╮▕▕╮▏ --------▕▏▕▋▕▕▋  "
                       "\n--------╱▔▔╲╱▔▔╲╮┈┈╱▔▔╲  \n--------▏▔▏┈┈▔┈┈▔▔▔╱▔▔╱ \n ---------╲┈╲┈┈┈┈┈┈┈╱▔▔▔  "
                       "\n----------┈▔╲╲▂▂▂▂▂╱  \n----------┈┈▕━━▏ \n ⠄⠄⠄⠄⠄⠄⣠⢼⣿⣷⣶⣾⡷⢸⣗⣯⣿⣶⣿⣶⡄ \n⠄⠄⠄ "
                       "⠄⠄⣀⣤⣴⣾⣿⣷⣭⣭⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀ \n⠄⠄ ⠄⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣧ \n⠄⠄ ⠄⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢻⣿⣿⡄ \n⠄ "
                       "⠄⢸⣿⣮⣿⣿⣿⣿⣿⣿⣿⡟⢹⣿⣿⣿⡟⢛⢻⣷⢻⣿⣧ \n⠄ ⠄⠄⣿⡏⣿⡟⡛⢻⣿⣿⣿⣿⠸⣿⣿⣿⣷⣬⣼⣿⢸⣿⣿ \n⠄ ⠄⠄⣿⣧⢿⣧⣥⣾⣿⣿⣿⡟⣴⣝⠿⣿⣿⣿⠿⣫⣾⣿⣿⡆ \n "
                       "⠄⠄⢸⣿⣮⡻⠿⣿⠿⣟⣫⣾⣿⣿⣿⣷⣶⣾⣿⡏⣿⣿⣿⡇ \n ⠄⠄⢸⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⡇ \n ⠄⠄⢸⣿⣿⣿⡇⠄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠄ \n "
                       "⠄⠄⣼⣿⣿⣿⢃⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿ \n⠄ ⠄⠄⣿⣿⡟⣵⣿")

    if message == "<:Quagsire:651960845944750083>":
        with open('etc/images/quagsire1.jpg', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(picture)


@client.command()
async def start(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def end(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@client.command(aliases=['disconnect'])
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()


# @client.command()
# async def play(ctx, url):
#    print(url)
#    server = ctx.message.guild
#    voice_channel = server.voice_client
#
#    async with ctx.typing():
#        player = await YTDLSource.from_url(url, loop=self.bot.loop)
#        ctx.voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
#    await ctx.send('Now playing: {}'.format(player.title))


basepath = 'C:/Users/Beck/Desktop/Projects/Sullybot (Python)/cogs'
for file in os.listdir(basepath):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

client.run(TOKEN)
