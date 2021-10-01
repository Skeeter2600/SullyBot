import random

import discord
from discord import Reaction
from discord.ext import commands
from discord.ext.commands import bot

import json

TOKEN = json.loads(open("json/TOKEN_ID.json", "r").read()).get("TOKEN")

client = commands.Bot(command_prefix="~")


@client.event
async def on_ready():
    activity = discord.Game(name="Just Chilling")
    await client.change_presence(activity=activity, status=discord.Status.online)
    print("I'm back, baybee")


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
        await ctx.send(f' Dayum, yo internet slow : "( {round(client.latency * 1000)} ms )"')
    else:
        await ctx.send(f' You good : ( {round(client.latency * 1000)} ms )')


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


# --------------------------------------------------------------------------------------------------------------------

@client.command()
async def image(ctx, message):
    if message == "🥺":
        reaction = json.loads(open("responses/funtext.json", "r").read()).get("🥺")
        await ctx.send(reaction)
    elif message == "jerkoff":
        reaction = json.loads(open("responses/funtext.json", "r").read()).get("jerkoff")
        await ctx.send(reaction)
    elif message == "daffy":
        reaction = json.loads(open("responses/funtext.json", "r").read()).get("daffy")
        await ctx.send(reaction)
    elif message == "quagsire":
        image_number = random.randint(1, 3)
        with open('etc/images/quagsire' + image_number + '.jpg', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(picture)


# --------------------------------------------------------------------------------------------------------------------

@client.command()
async def start(extension):
    client.load_extension(f'cogs.{extension}')


# --------------------------------------------------------------------------------------------------------------------

@client.command()
async def end(extension):
    client.unload_extension(f'cogs.{extension}')


# --------------------------------------------------------------------------------------------------------------------

@client.command()
async def dev(ctx, condition, person):
    try:
        user = client.get_user(int(person[3: len(person) - 1]))
    except ValueError:
        await ctx.send(f'User "{person}" doesn\'t exist. Mention one that does...')

    if user is not None:
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


# --------------------------------------------------------------------------------------------------------------------

@client.command(aliases=["quit", "kil", "kill", "die"])
async def close(ctx):
    devs = json.loads(open("json/devs.json", "r").read()).get("devs")
    if ctx.author.id in devs:
        await ctx.send("😏")
        await client.close()
        print("Good riddance")
    else:
        await ctx.send("**you lack the power to shut me down**")


# --------------------------------------------------------------------------------------------------------------------

@client.event
async def on_raw_reaction_add(reaction, user):
    thumbs_up_count = 0
    channel_main = json.loads(open("json/dankest.json", "r").read()).get("terrabites main")
    if await reaction.channel_id == channel_main:
        reactions = reaction.message_id
        for reaction in reactions:
            if reaction == ":thumbsup:":
                thumbs_up_count += 1
        if thumbs_up_count == 4:
            message_content = reaction.message.content
            dankest_channel = json.loads(open("json/dankest.json", "r").read()).get("terrabites dank")
            await dankest_channel.send(message_content)


# --------------------------------------------------------------------------------------------------------------------

client.load_extension("cogs.smash_cog")
client.load_extension("cogs.rpg_quest")
client.load_extension("cogs.music_cog")

client.run(TOKEN)
