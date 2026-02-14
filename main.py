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

MISSIONS = [
    {
        "name": "Hunt in the Dark Alley",
        "description": "Your vampire prowls the dark alleys looking for prey",
        "difficulty": "easy"
    },
    {
        "name": "Raid the Blood Bank",
        "description": "A risky mission to steal fresh blood from the hospital",
        "difficulty": "medium"
    },
    {
        "name": "Challenge the Elder Vampire",
        "description": "Face off against an ancient and powerful vampire",
        "difficulty": "hard"
    },
    {
        "name": "Defend Your Territory",
        "description": "Enemy vampires are invading your hunting grounds",
        "difficulty": "medium"
    },
    {
        "name": "Infiltrate the Vampire Council",
        "description": "Sneak into the secret meeting of vampire elders",
        "difficulty": "hard"
    },
    {
        "name": "Hunt the Werewolf Pack",
        "description": "Ancient enemies cross paths in the forest",
        "difficulty": "hard"
    },
    {
        "name": "Scavenge the Graveyard",
        "description": "Search for mystic artifacts among the tombstones",
        "difficulty": "easy"
    },
    {
        "name": "Battle in the Underground Arena",
        "description": "Fight for glory in the secret vampire fighting pits",
        "difficulty": "medium"
    }
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
        "wins": 0,
        "losses": 0,
        "created_at": datetime.now().isoformat()
    }
    
    return vampire

def create_ai_vampire(difficulty):
    """Create an AI vampire based on difficulty"""
    first_name = random.choice(VAMPIRE_FIRST_NAMES)
    last_name = random.choice(VAMPIRE_LAST_NAMES)
    clan = random.choice(VAMPIRE_CLANS)
    
    # Scale stats based on difficulty
    if difficulty == "easy":
        stat_range = (40, 80)
    elif difficulty == "medium":
        stat_range = (60, 90)
    else:  # hard
        stat_range = (70, 110)
    
    stats = {
        "strength": random.randint(stat_range[0], stat_range[1]),
        "speed": random.randint(stat_range[0], stat_range[1]),
        "intelligence": random.randint(stat_range[0], stat_range[1]),
        "blood_power": random.randint(stat_range[0], stat_range[1]),
        "defense": random.randint(stat_range[0], stat_range[1])
    }
    
    return {
        "name": f"{first_name} {last_name}",
        "clan": clan,
        "stats": stats,
        "power": calculate_power(stats),
        "is_ai": True
    }

def simulate_battle(vampire1, vampire2):
    """Simulate a battle between two vampires"""
    v1_combat = (
        vampire1['stats']['strength'] * 0.3 +
        vampire1['stats']['speed'] * 0.2 +
        vampire1['stats']['blood_power'] * 0.3 +
        vampire1['stats']['defense'] * 0.2
    ) * random.uniform(0.85, 1.15)
    
    v2_combat = (
        vampire2['stats']['strength'] * 0.3 +
        vampire2['stats']['speed'] * 0.2 +
        vampire2['stats']['blood_power'] * 0.3 +
        vampire2['stats']['defense'] * 0.2
    ) * random.uniform(0.85, 1.15)
    
    if v1_combat > v2_combat:
        winner = vampire1
        loser = vampire2
        margin = v1_combat - v2_combat
    else:
        winner = vampire2
        loser = vampire1
        margin = v2_combat - v1_combat
    
    return {
        "winner": winner,
        "loser": loser,
        "margin": margin,
        "v1_score": round(v1_combat, 2),
        "v2_score": round(v2_combat, 2)
    }

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
    vampire_number = len(vampires[user_id])
    
    embed = discord.Embed(
        title="🧛 Vampire Created!",
        description=f"**{v['name']}** has risen from the grave!",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="Clan", value=v['clan'], inline=True)
    embed.add_field(name="Power", value=v['power'], inline=True)
    embed.add_field(name="Record", value=f"{v['wins']}W - {v['losses']}L", inline=True)
    embed.add_field(name="Number", value=f"#{vampire_number}", inline=False)
    embed.add_field(name="Stats", value=f"**Strength:** {v['stats']['strength']}\n**Speed:** {v['stats']['speed']}\n**Intelligence:** {v['stats']['intelligence']}\n**Blood Power:** {v['stats']['blood_power']}\n**Defense:** {v['stats']['defense']}", inline=False)
    embed.set_footer(text=f"Use ?mission {vampire_number} to send on a mission!")
    
    await ctx.send(embed=embed)

