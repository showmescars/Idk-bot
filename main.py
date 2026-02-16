import discord
from discord.ext import commands
import json
import os
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# Files
CHARACTERS_FILE = 'characters.json'
GRAVEYARD_FILE = 'graveyard.json'

# Vampire abilities pool with power ratings
SKILLS = {
    "Blood Manipulation": {"offensive": 8, "defensive": 6},
    "Shadow Travel": {"offensive": 5, "defensive": 9},
    "Hypnotic Gaze": {"offensive": 7, "defensive": 4},
    "Supernatural Speed": {"offensive": 7, "defensive": 8},
    "Enhanced Strength": {"offensive": 9, "defensive": 5},
    "Regeneration": {"offensive": 3, "defensive": 10},
    "Mist Form": {"offensive": 4, "defensive": 9},
    "Bat Transformation": {"offensive": 5, "defensive": 7},
    "Mind Control": {"offensive": 9, "defensive": 6},
    "Night Vision": {"offensive": 6, "defensive": 5},
    "Wall Crawling": {"offensive": 4, "defensive": 6},
    "Blood Drain": {"offensive": 10, "defensive": 4},
    "Immortality": {"offensive": 5, "defensive": 8},
    "Shapeshifting": {"offensive": 6, "defensive": 8},
    "Feral Claws": {"offensive": 8, "defensive": 5},
    "Venomous Bite": {"offensive": 9, "defensive": 4},
    "Telepathy": {"offensive": 7, "defensive": 6},
    "Superhuman Agility": {"offensive": 7, "defensive": 8},
    "Blood Sense": {"offensive": 6, "defensive": 7},
    "Darkness Manipulation": {"offensive": 8, "defensive": 7},
    "Charm": {"offensive": 7, "defensive": 5},
    "Fear Inducement": {"offensive": 8, "defensive": 6},
    "Enhanced Senses": {"offensive": 6, "defensive": 7},
    "Undead Resilience": {"offensive": 4, "defensive": 9},
    "Thrall Creation": {"offensive": 7, "defensive": 5},
    "Blood Healing": {"offensive": 3, "defensive": 9},
    "Vampiric Speed": {"offensive": 8, "defensive": 7},
    "Death Touch": {"offensive": 10, "defensive": 3},
    "Soul Drain": {"offensive": 9, "defensive": 5},
    "Crimson Lightning": {"offensive": 10, "defensive": 5},
    "Bloodlust Rage": {"offensive": 10, "defensive": 4},
    "Eternal Youth": {"offensive": 4, "defensive": 8},
    "Mesmerize": {"offensive": 8, "defensive": 5},
    "Bloodfire": {"offensive": 9, "defensive": 5},
    "Cursed Bite": {"offensive": 9, "defensive": 4},
    "Nightmare Inducement": {"offensive": 7, "defensive": 6},
    "Blood Wings": {"offensive": 7, "defensive": 8},
    "Lunar Empowerment": {"offensive": 8, "defensive": 7},
    "Corpse Animation": {"offensive": 7, "defensive": 6},
    "Dark Pact": {"offensive": 9, "defensive": 6}
}

# Human combat skills
HUMAN_SKILLS = {
    "Silver Bullets": {"offensive": 9, "defensive": 5},
    "Holy Water": {"offensive": 8, "defensive": 6},
    "Wooden Stakes": {"offensive": 10, "defensive": 4},
    "Garlic Barrier": {"offensive": 4, "defensive": 9},
    "UV Light": {"offensive": 8, "defensive": 7},
    "Crossbow Mastery": {"offensive": 9, "defensive": 5},
    "Blessed Blades": {"offensive": 8, "defensive": 6},
    "Faith Shield": {"offensive": 5, "defensive": 10},
    "Hunter Reflexes": {"offensive": 7, "defensive": 8},
    "Vampire Lore": {"offensive": 6, "defensive": 7},
    "Tactical Combat": {"offensive": 8, "defensive": 7},
    "Sacred Rituals": {"offensive": 7, "defensive": 8},
    "Sunlight Grenades": {"offensive": 10, "defensive": 4},
    "Blood Ward": {"offensive": 5, "defensive": 9},
    "Quick Draw": {"offensive": 8, "defensive": 6}
}

# Vampire name pools
FIRST_NAMES = [
    "Dracula", "Vladislav", "Carmilla", "Lestat", "Akasha", "Armand", "Blade", "Selene",
    "Viktor", "Marcus", "Lucian", "Sonja", "Aro", "Caius", "Demetri", "Jane",
    "Alec", "Elijah", "Klaus", "Rebekah", "Kol", "Finn", "Alaric", "Damon",
    "Stefan", "Katherine", "Silas", "Qetsiyah", "Amara", "Niklaus", "Mikael", "Esther",
    "Freya", "Dahlia", "Lucien", "Tristan", "Aurora", "Rayna", "Julian", "Lily",
    "Valerie", "Nora", "Mary", "Beau", "Oscar", "Malcolm", "Sage", "Maddox",
    "Atticus", "Greta", "Antoinette"
]

LAST_NAMES = [
    "Tepes", "Drăculești", "Karnstein", "De Lioncourt", "Enkil", "Romanus", "Corvinus", "Nightshade",
    "Von Doom", "Bloodworth", "Blackthorn", "Darkmore", "Volturi", "Mikaelson", "Salvatore", "Pierce",
    "Bennett", "Forbes", "Lockwood", "Donovan", "Gilbert", "Fell", "Whitmore", "St. John",
    "Ashford", "Bloodmoon", "Crimson", "Ravencroft", "Shadowend", "Duskbane", "Nocturne", "Grave",
    "Morningstar", "Hellsing", "Alucard", "Belmont", "Castlevania", "Blackwood", "Von Carstein", "Draken",
    "Mourning", "Eclipse", "Eventide", "Twilight", "Sanguine", "Hemlock", "Mortis", "Grimwood",
    "Nightfall", "Darkholm"
]

