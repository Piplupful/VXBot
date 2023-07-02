import os
import datetime
import logging
import logging.handlers

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler("log/errors.log", maxBytes=1024, backupCount=2)
logger.addHandler(handler)

@client.event
async def on_message(message):
    try:
        if(message.author.id == client.user.id):
            return
        if("https://twitter.com/" in message.content):
            new_message = f"From {message.author.mention} {message.content[0:8]}vx{message.content[8:]}"
            await message.channel.send(new_message, silent=True)
            await message.delete()
    except Exception as e:
        logger.error(f"{datetime.now()}: {e}\t{message}")
        
client.run(TOKEN)