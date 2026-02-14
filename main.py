import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime
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
“Dracula”, “Vlad”, “Carmilla”, “Lestat”, “Akasha”, “Blade”, “Selene”,
“Viktor”, “Marcus”, “Lucian”, “Sonja”, “Amelia”, “Klaus”, “Elijah”,
“Rebekah”, “Kol”, “Finn”, “Mikael”, “Esther”, “Damon”, “Stefan”,
“Katherine”, “Alaric”, “Enzo”, “Valerie”, “Nora”, “Mary Louise”,
“Rayna”, “Julian”, “Lily”, “Kai”, “Bonnie”, “Caroline”, “Elena”,
“Alucard”, “Seras”, “Integra”, “Walter”, “Anderson”, “Jan”,
“Luke”, “Rip”, “Zorin”, “Tubalcain”, “Dandyman”, “Louis”,
“Claudia”, “Armand”, “Marius”, “Pandora”, “Maharet”, “Mekare”,
“Khayman”, “Enkil”, “Jesse”, “David”, “Daniel”, “Gabrielle”
]

LAST_NAMES = [
“Tepes”, “Draculesti”, “Karnstein”, “de Lioncourt”, “de Romanus”,
“Corvinus”, “Mikaelson”, “Salvatore”, “Pierce”, “St. John”,
“Hellsing”, “Victoria”, “Penwood”, “von Helsing”, “Valentine”,
“Belmont”, “de Pointe du Lac”, “Talamasca”, “Blackwood”, “Nosferatu”,
“Bathory”, “Varney”, “Ruthven”, “Polidori”, “Stoker”, “Rice”,
“von Krolock”, “Montague”, “Capulet”, “Darkmore”, “Nightshade”,
“Crimson”, “Bloodworth”, “Shadowmere”, “Moonveil”, “Starling”,
“Ravenwood”, “Thornheart”, “Ashford”, “Blackthorne”, “Crowley”,
“Morningstar”, “Duskwalker”, “Silverblade”, “Ironheart”, “Grimwood”,
“Wolfsbane”, “Deathwhisper”, “Bloodmoon”, “Nightfall”, “Darkwind”
]

TITLES = [
“The Ancient”, “The Immortal”, “The Bloodthirsty”, “The Elegant”,
“The Ruthless”, “The Cunning”, “The Wise”, “The Feral”, “The Noble”,
“The Savage”, “The Mysterious”, “The Charming”, “The Deadly”,
“The Merciless”, “The Graceful”, “The Powerful”, “The Seductive”,
“The Vengeful”, “The Patient”, “The Swift”, “The Shadow”,
“The Daywalker”, “The Elder”, “The Progenitor”, “The Forsaken”,
“The Reborn”, “The Eternal”, “The Cursed”, “The Blessed”,
“The Undying”, “The Nightwalker”, “The Bloodlord”, “The Sire”
]

VAMPIRE_CLANS = [
“Nosferatu”, “Toreador”, “Ventrue”, “Malkavian”, “Tremere”,
“Brujah”, “Gangrel”, “Giovanni”, “Tzimisce”, “Lasombra”,
“Assamite”, “Setite”, “Ravnos”, “Salubri”, “Cappadocian”,
“True Brood”, “Purebloods”, “Dhampir”, “Strigoi”, “Moroi”
]

ABILITIES = [
“Blood Manipulation”, “Mind Control”, “Super Speed”, “Super Strength”,
“Shapeshifting”, “Shadow Walking”, “Hypnosis”, “Regeneration”,
“Blood Magic”, “Telekinesis”, “Weather Control”, “Animal Control”,
“Illusion Casting”, “Precognition”, “Telepathy”, “Invisibility”,
“Flight”, “Mist Form”, “Wall Crawling”, “Enhanced Senses”,
“Blood Absorption”, “Life Drain”, “Necromancy”, “Time Dilation”,
“Reality Warping”, “Dimensional Shift”, “Soul Binding”, “Death Touch”
]

