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

VAMPIRES_FILE = 'vampires.json'

VAMPIRE_FIRST_NAMES = [
    "Dracula", "Vlad", "Lestat", "Armand", "Louis", "Akasha", "Marius", "Kain",
    "Alucard", "Selene", "Blade", "Viktor", "Marcus", "Amelia", "Sonja", "Lucian",
    "Nosferatu", "Carmilla", "Erzsebet", "Lilith", "Cain", "Abel", "Seras", "Integra",
    "D", "Rayne", "Astaroth", "Malachi", "Corvinus", "Demetrius", "Theron", "Sanctus",
    "Nyx", "Raven", "Eclipse", "Crimson", "Shadow", "Obsidian", "Scarlet", "Vesper"
]

VAMPIRE_LAST_NAMES = [
    "Tepes", "Drăculești", "de Lioncourt", "Romanus", "de Pointe du Lac", "Blackwood",
    "Nightshade", "Bloodmoon", "Darkholme", "von Carstein", "Ravenscroft", "Thornheart",
    "Ashborne", "Grimveil", "Shadowfang", "Crimsonbane", "Duskwalker", "Bloodworth",
    "Blackthorn", "Nightingale", "Darkmore", "Bloodstone", "Shadowmere", "Ravenclaw",
    "Grimshaw", "Nightfall", "Duskwood", "Ashwood", "Ironblood", "Stormveil"
]

VAMPIRE_CLANS = [
    "Nosferatu", "Ventrue", "Tremere", "Toreador", "Brujah", "Malkavian",
    "Gangrel", "Tzimisce", "Lasombra", "Setite", "Giovanni", "Ravnos",
    "Assamite", "Salubri", "Cappadocian", "Blood Moon", "Shadow Council",
    "Crimson Court", "Night Legion", "Dark Covenant"
]

def load_vampires():
    if os.path.exists(VAMPIRES_FILE):
        with open(VAMPIRES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_vampires(vampires):
    with open(VAMPIRES_FILE, 'w') as f:
        json.dump(vampires, f, indent=4)

vampires = load_vampires()

def generate_vampire_stats():
    return {
        "strength": random.randint(50, 100),
        "speed": random.randint(50, 100),
        "intelligence": random.randint(50, 100),
        "blood_power": random.randint(50, 100),
        "defense": random.randint(50, 100)
    }

def calculate_power(stats):
    return sum(stats.values())

def create_vampire(owner_id, owner_name):
    first_name = random.choice(VAMPIRE_FIRST_NAMES)
    last_name = random.choice(VAMPIRE_LAST_NAMES)
    clan = random.choice(VAMPIRE_CLANS)
    stats = generate_vampire_stats()
    
    vampire = {
        "id": f"vamp_{owner_id}_{int(datetime.now().timestamp() * 1000)}",
        "name": f"{first_name} {last_name}",
        "clan": clan,
        "stats": stats,
        "power": calculate_power(stats),
        "owner_id": owner_id,
        "owner_name": owner_name,
        "created_at": datetime.now().isoformat()
    }
    
    return vampire

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Vampire Bot Ready')
    print('Command prefix: ?')

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True

@bot.command(name='make')
async def make_vampire(ctx):
    """Create a random vampire"""
    user_id = str(ctx.author.id)
    
    vampire = create_vampire(user_id, str(ctx.author))
    
    if user_id not in vampires:
        vampires[user_id] = []
    
    vampires[user_id].append(vampire)
    save_vampires(vampires)
    
    v = vampire
    embed = discord.Embed(
        title="🧛 Vampire Created!",
        description=f"**{v['name']}** has risen from the grave!",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="Clan", value=v['clan'], inline=True)
    embed.add_field(name="Power", value=v['power'], inline=True)
    embed.add_field(name="ID", value=f"`{v['id']}`", inline=False)
    embed.add_field(name="Stats", value=f"**Strength:** {v['stats']['strength']}\n**Speed:** {v['stats']['speed']}\n**Intelligence:** {v['stats']['intelligence']}\n**Blood Power:** {v['stats']['blood_power']}\n**Defense:** {v['stats']['defense']}", inline=False)
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found!")
        print("Create a .env file with DISCORD_TOKEN=your_token")
    else:
        print("Token found! Starting Vampire Bot...")
        bot.run(TOKEN)
