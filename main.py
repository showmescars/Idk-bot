import discord
from discord.ext import commands, tasks
import json
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio

# Load environment variables

load_dotenv()

# Bot setup

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=’!’, intents=intents, help_command=None)

# Files

VAMPIRES_FILE = ‘vampires.json’
BATTLES_FILE = ‘battles.json’
USER_VAMPIRES_FILE = ‘user_vampires.json’

# Vampire name components for generation

FIRST_NAMES = [
“Vladimir”, “Dracula”, “Lestat”, “Armand”, “Magnus”, “Lucian”, “Corvinus”,
“Selene”, “Akasha”, “Carmilla”, “Lilith”, “Nyx”, “Seraphina”, “Morgana”,
“Viktor”, “Marcus”, “Blade”, “Alucard”, “Kain”, “Raziel”, “Vorador”,
“Dimitri”, “Raphael”, “Gabriel”, “Michael”, “Azrael”, “Dante”, “Nero”,
“Isabella”, “Claudia”, “Mina”, “Lucy”, “Elizabeth”, “Anastasia”, “Katrina”
]

LAST_NAMES = [
“Bloodmoon”, “Nightshade”, “Darkborne”, “Ravencroft”, “Blackwood”, “Thornheart”,
“Crimson”, “Shadowfang”, “Duskwalker”, “Grimoire”, “Nightfall”, “Stormborn”,
“Ashenheart”, “Ironblood”, “Silverthorn”, “Moonwhisper”, “Darkwater”, “Hellsing”,
“Dracul”, “Corvinus”, “Blackthorne”, “Ravenscroft”, “Darkmore”, “Bloodworth”
]

VAMPIRE_TITLES = [
“The Ancient”, “The Immortal”, “The Blood Lord”, “The Nightwalker”, “The Eternal”,
“The Cursed”, “The Undying”, “The Shadow”, “The Reaper”, “The Devourer”,
“The First Born”, “The Elder”, “The Progenitor”, “The Dark One”, “The Corrupted”
]

ORIGINS = [
“Born in the shadows of medieval Transylvania during a blood moon”,
“Created by an ancient vampire lord in the catacombs of Rome”,
“Cursed by a witch after betraying their mortal family in 1500s France”,
“Turned during the Black Plague while searching for a cure”,
“Rose from the grave after being wrongfully executed in Salem”,
“Created in ancient Egypt by a cult of blood worshippers”,
“Turned while serving as a knight during the Crusades”,
“Became immortal through a dark ritual in medieval Scotland”,
“Transformed in the depths of a Victorian London mansion”,
“Created by a vampire queen in ancient Mesopotamia”,
“Turned during a masquerade ball in 18th century Venice”,
“Rose as a vampire after dying in a duel over forbidden love”,
“Created in the mountains of Romania by Dracula himself”,
“Transformed during the Renaissance while studying dark arts”,
“Turned in a monastery after discovering ancient blood magic”
]

PERSONALITIES = [
“Ruthless and cunning, shows no mercy to enemies”,
“Noble and honorable, follows an ancient code of conduct”,
“Chaotic and unpredictable, thrives on chaos and blood”,
“Wise and calculating, always three steps ahead”,
“Savage and primal, barely controlled bloodlust”,
“Elegant and sophisticated, kills with style and grace”,
“Brooding and melancholic, haunted by immortality”,
“Arrogant and prideful, believes they are superior to all”,
“Mysterious and enigmatic, motivations unknown”,
“Sadistic and cruel, enjoys the suffering of others”,
“Protective and loyal to their coven, fierce to outsiders”,
“Seductive and manipulative, uses charm as a weapon”
]

POWERS = [
“Shadow Manipulation”, “Blood Magic”, “Mind Control”, “Superhuman Strength”,
“Hypnotic Gaze”, “Bat Transformation”, “Mist Form”, “Telekinesis”,
“Regeneration”, “Speed Enhancement”, “Dark Energy Projection”, “Blood Drain”,
“Fear Inducement”, “Night Vision”, “Enhanced Senses”, “Immortality”,
“Weather Control”, “Necromancy”, “Shape Shifting”, “Time Dilation”
]

# Load/Save functions

def load_json(filename, default=None):
“”“Load JSON file with error handling”””
if default is None:
default = {}
try:
if os.path.exists(filename):
with open(filename, ‘r’) as f:
return json.load(f)
except Exception as e:
print(f”Error loading {filename}: {e}”)
return default

