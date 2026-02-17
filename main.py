import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import os

# Load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)

# Name pools
FIRST_NAMES = [
    "Dracula", "Vlad", "Carmilla", "Lestat", "Akasha",
    "Armand", "Selene", "Lucian", "Sonja", "Aro",
    "Elijah", "Klaus", "Damon", "Stefan", "Katherine"
]

LAST_NAMES = [
    "Tepes", "Karnstein", "Nightshade", "Bloodworth",
    "Blackthorn", "Darkmore", "Grimwood",
    "Shadowend", "Nocturne", "Draven",
    "Sanguine", "Mortis", "Duskbane"
]

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
async def make(ctx):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"

    await ctx.send(f"🧛 Your vampire name is: **{name}**")

bot.run(TOKEN)
