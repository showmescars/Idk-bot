import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
from datetime import datetime
import json

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

VAMPIRES_FILE = 'vampires.json'

FIRST_NAMES = [
    "Dracula", "Vladislav", "Carmilla", "Lestat", "Akasha", "Armand", "Selene", "Viktor",
    "Marcus", "Lucian", "Sonja", "Aro", "Caius", "Demetri", "Elijah", "Klaus",
    "Rebekah", "Damon", "Stefan", "Katherine", "Silas", "Niklaus", "Mikael", "Esther",
    "Freya", "Lucien", "Tristan", "Aurora", "Atticus", "Antoinette", "Sage", "Maddox",
    "Valerie", "Nora", "Finn", "Kol", "Alaric", "Rayna", "Julian", "Lily"
]

LAST_NAMES = [
    "Tepes", "Karnstein", "De Lioncourt", "Enkil", "Romanus", "Corvinus", "Nightshade",
    "Bloodworth", "Blackthorn", "Darkmore", "Volturi", "Mikaelson", "Salvatore", "Pierce",
    "Bloodmoon", "Crimson", "Ravencroft", "Shadowend", "Duskbane", "Nocturne",
    "Morningstar", "Blackwood", "Draken", "Eclipse", "Eventide", "Sanguine",
    "Hemlock", "Mortis", "Grimwood", "Nightfall", "Darkholm", "Ashford"
]

ORIGINS = [
    "Transylvania", "Romania", "Italy", "France", "England", "Russia",
    "Egypt", "Greece", "Spain", "Hungary", "Germany", "Scandinavia",
    "The Ottoman Empire", "The Byzantine Empire", "Ancient Persia"
]

BLOODLINES = [
    "Pureblooded Ancient", "Turned by an Elder", "Born of a Progenitor",
    "Cursed Lineage", "Royal Vampire Court", "Rogue Sire Line",
    "Lost Bloodline", "The First Brood", "Shadowborn Clan", "The Crimson Order"
]

WEAKNESSES = [
    "Sunlight", "Silver", "Holy water", "Wooden stakes", "Garlic",
    "Running water", "Invitation barrier", "Sacred ground", "Fire", "Decapitation"
]

ABILITIES = [
    "Blood Manipulation", "Shadow Travel", "Hypnotic Gaze", "Supernatural Speed",
    "Enhanced Strength", "Regeneration", "Mist Form", "Bat Transformation",
    "Mind Control", "Blood Drain", "Shapeshifting", "Feral Claws",
    "Venomous Bite", "Telepathy", "Darkness Manipulation", "Fear Inducement",
    "Thrall Creation", "Death Touch", "Soul Drain", "Crimson Lightning",
    "Bloodlust Rage", "Mesmerize", "Bloodfire", "Cursed Bite",
    "Blood Wings", "Lunar Empowerment", "Corpse Animation", "Dark Pact"
]


def load_vampires():
    if os.path.exists(VAMPIRES_FILE):
        with open(VAMPIRES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_vampires(vampires):
    with open(VAMPIRES_FILE, 'w') as f:
        json.dump(vampires, f, indent=4)

def generate_id():
    vampires = load_vampires()
    existing = {v.get('id') for v in vampires.values()}
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing:
            return new_id

def get_tier(power):
    if power <= 500:      return "Fledgling"
    elif power <= 1000:   return "Stalker"
    elif power <= 2000:   return "Nightlord"
    elif power <= 3500:   return "Elder"
    elif power <= 5000:   return "Ancient"
    elif power <= 7000:   return "Progenitor"
    elif power <= 9000:   return "Blood God"
    else:                 return "Primordial"

def get_personality(power):
    if power <= 1000:
        return random.choice(["Impulsive", "Reckless", "Hungry", "Unstable", "Naive"])
    elif power <= 4000:
        return random.choice(["Calculating", "Patient", "Cunning", "Ruthless", "Disciplined"])
    else:
        return random.choice(["Omniscient", "Cold", "Godlike", "Detached", "Tyrannical"])


@bot.event
async def on_ready():
    print(f'{bot.user} is online')

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs.")
        return False
    return True


@bot.command(name='make')
async def make_vampire(ctx):
    vampires = load_vampires()
    vid      = generate_id()

    name        = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    power       = random.randint(100, 10000)
    tier        = get_tier(power)
    age         = random.randint(100, 3000)
    origin      = random.choice(ORIGINS)
    bloodline   = random.choice(BLOODLINES)
    personality = get_personality(power)
    height      = f"{random.randint(5, 7)}'{random.randint(0, 11)}\""
    weight      = random.randint(130, 230)
    num_abilities = random.randint(2, 6)
    abilities   = random.sample(ABILITIES, num_abilities)
    weakness    = random.sample(WEAKNESSES, random.randint(1, 3))
    turned_age  = random.randint(17, 60)

    vampire = {
        "id":          vid,
        "name":        name,
        "owner_id":    str(ctx.author.id),
        "owner_name":  str(ctx.author),
        "power":       power,
        "tier":        tier,
        "age":         age,
        "turned_at":   turned_age,
        "origin":      origin,
        "bloodline":   bloodline,
        "personality": personality,
        "height":      height,
        "weight":      weight,
        "abilities":   abilities,
        "weaknesses":  weakness,
        "created_at":  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    vampires[vid] = vampire
    save_vampires(vampires)

    embed = discord.Embed(
        title=name,
        description=f"Owner: {ctx.author.name}\nID: {vid}",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="Power Level", value=str(power),      inline=True)
    embed.add_field(name="Tier",        value=tier,             inline=True)
    embed.add_field(name="Age",         value=f"{age} years",  inline=True)
    embed.add_field(name="Turned At",   value=f"Age {turned_age}", inline=True)
    embed.add_field(name="Origin",      value=origin,           inline=True)
    embed.add_field(name="Bloodline",   value=bloodline,        inline=True)
    embed.add_field(name="Personality", value=personality,      inline=True)
    embed.add_field(name="Height",      value=height,           inline=True)
    embed.add_field(name="Weight",      value=f"{weight} lbs",  inline=True)
    embed.add_field(name="Abilities",   value="\n".join(abilities),           inline=False)
    embed.add_field(name="Weaknesses",  value="\n".join(weakness),            inline=False)
    embed.set_footer(text=f"Created {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    await ctx.send(embed=embed)


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found!")
    else:
        print("Token found! Starting bot...")
        bot.run(TOKEN)