def save_json(filename, data):
“”“Save JSON file with error handling”””
try:
with open(filename, ‘w’) as f:
json.dump(data, f, indent=4)
except Exception as e:
print(f”Error saving {filename}: {e}”)

# Initialize data

vampires_db = load_json(VAMPIRES_FILE, {})
battles_history = load_json(BATTLES_FILE, [])
user_vampires = load_json(USER_VAMPIRES_FILE, {})

def generate_vampire():
“”“Generate a random vampire with stats and background”””
first_name = random.choice(FIRST_NAMES)
last_name = random.choice(LAST_NAMES)
title = random.choice(VAMPIRE_TITLES)

```
vampire = {
    'id': f"vamp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
    'name': f"{first_name} {last_name}",
    'title': title,
    'full_name': f"{first_name} {last_name}, {title}",
    'age': random.randint(100, 3000),
    'origin': random.choice(ORIGINS),
    'personality': random.choice(PERSONALITIES),
    'stats': {
        'strength': random.randint(50, 100),
        'speed': random.randint(50, 100),
        'intelligence': random.randint(50, 100),
        'bloodlust': random.randint(50, 100),
        'dark_magic': random.randint(50, 100),
        'endurance': random.randint(50, 100)
    },
    'powers': random.sample(POWERS, random.randint(3, 6)),
    'wins': 0,
    'losses': 0,
    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'creator': None
}

# Calculate overall power level
total_stats = sum(vampire['stats'].values())
vampire['power_level'] = total_stats
vampire['rank'] = get_rank(total_stats)

return vampire
```

def get_rank(power_level):
“”“Determine vampire rank based on power level”””
if power_level >= 550:
return “🌟 Ancient Elder”
elif power_level >= 500:
return “👑 Vampire Lord”
elif power_level >= 450:
return “⚔️ Master Vampire”
elif power_level >= 400:
return “🗡️ Veteran Vampire”
elif power_level >= 350:
return “🦇 Skilled Vampire”
else:
return “🩸 Fledgling Vampire”

def create_vampire_embed(vampire):
“”“Create a detailed embed for a vampire”””
embed = discord.Embed(
title=f”🧛 {vampire[‘full_name’]}”,
description=f”*{vampire[‘origin’]}*”,
color=discord.Color.dark_red(),
timestamp=datetime.now()
)

```
embed.add_field(name="👤 Age", value=f"{vampire['age']} years", inline=True)
embed.add_field(name="⚡ Power Level", value=f"{vampire['power_level']}", inline=True)
embed.add_field(name="🏆 Rank", value=vampire['rank'], inline=True)

stats_text = "\n".join([f"**{stat.title()}**: {value}" for stat, value in vampire['stats'].items()])
embed.add_field(name="📊 Stats", value=stats_text, inline=False)

embed.add_field(name="🧠 Personality", value=vampire['personality'], inline=False)

powers_text = ", ".join(vampire['powers'])
embed.add_field(name="✨ Powers", value=powers_text, inline=False)

embed.add_field(name="🎮 Record", value=f"Wins: {vampire['wins']} | Losses: {vampire['losses']}", inline=False)

embed.set_footer(text=f"Vampire ID: {vampire['id']}")

return embed
```

def simulate_battle(vamp1, vamp2):
“”“Simulate a battle between two vampires”””
battle_log = []
battle_log.append(f”⚔️ **BATTLE BEGINS!** ⚔️”)
battle_log.append(f”**{vamp1[‘name’]}** vs **{vamp2[‘name’]}**\n”)

```
# Battle rounds
rounds = random.randint(3, 7)
v1_hp = 100
v2_hp = 100

for round_num in range(1, rounds + 1):
    battle_log.append(f"\n**--- Round {round_num} ---**")
    
    # Vampire 1 attacks
    power1 = random.choice(vamp1['powers'])
    damage1 = random.randint(10, 25) + (vamp1['stats']['strength'] // 10)
    v2_hp -= damage1
    battle_log.append(f"🔴 {vamp1['name']} uses **{power1}**! Deals {damage1} damage!")
    
    if v2_hp <= 0:
        battle_log.append(f"\n💀 {vamp2['name']} has been defeated!")
        break
        
    battle_log.append(f"   {vamp2['name']}: {max(0, v2_hp)} HP remaining")
    
    # Vampire 2 attacks
    power2 = random.choice(vamp2['powers'])
    damage2 = random.randint(10, 25) + (vamp2['stats']['strength'] // 10)
    v1_hp -= damage2
    battle_log.append(f"🔵 {vamp2['name']} uses **{power2}**! Deals {damage2} damage!")
    
    if v1_hp <= 0:
        battle_log.append(f"\n💀 {vamp1['name']} has been defeated!")
        break
        
    battle_log.append(f"   {vamp1['name']}: {max(0, v1_hp)} HP remaining")

# Determine winner
if v1_hp > v2_hp:
    winner = vamp1
    loser = vamp2
    battle_log.append(f"\n🏆 **WINNER: {vamp1['name']}!** 🏆")
else:
    winner = vamp2
    loser = vamp1
    battle_log.append(f"\n🏆 **WINNER: {vamp2['name']}!** 🏆")

return winner, loser, "\n".join(battle_log)
```

