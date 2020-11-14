import discord
from discord.ext import commands


class rpg_quest(commands.Cog):

    startup = False
    players = {}
    enemy = None


    def __init__(self, client):
        self.client = client

# Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("RPG Quest is online")

# commands

    #begin
    @commands.command()
    async def begin(self, ctx):
        # commands
        author = ctx.author
        await ctx.send("Wait a bit to play RPG Quest, but in the mean time, I'll tell you the controls. \n"
                       "*choose + option: this will choose an option presented to you \n"
                       "*attack + option + target: this will attack with chosen weapon/spell at chosen target \n"
                       "*items: displays a list of all items acquired \n"
                       "*item + option: use the selected item \n"
                       "*talk + target: will talk to the selected target")
        # setup begin
        num = 12
        while num != 1 or num != 2 or num != 3 or num != 4 or num != 5:
            await ctx.send("How many characters do you wish to have in your party (between 1 and 5)?")
            temp = await self.client.wait_for('message')
            num = temp

        ctx.send("yay")


def setup(client):
    client.add_cog(rpg_quest(client))