ORIGINS = [
“Turned during the Crusades by a mysterious knight”,
“Born from an ancient bloodline dating back to Mesopotamia”,
“Created by a dark ritual gone wrong in Victorian London”,
“Awakened from centuries of slumber in a forgotten tomb”,
“Transformed by drinking from the Holy Grail corrupted by demon blood”,
“Cursed by a witch during the Salem trials”,
“Infected by a progenitor vampire in ancient Rome”,
“Rose from the dead after a betrayal in medieval Europe”,
“Created in a secret laboratory experiment combining science and dark magic”,
“Descended from the first vampire created by a fallen angel”,
“Turned during the Black Plague as part of a survival pact”,
“Transformed during a full moon eclipse in ancient Egypt”,
“Created by consuming the heart of an elder vampire”,
“Born from the union of a vampire lord and a powerful sorceress”,
“Emerged from the shadows after witnessing unspeakable horror”
]

PERSONALITIES = [
“Charismatic and manipulative, enjoys toying with mortals”,
“Honorable and follows an ancient code despite their nature”,
“Savage and feral, barely clinging to their humanity”,
“Calculating and strategic, always planning three steps ahead”,
“Melancholic and regretful of their immortal curse”,
“Sadistic and revels in causing pain and suffering”,
“Noble and protective of the innocent despite being a monster”,
“Hedonistic and indulges in every pleasure immortality offers”,
“Wise and philosophical, seeking meaning in eternal existence”,
“Wrathful and seeking revenge against those who wronged them”,
“Artistic and obsessed with beauty and perfection”,
“Mysterious and speaks in riddles and prophecies”,
“Cold and detached, viewing mortals as mere cattle”,
“Playful and mischievous, enjoying pranks and games”,
“Brooding and tormented by memories of their mortal life”
]

WEAKNESSES = [
“Sunlight (reduced)”, “Silver weapons”, “Holy water”, “Wooden stakes”,
“Garlic”, “Running water”, “Religious symbols”, “Fire”,
“Decapitation”, “Invitation required”, “Counting compulsion”,
“Cannot cross running water”, “Reflection weakness”, “Obsession with blood”
]

# Load/Save functions

def load_json(filename, default=None):
if default is None:
default = {}
if os.path.exists(filename):
with open(filename, ‘r’) as f:
return json.load(f)
return default

def save_json(filename, data):
with open(filename, ‘w’) as f:
json.dump(data, f, indent=4)

vampires = load_json(VAMPIRES_FILE, {})
battles = load_json(BATTLES_FILE, [])
user_vampires = load_json(USER_VAMPIRES_FILE, {})

# Generate a random vampire

def generate_vampire(custom_name=None):
vampire_id = f”vamp_{datetime.now().strftime(’%Y%m%d%H%M%S’)}_{random.randint(1000, 9999)}”

```
# Generate name
if custom_name:
    name = custom_name
else:
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    title = random.choice(TITLES)
    name = f"{first} {last} {title}"

# Generate age (100-5000 years)
age = random.randint(100, 5000)

# Generate stats (influenced by age)
age_bonus = min(age // 100, 30)  # Max +30 from age

strength = random.randint(50, 85) + age_bonus
speed = random.randint(50, 85) + age_bonus
intelligence = random.randint(50, 85) + age_bonus
charisma = random.randint(40, 80) + age_bonus
bloodlust = random.randint(30, 90)
regeneration = random.randint(40, 85) + age_bonus

# Cap stats at 150
strength = min(strength, 150)
speed = min(speed, 150)
intelligence = min(intelligence, 150)
charisma = min(charisma, 150)
regeneration = min(regeneration, 150)

# Calculate total power
power = (strength + speed + intelligence + charisma + regeneration) // 5

# Generate abilities (2-5 based on age)
num_abilities = min(2 + (age // 500), 6)
abilities = random.sample(ABILITIES, num_abilities)

# Select weaknesses (2-4)
weaknesses = random.sample(WEAKNESSES, random.randint(2, 4))

vampire = {
    "id": vampire_id,
    "name": name,
    "clan": random.choice(VAMPIRE_CLANS),
    "age": age,
    "origin": random.choice(ORIGINS),
    "personality": random.choice(PERSONALITIES),
    "stats": {
        "strength": strength,
        "speed": speed,
        "intelligence": intelligence,
        "charisma": charisma,
        "bloodlust": bloodlust,
        "regeneration": regeneration,
        "power": power
    },
    "abilities": abilities,
    "weaknesses": weaknesses,
    "wins": 0,
    "losses": 0,
    "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

return vampire
```

