import os
from datetime import datetime
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
        if("https://twitter.com/" in message.content and "/status/" in message.content):
            #To maintain original message, find twitter link index
            twit_idx = message.content.index("https://twitter") + 8
            new_message = f"From {message.author.mention}: {message.content[0:twit_idx]}vx{message.content[twit_idx:]}"
            #await message.channel.send(new_message.split("?", 1)[0])
            await message.delete()
        elif("https://x.com" in message.content and "/status/" in message.content):
            #To maintain original message, find x link index
            x_idx = message.content.index("https://x") + 8
            new_message = f"From {message.author.mention}: {message.content[0:x_idx]}fixv{message.content[x_idx:]}"
            #await message.channel.send(new_message.split("?", 1)[0])
            await message.delete()
    except Exception as e:
        logger.error(f"{datetime.now()}: {e}\t{message}")
        
client.run(TOKEN)