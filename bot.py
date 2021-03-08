import asyncio

import discord
import os
import random
# import youtube_dl
from discord.ext import commands
from itertools import chain, combinations
import json

TOKEN = json.loads(open("cogs/TOKEN_ID.json", "r").read()).get("TOKEN")

client = commands.Bot(command_prefix="*")
players = {}
smashers = []
smash_queue = []
mix_up = 1

smash_queue_pointer = 0


# ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
# howdy ho
# youtube_dl.utils.bug_reports_message = lambda: ''
# # 🥺🥺🥺🥺🥺🥺
# ytdl_format_options = {
#     'format': 'bestaudio/best',
#     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
# }


# ffmpeg_options = {
#     'options': '-vn'
# }

# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get('title')
#         self.url = data.get('url')

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]

#         filename = data['url'] if stream else ytdl.prepare_filename(data)
#         return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


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
    answers = json.loads(open("responses/questions.json", "r").read()).get("answers")
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(answers)}')


@client.command(aliases=['hi'])
async def hello(ctx):
    hellos = json.loads(open("responses/hellos.json", "r").read()).get("hellos")
    await ctx.send(random.choice(hellos))


@client.command()
async def smash(ctx, condition, person=None):
    global smashers
    global smash_queue
    personCmd = ["add", "drop", "remove"]
    if condition == "clear":
        smashers = []
        smash_queue = []
        await ctx.send("The roster was cleared")
    elif condition == "roster":
        msg = ""
        for i in range(len(smashers)):
            msg += f'{smashers[i].name}'
            if i + 1 != len(smashers):
                msg += ", "
        await ctx.send("Current smash roster: " + msg)
    elif condition in personCmd:
        player = client.get_user(int(person[3: len(person) - 1]))
        if player != None:
            if condition == "add":
                if player in smashers:
                    await ctx.send(f'{player.name} is already in the roster...')
                else:
                    smashers.append(player)
                    await ctx.send(f'{player.name} was added to the roster!')
            else:
                if player in smashers:
                    smashers.remove(player)
                    await ctx.send(
                        f'{player.name} was dropped from the roster. Please make a new fight queue to see the update.')
                else:
                    await ctx.send(f'{player.name} isn\'t in the queue stupid!')
        else:
            await ctx.send(f"User \"{player.name}\"doesn't exist. Mention one that does...")


