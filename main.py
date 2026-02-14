import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

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

def generate_short_id():
    """Generate a short 6-character ID"""
    import string
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

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
        "id": generate_short_id(),
        "name": f"{first_name} {last_name}",
        "clan": clan,
        "stats": stats,
        "power": calculate_power(stats),
        "owner_id": owner_id,
        "owner_name": owner_name,
        "wins": 0,
        "losses": 0,
        "last_trained": None,
        "multiplier": 1,
        "created_at": datetime.now().isoformat()
    }
    
    return vampire

def create_ai_vampire():
    """Create an AI vampire with 30% weak, 70% strong distribution"""
    first_name = random.choice(VAMPIRE_FIRST_NAMES)
    last_name = random.choice(VAMPIRE_LAST_NAMES)
    clan = random.choice(VAMPIRE_CLANS)
    
    # 30% chance for weak vampire, 70% chance for strong vampire
    if random.random() < 0.3:
        # Weak vampire: 330-1500
        target_power = random.randint(330, 1500)
    else:
        # Strong vampire: 1501-5000
        target_power = random.randint(1501, 5000)
    
    # Distribute power across 5 stats
    remaining_power = target_power
    stats = {}
    
    stat_names = ["strength", "speed", "intelligence", "blood_power", "defense"]
    
    for i, stat in enumerate(stat_names):
        if i == len(stat_names) - 1:
            # Last stat gets whatever is remaining
            stats[stat] = remaining_power
        else:
            # Random portion of remaining power
            min_val = int(remaining_power * 0.15)
            max_val = int(remaining_power * 0.25)
            stat_value = random.randint(min_val, max_val)
            stats[stat] = stat_value
            remaining_power -= stat_value
    
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

@bot.command(name='help')
async def help_command(ctx):
    """Display all available commands"""
    is_admin = ctx.author.guild_permissions.administrator
    
    embed = discord.Embed(
        title="Vampire Bot - Command List",
        description="All available commands for the Vampire Bot",
        color=discord.Color.dark_red()
    )
    
    # User Commands
    user_commands = """
    **?make** - Create a random vampire
    **?list** - View all your vampires
    **?mission <ID>** - Send your vampire on a mission
    **?train <ID>** - Train your vampire (1 hour cooldown)
    **?viewmultiplier <ID>** - Check a vampire's training multiplier
    **?help** - Display this command list
    """
    embed.add_field(name="User Commands", value=user_commands, inline=False)
    
    if is_admin:
        admin_commands = """
        **?multiplier <ID> <amount>** - Set training multiplier for a vampire
        """
        embed.add_field(name="Admin Commands", value=admin_commands, inline=False)
    
    embed.set_footer(text="Use ? before each command")
    
    await ctx.send(embed=embed)

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
        title="Vampire Created!",
        description=f"**{v['name']}** has risen from the grave!",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="ID", value=f"`{v['id']}`", inline=True)
    embed.add_field(name="Clan", value=v['clan'], inline=True)
    embed.add_field(name="Power", value=v['power'], inline=True)
    embed.add_field(name="Record", value=f"{v['wins']}W - {v['losses']}L", inline=True)
    embed.add_field(name="Stats", value=f"**Strength:** {v['stats']['strength']}\n**Speed:** {v['stats']['speed']}\n**Intelligence:** {v['stats']['intelligence']}\n**Blood Power:** {v['stats']['blood_power']}\n**Defense:** {v['stats']['defense']}", inline=False)
    embed.set_footer(text=f"Use ?mission {v['id']} to send on a mission or ?train {v['id']} to train!")
    
    await ctx.send(embed=embed)