# Battle simulation

def simulate_battle(vamp1, vamp2):
“”“Simulates a battle between two vampires with detailed combat rounds”””

```
# Initialize battle state
v1_hp = 100
v2_hp = 100
rounds = []
max_rounds = 15

for round_num in range(1, max_rounds + 1):
    round_data = {
        "round": round_num,
        "actions": []
    }
    
    # Determine who goes first based on speed
    if vamp1["stats"]["speed"] > vamp2["stats"]["speed"]:
        first, second = (vamp1, 1), (vamp2, 2)
    elif vamp2["stats"]["speed"] > vamp1["stats"]["speed"]:
        first, second = (vamp2, 2), (vamp1, 1)
    else:
        first, second = random.choice([((vamp1, 1), (vamp2, 2)), ((vamp2, 2), (vamp1, 1))])
    
    # First attacker's turn
    attacker, attacker_num = first
    defender, defender_num = second
    
    if (attacker_num == 1 and v1_hp > 0) or (attacker_num == 2 and v2_hp > 0):
        damage, action = calculate_damage(attacker, defender)
        
        if defender_num == 1:
            v1_hp -= damage
            v1_hp = max(0, v1_hp)
            round_data["actions"].append({
                "attacker": attacker["name"],
                "defender": defender["name"],
                "action": action,
                "damage": damage,
                "defender_hp": v1_hp
            })
        else:
            v2_hp -= damage
            v2_hp = max(0, v2_hp)
            round_data["actions"].append({
                "attacker": attacker["name"],
                "defender": defender["name"],
                "action": action,
                "damage": damage,
                "defender_hp": v2_hp
            })
    
    # Check if battle is over
    if v1_hp <= 0 or v2_hp <= 0:
        rounds.append(round_data)
        break
    
    # Second attacker's turn
    attacker, attacker_num = second
    defender, defender_num = first
    
    if (attacker_num == 1 and v1_hp > 0) or (attacker_num == 2 and v2_hp > 0):
        damage, action = calculate_damage(attacker, defender)
        
        if defender_num == 1:
            v1_hp -= damage
            v1_hp = max(0, v1_hp)
            round_data["actions"].append({
                "attacker": attacker["name"],
                "defender": defender["name"],
                "action": action,
                "damage": damage,
                "defender_hp": v1_hp
            })
        else:
            v2_hp -= damage
            v2_hp = max(0, v2_hp)
            round_data["actions"].append({
                "attacker": attacker["name"],
                "defender": defender["name"],
                "action": action,
                "damage": damage,
                "defender_hp": v2_hp
            })
    
    rounds.append(round_data)
    
    # Check if battle is over
    if v1_hp <= 0 or v2_hp <= 0:
        break

# Determine winner
if v1_hp > v2_hp:
    winner = vamp1
    loser = vamp2
elif v2_hp > v1_hp:
    winner = vamp2
    loser = vamp1
else:
    # Tie - use power level as tiebreaker
    if vamp1["stats"]["power"] > vamp2["stats"]["power"]:
        winner = vamp1
        loser = vamp2
    else:
        winner = vamp2
        loser = vamp1

return {
    "winner": winner,
    "loser": loser,
    "rounds": rounds,
    "final_hp": {
        vamp1["name"]: v1_hp,
        vamp2["name"]: v2_hp
    }
}
```

def calculate_damage(attacker, defender):
“”“Calculate damage for one attack with ability usage”””

