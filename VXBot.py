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

async def send_message(original_message, fixed_message):
    await original_message.channel.send(fixed_message)
    await original_message.delete()

@client.event
async def on_message(message):
    try:
        if(message.author.id == client.user.id):
            return
        
        new_message = None

        if("https://twitter.com/" in message.content and "/status/" in message.content):
            #To maintain original message, find twitter link index
            twit_idx = message.content.index("https://twitter") + 8
            new_message = f"From {message.author.mention}: {message.content[0:twit_idx]}vx{message.content[twit_idx:]}"
        elif("https://x.com" in message.content and "/status/" in message.content):
            #To maintain original message, find x link index
            x_idx = message.content.index("https://x") + 8
            new_message = f"From {message.author.mention}: {message.content[0:x_idx]}vxtwitter{message.content[x_idx + 1:]}"
        elif("https://www.tiktok.com/" in message.content):
            #To maintain original message, find o in tiktok index
            tik_idx = message.content.index("https://www.tiktok") + 16
            new_message = f"From {message.author.mention}: {message.content[0:tik_idx]}x{message.content[tik_idx + 1:]}"
        
        if new_message:
            await send_message(message, new_message)
            
    except Exception as e:
        logger.error(f"{datetime.now()}: {e}\t{message}")
        
client.run(TOKEN)