@bot.command(name='list')
async def list_vampires(ctx):
    """View all your vampires"""
    user_id = str(ctx.author.id)
    
    if user_id not in vampires or len(vampires[user_id]) == 0:
        await ctx.send("❌ You don't have any vampires yet! Use `?make` to create one.")
        return
    
    user_vamps = vampires[user_id]
    
    embed = discord.Embed(
        title=f"🧛 {ctx.author.name}'s Vampires",
        description=f"Total: {len(user_vamps)} vampires",
        color=discord.Color.dark_red()
    )
    
    for idx, v in enumerate(user_vamps, 1):
        embed.add_field(
            name=f"#{idx} - {v['name']}",
            value=f"Clan: {v['clan']}\nPower: {v['power']}\nRecord: {v['wins']}W - {v['losses']}L",
            inline=True
        )
    
    embed.set_footer(text="Use ?mission <number> to send a vampire on a mission!")
    
    await ctx.send(embed=embed)

@bot.command(name='mission')
async def send_mission(ctx, vampire_number: int):
    """Send your vampire on a random mission to fight AI vampires"""
    
    # Find the vampire by number
    user_id = str(ctx.author.id)
    
    if user_id not in vampires or len(vampires[user_id]) == 0:
        await ctx.send("❌ You don't have any vampires! Use `?make` to create one.")
        return
    
    if vampire_number < 1 or vampire_number > len(vampires[user_id]):
        await ctx.send(f"❌ Invalid vampire number! You have {len(vampires[user_id])} vampires. Use `?list` to see them.")
        return
    
    found_vampire = vampires[user_id][vampire_number - 1]
    
    # Select random mission
    mission = random.choice(MISSIONS)
    
    # Create AI opponent
    ai_vampire = create_ai_vampire(mission['difficulty'])
    
    # Simulate battle
    result = simulate_battle(found_vampire, ai_vampire)
    
    # Update player vampire stats
    if result['winner'] == found_vampire:
        found_vampire['wins'] += 1
        outcome = "VICTORY"
        outcome_color = discord.Color.green()
        outcome_icon = "✅"
    else:
        found_vampire['losses'] += 1
        outcome = "DEFEAT"
        outcome_color = discord.Color.red()
        outcome_icon = "❌"
    
    save_vampires(vampires)
    
    # Create result embed
    embed = discord.Embed(
        title=f"⚔️ MISSION: {mission['name']}",
        description=mission['description'],
        color=outcome_color
    )
    
    embed.add_field(
        name="Your Vampire",
        value=f"**{found_vampire['name']}** (#{vampire_number})\nClan: {found_vampire['clan']}\nPower: {found_vampire['power']}\nCombat Score: {result['v1_score']}",
        inline=True
    )
    
    embed.add_field(
        name="Enemy Vampire",
        value=f"**{ai_vampire['name']}**\nClan: {ai_vampire['clan']}\nPower: {ai_vampire['power']}\nCombat Score: {result['v2_score']}",
        inline=True
    )
    
    embed.add_field(
        name=f"{outcome_icon} Result",
        value=f"**{outcome}!**\n{result['winner']['name']} wins!\n\n{found_vampire['name']}'s Record: {found_vampire['wins']}W - {found_vampire['losses']}L",
        inline=False
    )
    
    difficulty_emoji = "⭐" if mission['difficulty'] == "easy" else "⭐⭐" if mission['difficulty'] == "medium" else "⭐⭐⭐"
    embed.set_footer(text=f"Difficulty: {mission['difficulty'].upper()} {difficulty_emoji}")
    
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
