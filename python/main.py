import discord
from discord.ext import commands
import asyncio
import random
import os
import datetime

last_sent_date = None

def read_token_from_file(filename):
    with open(filename, 'r') as file:
        token = file.read().strip()
    return token

async def send_random_image(channel):
    global last_sent_date
    directory = 'memes'
    files = os.listdir(directory)
    if len(files) == 0:
        await channel.send("Memy się skończyły. Usunięcie serwera nastąpi za 24h")
        return

    file = random.choice(files)
    file_path = os.path.join(directory, file)
    with open(file_path, "rb") as f:
        await channel.send(file=discord.File(f))

    os.remove(file_path)

    now = datetime.datetime.now()
    last_sent_date = now.date()

def generate_command_list(bot):
    command_list = []
    for command in bot.commands:
        if command.description:
            command_list.append(f"{command.name}: {command.description}")
        else:
            command_list.append(f"{command.name}")
    return "\n".join(command_list)

def run_discord_bot():

    filename = 'token.txt'
    TOKEN = read_token_from_file(filename)
    bot = commands.Bot(command_prefix="?", intents=discord.Intents.all(), help_command=commands.DefaultHelpCommand())
    bot.remove_command('help')

#komendy


    @bot.command(name="muzyka", description="Odtwarza utwór o podanym numerze.")
    async def muzyka(ctx, numer):
        voice_channel = None

        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
        else:
            await ctx.send("Nie jesteś na żadnym kanale głosowym.")
            return

        try:
            voice_channel = await voice_channel.connect()

            # Odtwarzaj wybrany plik audio
            if numer == "1":
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="videoplayback.m4a"))
            elif numer == "2":
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="videoplayback2.m4a"))

            while voice_channel.is_playing():
                await asyncio.sleep(1)

            # Sprawdź, czy bot nadal jest połączony przed rozłączeniem
            if voice_channel.is_connected():
                await voice_channel.disconnect()
        except Exception as e:
            print(e)
            await ctx.send("Wystąpił problem podczas odtwarzania.")

    @bot.command(name="stop", description="Zatrzymuje odtwarzanie i wychodzi z kanału głosowego.")
    async def stop(ctx):
        voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)

        if voice_channel and voice_channel.is_playing():
            voice_channel.stop()
            await voice_channel.disconnect()
            await ctx.send("Odtwarzanie zatrzymane, bot opuścił kanał.")
        else:
            await ctx.send("Nic nie jest odtwarzane lub bot nie jest na żadnym kanale.")



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

    #@bot.slash_command(name="sekret",guild_ids=[315430106271186944,1128678715744849953])
    #async def sekret(ctx):
        #await ctx.respond(f"żyję",ephemeral=True)

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

        #while True:
            #now = datetime.datetime.now()
            #if now.hour == 21 and now.minute == 37 and (last_sent_date is None or last_sent_date < now.date()):
                #channel = discord.utils.get(bot.get_all_channels(), name='2137')
                #await send_random_image(channel)
            #await asyncio.sleep(60)

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