```
# Select a random ability to use
ability = random.choice(attacker["abilities"])

# Base damage from strength
base_damage = attacker["stats"]["strength"] / 10

# Ability modifiers
ability_bonus = 0
action_text = ""

if ability == "Blood Manipulation":
    ability_bonus = random.randint(5, 15)
    action_text = f"uses {ability} to control their opponent's blood"
elif ability == "Mind Control":
    ability_bonus = attacker["stats"]["intelligence"] / 15
    action_text = f"attempts {ability} to disorient their foe"
elif ability == "Super Speed":
    ability_bonus = attacker["stats"]["speed"] / 12
    action_text = f"moves with {ability} for a devastating strike"
elif ability == "Super Strength":
    ability_bonus = attacker["stats"]["strength"] / 10
    action_text = f"channels {ability} into their attack"
elif ability == "Shapeshifting":
    ability_bonus = random.randint(3, 12)
    action_text = f"uses {ability} to transform and attack"
elif ability == "Shadow Walking":
    ability_bonus = random.randint(4, 14)
    action_text = f"emerges from shadows using {ability}"
elif ability == "Blood Magic":
    ability_bonus = attacker["stats"]["intelligence"] / 10
    action_text = f"casts a {ability} spell"
elif ability == "Telekinesis":
    ability_bonus = random.randint(5, 13)
    action_text = f"uses {ability} to hurl objects"
elif ability == "Life Drain":
    ability_bonus = random.randint(6, 16)
    action_text = f"drains life force with {ability}"
elif ability == "Necromancy":
    ability_bonus = random.randint(5, 15)
    action_text = f"summons dark forces through {ability}"
else:
    ability_bonus = random.randint(3, 10)
    action_text = f"strikes with {ability}"

# Intelligence bonus (strategy)
intelligence_bonus = attacker["stats"]["intelligence"] / 20

# Bloodlust bonus (aggression)
bloodlust_bonus = attacker["stats"]["bloodlust"] / 30

# Calculate total damage
total_damage = base_damage + ability_bonus + intelligence_bonus + bloodlust_bonus

# Defender's regeneration reduces damage
damage_reduction = defender["stats"]["regeneration"] / 20
total_damage = max(1, total_damage - damage_reduction)

# Add some randomness
total_damage *= random.uniform(0.8, 1.2)

# Round to integer
total_damage = int(total_damage)

return total_damage, action_text
```

# Format vampire info as embed

def create_vampire_embed(vampire, show_record=True):
embed = discord.Embed(
title=f”🦇 {vampire[‘name’]}”,
description=f”**Clan:** {vampire[‘clan’]}\n**Age:** {vampire[‘age’]} years”,
color=discord.Color.dark_red()
)

```
# Stats
stats_text = f"💪 Strength: {vampire['stats']['strength']}\n"
stats_text += f"⚡ Speed: {vampire['stats']['speed']}\n"
stats_text += f"🧠 Intelligence: {vampire['stats']['intelligence']}\n"
stats_text += f"✨ Charisma: {vampire['stats']['charisma']}\n"
stats_text += f"🩸 Bloodlust: {vampire['stats']['bloodlust']}\n"
stats_text += f"💚 Regeneration: {vampire['stats']['regeneration']}\n"
stats_text += f"⚔️ **Power Level: {vampire['stats']['power']}**"

embed.add_field(name="📊 Stats", value=stats_text, inline=False)

# Abilities
abilities_text = "\n".join([f"• {ability}" for ability in vampire['abilities']])
embed.add_field(name="🔮 Abilities", value=abilities_text, inline=True)

# Weaknesses
weaknesses_text = "\n".join([f"• {weakness}" for weakness in vampire['weaknesses']])
embed.add_field(name="⚠️ Weaknesses", value=weaknesses_text, inline=True)

# Origin & Personality
embed.add_field(name="📜 Origin", value=vampire['origin'], inline=False)
embed.add_field(name="🎭 Personality", value=vampire['personality'], inline=False)

# Battle record
if show_record:
    record_text = f"Wins: {vampire['wins']} | Losses: {vampire['losses']}"
    if vampire['wins'] + vampire['losses'] > 0:
        win_rate = (vampire['wins'] / (vampire['wins'] + vampire['losses'])) * 100
        record_text += f" | Win Rate: {win_rate:.1f}%"
    embed.add_field(name="⚔️ Battle Record", value=record_text, inline=False)

embed.set_footer(text=f"ID: {vampire['id']} | Created: {vampire['created_at']}")

return embed
```

@bot.event
async def on_ready():
print(f’{bot.user} is online’)
print(‘Vampire Battle Bot Ready!’)
print(f’Loaded {len(vampires)} vampires’)
print(f’Recorded {len(battles)} battles’)

@bot.command(name=‘help’)
async def help_command(ctx):
embed = discord.Embed(
title=“🦇 Vampire Battle Bot - Commands”,
description=“Generate vampires and watch them fight!”,
color=discord.Color.dark_purple()
)

