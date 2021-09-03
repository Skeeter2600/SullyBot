import discord
import random
# import youtube_dl
from discord.ext import commands
import json
from smash.smash import Singles, Doubles, Fighter
import sys

TOKEN = json.loads(open("json/TOKEN_ID.json", "r").read()).get("TOKEN")

client = commands.Bot(command_prefix="*")
players = {}
smashers = []
smash_queue = []
playersPerGame = 2
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


# --------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server. Get the chalice ready, NotSoBot.')


# --------------------------------------------------------------------------------------------------------------------
@client.event
async def on_member_remove(member):
    print("Hasta la vista, " + f'{member}')


# --------------------------------------------------------------------------------------------------------------------
@client.command()
async def ping(ctx):
    if client.latency * 1000 > 500:
        await ctx.send(f' Dayum, yo internet slow as fuck "( {round(client.latency * 1000)} ms )"')
    else:
        await ctx.send(f' You good ( {round(client.latency * 1000)} ms )')


# --------------------------------------------------------------------------------------------------------------------
@client.command()
async def pong(ctx):
    await ctx.send("Ping!!!!!!!!!")


# --------------------------------------------------------------------------------------------------------------------
@client.command()
async def advise(ctx, *, question):
    answers = json.loads(open("responses/questions.json", "r").read()).get("answers")
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(answers)}')


# --------------------------------------------------------------------------------------------------------------------
@client.command(aliases=['hi'])
async def hello(ctx):
    hellos = json.loads(open("responses/hellos.json", "r").read()).get("hellos")
    await ctx.send(random.choice(hellos))
   

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
        # smash_queue_pointer += 1


# --------------------------------------------------------------------------------------------------------------------
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


# --------------------------------------------------------------------------------------------------------------------
@client.command()
async def start(ctx, extension):
    client.load_extension(f'cogs.{extension}')


# --------------------------------------------------------------------------------------------------------------------
@client.command()
async def end(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


# --------------------------------------------------------------------------------------------------------------------
@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


# --------------------------------------------------------------------------------------------------------------------
@client.command(aliases=['disconnect'])
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()


# --------------------------------------------------------------------------------------------------------------------
@client.command()
async def dev(ctx, condition, person):
    try:
        user = client.get_user(int(person[3: len(person) - 1]))
    except ValueError:
        await ctx.send(f'User "{person}" doesn\'t exist. Mention one that does...')

    if user != None:
        devs = json.loads(open("json/devs.json", "r").read())
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
        open("json/devs.json", "w").write(json.dumps(devs))
    else:
        await ctx.send(f"User \"{person}\"doesn't exist. Mention one that does...")


@client.command(aliases=["quit", "q", "kil", "kill", "die"])
async def close(ctx):
    devs = json.loads(open("json/devs.json", "r").read()).get("devs")
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

client.load_extension("cogs.smashCog")
client.load_extension("cogs.rpg_quest")

client.run(TOKEN)
