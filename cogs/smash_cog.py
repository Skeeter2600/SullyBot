import discord
import random

from discord.ext import commands
from smash.smash import Singles, Doubles

smashers = []
smash_queue = None
playersPerGame = 2


class smash_cog(commands.Cog):

    # Constructor
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Smash Cog is online")

    # Commands
    @commands.command()
    async def smash(self, ctx, condition, arg=None):
        global smashers
        global smash_queue
        global playersPerGame
        person_cmd = ["add", "drop", "remove"]
        if condition == "clear":
            smashers = []
            smash_queue = []
            await ctx.send("The roster was cleared")
        elif condition == "roster":
            if len(smashers) == 0:
                await ctx.send("The smash roster is currently empty!")
            else:
                msg = ""
                for i in range(len(smashers)):
                    msg += f'{smashers[i].name}'
                    if i + 1 != len(smashers):
                        msg += ", "
                await ctx.send("Current smash roster: " + msg)
        elif condition == "players":
            # Here arg is used to hold the number of players
            if arg is None:
                await ctx.send(str(playersPerGame) + " players currently play in each singles game.")
            elif arg is not None:
                num = int(arg)
                if 4 >= num > 1:
                    playersPerGame = num
                    await ctx.send("OK, singles games will now have " + str(playersPerGame) + " players per game.")
                else:
                    await ctx.send("Singles games can only have 2 to 4 per game!")
        elif condition in person_cmd:
            # Here arg is used to hold the user id of the player
            player = self.client.get_user(int(arg[3: len(arg) - 1]))
            if player is not None:
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
                            f'{player.name} was dropped from the roster. Please make a new fight queue to see the '
                            f'update.')
                    else:
                        await ctx.send(f'{player.name} isn\'t in the queue stupid!')
            else:
                await ctx.send(f"User \"{player.name}\"doesn't exist. Mention one that does...")

    @commands.command()
    async def fight(self, ctx, fight_type):
        global smash_queue
        global smashers
        global playersPerGame

        smash_queue = None

        if len(smashers) == 0:
            await ctx.send("Gotta add people to the roster in order to fight, retard (if we used the word)!")
        elif len(smashers) == 1:
            await ctx.send("It's not good to play with yourself. Add others to the roster.")
        elif len(smashers) > 8:
            await ctx.send("You can't fit more than 8 people in a lobby! Try removing one or two...")
        else:
            if len(smashers) < 3:
                await ctx.send("Do you really need my help with this? Either fight by yourselves or rotate.")

            # Singles Fights (1v1 or FFA)
            if fight_type == "singles":
                smash_queue = Singles(smashers, playersPerGame)
                await self.next_fight(ctx)

            # 2 on 2 fights
            elif fight_type == "doubles":
                if len(smashers) < 4:
                    await ctx.send("You can't do doubles with less than 4 people!")
                else:
                    smash_queue = Doubles(smashers)
                    await self.next_fight(ctx)

    @commands.command()
    async def next_fight(self, ctx):
        fight_flares = ["! I heard that ",
                        " , watch out for the uppercuts!",
                        "! 5 brownie points if ",
                        "! This'll be boring. Let me know when it's over",
                        "! Who cares?",
                        "! This should be interesting",
                        "! Maybe the match up will be better for ",
                        "! Imagine thinking "]
        global smash_queue
        flare = random.randint(0, 7)

        if isinstance(smash_queue, Singles):
            q = smash_queue.generate()
            c = 0
            s = "Next up: "

            while c < (len(q) - 1):
                s += q[c].getUser().mention + ", "
                c += 1
            s += q[-1].getUser().mention + "."

            await ctx.send(s)

        elif isinstance(smash_queue, Doubles):
            q = smash_queue.generate()
            await ctx.send(
                "Next up: " + q[0].getUser().mention + " and " + q[1].getUser().mention + " vs. " +
                q[2].getUser().mention + " and " + q[3].getUser().mention
            )


def setup(client):
    client.add_cog(smash_cog(client))
