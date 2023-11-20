# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime, timedelta, time

load_dotenv()

environmentConfig: dict = dict(
    token = os.getenv('DISCORD_TOKEN'),
    guild = os.getenv('DISCORD_GUILD'),
    user = os.getenv('PERDEZH_USER'),
    fixCommandName = os.getenv('FIX_COMMAND_NAME'),
    timeoutDuration = int(os.getenv('TIMEOUT_DURATION'))
)

botState: dict = dict(
    lastShuffle = datetime.min
)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def shuffleIvan(message: discord.Message):
    if environmentConfig["fixCommandName"] in message.content:
        guild: discord.Guild = discord.utils.find(lambda g: g.name == environmentConfig["guild"], client.guilds)
        ivanUser: discord.User = discord.utils.find(lambda g: g.global_name == environmentConfig["user"], guild.members)

        withIvanChannel: discord.ChannelType = None
        woIvanChannel: discord.ChannelType = None
    
        for channel in guild.channels:
            if channel.type == discord.ChannelType.voice:
            
                if discord.utils.find(lambda g: g.global_name == environmentConfig["user"], channel.members):
                    withIvanChannel = channel
                elif not woIvanChannel:
                    woIvanChannel = channel

                if withIvanChannel and woIvanChannel:
                    break
    
        if withIvanChannel and woIvanChannel:
            try:
                await ivanUser.move_to(woIvanChannel)
                await ivanUser.move_to(withIvanChannel)
            except err:
                print(err)

@client.event
async def on_ready():    
    print(f'Bot runned')


@client.event
async def on_message(message: discord.Message):

    currentDateTime: datetime = datetime.now()
    
    if (currentDateTime - botState["lastShuffle"]).total_seconds() >= int(environmentConfig["timeoutDuration"]) * 60:
        botState["lastShuffle"] = currentDateTime
        await shuffleIvan(message)

client.run(environmentConfig["token"])