# Bot events

@bot.event
async def on_ready():
print(f’{bot.user} has connected to Discord!’)
print(f’Bot is ready to summon vampires!’)
print(f’Logged in as {bot.user.name} ({bot.user.id})’)
print(’——’)

@bot.event
async def on_command_error(ctx, error):
“”“Handle command errors”””
if isinstance(error, commands.CommandNotFound):
return
elif isinstance(error, commands.MissingRequiredArgument):
await ctx.send(f”❌ Missing required argument: {error.param.name}”)
elif isinstance(error, commands.MissingPermissions):
await ctx.send(“❌ You don’t have permission to use this command!”)
else:
print(f”Error: {error}”)
await ctx.send(f”❌ An error occurred: {str(error)}”)

@bot.command(name=‘help’)
async def help_command(ctx):
“”“Display help information”””
embed = discord.Embed(
title=“🧛 Vampire Battle Bot Commands”,
description=“Generate vampire characters and watch them battle!”,
color=discord.Color.dark_red()
)

```
embed.add_field(
    name="!generate or !gen",
    value="Generate a random vampire character",
    inline=False
)

embed.add_field(
    name="!battle <vampire_id_1> <vampire_id_2>",
    value="Make two vampires fight each other",
    inline=False
)

embed.add_field(
    name="!random_battle or !rb",
    value="Generate two random vampires and make them fight",
    inline=False
)

embed.add_field(
    name="!view <vampire_id>",
    value="View detailed information about a vampire",
    inline=False
)

embed.add_field(
    name="!myvampires or !mv",
    value="View all vampires you've generated",
    inline=False
)

embed.add_field(
    name="!leaderboard or !lb",
    value="View the top vampires by wins",
    inline=False
)

embed.add_field(
    name="!stats",
    value="View battle statistics",
    inline=False
)

await ctx.send(embed=embed)
```

@bot.command(name=‘generate’, aliases=[‘gen’])
async def generate_vampire_cmd(ctx):
“”“Generate a random vampire”””
try:
vampire = generate_vampire()
vampire[‘creator’] = str(ctx.author.id)

```
    vampires_db[vampire['id']] = vampire
    save_json(VAMPIRES_FILE, vampires_db)
    
    # Add to user's vampires
    user_id = str(ctx.author.id)
    if user_id not in user_vampires:
        user_vampires[user_id] = []
    user_vampires[user_id].append(vampire['id'])
    save_json(USER_VAMPIRES_FILE, user_vampires)
    
    embed = create_vampire_embed(vampire)
    embed.set_author(name=f"Generated by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    await ctx.send(f"🧛 A new vampire has been summoned from the darkness!", embed=embed)
except Exception as e:
    print(f"Error in generate command: {e}")
    await ctx.send("❌ An error occurred while generating the vampire.")
```

@bot.command(name=‘view’)
async def view_vampire(ctx, vampire_id: str = None):
“”“View a specific vampire”””
if vampire_id is None:
await ctx.send(“❌ Please provide a vampire ID! Usage: `!view <vampire_id>`”)
return

```
if vampire_id not in vampires_db:
    await ctx.send("❌ Vampire not found! Use `!myvampires` to see your vampire IDs.")
    return

try:
    vampire = vampires_db[vampire_id]
    embed = create_vampire_embed(vampire)
    await ctx.send(embed=embed)
except Exception as e:
    print(f"Error in view command: {e}")
    await ctx.send("❌ An error occurred while viewing the vampire.")
```

@bot.command(name=‘battle’)
async def battle_vampires(ctx, vamp_id_1: str = None, vamp_id_2: str = None):
“”“Battle two vampires”””
if vamp_id_1 is None or vamp_id_2 is None:
await ctx.send(“❌ Please provide two vampire IDs! Usage: `!battle <vampire_id_1> <vampire_id_2>`”)
return

