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
bot = commands.Bot(command_prefix=’?’, intents=intents, help_command=None)
VAMPIRES_FILE = ‘vampires.json’
VAMPIRE_FIRST_NAMES = [
“Dracula”, “Vlad”, “Lestat”, “Armand”, “Louis”, “Akasha”, “Marius”, “Kain”,
“Alucard”, “Selene”, “Blade”, “Viktor”, “Marcus”, “Amelia”, “Sonja”, “Lucian”,
“Nosferatu”, “Carmilla”, “Erzsebet”, “Lilith”, “Cain”, “Abel”, “Seras”, “Integra”,
“D”, “Rayne”, “Astaroth”, “Malachi”, “Corvinus”, “Demetrius”, “Theron”, “Sanctus”,
“Nyx”, “Raven”, “Eclipse”, “Crimson”, “Shadow”, “Obsidian”, “Scarlet”, “Vesper”
]
VAMPIRE_LAST_NAMES = [
“Tepes”, “Drăculești”, “de Lioncourt”, “Romanus”, “de Pointe du Lac”, “Blackwood”,
“Nightshade”, “Bloodmoon”, “Darkholme”, “von Carstein”, “Ravenscroft”, “Thornheart”,
“Ashborne”, “Grimveil”, “Shadowfang”, “Crimsonbane”, “Duskwalker”, “Bloodworth”,
“Blackthorn”, “Nightingale”, “Darkmore”, “Bloodstone”, “Shadowmere”, “Ravenclaw”,
“Grimshaw”, “Nightfall”, “Duskwood”, “Ashwood”, “Ironblood”, “Stormveil”
]
VAMPIRE_CLANS = [
“Nosferatu”, “Ventrue”, “Tremere”, “Toreador”, “Brujah”, “Malkavian”,
“Gangrel”, “Tzimisce”, “Lasombra”, “Setite”, “Giovanni”, “Ravnos”,
“Assamite”, “Salubri”, “Cappadocian”, “Blood Moon”, “Shadow Council”,
“Crimson Court”, “Night Legion”, “Dark Covenant”
]
MISSIONS = [
{
“name”: “Hunt in the Dark Alley”,
“description”: “Your vampire prowls the dark alleys looking for prey”,
“difficulty”: “easy”
},
{
“name”: “Raid the Blood Bank”,
“description”: “A risky mission to steal fresh blood from the hospital”,
“difficulty”: “medium”
},
{
“name”: “Challenge the Elder Vampire”,
“description”: “Face off against an ancient and powerful vampire”,
“difficulty”: “hard”
},
{
“name”: “Defend Your Territory”,
“description”: “Enemy vampires are invading your hunting grounds”,
“difficulty”: “medium”
},
{
“name”: “Infiltrate the Vampire Council”,
“description”: “Sneak into the secret meeting of vampire elders”,
“difficulty”: “hard”
},
{
“name”: “Hunt the Werewolf Pack”,
“description”: “Ancient enemies cross paths in the forest”,
“difficulty”: “hard”
},
{
“name”: “Scavenge the Graveyard”,
“description”: “Search for mystic artifacts among the tombstones”,
“difficulty”: “easy”
},
{
“name”: “Battle in the Underground Arena”,
“description”: “Fight for glory in the secret vampire fighting pits”,
“difficulty”: “medium”
}
]
def load_vampires():
if os.path.exists(VAMPIRES_FILE):
with open(VAMPIRES_FILE, ‘r’) as f:
return json.load(f)
return {}
def save_vampires(vampires):
with open(VAMPIRES_FILE, ‘w’) as f:
json.dump(vampires, f, indent=4)
vampires = load_vampires()
def generate_short_id():
“”“Generate a short 6-character ID”””
import string
chars = string.ascii_uppercase + string.digits
return ‘’.join(random.choice(chars) for _ in range(6))
def generate_vampire_stats():
return {
“strength”: random.randint(50, 100),
“speed”: random.randint(50, 100),
“intelligence”: random.randint(50, 100),
“blood_power”: random.randint(50, 100),
“defense”: random.randint(50, 100)
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
“”“Create an AI vampire with 30% weak, 70% strong distribution”””
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

stat_names = ["strength", "speed", "intelligence", "blood_