@client.command()
async def fight(ctx, fight_type):
    global smash_queue
    global smashers
    smash_queue = []
    create = False
    if len(smashers) == 0:
        await ctx.send("Gotta add people to the roster in order to fight, retard (if we used the word)!")
    elif len(smashers) == 1:
        await ctx.send("It's not good to play with yourself. Add others to the roster.")
    else:
        smashers_total = len(smashers)

        if smashers_total < 3:
            await ctx.send("Do you really need my help with this? Either fight by yourselves or rotate.")

        # 1 on 1 fights
        if fight_type == "singles":

            # BECK APPROACH

            for fighter in smashers:
                opponents = []
                name_design = ["singles", fighter, False, opponents]
                smash_queue.append(name_design)

            # JOSH APPROACH
            # generate all combinations of pairings of fighters
            # for i in list(combinations(smashers, 2)):
            # i.insert(0, "singles")
            # smash_queue.append(i)

            create = True

        # 2 on 2 fights
        elif fight_type == "doubles":
            if smashers_total < 4:
                await ctx.send("You can't do doubles with less than 4 people!")
            else:

                # Beck Approach

                for fighter in smashers:
                    partners = []
                    opponents = []
                    name_design = ["doubles", fighter, False, partners, opponents]
                    smash_queue.append(name_design)

                create = True
                # Josh Approach
                # generate all combinations of pairs of fighters
                # in all sets of 4 fighters
                # for i in list(combinations(smashers, 4)):
                # inside each possible quadruple

                # l = []

                # for j in list(combinations(i, 2)):
                # inside each pair in quadruple

                # for k in j:
                # each fighter instance in pair
                # flatten list and append
                # l.append(k)

                # for m in range(0, int(len(l) / 4)):
                # collect pairs from quadruple and append to queue
                # smash_queue.append(["doubles",
                #       l[2 * m], l[2 * m + 1], l[11 - (2 * m)], l[10 - (2 * m)]])

                # create = True

        if create:
            random.shuffle(smash_queue)
            await ctx.send("The queue is ready!")
            await next_fight(ctx)
            global smash_queue_pointer
            smash_queue_pointer += 1
        else:
            await ctx.send("Add people so there are at least 4 people in the roster.")


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
    global smash_queue
    global mix_up
    past_fighters = []
    flare = random.randint(0, 7)

    # temp, remove after debug
    flare = 8

    player = random.randint(0, 1)
    current_fighter = smash_queue[smash_queue_pointer % len(smash_queue)]
    if not smash_queue:
        await ctx.send("Make sure the smash queue exists. Can't fight without one!")
    else:
        if flare == 8:
            for fighters in smash_queue:
                if fighters[2]:
                    past_fighters.append(fighters)
            if len(past_fighters) == len(smash_queue):
                for fighters in smash_queue:
                    fighters[2] = False
                past_fighters = []
            if current_fighter[0] == "singles":
                condition = True
                checking = 0
                opponent_queue_pointer = smash_queue_pointer
                while condition:
                    current_fighter = smash_queue[smash_queue_pointer % len(smash_queue)]
                    if current_fighter not in past_fighters:
                        if len(current_fighter[3]) != len(smash_queue)-1:
                            opponent_queue_pointer = opponent_queue_pointer + mix_up
                            attempted_fight = smash_queue[opponent_queue_pointer % len(smash_queue)]
                            while attempted_fight in past_fighters:
                                opponent_queue_pointer = opponent_queue_pointer + 1
                                attempted_fight = smash_queue[opponent_queue_pointer % len(smash_queue)]
                                if attempted_fight[1] == current_fighter[1]:
                                    opponent_queue_pointer = opponent_queue_pointer + 1
                                    attempted_fight = smash_queue[opponent_queue_pointer % len(smash_queue)]
                            if attempted_fight[1] != current_fighter[1]:
                                opponents = current_fighter[3]
                                if attempted_fight[1] not in opponents:
                                    current_fighter[3].append(attempted_fight[1])
                                    attempted_fight[3].append(current_fighter[1])
                                    current_fighter[2] = True
                                    attempted_fight[2] = True
                                    await ctx.send("This step of the test matched up " + current_fighter[1].mention + " versus " +
                                                   attempted_fight[1].mention)
                                    condition = False
                                    checking = 0
                                elif attempted_fight[1] in current_fighter[3]:
                                    if len(opponents) == len(smash_queue)-1:
                                        checking += 1
                            else:
                                opponent_queue_pointer += 1
                        else:
                            smash_queue_pointer += 1
                            checking += 1
                            if checking == len(smash_queue) - 1:
                                checking = 0
                                mix_up += 1
                                if mix_up == len(smash_queue):
                                    mix_up = 1
                                for fighter in smash_queue:
                                    fighter[3] = []
                    else:
                        smash_queue_pointer += 1
                        checking += 1
                        if checking == len(smash_queue) - 1:
                            checking = 0
                            mix_up += 1
                            if mix_up == len(smash_queue):
                                mix_up = 1
                            for fighter in smash_queue:
                                fighter[3] = []

        # if flare == 0:
        #   if read[0] == "singles":
        #      await ctx.send("Next up: " + read[1].name + " VS " + read[2].name + fight_flares[0] +
        #                    read[player + 1] + " fights dirty!")
        # else:
        #   if player == 1:
        #      await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                    " and " + read[4] + fight_flares[0] + read[1] + " and " + read[2] + " fight dirty!")
        # else:
        #   await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                 " and " + read[4] + fight_flares[0] + read[3] + " and " + read[4] + " fight dirty!")
        # elif flare == 1:
        #   if read[0] == "singles":
        #      await ctx.send("Next up: " + read[1] + " VS " + read[2] + " ! " + read[player + 1] + fight_flares[1])
        # else:
        #    if player == 1:
        #       await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                     " and " + read[4] + " ! " + + read[1] + " and " + read[2] + fight_flares[1])
        # else:
        #    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                  " and " + read[4] + " ! " + read[3] + " and " + read[4] + fight_flares[1])
        # elif flare == 2:
        #   if read[0] == "singles":
        #      await ctx.send("Next up: " + read[1] + " VS " + read[2] + fight_flares[2] +
        #                    read[player + 1] + " wins.")
        # else:
        #   if player == 1:
        #      await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                    " and " + read[4] + fight_flares[2] + read[1] + " and " + read[2] + " win.")
        # else:
        #   await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                 " and " + read[4] + fight_flares[2] + read[3] + " and " + read[4] + " win.")
        # elif flare == 6:
        #   if read[0] == "singles":
        #      await ctx.send("Next up: " + read[1] + " VS " + read[2] + fight_flares[6] +
        #                    read[player + 1] + " next time.")
        # else:
        #   if player == 1:
        #      await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                    " and " + read[4] + fight_flares[6] + read[1] + " and " + read[2] + " next time.")
        # else:
        #   await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                 " and " + read[4] + fight_flares[6] + read[3] + " and " + read[4] + " next time.")
        # elif flare == 7:
        #   if read[0] == "singles":
        #      await ctx.send("Next up: " + read[1] + " VS " + read[2] + fight_flares[7] +
        #                    read[player + 1] + " will win this one.")
        # else:
        #   if player == 1:
        #      await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                    " and " + read[4] + fight_flares[7] + read[1] + " and " + read[2] +
        #                   "  will win this one.")
        # else:
        #   await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                 " and " + read[4] + fight_flares[7] + read[3] + " and " + read[
        #                    4] + "  will win this one.")
        # else:
        #   if read[0] == "singles":
        #      await ctx.send("Next up: " + read[1] + " VS " + read[2] + fight_flares[flare])
        # else:
        #    await ctx.send("Next up: " + read[1] + " and " + read[2] + " VS " + read[3] +
        #                  " and " + read[4] + fight_flares[flare])
        smash_queue_pointer += 1


