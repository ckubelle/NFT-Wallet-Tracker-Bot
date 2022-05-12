import discord
import os
import track
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

cogs = [track]

client = commands.Bot(command_prefix='-')

for i in range(len(cogs)):
    cogs[i].setup(client)


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
client.run(DISCORD_TOKEN)