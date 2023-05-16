import discord
import asyncio
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
discord_token = [Ton Token discord]

@client.event
async def on_ready():
    chan = client.get_channel(1088542436558639104)
    while True:
        await asyncio.sleep(3)
        await channel.send("<@463652129878573056>")

client.run(os.environ['TOKEN'])
