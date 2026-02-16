import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

WOLVES_FILE = 'wolves.json'

WOLF_FIRST_NAMES = [
    "Fenrir", "Lycaon", "Ragnar", "Alaric", "Gunnar", "Bjorn", "Sigurd", "Leif",
    "Ulfric", "Thorin", "Aldric", "Wulfgar", "Draven", "Kael", "Zephyr", "Cain",
    "Lucan", "Darian", "Vance", "Rowan", "Hadrian", "Cormac", "Bram", "Eldric",
    "Soren", "Magnus", "Ragnor", "Ivar", "Floki", "Orm", "Vidar", "Tyr",
    "Hati", "Skoll", "Geri", "Freki", "Amarok", "Akela", "Lobo", "Fang"
]

WOLF_LAST_NAMES = [
    "Blackfang", "Ironpelt", "Bloodmoon", "Grayclaw", "Darkwood", "Stonehowl",
    "Nightprowl", "Ashcoat", "Embermane", "Frostbite", "Duskrunner", "Grimclaw",
    "Shadowpelt", "Ravencoat", "Thornfang", "Wolfsbane", "Moonshard", "Starclaw",
    "Wildmane", "Bonecrusher", "Icefang", "Firepelt", "Stormhowl", "Voidclaw",
    "Splitfang", "Rustcoat", "Mudpelt", "Copperback", "Slateclaw", "Cragmane"
]


def load_wolves():
    if os.path.exists(WOLVES_FILE):
        with open(WOLVES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_wolves(wolves):
    with open(WOLVES_FILE, 'w') as f:
        json.dump(wolves, f, indent=4)

def generate_unique_id():
    wolves = load_wolves()
    existing_ids = {w.get('wolf_id') for w in wolves.values() if 'wolf_id' in w}
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing_ids:
            return new_id

def get_strength_label(strength):
    if strength <= 20:   return "Pup"
    elif strength <= 40: return "Scrapper"
    elif strength <= 60: return "Packmate"
    elif strength <= 80: return "Alpha"
    else:                return "Apex"


@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Werewolf Bot Ready')

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs.")
        return False
    return True


@bot.command(name='wolf')
async def make_wolf(ctx):
    """Create a new werewolf. Usage: ?wolf"""
    wolves  = load_wolves()
    wolf_id = generate_unique_id()

    name     = f"{random.choice(WOLF_FIRST_NAMES)} {random.choice(WOLF_LAST_NAMES)}"
    strength = random.randint(1, 100)
    label    = get_strength_label(strength)

    wolf_data = {
        "wolf_id":    wolf_id,
        "name":       name,
        "username":   str(ctx.author),
        "user_id":    str(ctx.author.id),
        "strength":   strength,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    wolves[wolf_id] = wolf_data
    save_wolves(wolves)

    embed = discord.Embed(
        title=name,
        description=f"Owner: {ctx.author.name}\nID: `{wolf_id}`",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="Strength", value=str(strength), inline=True)
    embed.add_field(name="Class",    value=label,          inline=True)

    await ctx.send(embed=embed)


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found!")
        print("For local: Create a .env file with DISCORD_TOKEN=your_token")
        print("For Railway: Add DISCORD_TOKEN in the Variables tab")
    else:
        print("Token found! Starting bot...")
        bot.run(TOKEN)
