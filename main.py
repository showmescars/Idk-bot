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
TRAINING_CHANNEL_ID = 1472381719465164965  # The channel where "train" command works

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
        "boost": 1,  # Changed from multiplier to boost
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
            # Last stat gets whatever's remaining
            stats[stat] = max(50, remaining_power)
        else:
            # Random portion of remaining power
            avg_remaining = remaining_power // (len(stat_names) - i)
            variation = avg_remaining // 2
            stat_value = random.randint(max(50, avg_remaining - variation), avg_remaining + variation)
            stats[stat] = stat_value
            remaining_power -= stat_value
    
    vampire = {
        "id": generate_short_id(),
        "name": f"{first_name} {last_name}",
        "clan": clan,
        "stats": stats,
        "power": calculate_power(stats),
        "owner_id": "AI",
        "owner_name": "AI",
        "wins": 0,
        "losses": 0,
        "boost": 1  # Changed from multiplier to boost
    }
    
    return vampire

def get_user_vampire(user_id):
    user_id_str = str(user_id)
    if user_id_str in vampires:
        return vampires[user_id_str]
    return None

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author.bot:
        return
    
    # Check if message is "train" in the specific channel
    if message.content.lower() == "train" and message.channel.id == TRAINING_CHANNEL_ID:
        ctx = await bot.get_context(message)
        await train_vampire(ctx)
        return
    
    # Process other commands
    await bot.process_commands(message)

@bot.command(name='create')
async def create_vampire_command(ctx):
    """Create your vampire"""
    user_id = str(ctx.author.id)
    
    if user_id in vampires:
        await ctx.send(f"❌ You already have a vampire! Use `?stats` to view it.")
        return
    
    vampire = create_vampire(user_id, ctx.author.name)
    vampires[user_id] = vampire
    save_vampires(vampires)
    
    embed = discord.Embed(
        title="🧛 Vampire Created!",
        description=f"**{vampire['name']}** has risen from the grave!",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="Clan", value=vampire['clan'], inline=True)
    embed.add_field(name="Power", value=f"{vampire['power']} ⚡", inline=True)
    embed.add_field(name="ID", value=vampire['id'], inline=True)
    embed.add_field(name="📊 Stats", value=f"""
    💪 Strength: {vampire['stats']['strength']}
    ⚡ Speed: {vampire['stats']['speed']}
    🧠 Intelligence: {vampire['stats']['intelligence']}
    🩸 Blood Power: {vampire['stats']['blood_power']}
    🛡️ Defense: {vampire['stats']['defense']}
    """, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='stats')
async def stats_command(ctx, user: discord.User = None):
    """View vampire stats"""
    if user is None:
        user = ctx.author
    
    vampire = get_user_vampire(user.id)
    
    if not vampire:
        await ctx.send(f"❌ {'You don' if user == ctx.author else f'{user.name} doesn'}t have a vampire yet! Use `?create` to make one.")
        return
    
    win_rate = (vampire['wins'] / (vampire['wins'] + vampire['losses']) * 100) if (vampire['wins'] + vampire['losses']) > 0 else 0
    
    embed = discord.Embed(
        title=f"🧛 {vampire['name']}",
        description=f"Clan: **{vampire['clan']}**",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="Owner", value=vampire['owner_name'], inline=True)
    embed.add_field(name="Power", value=f"{vampire['power']} ⚡", inline=True)
    embed.add_field(name="Boost", value=f"{vampire['boost']}x", inline=True)  # Changed from Multiplier to Boost
    embed.add_field(name="📊 Stats", value=f"""
    💪 Strength: {vampire['stats']['strength']}
    ⚡ Speed: {vampire['stats']['speed']}
    🧠 Intelligence: {vampire['stats']['intelligence']}
    🩸 Blood Power: {vampire['stats']['blood_power']}
    🛡️ Defense: {vampire['stats']['defense']}
    """, inline=False)
    embed.add_field(name="⚔️ Battle Record", value=f"""
    Wins: {vampire['wins']} 🏆
    Losses: {vampire['losses']} 💀
    Win Rate: {win_rate:.1f}%
    """, inline=False)
    
    await ctx.send(embed=embed)

async def train_vampire(ctx):
    """Train your vampire (cooldown: 1 hour)"""
    vampire = get_user_vampire(ctx.author.id)
    
    if not vampire:
        await ctx.send("❌ You don't have a vampire yet! Use `?create` to make one.")
        return
    
    # Check cooldown
    if vampire['last_trained']:
        last_trained = datetime.fromisoformat(vampire['last_trained'])
        cooldown = timedelta(hours=1)
        time_since = datetime.now() - last_trained
        
        if time_since < cooldown:
            remaining = cooldown - time_since
            minutes = int(remaining.total_seconds() / 60)
            await ctx.send(f"⏰ Your vampire is still resting! Try again in {minutes} minutes.")
            return
    
    # Random stat improvement
    stat_to_improve = random.choice(list(vampire['stats'].keys()))
    improvement = random.randint(5, 15)
    vampire['stats'][stat_to_improve] += improvement
    vampire['power'] = calculate_power(vampire['stats'])
    vampire['last_trained'] = datetime.now().isoformat()
    
    save_vampires(vampires)
    
    await ctx.send(f"🏋️ Training complete! **{vampire['name']}** improved their **{stat_to_improve}** by **+{improvement}**! (Total Power: {vampire['power']} ⚡)")

