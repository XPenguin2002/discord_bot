import discord
import responses
import random
import os
import datetime
import asyncio
import time

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

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
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user and message.content == 'Ktoś ci pozwolił tu pisać?':
            await asyncio.sleep(10)  # Oczekiwanie 10 sekund
            await message.delete()

        if message.author == client.user:
            return

        if message.channel.name == '2137' and message.author.bot:
            await message.delete()

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if message.channel.name == '2137':
            await message.channel.send('Ktoś ci pozwolił tu pisać?')

        if message.channel.name == '2137':
            #tutaj trzeba dodać że nakładana jest przerwa na tego co wysłał wiadomość
            await message.delete()

    @client.event
    async def on_member_join(member):
        channel = discord.utils.get(member.guild.channels, name='witaj')
        await channel.send(f'Elo elo {member.mention}. Witamy na serwerze.')
        # Tutaj możesz dodać dodatkowe działania, które mają być wykonane po dołączeniu użytkownika

    @client.event
    async def on_member_remove(member):
        channel = discord.utils.get(member.guild.channels, name='witaj')
        await channel.send(f'Zdychaj tam {member.mention}. Nikt płakać za tobą nie będzie.')
        # Tutaj możesz dodać dodatkowe działania, które mają być wykonane po opuszczeniu użytkownika

    @client.event
    async def on_ready():
        while True:
            now = datetime.datetime.now()
            if now.hour == 21 and now.minute == 37:
                channel = discord.utils.get(client.get_all_channels(), name='2137')
                await send_random_image(channel)
            await asyncio.sleep(60)  # Sprawdzaj co minutę

    client.run(TOKEN)