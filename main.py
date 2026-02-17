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
    "Dracula","Vlad","Carmilla","Lestat","Akasha",
    "Armand","Selene","Lucian","Sonja","Aro",
    "Elijah","Klaus","Damon","Stefan","Katherine"
]

LAST_NAMES = [
    "Tepes","Karnstein","Nightshade","Bloodworth",
    "Blackthorn","Darkmore","Grimwood",
    "Shadowend","Nocturne","Draven",
    "Sanguine","Mortis","Duskbane"
]

# Random vampire events
EVENTS = [
    "A blood moon rises over the vampire council.",
    "Hunters have entered the city searching for vampires.",
    "An ancient vampire awakens from centuries of sleep.",
    "A secret vampire gathering is held at midnight.",
    "A rival clan challenges your lineage.",
    "A forbidden ritual is being performed in the catacombs.",
    "A powerful relic has been discovered.",
    "A vampire lord declares a new rule.",
    "A shadow war begins between covens.",
    "A newly turned vampire loses control."
]

@bot.event
async def on_ready():
    print(f"{bot.user} is online")

# MAKE COMMAND
@bot.command()
async def make(ctx):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)

    name = f"{first} {last}"
    char_id = random.randint(1000, 9999)

    embed = discord.Embed(
        title="Vampire Created",
        color=discord.Color.dark_purple()
    )

    embed.add_field(
        name="Name",
        value=f"`{name}`",
        inline=False
    )

    embed.add_field(
        name="ID",
        value=f"`{char_id}`",
        inline=False
    )

    embed.set_footer(text="A new vampire walks the night")

    await ctx.send(embed=embed)

# RANDOM EVENT COMMAND
@bot.command()
async def random(ctx):
    event = random.choice(EVENTS)

    embed = discord.Embed(
        title="Random Vampire Event",
        description=f"`{event}`",
        color=discord.Color.dark_red()
    )

    await ctx.send(embed=embed)

bot.run(TOKEN)
