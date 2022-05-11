import discord
from discord.ext import commands


class WalletTracker(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello World!")

def setup(client):
        client.add_cog(WalletTracker(client))