```
embed.add_field(
    name="🎲 Generation",
    value="**!genvamp** - Generate a random vampire\n"
          "**!genvamp [name]** - Generate with custom name\n"
          "**!myvamps** - View your vampire collection\n"
          "**!vampire [ID]** - View specific vampire details",
    inline=False
)

embed.add_field(
    name="⚔️ Battles",
    value="**!battle [ID1] [ID2]** - Battle two vampires\n"
          "**!quickbattle** - Generate 2 vampires and battle them\n"
          "**!tournament** - Generate 4 vampires for a tournament\n"
          "**!history** - View recent battle history",
    inline=False
)

embed.add_field(
    name="📊 Leaderboards",
    value="**!leaderboard** - Top 10 vampires by wins\n"
          "**!strongest** - Top 10 by power level\n"
          "**!oldest** - Top 10 oldest vampires",
    inline=False
)

embed.add_field(
    name="🗑️ Management",
    value="**!deletevamp [ID]** - Delete your vampire\n"
          "**!clearmy** - Delete all your vampires\n"
          "**!stats** - View bot statistics",
    inline=False
)

embed.set_footer(text="Vampire IDs look like: vamp_20240214123456_1234")

await ctx.send(embed=embed)
```

@bot.command(name=‘genvamp’)
async def generate_vampire_command(ctx, *, custom_name: str = None):
“”“Generate a new vampire”””
vampire = generate_vampire(custom_name)

```
# Save to global vampires
vampires[vampire['id']] = vampire
save_json(VAMPIRES_FILE, vampires)

# Add to user's collection
user_id = str(ctx.author.id)
if user_id not in user_vampires:
    user_vampires[user_id] = []
user_vampires[user_id].append(vampire['id'])
save_json(USER_VAMPIRES_FILE, user_vampires)

embed = create_vampire_embed(vampire, show_record=False)
embed.set_author(name=f"Created by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

await ctx.send(f"✨ **A new vampire rises from the shadows!**", embed=embed)
```

@bot.command(name=‘vampire’)
async def view_vampire(ctx, vampire_id: str):
“”“View details of a specific vampire”””
if vampire_id not in vampires:
await ctx.send(“❌ Vampire not found! Use !myvamps to see your vampire IDs.”)
return

```
vampire = vampires[vampire_id]
embed = create_vampire_embed(vampire)
await ctx.send(embed=embed)
```

@bot.command(name=‘myvamps’)
async def my_vampires(ctx):
“”“View your vampire collection”””
user_id = str(ctx.author.id)

```
if user_id not in user_vampires or len(user_vampires[user_id]) == 0:
    await ctx.send("❌ You haven't created any vampires yet! Use !genvamp to create one.")
    return

embed = discord.Embed(
    title=f"🦇 {ctx.author.display_name}'s Vampire Collection",
    color=discord.Color.dark_red()
)

vamp_list = ""
for vamp_id in user_vampires[user_id]:
    if vamp_id in vampires:
        vamp = vampires[vamp_id]
        vamp_list += f"**{vamp['name']}**\n"
        vamp_list += f"Power: {vamp['stats']['power']} | W/L: {vamp['wins']}/{vamp['losses']}\n"
        vamp_list += f"ID: `{vamp_id}`\n\n"

if not vamp_list:
    vamp_list = "No vampires found."

embed.description = vamp_list
embed.set_footer(text=f"Total: {len(user_vampires[user_id])} vampires")

await ctx.send(embed=embed)
```

@bot.command(name=‘battle’)
async def battle_command(ctx, vamp1_id: str, vamp2_id: str):
“”“Battle two vampires”””
if vamp1_id not in vampires:
await ctx.send(f”❌ Vampire 1 not found! ID: {vamp1_id}”)
return