# Human first names for blood transfer victims
HUMAN_FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald",
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica",
    "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra", "Ashley",
    "Emily", "Emma", "Olivia", "Sophia", "Isabella", "Mia", "Charlotte", "Amelia"
]

HUMAN_LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris",
    "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright"
]

# Transfer requests storage (temporary, in-memory)
transfer_requests = {}


# ---------- helpers ----------

def load_characters():
    if os.path.exists(CHARACTERS_FILE):
        with open(CHARACTERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_characters(characters):
    with open(CHARACTERS_FILE, 'w') as f:
        json.dump(characters, f, indent=4)

def load_graveyard():
    if os.path.exists(GRAVEYARD_FILE):
        with open(GRAVEYARD_FILE, 'r') as f:
            return json.load(f)
    return []

def save_graveyard(graveyard):
    with open(GRAVEYARD_FILE, 'w') as f:
        json.dump(graveyard, f, indent=4)

def generate_unique_id():
    characters = load_characters()
    graveyard = load_graveyard()
    existing_ids = [char.get('character_id') for char in characters.values() if 'character_id' in char]
    existing_ids += [char.get('character_id') for char in graveyard if 'character_id' in char]
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing_ids:
            return new_id

def get_vampire_rank(power_level):
    if power_level <= 50:   return "Fledgling"
    elif power_level <= 100: return "Stalker"
    elif power_level <= 200: return "Nightlord"
    elif power_level <= 350: return "Elder"
    elif power_level <= 500: return "Ancient"
    elif power_level <= 650: return "Progenitor"
    elif power_level <= 800: return "Blood God"
    else:                    return "Primordial"

def get_human_rank(power_level):
    if power_level <= 50:   return "Novice Hunter"
    elif power_level <= 100: return "Hunter"
    elif power_level <= 200: return "Veteran Hunter"
    elif power_level <= 350: return "Master Hunter"
    elif power_level <= 500: return "Legendary Hunter"
    elif power_level <= 650: return "Slayer"
    elif power_level <= 800: return "Grand Slayer"
    else:                    return "Ultimate Slayer"

def get_opponent_power_range(player_power):
    if player_power <= 50:   return 10,  70
    elif player_power <= 100: return 50,  130
    elif player_power <= 200: return 100, 250
    elif player_power <= 350: return 200, 400
    elif player_power <= 500: return 350, 550
    elif player_power <= 650: return 500, 700
    elif player_power <= 800: return 650, 850
    else:                     return 750, 1000

def calculate_death_chance(player_power, enemy_power):
    power_diff  = enemy_power - player_power
    death_chance = 30 + (power_diff / 50) * 5
    return int(max(10, min(70, death_chance)))

def simulate_battle(attacker_name, attacker_power, attacker_skills,
                    defender_name, defender_power, defender_skills,
                    skill_dict=None):
    if skill_dict is None:
        skill_dict = SKILLS

    def skill_stat(skill, stat):
        entry = skill_dict.get(skill)
        if entry:
            return entry[stat]
        # fall back to whichever pool has it
        return SKILLS.get(skill, HUMAN_SKILLS.get(skill, {stat: 5}))[stat]

    attacker_offense = sum(skill_stat(s, "offensive") for s in attacker_skills) / len(attacker_skills)
    attacker_defense = sum(skill_stat(s, "defensive") for s in attacker_skills) / len(attacker_skills)
    defender_offense = sum(skill_stat(s, "offensive") for s in defender_skills) / len(defender_skills)
    defender_defense = sum(skill_stat(s, "defensive") for s in defender_skills) / len(defender_skills)

    attacker_hp = 100 + attacker_power * 0.5
    defender_hp = 100 + defender_power * 0.5
    battle_log   = []

    for round_num in range(1, 4):
        if attacker_hp <= 0 or defender_hp <= 0:
            break

        # Attacker hits
        atk_skill   = random.choice(attacker_skills)
        base_dmg    = attacker_power * 0.3 + skill_stat(atk_skill, "offensive") * 2 + random.randint(5, 15)
        final_dmg   = max(5, base_dmg - defender_defense * 0.8)
        defender_hp -= final_dmg
        battle_log.append({"round": round_num, "attacker": attacker_name,
                            "action": f"uses {atk_skill}", "damage": int(final_dmg),
                            "target": defender_name, "target_hp": max(0, int(defender_hp))})

        if defender_hp <= 0:
            break

        # Defender counters
        def_skill   = random.choice(defender_skills)
        base_dmg    = defender_power * 0.3 + skill_stat(def_skill, "offensive") * 2 + random.randint(5, 15)
        final_dmg   = max(5, base_dmg - attacker_defense * 0.8)
        attacker_hp -= final_dmg
        battle_log.append({"round": round_num, "attacker": defender_name,
                            "action": f"counters with {def_skill}", "damage": int(final_dmg),
                            "target": attacker_name, "target_hp": max(0, int(attacker_hp))})

    winner = attacker_name if attacker_hp > defender_hp else defender_name
    winner_hp = int(max(attacker_hp, defender_hp))
    return {"winner": winner, "winner_hp": winner_hp, "battle_log": battle_log}


# ---------- bot ----------

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Vampire Generator Ready')

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True


# ---------- commands ----------

@bot.command(name='make')
async def make_character(ctx):
    """Generate a unique vampire with random abilities and power level"""
    characters = load_characters()

    first_name    = random.choice(FIRST_NAMES)
    last_name     = random.choice(LAST_NAMES)
    character_name = f"{first_name} {last_name}"
    character_id  = generate_unique_id()
    power_level   = random.randint(10, 100)
    num_skills    = random.randint(3, 5)
    selected_skills = random.sample(list(SKILLS.keys()), num_skills)

    character_data = {
        "character_id": character_id,
        "name": character_name,
        "username": str(ctx.author),
        "user_id": str(ctx.author.id),
        "power_level": power_level,
        "skills": selected_skills,
        "wins": 0,
        "losses": 0,
        "race": "vampire",
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    characters[character_id] = character_data
    save_characters(characters)

    rank  = get_vampire_rank(power_level)
    embed = discord.Embed(
        title=character_name,
        description=f"Owner: {ctx.author.name}\nID: `{character_id}`\nRace: Vampire",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="Blood Power", value=str(power_level), inline=False)
    embed.add_field(name="Rank", value=rank, inline=False)
    embed.add_field(name="Vampiric Abilities", value="\n".join(f"- {s}" for s in selected_skills), inline=False)
    embed.add_field(name="Battle Record", value="0-0", inline=False)
    embed.set_footer(text="Use this ID for commands: ?show, ?train, ?fight, ?hunt, ?blood")
    await ctx.send(embed=embed)


@bot.command(name='show')
async def show_character(ctx, character_id: str = None):
    """Show a character by ID. Usage: ?show <character_id>"""
    if character_id is None:
        await ctx.send("Usage: `?show <character_id>`\nExample: `?show 123456`")
        return

    characters = load_characters()

    if character_id not in characters:
        await ctx.send(f"Character ID `{character_id}` not found!")
        return

    char = characters[character_id]
    race = char.get('race', 'vampire')

    if race == "vampire":
        color        = discord.Color.dark_red()
        rank         = get_vampire_rank(char['power_level'])
        power_label  = "Blood Power"
        ability_label = "Vampiric Abilities"
    else:
        color        = discord.Color.blue()
        rank         = get_human_rank(char['power_level'])
        power_label  = "Combat Power"
        ability_label = "Hunter Skills"

    embed = discord.Embed(
        title=char['name'],
        description=f"Owner: {char.get('username', 'Unknown')}\nID: `{char['character_id']}`\nRace: {race.capitalize()}",
        color=color
    )
    embed.add_field(name=power_label, value=str(char['power_level']), inline=False)
    embed.add_field(name="Rank", value=rank, inline=False)
    embed.add_field(name=ability_label, value="\n".join(f"- {s}" for s in char['skills']), inline=False)
    embed.add_field(name="Battle Record", value=f"{char.get('wins', 0)}-{char.get('losses', 0)}", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='mycollection')
async def my_collection(ctx):
    """View your complete character collection with detailed stats"""
    characters  = load_characters()
    user_id     = str(ctx.author.id)
    user_chars  = [c for c in characters.values()
                   if c.get('user_id') == user_id or c.get('shared_user_id') == user_id]

    if not user_chars:
        await ctx.send("You don't have any characters yet! Use `?make` to create one.")
        return

    user_chars.sort(key=lambda x: x['power_level'], reverse=True)

    total_chars   = len(user_chars)
    total_power   = sum(c['power_level'] for c in user_chars)
    avg_power     = total_power // total_chars
    total_wins    = sum(c.get('wins', 0) for c in user_chars)
    total_losses  = sum(c.get('losses', 0) for c in user_chars)
    vampires      = [c for c in user_chars if c.get('race', 'vampire') == 'vampire']
    humans        = [c for c in user_chars if c.get('race', 'vampire') == 'human']

    main_embed = discord.Embed(
        title=f"🧛 {ctx.author.name}'s Character Collection",
        description=(f"**Total Characters:** {total_chars}\n"
                     f"**Vampires:** {len(vampires)} | **Humans:** {len(humans)}\n"
                     f"**Total Power:** {total_power}\n"
                     f"**Average Power:** {avg_power}\n"
                     f"**Overall Record:** {total_wins}-{total_losses}"),
        color=discord.Color.dark_purple()
    )
    await ctx.send(embed=main_embed)

    total_pages = (len(user_chars) + 9) // 10
    for i in range(0, len(user_chars), 10):
        batch      = user_chars[i:i + 10]
        list_embed = discord.Embed(title=f"Character Collection (Page {i // 10 + 1})",
                                   color=discord.Color.dark_red())
        for char in batch:
            race = char.get('race', 'vampire')
            if race == 'vampire':
                rank = get_vampire_rank(char['power_level'])
                icon = "🧛"
            else:
                rank = get_human_rank(char['power_level'])
                icon = "🗡️"
            hybrid_tag = " [HYBRID]" if char.get('is_hybrid', False) else ""
            list_embed.add_field(
                name=f"{char['name']}{hybrid_tag}",
                value=(f"**ID:** `{char['character_id']}`\n"
                       f"**Race:** {icon} {race.capitalize()}\n"
                       f"**Rank:** {rank}\n"
                       f"**Power:** {char['power_level']}\n"
                       f"**Abilities:** {len(char['skills'])}\n"
                       f"**Record:** {char.get('wins', 0)}-{char.get('losses', 0)}"),
                inline=True
            )
        list_embed.set_footer(text=f"Page {i // 10 + 1} of {total_pages} | Use ?show <id> for detailed view")
        await ctx.send(embed=list_embed)


@bot.command(name='list')
async def list_characters(ctx):
    """List all your characters (compact view)"""
    characters = load_characters()
    user_id    = str(ctx.author.id)
    user_chars = [c for c in characters.values()
                  if c.get('user_id') == user_id or c.get('shared_user_id') == user_id]

    if not user_chars:
        await ctx.send("You don't have any characters yet! Use `?make` to create one.")
        return

    user_chars.sort(key=lambda x: x['power_level'], reverse=True)

    embed = discord.Embed(
        title=f"{ctx.author.name}'s Characters",
        description=f"Total: {len(user_chars)} characters | Use `?mycollection` for detailed view",
        color=discord.Color.dark_purple()
    )
    for char in user_chars[:10]:
        race = char.get('race', 'vampire')
        if race == 'vampire':
            rank = get_vampire_rank(char['power_level'])
            icon = "🧛"
        else:
            rank = get_human_rank(char['power_level'])
            icon = "🗡️"
        hybrid_tag = " [HYBRID]" if char.get('is_hybrid', False) else ""
        embed.add_field(
            name=f"{char['name']}{hybrid_tag}",
            value=f"{icon} ID: `{char['character_id']}` | {rank} | Power: {char['power_level']} | {char.get('wins', 0)}-{char.get('losses', 0)}",
            inline=False
        )
    if len(user_chars) > 10:
        embed.set_footer(text=f"Showing 10 of {len(user_chars)} characters")
    await ctx.send(embed=embed)


@bot.command(name='rank')
async def show_ranks(ctx):
    """Display rank tiers for vampires and humans"""
    embed = discord.Embed(
        title="RANK TIERS",
        description="Power rankings for vampires and vampire hunters",
        color=discord.Color.dark_gold()
    )
    embed.add_field(
        name="🧛 VAMPIRE RANKS",
        value=("**Fledgling** (0-50)\n**Stalker** (51-100)\n**Nightlord** (101-200)\n"
               "**Elder** (201-350)\n**Ancient** (351-500)\n**Progenitor** (501-650)\n"
               "**Blood God** (651-800)\n**Primordial** (801-1000)"),
        inline=True
    )
    embed.add_field(
        name="🗡️ HUNTER RANKS",
        value=("**Novice Hunter** (0-50)\n**Hunter** (51-100)\n**Veteran Hunter** (101-200)\n"
               "**Master Hunter** (201-350)\n**Legendary Hunter** (351-500)\n**Slayer** (501-650)\n"
               "**Grand Slayer** (651-800)\n**Ultimate Slayer** (801-1000)"),
        inline=True
    )
    await ctx.send(embed=embed)


@bot.command(name='train')
async def train_character(ctx, character_id: str = None):
    """Train your character to increase their power! Usage: ?train <character_id>"""
    if character_id is None:
        await ctx.send("Usage: `?train <character_id>`\nExample: `?train 123456`\n\nUse `?list` to see your character IDs.")
        return

    characters = load_characters()

    if character_id not in characters:
        await ctx.send(f"Character ID `{character_id}` not found!")
        return

    player_char = characters[character_id]
    user_id     = str(ctx.author.id)

    if player_char.get('user_id') != user_id and player_char.get('shared_user_id') != user_id:
        await ctx.send("You don't own this character!")
        return

    race = player_char.get('race', 'vampire')

    await ctx.send(embed=discord.Embed(
        title="TRAINING SESSION",
        description=f"{player_char['name']} begins intense training...",
        color=discord.Color.blue()
    ))
    await asyncio.sleep(3)

    power_gain = random.randint(5, 25)
    old_power  = player_char['power_level']
    new_power  = min(old_power + power_gain, 1000)
    power_gain = new_power - old_power

    skill_pool = SKILLS if race == 'vampire' else HUMAN_SKILLS
    old_rank   = get_vampire_rank(old_power) if race == 'vampire' else get_human_rank(old_power)
    new_rank   = get_vampire_rank(new_power) if race == 'vampire' else get_human_rank(new_power)
    ranked_up  = old_rank != new_rank

    player_char['power_level'] = new_power

    learned_new_skill = False
    new_skill         = None
    if random.randint(1, 100) <= 20 and len(player_char['skills']) < 15:
        available = [s for s in skill_pool if s not in player_char['skills']]
        if available:
            new_skill = random.choice(available)
            player_char['skills'].append(new_skill)
            learned_new_skill = True

    characters[character_id] = player_char
    save_characters(characters)

    result_embed = discord.Embed(
        title="TRAINING COMPLETE",
        description=f"{player_char['name']} has grown stronger!",
        color=discord.Color.gold()
    )
    result_embed.add_field(name="Power Increase", value=f"{old_power} → {new_power} (+{power_gain})", inline=False)
    if ranked_up:
        result_embed.add_field(name="RANK UP!", value=f"{old_rank} → **{new_rank}**", inline=False)
    if learned_new_skill:
        result_embed.add_field(name="New Ability Learned!", value=new_skill, inline=False)
    result_embed.add_field(name="Total Abilities", value=f"{len(player_char['skills'])} abilities", inline=False)
    await ctx.send(embed=result_embed)


@bot.command(name='hunt')
async def hunt_vampire(ctx, character_id: str = None):
    """Go hunting for blood! Usage: ?hunt <character_id> (Vampires only)"""
    if character_id is None:
        await ctx.send("Usage: `?hunt <character_id>`\nExample: `?hunt 123456`\n\nUse `?list` to see your character IDs.")
        return

    characters = load_characters()

    if character_id not in characters:
        await ctx.send(f"Character ID `{character_id}` not found!")
        return

    player_char = characters[character_id]
    user_id     = str(ctx.author.id)

    if player_char.get('user_id') != user_id and player_char.get('shared_user_id') != user_id:
        await ctx.send("You don't own this character!")
        return

    if player_char.get('race', 'vampire') != 'vampire':
        await ctx.send("Only vampires can hunt for blood! Humans use `?train` instead.")
        return

    await ctx.send(embed=discord.Embed(
        title="BLOOD HUNT",
        description=f"{player_char['name']} prowls through the darkness, searching for prey...",
        color=discord.Color.dark_red()
    ))
    await asyncio.sleep(3)

    old_power    = player_char['power_level']
    outcome_roll = random.randint(1, 100)

    if outcome_roll <= 60:
        power_gain = random.randint(3, 15)
        new_power  = min(old_power + power_gain, 1000)
        player_char['power_level'] = new_power

        learned_skill = False
        new_skill     = None
        if random.randint(1, 100) <= 15 and len(player_char['skills']) < 15:
            available = [s for s in SKILLS if s not in player_char['skills']]
            if available:
                new_skill = random.choice(available)
                player_char['skills'].append(new_skill)
                learned_skill = True

        characters[character_id] = player_char
        save_characters(characters)

        result = discord.Embed(title="SUCCESSFUL HUNT",
                               description=f"{player_char['name']} drains their victim's blood!",
                               color=discord.Color.green())
        result.add_field(name="Blood Consumed", value=f"Power: {old_power} → {new_power} (+{power_gain})", inline=False)
        if learned_skill:
            result.add_field(name="New Ability Learned!", value=f"The hunt has awakened a new power: **{new_skill}**", inline=False)

    elif outcome_roll <= 85:
        power_gain = random.randint(1, 5)
        new_power  = min(old_power + power_gain, 1000)
        player_char['power_level'] = new_power
        characters[character_id]   = player_char
        save_characters(characters)

        result = discord.Embed(title="MODEST HUNT",
                               description=f"{player_char['name']} finds meager prey in the shadows.",
                               color=discord.Color.orange())
        result.add_field(name="Blood Consumed", value=f"Power: {old_power} → {new_power} (+{power_gain})", inline=False)

    else:
        power_loss = random.randint(5, 15)
        new_power  = max(old_power - power_loss, 10)
        player_char['power_level'] = new_power
        characters[character_id]   = player_char
        save_characters(characters)

        result = discord.Embed(title="HUNT GONE WRONG",
                               description=f"{player_char['name']} is injured by vampire hunters!",
                               color=discord.Color.red())
        result.add_field(name="Injured", value=f"Power: {old_power} → {new_power} (-{power_loss})", inline=False)
        result.add_field(name="Status", value="Your vampire has been wounded and will need time to recover.", inline=False)

    await ctx.send(embed=result)


@bot.command(name='blood')
async def blood_transfer(ctx, character_id: str = None):
    """Transfer vampire essence into a human body. Usage: ?blood <character_id>"""
    if character_id is None:
        await ctx.send("Usage: `?blood <character_id>`\nExample: `?blood 123456`\n\n⚠️ **WARNING:** If this ritual fails, your vampire will DIE and you'll become the HUMAN HOST!")
        return

    characters = load_characters()
    graveyard  = load_graveyard()

    if character_id not in characters:
        await ctx.send(f"Character ID `{character_id}` not found!")
        return

    attacker_char = characters[character_id]
    user_id       = str(ctx.author.id)

    if attacker_char.get('user_id') != user_id and attacker_char.get('shared_user_id') != user_id:
        await ctx.send("You don't own this character!")
        return

    if attacker_char.get('race', 'vampire') != 'vampire':
        await ctx.send("Only vampires can use the blood transfer ritual!")
        return

    human_name = f"{random.choice(HUMAN_FIRST_NAMES)} {random.choice(HUMAN_LAST_NAMES)}"

    ritual_embed = discord.Embed(
        title="BLOOD TRANSFER RITUAL",
        description=(f"{attacker_char['name']} stalks through the night and finds {human_name}...\n\n"
                     f"⚠️ The forbidden ritual begins!\n\n"
                     f"**Success:** Gain power as vampire\n**Failure:** Become {human_name}, a human vampire hunter!"),
        color=discord.Color.dark_red()
    )
    ritual_embed.add_field(name=f"Vampire: {attacker_char['name']}",
                           value=f"Power: {attacker_char['power_level']} | Abilities: {len(attacker_char['skills'])}",
                           inline=True)
    ritual_embed.add_field(name=f"Human Victim: {human_name}", value="An unsuspecting mortal...", inline=True)
    await ctx.send(embed=ritual_embed)
    await asyncio.sleep(4)

    success_chance = max(50, min(90, 50 + (attacker_char['power_level'] / 100) * 5))
    roll           = random.randint(1, 100)
    ritual_success = roll <= success_chance

    if ritual_success:
        power_bonus  = random.randint(30, 80)
        new_power    = min(attacker_char['power_level'] + power_bonus, 1000)
        all_skills   = attacker_char['skills'].copy()

        if random.randint(1, 100) <= 40 and len(all_skills) < 15:
            available = [s for s in SKILLS if s not in all_skills]
            if available:
                all_skills.append(random.choice(available))

        old_rank = get_vampire_rank(attacker_char['power_level'])
        new_rank = get_vampire_rank(new_power)

        characters[character_id] = {
            "character_id": attacker_char['character_id'],
            "name": attacker_char['name'],
            "username": str(ctx.author),
            "user_id": user_id,
            "power_level": new_power,
            "skills": all_skills,
            "wins": attacker_char.get('wins', 0),
            "losses": attacker_char.get('losses', 0),
            "race": "vampire",
            "created_at": attacker_char.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            "blood_transfer_count": attacker_char.get('blood_transfer_count', 0) + 1
        }
        save_characters(characters)

        success_embed = discord.Embed(
            title="✅ BLOOD TRANSFER SUCCESSFUL",
            description=f"The ritual is complete! {attacker_char['name']}'s essence has taken over {human_name}'s body!",
            color=discord.Color.gold()
        )
        success_embed.add_field(name="Success Roll", value=f"Rolled {roll} (Success at ≤{int(success_chance)})", inline=False)
        success_embed.add_field(name="Blood Power", value=f"{attacker_char['power_level']} → {new_power} (+{power_bonus})", inline=False)
        if old_rank != new_rank:
            success_embed.add_field(name="RANK UP!", value=f"{old_rank} → **{new_rank}**", inline=False)
        success_embed.add_field(name="Total Abilities", value=f"{len(all_skills)} abilities", inline=False)
        await ctx.send(embed=success_embed)

    else:
        human_power  = random.randint(30, 80)
        human_skills = random.sample(list(HUMAN_SKILLS.keys()), random.randint(3, 5))

        dead_vampire = attacker_char.copy()
        dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dead_vampire['killed_by']  = f"Failed Blood Transfer Ritual (Resisted by {human_name})"
        graveyard.append(dead_vampire)
        save_graveyard(graveyard)

        characters[character_id] = {
            "character_id": attacker_char['character_id'],
            "name": human_name,
            "username": str(ctx.author),
            "user_id": user_id,
            "power_level": human_power,
            "skills": human_skills,
            "wins": 0,
            "losses": 0,
            "race": "human",
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "origin": f"Resisted vampire {attacker_char['name']}"
        }
        save_characters(characters)

        failure_embed = discord.Embed(
            title="💀 RITUAL FAILED - YOU ARE NOW HUMAN",
            description=f"The ritual backfired! {attacker_char['name']} has been DESTROYED!\n\n{human_name} resisted the possession!",
            color=discord.Color.blue()
        )
        failure_embed.add_field(name="Failure Roll", value=f"Rolled {roll} (Success at ≤{int(success_chance)})", inline=False)
        failure_embed.add_field(name="Vampire's Final Record",
                                value=f"{attacker_char.get('wins', 0)}-{attacker_char.get('losses', 0)}", inline=False)
        failure_embed.add_field(
            name="🗡️ YOU ARE NOW A HUMAN VAMPIRE HUNTER",
            value=(f"**Name:** {human_name}\n**ID:** `{attacker_char['character_id']}`\n"
                   f"**Race:** Human\n**Power:** {human_power}\n"
                   f"**Rank:** {get_human_rank(human_power)}\n**Skills:** {len(human_skills)} hunter abilities"),
            inline=False
        )
        await ctx.send(embed=failure_embed)


@bot.command(name='transfer')
async def blood_transfer_hybrid(ctx, character_id_1: str = None, character_id_2: str = None):
    """Initiate a blood transfer ritual between two vampires. Usage: ?transfer <your_vampire_id> <target_vampire_id>"""
    if character_id_1 is None or character_id_2 is None:
        await ctx.send("Usage: `?transfer <your_vampire_id> <target_vampire_id>`")
        return

    characters = load_characters()
    graveyard  = load_graveyard()

    if character_id_1 not in characters:
        await ctx.send(f"Character ID `{character_id_1}` not found!")
        return
    if character_id_2 not in characters:
        await ctx.send(f"Character ID `{character_id_2}` not found!")
        return

    initiator_char = characters[character_id_1]
    target_char    = characters[character_id_2]
    user_id        = str(ctx.author.id)

    if initiator_char.get('user_id') != user_id and initiator_char.get('shared_user_id') != user_id:
        await ctx.send("You don't own the first character!")
        return
    if initiator_char.get('race', 'vampire') != 'vampire' or target_char.get('race', 'vampire') != 'vampire':
        await ctx.send("Both characters must be vampires for the transfer ritual!")
        return
    if initiator_char.get('user_id') == target_char.get('user_id'):
        await ctx.send("You cannot transfer with your own vampire! Both vampires must have different owners.")
        return

    target_user_id = target_char.get('user_id')
    request_key    = f"{character_id_1}_{character_id_2}"
    reverse_key    = f"{character_id_2}_{character_id_1}"

    if reverse_key in transfer_requests:
        await ctx.send(f"Both vampire owners have agreed to the blood transfer ritual!")

        ritual_embed = discord.Embed(
            title="BLOOD TRANSFER RITUAL",
            description=f"{initiator_char['name']} and {target_char['name']} begin the ancient blood ritual...",
            color=discord.Color.dark_purple()
        )
        ritual_embed.add_field(name=initiator_char['name'],
                               value=f"Power: {initiator_char['power_level']} | Skills: {len(initiator_char['skills'])}",
                               inline=True)
        ritual_embed.add_field(name=target_char['name'],
                               value=f"Power: {target_char['power_level']} | Skills: {len(target_char['skills'])}",
                               inline=True)
        await ctx.send(embed=ritual_embed)
        await asyncio.sleep(5)

        hybrid_name  = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        hybrid_id    = generate_unique_id()
        bonus        = random.randint(50, 150)
        hybrid_power = min(initiator_char['power_level'] + target_char['power_level'] + bonus, 1000)
        all_skills   = list(set(initiator_char['skills'] + target_char['skills']))
        available    = [s for s in SKILLS if s not in all_skills]
        if available:
            all_skills.extend(random.sample(available, min(random.randint(1, 3), len(available))))
        total_wins = initiator_char.get('wins', 0) + target_char.get('wins', 0)

        for old_char in [initiator_char, target_char]:
            dead = old_char.copy()
            dead['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead['killed_by']  = "Blood Transfer Ritual"
            graveyard.append(dead)
        save_graveyard(graveyard)

        del characters[character_id_1]
        del characters[character_id_2]

        characters[hybrid_id] = {
            "character_id": hybrid_id,
            "name": hybrid_name,
            "username": f"{initiator_char.get('username', 'Unknown')} & {target_char.get('username', 'Unknown')}",
            "user_id": user_id,
            "shared_user_id": target_user_id,
            "power_level": hybrid_power,
            "skills": all_skills,
            "wins": total_wins,
            "losses": 0,
            "race": "vampire",
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "is_hybrid": True
        }
        save_characters(characters)
        del transfer_requests[reverse_key]

        result_embed = discord.Embed(
            title="HYBRID VAMPIRE BORN",
            description=f"The ritual is complete! {hybrid_name} emerges from the darkness!\n\nID: `{hybrid_id}`",
            color=discord.Color.gold()
        )
        result_embed.add_field(name="Hybrid Name", value=hybrid_name, inline=False)
        result_embed.add_field(name="Blood Power", value=f"{hybrid_power} (+{bonus} ritual bonus)", inline=False)
        result_embed.add_field(name="Rank", value=get_vampire_rank(hybrid_power), inline=False)
        result_embed.add_field(name="Total Abilities", value=f"{len(all_skills)} abilities", inline=False)
        result_embed.add_field(name="Battle Record", value=f"{total_wins}-0", inline=False)
        await ctx.send(embed=result_embed)

    else:
        transfer_requests[request_key] = {
            "initiator": user_id,
            "target": target_user_id,
            "timestamp": datetime.now()
        }
        request_embed = discord.Embed(
            title="BLOOD TRANSFER REQUEST",
            description="Blood transfer ritual initiated!",
            color=discord.Color.orange()
        )
        request_embed.add_field(name="Warning",
                                value="Both vampires will be sacrificed to create a powerful hybrid vampire!",
                                inline=False)
        request_embed.add_field(name="Vampire 1",
                                value=f"{initiator_char['name']} (ID: `{character_id_1}`) - Power: {initiator_char['power_level']}",
                                inline=True)
        request_embed.add_field(name="Vampire 2",
                                value=f"{target_char['name']} (ID: `{character_id_2}`) - Power: {target_char['power_level']}",
                                inline=True)
        request_embed.add_field(name="To Accept",
                                value=f"The owner of {target_char['name']} must use `?transfer {character_id_2} {character_id_1}` to accept!",
                                inline=False)
        await ctx.send(embed=request_embed)


@bot.command(name='fight')
async def fight_character(ctx, character_id: str = None):
    """Fight an opponent matched to your rank! Usage: ?fight <character_id>"""
    if character_id is None:
        await ctx.send("Usage: `?fight <character_id>`\nExample: `?fight 123456`\n\nUse `?list` to see your character IDs.")
        return

    # Always read fresh from disk
    characters = load_characters()
    graveyard  = load_graveyard()

    if character_id not in characters:
        await ctx.send(f"Character ID `{character_id}` not found!")
        return

    player_char = characters[character_id]
    user_id     = str(ctx.author.id)

    if player_char.get('user_id') != user_id and player_char.get('shared_user_id') != user_id:
        await ctx.send("You don't own this character!")
        return

    race = player_char.get('race', 'vampire')

    # Generate rank-appropriate AI opponent (opposite race)
    min_power, max_power = get_opponent_power_range(player_char['power_level'])

    if race == 'vampire':
        ai_name       = f"{random.choice(HUMAN_FIRST_NAMES)} {random.choice(HUMAN_LAST_NAMES)}"
        ai_race       = "human"
        ai_skill_pool = HUMAN_SKILLS
        player_color  = discord.Color.dark_red()
    else:
        ai_name       = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        ai_race       = "vampire"
        ai_skill_pool = SKILLS
        player_color  = discord.Color.blue()

    ai_power_level = random.randint(min_power, max_power)

    if ai_power_level <= 50:        ai_num_skills = random.randint(3, 5)
    elif ai_power_level <= 100:     ai_num_skills = random.randint(4, 6)
    elif ai_power_level <= 200:     ai_num_skills = random.randint(5, 7)
    elif ai_power_level <= 350:     ai_num_skills = random.randint(6, 8)
    elif ai_power_level <= 500:     ai_num_skills = random.randint(7, 10)
    elif ai_power_level <= 650:     ai_num_skills = random.randint(8, 12)
    elif ai_power_level <= 800:     ai_num_skills = random.randint(10, 14)
    else:                           ai_num_skills = random.randint(12, 15)

    ai_skills     = random.sample(list(ai_skill_pool.keys()), min(ai_num_skills, len(ai_skill_pool)))
    death_chance  = calculate_death_chance(player_char['power_level'], ai_power_level)
    player_rank   = get_vampire_rank(player_char['power_level']) if race == 'vampire' else get_human_rank(player_char['power_level'])
    ai_rank       = get_vampire_rank(ai_power_level) if ai_race == 'vampire' else get_human_rank(ai_power_level)

    battle_embed = discord.Embed(title="⚔️ BATTLE",
                                 description=f"A {race} faces off against a {ai_race}!",
                                 color=player_color)
    battle_embed.add_field(
        name=f"{'🧛' if race == 'vampire' else '🗡️'} {player_char['name']} (YOU)",
        value=f"Power: {player_char['power_level']}\nRank: {player_rank}\nAbilities: {len(player_char['skills'])}",
        inline=True
    )
    battle_embed.add_field(
        name=f"{'🧛' if ai_race == 'vampire' else '🗡️'} {ai_name} (ENEMY)",
        value=f"Power: {ai_power_level}\nRank: {ai_rank}\nAbilities: {len(ai_skills)}",
        inline=True
    )
    battle_embed.add_field(name="Death Risk",
                           value=f"{death_chance}% chance of permanent death if defeated",
                           inline=False)
    await ctx.send(embed=battle_embed)
    await asyncio.sleep(2)

    player_skill_dict = SKILLS if race == 'vampire' else HUMAN_SKILLS
    combined_skills   = {**player_skill_dict, **ai_skill_pool}

    battle_result = simulate_battle(
        player_char['name'], player_char['power_level'], player_char['skills'],
        ai_name, ai_power_level, ai_skills, combined_skills
    )

    player_wins = battle_result['winner'] == player_char['name']

    if player_wins:
        player_char['wins'] = player_char.get('wins', 0) + 1
        characters[character_id] = player_char
        save_characters(characters)

        result_embed = discord.Embed(
            title="🎉 VICTORY",
            description=f"{player_char['name']} has defeated {ai_name}!",
            color=discord.Color.green()
        )
        result_embed.add_field(name="Battle Summary",
                               value=f"{player_char['name']} emerged victorious with {battle_result['winner_hp']} HP remaining!",
                               inline=False)
        result_embed.add_field(name="New Record",
                               value=f"{player_char['wins']}-{player_char.get('losses', 0)}",
                               inline=False)
        await ctx.send(embed=result_embed)

    else:
        death_roll     = random.randint(1, 100)
        character_dies = death_roll <= death_chance

        if character_dies:
            result_embed = discord.Embed(
                title="💀 PERMANENT DEATH",
                description=f"{player_char['name']} has been destroyed by {ai_name}!",
                color=discord.Color.black()
            )
            result_embed.add_field(name="Final Record",
                                   value=f"{player_char.get('wins', 0)}-{player_char.get('losses', 0)}",
                                   inline=False)
            result_embed.add_field(name="Death Roll",
                                   value=f"Rolled {death_roll} (Death at ≤{death_chance})",
                                   inline=False)
            result_embed.add_field(name="Battle Summary",
                                   value=f"{player_char['name']} has been killed...\n\nUse `?make` to create a new vampire.",
                                   inline=False)
            await ctx.send(embed=result_embed)

            dead_character               = player_char.copy()
            dead_character['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_character['killed_by']  = ai_name
            graveyard.append(dead_character)
            save_graveyard(graveyard)

            del characters[character_id]
            save_characters(characters)

        else:
            player_char['losses'] = player_char.get('losses', 0) + 1
            characters[character_id] = player_char
            save_characters(characters)

            result_embed = discord.Embed(
                title="😰 DEFEAT - BUT ALIVE",
                description=f"{player_char['name']} was defeated by {ai_name} but survived!",
                color=discord.Color.orange()
            )
            result_embed.add_field(name="Death Roll",
                                   value=f"Rolled {death_roll} (Death at ≤{death_chance}) - **You survived!**",
                                   inline=False)
            result_embed.add_field(name="Battle Summary",
                                   value=f"{player_char['name']} was defeated but managed to escape!\n\nYou can fight again!",
                                   inline=False)
            result_embed.add_field(name="New Record",
                                   value=f"{player_char.get('wins', 0)}-{player_char['losses']}",
                                   inline=False)
            await ctx.send(embed=result_embed)


@bot.command(name='stats')
async def world_stats(ctx):
    """View world statistics of all characters alive and dead"""
    alive_characters = load_characters()
    dead_characters  = load_graveyard()

    total_alive    = len(alive_characters)
    total_dead     = len(dead_characters)
    alive_vampires = sum(1 for c in alive_characters.values() if c.get('race', 'vampire') == 'vampire')
    alive_humans   = sum(1 for c in alive_characters.values() if c.get('race', 'vampire') == 'human')
    total_wins     = sum(c.get('wins', 0) for c in alive_characters.values())
    total_losses   = sum(c.get('losses', 0) for c in alive_characters.values())

    stats_embed = discord.Embed(
        title="🌍 WORLD STATISTICS",
        description="Global character data across all realms",
        color=discord.Color.dark_purple()
    )
    stats_embed.add_field(name="Total Characters Created", value=str(total_alive + total_dead), inline=True)
    stats_embed.add_field(name="Characters Alive",         value=str(total_alive),               inline=True)
    stats_embed.add_field(name="Characters Destroyed",     value=str(total_dead),                inline=True)
    stats_embed.add_field(name="🧛 Living Vampires",       value=str(alive_vampires),             inline=True)
    stats_embed.add_field(name="🗡️ Living Hunters",        value=str(alive_humans),              inline=True)
    stats_embed.add_field(name="Total Battles",            value=str(total_wins + total_losses),  inline=True)
    await ctx.send(embed=stats_embed)

    combined_embed = discord.Embed(title="🏆 CHARACTER RANKINGS", color=discord.Color.blurple())

    if alive_characters:
        seen, unique = set(), []
        for char in alive_characters.values():
            cid = char.get('character_id')
            if cid not in seen:
                seen.add(cid)
                unique.append(char)

        alive_list  = sorted(unique, key=lambda x: x.get('wins', 0), reverse=True)[:5]
        alive_text  = "**TOP LIVING CHARACTERS**\nThe strongest fighters in the world\n\n"
        for idx, char in enumerate(alive_list, 1):
            race = char.get('race', 'vampire')
            rank = get_vampire_rank(char['power_level']) if race == 'vampire' else get_human_rank(char['power_level'])
            icon = "🧛" if race == 'vampire' else "🗡️"
            hybrid_tag = " [HYBRID]" if char.get('is_hybrid', False) else ""
            alive_text += (f"{idx}. {icon} **{char['name']}{hybrid_tag}**\n"
                           f"ID: `{char['character_id']}` | {rank} | Power: {char['power_level']} | "
                           f"Record: {char.get('wins', 0)}-{char.get('losses', 0)}\n\n")
        combined_embed.add_field(name="\u200b", value=alive_text, inline=False)

    if dead_characters:
        recent_dead = list(reversed(dead_characters[-5:]))
        dead_text   = "**RECENTLY FALLEN**\nThose who met their end\n\n"
        for char in recent_dead:
            race = char.get('race', 'vampire')
            rank = get_vampire_rank(char['power_level']) if race == 'vampire' else get_human_rank(char['power_level'])
            icon = "🧛" if race == 'vampire' else "🗡️"
            dead_text += (f"{icon} **{char['name']}**\n"
                          f"ID: `{char['character_id']}` | {rank} | Power: {char['power_level']} | "
                          f"Record: {char.get('wins', 0)}-{char.get('losses', 0)}\n"
                          f"Killed by: {char.get('killed_by', 'Unknown')}\n\n")
        combined_embed.add_field(name="\u200b", value=dead_text, inline=False)

    await ctx.send(embed=combined_embed)


# ---------- run ----------

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