@client.command()
async def image(ctx, message):
    if message == "🥺":
        await ctx.send("🥺🥺🥺🥺🥺🥺")
    elif message == "jerkoff":
        await ctx.send(":middle_finger:         :weary:\n   :bug::zzz::necktie::bug:\n               ⛽️       :boot:\n "
                       "              ⚡️8=:punch:=D:sweat_drops:\n          :guitar: "
                       ":closed_umbrella:\n          ⛽️      ⛽️\n          :boot:      :boot:")
    elif message == "daffy":
        await ctx.send("--------┈┈╱╱╱▔ --------┈╱╭┈▔▔╲ \n--------▕▏┊╱╲┈╱▏  \n--------▕▏▕╮▕▕╮▏ --------▕▏▕▋▕▕▋  "
                       "\n--------╱▔▔╲╱▔▔╲╮┈┈╱▔▔╲  \n--------▏▔▏┈┈▔┈┈▔▔▔╱▔▔╱ \n ---------╲┈╲┈┈┈┈┈┈┈╱▔▔▔  "
                       "\n----------┈▔╲╲▂▂▂▂▂╱  \n----------┈┈▕━━▏ \n ⠄⠄⠄⠄⠄⠄⣠⢼⣿⣷⣶⣾⡷⢸⣗⣯⣿⣶⣿⣶⡄ \n⠄⠄⠄ "
                       "⠄⠄⣀⣤⣴⣾⣿⣷⣭⣭⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀ \n⠄⠄ ⠄⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣧ \n⠄⠄ ⠄⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢻⣿⣿⡄ \n⠄ "
                       "⠄⢸⣿⣮⣿⣿⣿⣿⣿⣿⣿⡟⢹⣿⣿⣿⡟⢛⢻⣷⢻⣿⣧ \n⠄ ⠄⠄⣿⡏⣿⡟⡛⢻⣿⣿⣿⣿⠸⣿⣿⣿⣷⣬⣼⣿⢸⣿⣿ \n⠄ ⠄⠄⣿⣧⢿⣧⣥⣾⣿⣿⣿⡟⣴⣝⠿⣿⣿⣿⠿⣫⣾⣿⣿⡆ \n "
                       "⠄⠄⢸⣿⣮⡻⠿⣿⠿⣟⣫⣾⣿⣿⣿⣷⣶⣾⣿⡏⣿⣿⣿⡇ \n ⠄⠄⢸⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⡇ \n ⠄⠄⢸⣿⣿⣿⡇⠄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠄ \n "
                       "⠄⠄⣼⣿⣿⣿⢃⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿ \n⠄ ⠄⠄⣿⣿⡟⣵⣿")

    elif message == "<:Quagsire:651960845944750083>":
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


@client.command()
async def dev(ctx, condition, person):
    try:
        user = client.get_user(int (person[3 : len(person) - 1]))
    except ValueError:
        await ctx.send(f'User "{person}" doesn\'t exist. Mention one that does...')

    if user != None:
        devs = json.loads(open("cogs/devs.json", "r").read())
        if condition == "add":
            devs["devs"].append(user.id)
            await ctx.send(f'@{user.name} has been hired.')
        elif condition == "remove":
            if user.id in devs["devs"]:
                devs["devs"].remove(user.id)
                await ctx.send(f'@{user.name} has been fired.')
            else:
                await ctx.send(f'@{user.name} isn\'t on the payroll')
        else:
            await ctx.send("Please either add or remove a dev")
        open("cogs/devs.json", "w").write(json.dumps(devs))
    else:
        await ctx.send(f"User \"{person}\"doesn't exist. Mention one that does...")

@client.command(aliases=["quit", "q", "kil", "kill", "die"])
async def close(ctx):
    devs = json.loads(open("cogs/devs.json", "r").read()).get("devs")
    if ctx.author.id in devs:
        await ctx.send("😏")
        await client.close()
        print("Good riddance")
    else:
        await ctx.send("**you lack the power to shut me down**")


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

client.load_extension("cogs.rpg_quest")

client.run(TOKEN)