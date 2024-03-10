import discord
import random
import os
import datetime
import asyncio
import time

async def send_random_image(channel):
    directory = "/home/jakub/bot/memes"
    files = os.listdir(directory)
    if len(files) == 0:
        await channel.send("Memy się skończyły. Usunięcie serwera nastąpi za 24h")
        return

    file = random.choice(files)
    file_path = os.path.join(directory, file)
    with open(file_path, "rb") as f:
        await channel.send(file=discord.File(f))

    os.remove(file_path)

def run_discord_bot():
    TOKEN = 'MTEyNzk3ODcwNDc0MDU2MDkyMA.GdqfXV.A0C792dX7BUUGw8Um59FZauHaO2m0LMdLtGDS4'
    intents = discord.Intents.default()
    intents.members = True # enable the members intent
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} jest włączony!')

    @client.event
    async def on_member_join(member):
        channel = discord.utils.get(client.get_all_channels(), name='witaj') # get the channel by name
        await channel.send(f'{member.mention} Elooo Elooo Mordeczko!') # send a welcome message

    @client.event
    async def on_member_remove(member):
        channel = discord.utils.get(client.get_all_channels(), name='witaj') # get the channel by name
        await channel.send(f'{member.mention} SPIERDOLIŁ, i tak był z niego tępy CHUJ!') # send a goodbye message

    @client.event
    async def on_ready():
        while True:
            now = datetime.datetime.now()
            if now.hour == 21 and now.minute == 37:
                channel = discord.utils.get(client.get_all_channels(), name='2137')
                await send_random_image(channel)
            await asyncio.sleep(60)  # Sprawdzaj co minutę

    client.run(TOKEN)