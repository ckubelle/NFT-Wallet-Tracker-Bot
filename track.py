import discord
from discord.ext import commands


class WalletTracker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dict_wallets = {}

    @commands.command()
    async def print(self, ctx):

        if not self.dict_wallets:
            await ctx.send("It appears no wallets are being tracked! Use the -add command")
            return
        
        await ctx.send("Printing wallets that are being tracked:")

        for wallet in self.dict_wallets:
            message = wallet + " " +  self.dict_wallets[wallet]
            await ctx.send(message)

    @commands.command()
    async def add(self, ctx, nickname, wallet = ""):

        if nickname in self.dict_wallets:
            message = f"This nickname is already being tracked. Try using a different nickname to add this address"
            await ctx.send(message)
            return

        if wallet:
            self.dict_wallets[nickname] = wallet
        else:
            message = f"The following nickname {nickname} was not added because of improper arguments"
            await ctx.send(message)
        
    @commands.command()
    async def remove(self, ctx, nickname):
        if nickname in self.dict_wallets:
            del self.dict_wallets[nickname]
        else:
            message = f"The following nickname {nickname} was not deleted because it couldn't find it. Try again"
            await ctx.send(message)

    @commands.command()
    async def clear(self, ctx):
        self.dict_wallets.clear()
        message = "All addresses have been removed!"
        await ctx.send(message)

def setup(client):
        client.add_cog(WalletTracker(client))