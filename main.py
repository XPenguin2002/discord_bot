import discord
from discord.ext import commands
import asyncio
import random
import os
import datetime

def read_token_from_file(filename):
    with open(filename, 'r') as file:
        token = file.read().strip()
    return token

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

    filename = '/home/jakub/bot/token.txt'
    TOKEN = read_token_from_file(filename)
    bot = commands.Bot(command_prefix="?", intents=discord.Intents.all(), help_command=commands.DefaultHelpCommand())

#komendy

    @bot.command(name="elo")
    async def elo(ctx):
        await ctx.send(f"Siema {ctx.author.mention}!")

    @bot.command(name="clear")
    @commands.has_permissions(administrator=True)
    async def clear(ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        feedback_message = await ctx.send(f"Usunięto {amount} wiadomości.")
        await asyncio.sleep(5)
        await feedback_message.delete()

#samoistne

    @bot.event
    async def on_ready():
        print(f'bot został włączony')
        print("Komendy zostały włączone")

        while True:
            now = datetime.datetime.now()
            if now.hour == 21 and now.minute == 37:
                channel = discord.utils.get(bot.get_all_channels(), name='2137')
                await send_random_image(channel)
            await asyncio.sleep(60)

    @bot.event
    async def on_member_join(member):
        channel = discord.utils.get(bot.get_all_channels(), name='witaj')
        await channel.send(f'{member.mention} Elooo Elooo Mordeczko!')

    @bot.event
    async def on_member_remove(member):
        channel = discord.utils.get(bot.get_all_channels(), name='witaj')
        await channel.send(f'{member.mention} SPIERDOLIŁ, i tak był z niego tępy CHUJ!')
    
    bot.run(TOKEN)

run_discord_bot()