```
if vamp_id_1 not in vampires_db:
    await ctx.send(f"❌ Vampire 1 (ID: {vamp_id_1}) not found!")
    return

if vamp_id_2 not in vampires_db:
    await ctx.send(f"❌ Vampire 2 (ID: {vamp_id_2}) not found!")
    return

try:
    vamp1 = vampires_db[vamp_id_1]
    vamp2 = vampires_db[vamp_id_2]
    
    # Battle announcement
    embed = discord.Embed(
        title="⚔️ VAMPIRE BATTLE ARENA ⚔️",
        description=f"**{vamp1['name']}** ({vamp1['rank']})\n🆚\n**{vamp2['name']}** ({vamp2['rank']})",
        color=discord.Color.red()
    )
    
    await ctx.send("🌙 The moon rises... A battle is about to begin!", embed=embed)
    await asyncio.sleep(2)
    
    # Simulate battle
    winner, loser, battle_log = simulate_battle(vamp1, vamp2)
    
    # Update records
    vampires_db[winner['id']]['wins'] += 1
    vampires_db[loser['id']]['losses'] += 1
    save_json(VAMPIRES_FILE, vampires_db)
    
    # Save battle history
    battle_record = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'vampire1': vamp1['name'],
        'vampire2': vamp2['name'],
        'winner': winner['name'],
        'initiated_by': str(ctx.author.id)
    }
    battles_history.append(battle_record)
    save_json(BATTLES_FILE, battles_history)
    
    # Send battle log in chunks if needed
    if len(battle_log) > 2000:
        chunks = [battle_log[i:i+2000] for i in range(0, len(battle_log), 2000)]
        for chunk in chunks:
            await ctx.send(chunk)
            await asyncio.sleep(1)
    else:
        await ctx.send(battle_log)
    
    # Send winner embed
    winner_embed = discord.Embed(
        title=f"👑 {winner['name']} WINS!",
        description=f"**New Record**: {vampires_db[winner['id']]['wins']} Wins - {vampires_db[winner['id']]['losses']} Losses",
        color=discord.Color.gold()
    )
    
    await ctx.send(embed=winner_embed)
except Exception as e:
    print(f"Error in battle command: {e}")
    await ctx.send("❌ An error occurred during the battle.")
```

@bot.command(name=‘random_battle’, aliases=[‘rb’])
async def random_battle(ctx):
“”“Generate two random vampires and make them fight”””
try:
await ctx.send(“🌙 Summoning two vampires from the darkness…”)

```
    vamp1 = generate_vampire()
    vamp1['creator'] = str(ctx.author.id)
    vampires_db[vamp1['id']] = vamp1
    
    vamp2 = generate_vampire()
    vamp2['creator'] = str(ctx.author.id)
    vampires_db[vamp2['id']] = vamp2
    
    save_json(VAMPIRES_FILE, vampires_db)
    
    # Show vampires
    embed1 = create_vampire_embed(vamp1)
    embed1.set_author(name="Challenger 1")
    await ctx.send(embed=embed1)
    
    await asyncio.sleep(1)
    
    embed2 = create_vampire_embed(vamp2)
    embed2.set_author(name="Challenger 2")
    await ctx.send(embed=embed2)
    
    await asyncio.sleep(2)
    
    # Battle announcement
    battle_embed = discord.Embed(
        title="⚔️ RANDOM BATTLE ARENA ⚔️",
        description=f"**{vamp1['name']}**\n🆚\n**{vamp2['name']}**",
        color=discord.Color.red()
    )
    
    await ctx.send("⚡ Let the battle begin!", embed=battle_embed)
    await asyncio.sleep(2)
    
    # Simulate battle
    winner, loser, battle_log = simulate_battle(vamp1, vamp2)
    
    # Update records
    vampires_db[winner['id']]['wins'] += 1
    vampires_db[loser['id']]['losses'] += 1
    save_json(VAMPIRES_FILE, vampires_db)
    
    # Save battle history
    battle_record = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'vampire1': vamp1['name'],
        'vampire2': vamp2['name'],
        'winner': winner['name'],
        'initiated_by': str(ctx.author.id)
    }
    battles_history.append(battle_record)
    save_json(BATTLES_FILE, battles_history)
    
    # Send battle log
    if len(battle_log) > 2000:
        chunks = [battle_log[i:i+2000] for i in range(0, len(battle_log), 2000)]
        for chunk in chunks:
            await ctx.send(chunk)
            await asyncio.sleep(1)
    else:
        await ctx.send(battle_log)
    
    # Send winner embed
    winner_embed = discord.Embed(
        title=f"👑 {winner['name']} IS VICTORIOUS!",
        description=f"**Record**: {vampires_db[winner['id']]['wins']} Wins - {vampires_db[winner['id']]['losses']} Losses",
        color=discord.Color.gold()
    )
    
    await ctx.send(embed=winner_embed)
except Exception as e:
    print(f"Error in random_battle command: {e}")
    await ctx.send("❌ An error occurred during the random battle.")
```

