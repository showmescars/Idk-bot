import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is online')

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs.")
        return False
    return True

@bot.command(name='start')
async def start(ctx):
    pass

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found!")
    else:
        print("Token found! Starting bot...")
        bot.run(TOKEN)
