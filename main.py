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

def generate_command_list(bot):
    command_list = []
    for command in bot.commands:
        if command.description:
            command_list.append(f"{command.name}: {command.description}")
        else:
            command_list.append(f"{command.name}")
    return "\n".join(command_list)

def run_discord_bot():

    filename = '/home/jakub/bot/token.txt'
    TOKEN = read_token_from_file(filename)
    bot = commands.Bot(command_prefix="?", intents=discord.Intents.all(), help_command=commands.DefaultHelpCommand())
    bot.remove_command('help')

#komendy

    @bot.command(name="elo", description="Wysyła powitanie do użytkownika.")
    async def elo(ctx):
        await ctx.send(f"Siema {ctx.author.mention}!")

    @bot.command(name="clear", description="Usuwa określoną ilość wiadomości.")
    @commands.has_permissions(administrator=True)
    async def clear(ctx, amount: int):
        if 0 < amount < 16:
            await ctx.channel.purge(limit=amount + 1)
            feedback_message = await ctx.send(f"Usunięto {amount} wiadomości.")
            await asyncio.sleep(3)
            await feedback_message.delete()
        else:
            feedback_message = await ctx.send("Wpisz liczbę od 1 do 15.")
            await asyncio.sleep(3)
            await feedback_message.delete()

    @bot.command(name="help", description="Wyświetla dostępne komendy.")
    async def help(ctx):
        command_list = generate_command_list(bot)
        await ctx.send(f"Dostępne komendy:\n```\n{command_list}\n```")

    @bot.slash_command(name="sekret",guild_ids=[315430106271186944,1128678715744849953])
    async def sekret(ctx):
        await ctx.respond(f"żyję",ephemeral=True)

#samoistne

    @bot.event
    async def on_ready():
        print(f'bot został włączony')

        try:
            loaded_commands=0
            for command in bot.commands:
                loaded_commands += 1
            print(f'Załadowano {loaded_commands} komend')
        except Exception as e:
            print(e)

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