@bot.command(name='list')
async def list_vampires(ctx):
    """View all your vampires"""
    user_id = str(ctx.author.id)
    
    if user_id not in vampires or len(vampires[user_id]) == 0:
        await ctx.send("You don't have any vampires yet! Use `?make` to create one.")
        return
    
    user_vamps = vampires[user_id]
    
    embed = discord.Embed(
        title=f"{ctx.author.name}'s Vampires",
        description=f"Total: {len(user_vamps)} vampires",
        color=discord.Color.dark_red()
    )
    
    for v in user_vamps:
        multiplier_text = f" | x{v.get('multiplier', 1)}" if v.get('multiplier', 1) > 1 else ""
        embed.add_field(
            name=f"{v['name']} - `{v['id']}`",
            value=f"Clan: {v['clan']}\nPower: {v['power']}{multiplier_text}\nRecord: {v['wins']}W - {v['losses']}L",
            inline=True
        )
    
    embed.set_footer(text="Use ?mission <ID> or ?train <ID>")
    
    await ctx.send(embed=embed)

@bot.command(name='mission')
async def send_mission(ctx, vampire_id: str):
    """Send your vampire on a random mission to fight AI vampires"""
    
    # Find the vampire by ID
    user_id = str(ctx.author.id)
    found_vampire = None
    
    if user_id in vampires:
        for v in vampires[user_id]:
            if v['id'].upper() == vampire_id.upper():
                found_vampire = v
                break
    
    if not found_vampire:
        await ctx.send("Vampire not found! Use `?list` to see your vampires and their IDs.")
        return
    
    # Select random mission
    mission = random.choice(MISSIONS)
    
    # Create AI opponent with 30/70 distribution
    ai_vampire = create_ai_vampire()
    
    # Simulate battle
    result = simulate_battle(found_vampire, ai_vampire)
    
    # Update player vampire stats
    if result['winner'] == found_vampire:
        found_vampire['wins'] += 1
        outcome = "VICTORY"
        outcome_color = discord.Color.green()
    else:
        found_vampire['losses'] += 1
        outcome = "DEFEAT"
        outcome_color = discord.Color.red()
    
    save_vampires(vampires)
    
    # Create result embed
    embed = discord.Embed(
        title=f"MISSION: {mission['name']}",
        description=mission['description'],
        color=outcome_color
    )
    
    embed.add_field(
        name="Your Vampire",
        value=f"**{found_vampire['name']}** (`{found_vampire['id']}`)\nClan: {found_vampire['clan']}\nPower: {found_vampire['power']}\nCombat Score: {result['v1_score']}",
        inline=True
    )
    
    embed.add_field(
        name="Enemy Vampire",
        value=f"**{ai_vampire['name']}**\nClan: {ai_vampire['clan']}\nPower: {ai_vampire['power']}\nCombat Score: {result['v2_score']}",
        inline=True
    )
    
    embed.add_field(
        name="Result",
        value=f"**{outcome}!**\n{result['winner']['name']} wins!\n\n{found_vampire['name']}'s Record: {found_vampire['wins']}W - {found_vampire['losses']}L",
        inline=False
    )
    
    difficulty_stars = "*" if mission['difficulty'] == "easy" else "**" if mission['difficulty'] == "medium" else "***"
    embed.set_footer(text=f"Difficulty: {mission['difficulty'].upper()} {difficulty_stars}")
    
    await ctx.send(embed=embed)