@bot.command(name='battle')
async def battle_command(ctx, opponent: discord.User = None):
    """Battle another vampire or AI"""
    vampire = get_user_vampire(ctx.author.id)
    
    if not vampire:
        await ctx.send("❌ You don't have a vampire yet! Use `?create` to make one.")
        return
    
    # Determine opponent
    if opponent:
        opponent_vampire = get_user_vampire(opponent.id)
        if not opponent_vampire:
            await ctx.send(f"❌ {opponent.name} doesn't have a vampire!")
            return
        opponent_name = opponent.name
    else:
        opponent_vampire = create_ai_vampire()
        opponent_name = "AI"
    
    # Calculate effective power with boost
    player_effective_power = vampire['power'] * vampire['boost']
    opponent_effective_power = opponent_vampire['power'] * opponent_vampire.get('boost', 1)
    
    # Battle logic with some randomness
    player_roll = player_effective_power * random.uniform(0.8, 1.2)
    opponent_roll = opponent_effective_power * random.uniform(0.8, 1.2)
    
    if player_roll > opponent_roll:
        winner = vampire
        loser = opponent_vampire
        result = "Victory!"
        color = discord.Color.gold()
        vampire['wins'] += 1
        if opponent:
            opponent_vampire['losses'] += 1
    else:
        winner = opponent_vampire
        loser = vampire
        result = "Defeat..."
        color = discord.Color.dark_gray()
        vampire['losses'] += 1
        if opponent:
            opponent_vampire['wins'] += 1
    
    save_vampires(vampires)
    
    embed = discord.Embed(
        title=f"⚔️ {result}",
        description=f"**{vampire['name']}** vs **{opponent_vampire['name']}**",
        color=color
    )
    embed.add_field(name=f"{ctx.author.name}'s Vampire", 
                    value=f"{vampire['name']}\nPower: {vampire['power']} (Boost: {vampire['boost']}x)\nEffective: {player_effective_power:.0f}", 
                    inline=True)
    embed.add_field(name=f"{opponent_name}'s Vampire", 
                    value=f"{opponent_vampire['name']}\nPower: {opponent_vampire['power']} (Boost: {opponent_vampire.get('boost', 1)}x)\nEffective: {opponent_effective_power:.0f}", 
                    inline=True)
    embed.add_field(name="Winner", value=f"🏆 **{winner['name']}**", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='mission')
async def mission_command(ctx):
    """Go on a random mission"""
    vampire = get_user_vampire(ctx.author.id)
    
    if not vampire:
        await ctx.send("❌ You don't have a vampire yet! Use `?create` to make one.")
        return
    
    mission = random.choice(MISSIONS)
    
    # Calculate success chance based on difficulty and vampire power
    if mission['difficulty'] == 'easy':
        base_success = 70
        reward_range = (10, 30)
    elif mission['difficulty'] == 'medium':
        base_success = 50
        reward_range = (20, 50)
    else:  # hard
        base_success = 30
        reward_range = (40, 80)
    
    # Adjust success chance based on power
    power_bonus = min(20, vampire['power'] // 100)
    success_chance = base_success + power_bonus
    
    success = random.randint(1, 100) <= success_chance
    
    embed = discord.Embed(
        title=f"🌙 {mission['name']}",
        description=mission['description'],
        color=discord.Color.purple()
    )
    
    if success:
        reward = random.randint(*reward_range)
        stat_to_improve = random.choice(list(vampire['stats'].keys()))
        vampire['stats'][stat_to_improve] += reward
        vampire['power'] = calculate_power(vampire['stats'])
        save_vampires(vampires)
        
        embed.add_field(name="✅ Success!", value=f"Your vampire gained **+{reward}** {stat_to_improve}!", inline=False)
        embed.add_field(name="New Power", value=f"{vampire['power']} ⚡", inline=False)
    else:
        embed.add_field(name="❌ Failure!", value="Your vampire barely escaped with their unlife!", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='leaderboard')
async def leaderboard_command(ctx):
    """View the top vampires"""
    if not vampires:
        await ctx.send("❌ No vampires have been created yet!")
        return
    
    # Sort by power
    sorted_vampires = sorted(vampires.values(), key=lambda v: v['power'], reverse=True)[:10]
    
    embed = discord.Embed(
        title="🏆 Vampire Leaderboard",
        description="Top 10 Most Powerful Vampires",
        color=discord.Color.gold()
    )
    
    for i, vamp in enumerate(sorted_vampires, 1):
        embed.add_field(
            name=f"{i}. {vamp['name']}",
            value=f"Power: {vamp['power']} ⚡ | Owner: {vamp['owner_name']}",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """Show all commands"""
    embed = discord.Embed(
        title="🧛 Vampire Bot Commands",
        description="Build and battle with your vampire!",
        color=discord.Color.dark_red()
    )
    
    embed.add_field(name="?create", value="Create your vampire", inline=False)
    embed.add_field(name="?stats [@user]", value="View vampire stats", inline=False)
    embed.add_field(name="train (in training channel)", value="Train your vampire (1 hour cooldown)", inline=False)
    embed.add_field(name="?battle [@user]", value="Battle another vampire or AI", inline=False)
    embed.add_field(name="?mission", value="Go on a random mission", inline=False)
    embed.add_field(name="?leaderboard", value="View top vampires", inline=False)
    
    await ctx.send(embed=embed)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
