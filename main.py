import discord
from discord.ext import commands
import json
import os
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

CHARACTERS_FILE = 'characters.json'
GRAVEYARD_FILE = 'graveyard.json'

FIRST_NAMES = [
    "Dracula","Vladislav","Carmilla","Lestat","Akasha","Armand","Blade","Selene",
    "Viktor","Marcus","Lucian","Sonja","Aro","Caius","Demetri","Jane",
    "Alec","Elijah","Klaus","Rebekah","Kol","Finn","Alaric","Damon",
    "Stefan","Katherine","Silas","Amara","Niklaus","Mikael","Esther",
    "Freya","Dahlia","Lucien","Tristan","Aurora","Rayna","Julian","Lily"
]

LAST_NAMES = [
    "Tepes","Karnstein","De Lioncourt","Romanus","Corvinus","Nightshade",
    "Bloodworth","Blackthorn","Darkmore","Mikaelson","Salvatore","Pierce",
    "Bennett","Forbes","Lockwood","Gilbert","Fell","Ashford",
    "Crimson","Ravencroft","Shadowend","Duskbane","Nocturne",
    "Morningstar","Hellsing","Belmont","Blackwood","Draken",
    "Eclipse","Twilight","Sanguine","Hemlock","Mortis"
]

# ---------------- FILE IO ----------------

def load_characters():
    if os.path.exists(CHARACTERS_FILE):
        with open(CHARACTERS_FILE,'r') as f:
            return json.load(f)
    return {}

def save_characters(data):
    with open(CHARACTERS_FILE,'w') as f:
        json.dump(data,f,indent=4)

def load_graveyard():
    if os.path.exists(GRAVEYARD_FILE):
        with open(GRAVEYARD_FILE,'r') as f:
            return json.load(f)
    return []

def save_graveyard(data):
    with open(GRAVEYARD_FILE,'w') as f:
        json.dump(data,f,indent=4)

# ---------------- UTILS ----------------

def generate_unique_id():
    chars = load_characters()
    graves = load_graveyard()

    ids = [c["character_id"] for c in chars.values()]
    ids += [g["character_id"] for g in graves]

    while True:
        i = str(random.randint(100000,999999))
        if i not in ids:
            return i

def generate_random_vampire_power():
    roll=random.randint(1,100)
    if roll<=45: return random.randint(10,400)
    if roll<=75: return random.randint(401,1000)
    if roll<=90: return random.randint(1001,1600)
    return random.randint(1601,2000)

def generate_ai_power():
    roll=random.randint(1,100)
    if roll<=50: return random.randint(10,800)
    if roll<=75: return random.randint(801,1400)
    if roll<=90: return random.randint(1401,1800)
    return random.randint(1801,2000)

def calculate_death_chance(player,enemy,won):
    if won:
        base=5
        if player-enemy<100: base=15
    else:
        base=35+(enemy-player)/200
    return int(max(5,min(80,base)))

def simulate_battle(pname,ppower,ename,epower):
    diff=ppower-epower
    prob=50+(diff/20)
    prob=max(5,min(95,prob))
    roll=random.randint(1,100)
    return roll<=prob

# ---------------- EVENTS ----------------

@bot.event
async def on_ready():
    print(f"{bot.user} online")

@bot.check
async def no_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Server only.")
        return False
    return True

@bot.event
async def on_command_error(ctx,error):
    print(error)

# ---------------- CREATE ----------------

@bot.command()
async def make(ctx):
    uid=str(ctx.author.id)
    chars=load_characters()

    if any(c["user_id"]==uid for c in chars.values()):
        await ctx.send("You already have a vampire.")
        return

    name=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    cid=generate_unique_id()
    power=generate_random_vampire_power()

    data={
        "character_id":cid,
        "name":name,
        "user_id":uid,
        "username":str(ctx.author),
        "power_level":power,
        "wins":0,
        "losses":0,
        "created_at":str(datetime.now())
    }

    chars[cid]=data
    save_characters(chars)

    tier=("Fledgling" if power<=400 else
          "Experienced" if power<=1000 else
          "Ancient" if power<=1600 else
          "Primordial")

    e=discord.Embed(title="Vampire Created",
        description=f"**{name}**",
        color=discord.Color.dark_red())

    e.add_field(name="ID",value=cid)
    e.add_field(name="Power",value=power)
    e.add_field(name="Tier",value=tier)
    e.add_field(name="Record",value="0-0")
    e.set_footer(text="Use ?random <ID>")

    await ctx.send(embed=e)

# ---------------- RANDOM EVENT ----------------

@bot.command()
async def random(ctx,character_id:str=None):
    if not character_id:
        await ctx.send("?random <id>")
        return

    chars=load_characters()
    graves=load_graveyard()

    if character_id not in chars:
        await ctx.send("Not found.")
        return

    v=chars[character_id]

    if v["user_id"]!=str(ctx.author.id):
        await ctx.send("Not yours.")
        return

    rival=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    rpower=generate_ai_power()

    e=discord.Embed(
        title="RIVAL ENCOUNTER",
        description=f"{rival} (Power {rpower}) challenges {v['name']}",
        color=discord.Color.red()
    )
    await ctx.send(embed=e)
    await asyncio.sleep(2)

    won=simulate_battle(v["name"],v["power_level"],rival,rpower)
    death=random.randint(1,100)<=calculate_death_chance(
        v["power_level"],rpower,won)

    if death:
        dead=v.copy()
        dead["death_date"]=str(datetime.now())
        dead["killed_by"]=rival
        graves.append(dead)
        save_graveyard(graves)

        del chars[character_id]
        save_characters(chars)

        await ctx.send(f"💀 {v['name']} was destroyed by {rival}")
        return

    if won:
        v["wins"]+=1
        gain=random.randint(20,120)
        v["power_level"]=min(2000,v["power_level"]+gain)
        await ctx.send(f"🏆 Victory! +{gain} power")
    else:
        v["losses"]+=1
        await ctx.send("Defeated but survived.")

    chars[character_id]=v
    save_characters(chars)

# ---------------- SHOW ----------------

@bot.command()
async def show(ctx):
    uid=str(ctx.author.id)
    chars=load_characters()

    for c in chars.values():
        if c["user_id"]==uid:
            e=discord.Embed(title=c["name"],
                            color=discord.Color.purple())
            e.add_field(name="ID",value=c["character_id"])
            e.add_field(name="Power",value=c["power_level"])
            e.add_field(name="Record",
                        value=f"{c['wins']}-{c['losses']}")
            await ctx.send(embed=e)
            return

    await ctx.send("No vampire.")

# ---------------- RUN ----------------

bot.run(os.getenv("DISCORD_TOKEN"))