```
if vamp2_id not in vampires:
    await ctx.send(f"❌ Vampire 2 not found! ID: {vamp2_id}")
    return

vamp1 = vampires[vamp1_id]
vamp2 = vampires[vamp2_id]

# Battle announcement
announce_embed = discord.Embed(
    title="⚔️ VAMPIRE BATTLE ⚔️",
    description=f"**{vamp1['name']}**\n*Power: {vamp1['stats']['power']}*\n\n🆚\n\n**{vamp2['name']}**\n*Power: {vamp2['stats']['power']}*",
    color=discord.Color.dark_red()
)
announce_embed.set_footer(text="The battle begins...")

await ctx.send(embed=announce_embed)
await asyncio.sleep(2)

# Simulate battle
result = simulate_battle(vamp1, vamp2)

# Create battle report
battle_embed = discord.Embed(
    title="📜 Battle Report",
    color=discord.Color.gold()
)

# Show each round
for round_data in result['rounds'][:10]:  # Show max 10 rounds
    round_text = ""
    for action in round_data['actions']:
        round_text += f"**{action['attacker']}** {action['action']}\n"
        round_text += f"💥 Damage: {action['damage']} | HP Remaining: {action['defender_hp']}\n\n"
    
    battle_embed.add_field(
        name=f"Round {round_data['round']}",
        value=round_text,
        inline=False
    )

if len(result['rounds']) > 10:
    battle_embed.add_field(
        name="...",
        value=f"Battle continued for {len(result['rounds']) - 10} more rounds...",
        inline=False
    )

await ctx.send(embed=battle_embed)
await asyncio.sleep(2)

# Winner announcement
winner_embed = discord.Embed(
    title="🏆 VICTORY!",
    description=f"**{result['winner']['name']}** emerges victorious!",
    color=discord.Color.gold()
)

winner_embed.add_field(
    name="Final HP",
    value=f"{result['winner']['name']}: {result['final_hp'][result['winner']['name']]}\n{result['loser']['name']}: {result['final_hp'][result['loser']['name']]}",
    inline=False
)

winner_embed.add_field(
    name="Battle Duration",
    value=f"{len(result['rounds'])} rounds",
    inline=True
)

await ctx.send(embed=winner_embed)

# Update records
vampires[result['winner']['id']]['wins'] += 1
vampires[result['loser']['id']]['losses'] += 1
save_json(VAMPIRES_FILE, vampires)

# Save battle history
battle_record = {
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "vamp1": vamp1['name'],
    "vamp2": vamp2['name'],
    "winner": result['winner']['name'],
    "rounds": len(result['rounds'])
}
battles.append(battle_record)
save_json(BATTLES_FILE, battles)
```

@bot.command(name=‘quickbattle’)
async def quick_battle(ctx):
“”“Generate 2 random vampires and battle them”””
await ctx.send(“🎲 Generating two random vampires…”)

```
vamp1 = generate_vampire()
vamp2 = generate_vampire()

vampires[vamp1['id']] = vamp1
vampires[vamp2['id']] = vamp2
save_json(VAMPIRES_FILE, vampires)

# Show both vampires
embed1 = create_vampire_embed(vamp1, show_record=False)
embed1.set_author(name="Contender 1")
await ctx.send(embed=embed1)

await asyncio.sleep(1)

embed2 = create_vampire_embed(vamp2, show_record=False)
embed2.set_author(name="Contender 2")
await ctx.send(embed=embed2)

await asyncio.sleep(2)

# Battle
await battle_command(ctx, vamp1['id'], vamp2['id'])
```

@bot.command(name=‘tournament’)
async def tournament(ctx):
“”“Generate 4 vampires and run a tournament”””
await ctx.send(“🏆 **VAMPIRE TOURNAMENT - 4 Contenders!**”)
await asyncio.sleep(1)

