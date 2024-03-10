import discord
from discord.ext import commands
import asyncio

def run_discord_bot():
    TOKEN = 'MTEyNzk3ODcwNDc0MDU2MDkyMA.GdqfXV.A0C792dX7BUUGw8Um59FZauHaO2m0LMdLtGDS4'
    bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print("Komendy zostały włączone")

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
    
    bot.run(TOKEN)