@bot.command(name=‘myvampires’, aliases=[‘mv’])
async def my_vampires(ctx):
“”“View all vampires created by the user”””
try:
user_id = str(ctx.author.id)

```
    if user_id not in user_vampires or not user_vampires[user_id]:
        await ctx.send("❌ You haven't generated any vampires yet! Use `!generate` to create one.")
        return
    
    embed = discord.Embed(
        title=f"🧛 {ctx.author.display_name}'s Vampires",
        description="Your created vampires:",
        color=discord.Color.dark_red()
    )
    
    for vamp_id in user_vampires[user_id]:
        if vamp_id in vampires_db:
            vamp = vampires_db[vamp_id]
            embed.add_field(
                name=f"{vamp['name']} ({vamp['rank']})",
                value=f"ID: `{vamp_id}`\nPower: {vamp['power_level']} | Record: {vamp['wins']}W - {vamp['losses']}L",
                inline=False
            )
    
    await ctx.send(embed=embed)
except Exception as e:
    print(f"Error in myvampires command: {e}")
    await ctx.send("❌ An error occurred while fetching your vampires.")
```

@bot.command(name=‘leaderboard’, aliases=[‘lb’])
async def leaderboard(ctx):
“”“Show top vampires by wins”””
try:
if not vampires_db:
await ctx.send(“❌ No vampires have been created yet!”)
return

```
    # Sort vampires by wins
    sorted_vampires = sorted(vampires_db.values(), key=lambda x: x['wins'], reverse=True)[:10]
    
    embed = discord.Embed(
        title="🏆 Vampire Leaderboard",
        description="Top 10 Vampires by Wins",
        color=discord.Color.gold()
    )
    
    for i, vamp in enumerate(sorted_vampires, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        embed.add_field(
            name=f"{medal} {vamp['name']}",
            value=f"Wins: {vamp['wins']} | Losses: {vamp['losses']} | Power: {vamp['power_level']}",
            inline=False
        )
    
    await ctx.send(embed=embed)
except Exception as e:
    print(f"Error in leaderboard command: {e}")
    await ctx.send("❌ An error occurred while fetching the leaderboard.")
```

@bot.command(name=‘stats’)
async def battle_stats(ctx):
“”“Show overall battle statistics”””
try:
total_vampires = len(vampires_db)
total_battles = len(battles_history)

```
    embed = discord.Embed(
        title="📊 Battle Statistics",
        description="Overall vampire battle stats",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="Total Vampires", value=str(total_vampires), inline=True)
    embed.add_field(name="Total Battles", value=str(total_battles), inline=True)
    embed.add_field(name="Active Users", value=str(len(user_vampires)), inline=True)
    
    if vampires_db:
        avg_power = sum(v['power_level'] for v in vampires_db.values()) / len(vampires_db)
        embed.add_field(name="Average Power Level", value=f"{avg_power:.1f}", inline=True)
        
        strongest = max(vampires_db.values(), key=lambda x: x['power_level'])
        embed.add_field(
            name="Strongest Vampire",
            value=f"{strongest['name']} ({strongest['power_level']})",
            inline=True
        )
        
        most_wins = max(vampires_db.values(), key=lambda x: x['wins'])
        embed.add_field(
            name="Most Wins",
            value=f"{most_wins['name']} ({most_wins['wins']} wins)",
            inline=True
        )
    
    await ctx.send(embed=embed)
except Exception as e:
    print(f"Error in stats command: {e}")
    await ctx.send("❌ An error occurred while fetching statistics.")
```

# Run the bot

if **name** == “**main**”:
TOKEN = os.getenv(‘DISCORD_TOKEN’)
if not TOKEN:
print(“ERROR: DISCORD_TOKEN not found in environment variables!”)
print(“Please set your Discord bot token in Railway or .env file”)
exit(1)
else:
try:
bot.run(TOKEN)
except Exception as e:
print(f”Failed to start bot: {e}”)
exit(1)