```
# Generate 4 vampires
contenders = []
for i in range(4):
    vamp = generate_vampire()
    vampires[vamp['id']] = vamp
    contenders.append(vamp)
    
    embed = create_vampire_embed(vamp, show_record=False)
    embed.set_author(name=f"Contender {i+1}")
    await ctx.send(embed=embed)
    await asyncio.sleep(1)

save_json(VAMPIRES_FILE, vampires)

await ctx.send("⚔️ **SEMI-FINALS**")
await asyncio.sleep(2)

# Semi-final 1
await ctx.send(f"**Match 1:** {contenders[0]['name']} vs {contenders[1]['name']}")
result1 = simulate_battle(contenders[0], contenders[1])
await ctx.send(f"✅ **Winner:** {result1['winner']['name']}")
await asyncio.sleep(2)

# Semi-final 2
await ctx.send(f"**Match 2:** {contenders[2]['name']} vs {contenders[3]['name']}")
result2 = simulate_battle(contenders[2], contenders[3])
await ctx.send(f"✅ **Winner:** {result2['winner']['name']}")
await asyncio.sleep(2)

# Finals
await ctx.send("🏆 **FINALS**")
await asyncio.sleep(2)

final_result = simulate_battle(result1['winner'], result2['winner'])

# Update all records
vampires[result1['winner']['id']]['wins'] += 1
vampires[result1['loser']['id']]['losses'] += 1
vampires[result2['winner']['id']]['wins'] += 1
vampires[result2['loser']['id']]['losses'] += 1

vampires[final_result['winner']['id']]['wins'] += 1
vampires[final_result['loser']['id']]['losses'] += 1

save_json(VAMPIRES_FILE, vampires)

# Championship announcement
champion_embed = discord.Embed(
    title="👑 TOURNAMENT CHAMPION! 👑",
    description=f"**{final_result['winner']['name']}**\n\nHas conquered all challengers and stands victorious!",
    color=discord.Color.gold()
)

champion_embed.add_field(
    name="Tournament Stats",
    value=f"Battles: 2\nWins: 2\nPower Level: {final_result['winner']['stats']['power']}",
    inline=False
)

await ctx.send(embed=champion_embed)
```

@bot.command(name=‘leaderboard’)
async def leaderboard(ctx):
“”“Show top 10 vampires by wins”””
if not vampires:
await ctx.send(“❌ No vampires have been created yet!”)
return

```
sorted_vamps = sorted(vampires.values(), key=lambda x: x['wins'], reverse=True)[:10]

embed = discord.Embed(
    title="🏆 Top 10 Vampires - Most Wins",
    color=discord.Color.gold()
)

leaderboard_text = ""
for i, vamp in enumerate(sorted_vamps, 1):
    win_rate = 0
    if vamp['wins'] + vamp['losses'] > 0:
        win_rate = (vamp['wins'] / (vamp['wins'] + vamp['losses'])) * 100
    
    leaderboard_text += f"**{i}.** {vamp['name']}\n"
    leaderboard_text += f"   Wins: {vamp['wins']} | Losses: {vamp['losses']} | Win Rate: {win_rate:.1f}%\n\n"

embed.description = leaderboard_text
await ctx.send(embed=embed)
```

@bot.command(name=‘strongest’)
async def strongest(ctx):
“”“Show top 10 vampires by power level”””
if not vampires:
await ctx.send(“❌ No vampires have been created yet!”)
return

```
sorted_vamps = sorted(vampires.values(), key=lambda x: x['stats']['power'], reverse=True)[:10]

embed = discord.Embed(
    title="💪 Top 10 Most Powerful Vampires",
    color=discord.Color.dark_red()
)

leaderboard_text = ""
for i, vamp in enumerate(sorted_vamps, 1):
    leaderboard_text += f"**{i}.** {vamp['name']}\n"
    leaderboard_text += f"   Power: {vamp['stats']['power']} | Age: {vamp['age']} years\n\n"

embed.description = leaderboard_text
await ctx.send(embed=embed)
```

@bot.command(name=‘oldest’)
async def oldest(ctx):
“”“Show top 10 oldest vampires”””
if not vampires:
await ctx.send(“❌ No vampires have been created yet!”)
return

```
sorted_vamps = sorted(vampires.values(), key=lambda x: x['age'], reverse=True)[:10]

embed = discord.Embed(
    title="🕰️ Top 10 Oldest Vampires",
    color=discord.Color.dark_purple()
)

leaderboard_text = ""
for i, vamp in enumerate(sorted_vamps, 1):
    leaderboard_text += f"**{i}.** {vamp['name']}\n"
    leaderboard_text += f"   Age: {vamp['age']} years | Clan: {vamp['clan']}\n\n"

embed.description = leaderboard_text
await ctx.send(embed=embed)
```

@bot.command(name=‘history’)
async def battle_history(ctx):
“”“Show recent battle history”””
if not battles:
await ctx.send(“❌ No battles have been fought yet!”)
return