@bot.command(name='train')
async def train_vampire(ctx, vampire_id: str):
    """Train your vampire to increase stats (1 hour cooldown, admins bypass cooldown)"""
    
    # Find the vampire by ID
    user_id = str(ctx.author.id)
    found_vampire = None
    
    if user_id in vampires:
        for v in vampires[user_id]:
            if v['id'].upper() == vampire_id.upper():
                found_vampire = v
                break
    
    if not found_vampire:
        await ctx.send("Vampire not found! Use `?list` to see your vampires and their IDs.")
        return
    
    # Check if user is admin
    is_admin = ctx.author.guild_permissions.administrator
    
    # Check cooldown (only for non-admins)
    if not is_admin:
        if found_vampire['last_trained']:
            last_trained = datetime.fromisoformat(found_vampire['last_trained'])
            time_since = datetime.now() - last_trained
            
            if time_since < timedelta(hours=1):
                remaining = timedelta(hours=1) - time_since
                minutes = int(remaining.total_seconds() / 60)
                await ctx.send(f"**{found_vampire['name']}** is exhausted! Can train again in **{minutes} minutes**.")
                return
    
    # Get vampire's multiplier (default is 1)
    vampire_multiplier = found_vampire.get('multiplier', 1)
    
    # Train the vampire - increase random stats
    stat_gains = {}
    total_gain = 0
    
    for stat in found_vampire['stats']:
        base_gain = random.randint(2, 8)
        gain = int(base_gain * vampire_multiplier)
        found_vampire['stats'][stat] += gain
        stat_gains[stat] = gain
        total_gain += gain
    
    # Update power
    old_power = found_vampire['power']
    found_vampire['power'] = calculate_power(found_vampire['stats'])
    power_gain = found_vampire['power'] - old_power
    
    # Update last trained time
    found_vampire['last_trained'] = datetime.now().isoformat()
    
    save_vampires(vampires)
    
    # Create result embed
    embed = discord.Embed(
        title="Training Complete!",
        description=f"**{found_vampire['name']}** has grown stronger!",
        color=discord.Color.gold()
    )
    
    embed.add_field(name="Vampire", value=f"`{found_vampire['id']}`\n{found_vampire['clan']}", inline=True)
    embed.add_field(name="New Power", value=f"{found_vampire['power']} (+{power_gain})", inline=True)
    
    if vampire_multiplier > 1:
        embed.add_field(name="Multiplier", value=f"x{vampire_multiplier}", inline=True)
    
    gains_text = "\n".join([f"**{stat.replace('_', ' ').title()}:** {found_vampire['stats'][stat]} (+{gain})" 
                            for stat, gain in stat_gains.items()])
    embed.add_field(name="Stat Gains", value=gains_text, inline=False)
    
    if is_admin:
        embed.set_footer(text="Admin - No cooldown")
    else:
        embed.set_footer(text="Train again in 1 hour!")
    
    await ctx.send(embed=embed)

@bot.command(name='multiplier')
@commands.has_permissions(administrator=True)
async def set_multiplier(ctx, vampire_id: str, amount: float):
    """Set training multiplier for a specific vampire (admin only)"""
    
    if amount < 1:
        await ctx.send("Multiplier must be at least 1!")
        return
    
    if amount > 100:
        await ctx.send("Multiplier cannot exceed 100!")
        return
    
    # Find the vampire by ID
    found_vampire = None
    owner_name = None
    
    for user_id, user_vamps in vampires.items():
        for v in user_vamps:
            if v['id'].upper() == vampire_id.upper():
                found_vampire = v
                owner_name = v['owner_name']
                break
        if found_vampire:
            break
    
    if not found_vampire:
        await ctx.send(f"Vampire with ID `{vampire_id}` not found!")
        return
    
    found_vampire['multiplier'] = amount
    save_vampires(vampires)
    
    await ctx.send(f"Set **{found_vampire['name']}** (`{vampire_id}`) training multiplier to **x{amount}**!\nOwner: {owner_name}")

@bot.command(name='viewmultiplier')
async def view_multiplier(ctx, vampire_id: str):
    """View a vampire's current training multiplier"""
    
    # Find the vampire by ID
    user_id = str(ctx.author.id)
    found_vampire = None
    
    if user_id in vampires:
        for v in vampires[user_id]:
            if v['id'].upper() == vampire_id.upper():
                found_vampire = v
                break
    
    if not found_vampire:
        await ctx.send("Vampire not found! Use `?list` to see your vampires and their IDs.")
        return
    
    vampire_multiplier = found_vampire.get('multiplier', 1)
    
    await ctx.send(f"**{found_vampire['name']}** (`{vampire_id}`) training multiplier: **x{vampire_multiplier}**")

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found!")
        print("Create a .env file with DISCORD_TOKEN=your_token")
    else:
        print("Token found! Starting Vampire Bot...")
        bot.run(TOKEN)
