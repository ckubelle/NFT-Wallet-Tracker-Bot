import discord
import time
import os
from discord.ext import commands
from etherscan import Etherscan
from dotenv import load_dotenv
from discord.ext import tasks
from datetime import datetime

class WalletTracker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dict_wallets = {}
        self.nftcheck.start()

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
            message = "This nickname is already being tracked. Try using a different nickname to add this address"
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

    @tasks.loop(seconds = 100) 
    async def nftcheck(self):
        curr_time = int(time.time())
        ETHERSCAN_KEY = os.getenv('ETHERSCAN_KEY')
        CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
        eth = Etherscan(ETHERSCAN_KEY) 

        for address in self.dict_wallets:

            transactions = eth.get_normal_txs_by_address_paginated(address=self.dict_wallets[address], startblock=14043957, endblock=99999999, page=1, offset=5, sort="desc")

            os_address = "0x7f268357a8c2552623316e2562d90e642bb538e5"
                          
            for transaction in transactions:

                if int(transaction["timeStamp"]) < (curr_time - 150):
                    break

                if transaction["to"] == os_address:
                    channel = self.client.get_channel(CHANNEL_ID)

                    embed = discord.Embed(
                        title = address + " Bought a NFT",
                        url = f"https://opensea.io/{address}?tab=activity&search[chains][0]=ETHEREUM&search[eventTypes][0]=AUCTION_SUCCESSFUL",
                        timestamp = datetime.now()
                    )

                    embed.add_field(name="Price Paid", value=str(float(transaction["value"]) / 1E18), inline=False)
                    embed.add_field(name="Etherscan", value=f"https://etherscan.io/tx/{transaction['hash']}", inline=False)

                    await channel.send(embed=embed)

def setup(client):
        client.add_cog(WalletTracker(client))