```
recent_battles = battles[-10:][::-1]  # Last 10, reversed

embed = discord.Embed(
    title="📜 Recent Battle History",
    color=discord.Color.blue()
)

history_text = ""
for i, battle in enumerate(recent_battles, 1):
    history_text += f"**{battle['timestamp']}**\n"
    history_text += f"{battle['vamp1']} vs {battle['vamp2']}\n"
    history_text += f"Winner: {battle['winner']} ({battle['rounds']} rounds)\n\n"

embed.description = history_text
await ctx.send(embed=embed)
```

@bot.command(name=‘deletevamp’)
async def delete_vampire(ctx, vampire_id: str):
“”“Delete a vampire you own”””
user_id = str(ctx.author.id)

```
if user_id not in user_vampires or vampire_id not in user_vampires[user_id]:
    await ctx.send("❌ You don't own this vampire or it doesn't exist!")
    return

if vampire_id not in vampires:
    await ctx.send("❌ Vampire not found!")
    return

vamp_name = vampires[vampire_id]['name']

# Remove from user's collection
user_vampires[user_id].remove(vampire_id)
save_json(USER_VAMPIRES_FILE, user_vampires)

# Remove from global vampires
del vampires[vampire_id]
save_json(VAMPIRES_FILE, vampires)

await ctx.send(f"✅ {vamp_name} has been permanently destroyed!")
```

@bot.command(name=‘clearmy’)
async def clear_my_vampires(ctx):
“”“Delete all your vampires”””
user_id = str(ctx.author.id)

```
if user_id not in user_vampires or len(user_vampires[user_id]) == 0:
    await ctx.send("❌ You don't have any vampires to delete!")
    return

count = len(user_vampires[user_id])

# Remove all vampires
for vamp_id in user_vampires[user_id]:
    if vamp_id in vampires:
        del vampires[vamp_id]

user_vampires[user_id] = []

save_json(VAMPIRES_FILE, vampires)
save_json(USER_VAMPIRES_FILE, user_vampires)

await ctx.send(f"✅ Destroyed {count} vampires from your collection!")
```

@bot.command(name=‘stats’)
async def bot_stats(ctx):
“”“Show bot statistics”””
total_vamps = len(vampires)
total_battles = len(battles)
total_users = len([u for u in user_vampires.values() if len(u) > 0])

```
# Calculate average power
if vampires:
    avg_power = sum(v['stats']['power'] for v in vampires.values()) / len(vampires)
else:
    avg_power = 0

# Find most powerful vampire
most_powerful = None
if vampires:
    most_powerful = max(vampires.values(), key=lambda x: x['stats']['power'])

# Find most wins
most_wins = None
if vampires:
    most_wins = max(vampires.values(), key=lambda x: x['wins'])

embed = discord.Embed(
    title="📊 Vampire Battle Bot Statistics",
    color=discord.Color.dark_blue()
)

embed.add_field(
    name="General Stats",
    value=f"Total Vampires: {total_vamps}\nTotal Battles: {total_battles}\nActive Users: {total_users}",
    inline=False
)

if most_powerful:
    embed.add_field(
        name="Most Powerful",
        value=f"{most_powerful['name']}\nPower: {most_powerful['stats']['power']}",
        inline=True
    )

if most_wins:
    embed.add_field(
        name="Most Victorious",
        value=f"{most_wins['name']}\nWins: {most_wins['wins']}",
        inline=True
    )

embed.add_field(
    name="Average Power Level",
    value=f"{avg_power:.1f}",
    inline=True
)

await ctx.send(embed=embed)
```

# Error handling

@bot.event
async def on_command_error(ctx, error):
if isinstance(error, commands.MissingRequiredArgument):
await ctx.send(f”❌ Missing required argument! Use !help to see command usage.”)
elif isinstance(error, commands.CommandNotFound):
pass  # Ignore unknown commands
else:
await ctx.send(f”❌ An error occurred: {str(error)}”)
print(f”Error: {error}”)

# Run the bot

if **name** == “**main**”:
TOKEN = os.getenv(‘DISCORD_TOKEN’)

```
if TOKEN is None:
    print("ERROR: DISCORD_TOKEN not found!")
    print("Create a .env file with DISCORD_TOKEN=your_token")
else:
    print("Token found! Starting Vampire Battle Bot...")
    bot.run(TOKEN)
```
