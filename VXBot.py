import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

@client.event
async def on_message(message):
    if(message.author.id == client.user.id):
        return
    if("https://twitter.com/" in message.content):
        new_message = "From " + message.author.display_name + " " + message.content[0:8] + "vx" + message.content[8:]
        channel = message.channel
        await channel.send(new_message, silent=True)
        await message.delete()
        
client.run(TOKEN)