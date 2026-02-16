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

# Transfer requests storage (temporary, in-memory)
transfer_requests = {}

# Battle simulation function
def simulate_battle(attacker_name, attacker_power, attacker_skills, defender_name, defender_power, defender_skills):
    """Simulate a detailed battle between two vampires"""
    
    battle_log = []
    
    # Calculate offensive and defensive ratings
    attacker_offense = sum(SKILLS[skill]["offensive"] for skill in attacker_skills) / len(attacker_skills)
    attacker_defense = sum(SKILLS[skill]["defensive"] for skill in attacker_skills) / len(attacker_skills)
    
    defender_offense = sum(SKILLS[skill]["offensive"] for skill in defender_skills) / len(defender_skills)
    defender_defense = sum(SKILLS[skill]["defensive"] for skill in defender_skills) / len(defender_skills)
    
    # Simulate 3 rounds of combat
    attacker_hp = 100 + (attacker_power * 0.5)
    defender_hp = 100 + (defender_power * 0.5)
    
    round_num = 1
    while round_num <= 3 and attacker_hp > 0 and defender_hp > 0:
        # Attacker's turn
        atk_skill = random.choice(attacker_skills)
        atk_skill_power = SKILLS[atk_skill]["offensive"]
        
        # Calculate damage
        base_damage = (attacker_power * 0.3) + (atk_skill_power * 2) + random.randint(5, 15)
        damage_reduction = defender_defense * 0.8
        final_damage = max(5, base_damage - damage_reduction)
        
        defender_hp -= final_damage
        
        battle_log.append({
            "round": round_num,
            "attacker": attacker_name,
            "action": f"uses {atk_skill}",
            "damage": int(final_damage),
            "target": defender_name,
            "target_hp": max(0, int(defender_hp))
        })
        
        if defender_hp <= 0:
            break
        
        # Defender's counter
        def_skill = random.choice(defender_skills)
        def_skill_power = SKILLS[def_skill]["offensive"]
        
        # Calculate counter damage
        base_damage = (defender_power * 0.3) + (def_skill_power * 2) + random.randint(5, 15)
        damage_reduction = attacker_defense * 0.8
        final_damage = max(5, base_damage - damage_reduction)
        
        attacker_hp -= final_damage
        
        battle_log.append({
            "round": round_num,
            "attacker": defender_name,
            "action": f"counters with {def_skill}",
            "damage": int(final_damage),
            "target": attacker_name,
            "target_hp": max(0, int(attacker_hp))
        })
        
        round_num += 1
    
    # Determine winner
    if attacker_hp > defender_hp:
        winner = attacker_name
        winner_hp = int(attacker_hp)
    else:
        winner = defender_name
        winner_hp = int(defender_hp)
    
    return {
        "winner": winner,
        "winner_hp": winner_hp,
        "battle_log": battle_log
    }

# Function to get vampire rank based on power level
def get_vampire_rank(power_level):
    if power_level <= 50:
        return "Fledgling"
    elif power_level <= 100:
        return "Stalker"
    elif power_level <= 200:
        return "Nightlord"
    elif power_level <= 350:
        return "Elder"
    elif power_level <= 500:
        return "Ancient"
    elif power_level <= 650:
        return "Progenitor"
    elif power_level <= 800:
        return "Blood God"
    else:  # 801-1000
        return "Primordial"

# Function to get opponent power range based on player rank
def get_opponent_power_range(player_power):
    """Generate opponent power range based on player's power level"""
    if player_power <= 50:  # Fledgling
        min_power = 10
        max_power = 70
    elif player_power <= 100:  # Stalker
        min_power = 50
        max_power = 130
    elif player_power <= 200:  # Nightlord
        min_power = 100
        max_power = 250
    elif player_power <= 350:  # Elder
        min_power = 200
        max_power = 400
    elif player_power <= 500:  # Ancient
        min_power = 350
        max_power = 550
    elif player_power <= 650:  # Progenitor
        min_power = 500
        max_power = 700
    elif player_power <= 800:  # Blood God
        min_power = 650
        max_power = 850
    else:  # Primordial (801-1000)
        min_power = 750
        max_power = 1000
    
    return min_power, max_power

# Function to calculate death chance based on power difference
def calculate_death_chance(player_power, enemy_power):
    """Calculate chance of death based on power difference"""
    power_diff = enemy_power - player_power
    
    # Base death chance is 30%
    base_chance = 30
    
    # Adjust based on power difference
    # Every 50 power difference changes death chance by 5%
    adjustment = (power_diff / 50) * 5
    
    death_chance = base_chance + adjustment
    
    # Cap between 10% and 70%
    death_chance = max(10, min(70, death_chance))
    
    return int(death_chance)

# Load characters
def load_characters():
    if os.path.exists(CHARACTERS_FILE):
        with open(CHARACTERS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save characters
def save_characters(characters):
    with open(CHARACTERS_FILE, 'w') as f:
        json.dump(characters, f, indent=4)

# Load graveyard
def load_graveyard():
    if os.path.exists(GRAVEYARD_FILE):
        with open(GRAVEYARD_FILE, 'r') as f:
            return json.load(f)
    return []

# Save graveyard
def save_graveyard(graveyard):
    with open(GRAVEYARD_FILE, 'w') as f:
        json.dump(graveyard, f, indent=4)

# Generate unique 6-digit ID
def generate_unique_id():
    characters = load_characters()
    graveyard = load_graveyard()
    existing_ids = [char.get('character_id') for char in characters.values() if 'character_id' in char]
    existing_ids += [char.get('character_id') for char in graveyard if 'character_id' in char]
    
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing_ids:
            return new_id

characters = load_characters()
graveyard = load_graveyard()

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Vampire Generator Ready')

# Check to block DM commands
@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True

# Make command - Creates a vampire (INFINITE VAMPIRES)
@bot.command(name='make')
async def make_character(ctx):
    """Generate a unique vampire with random abilities and power level"""
    
    user_id = str(ctx.author.id)
    
    # Generate random vampire name
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    character_name = f"{first_name} {last_name}"
    
    # Generate unique character ID
    character_id = generate_unique_id()
    
    # Generate random power level (10 to 100)
    power_level = random.randint(10, 100)
    
    # Generate 3-5 random unique vampiric abilities
    num_skills = random.randint(3, 5)
    selected_skills = random.sample(list(SKILLS.keys()), num_skills)
    
    # Create vampire data with unique ID as key
    character_data = {
        "character_id": character_id,
        "name": character_name,
        "username": str(ctx.author),
        "user_id": user_id,
        "power_level": power_level,
        "skills": selected_skills,
        "wins": 0,
        "losses": 0,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save vampire with character_id as key (allows infinite vampires per user)
    characters[character_id] = character_data
    save_characters(characters)
    
    # Display new vampire
    embed = discord.Embed(
        title=character_name,
        description=f"Owner: {ctx.author.name}\nID: `{character_id}`\nRace: Vampire",
        color=discord.Color.dark_red()
    )
    
    embed.add_field(name="Blood Power", value=f"{power_level}", inline=False)
    
    # Add rank
    rank = get_vampire_rank(power_level)
    embed.add_field(name="Rank", value=f"{rank}", inline=False)
    
    skills_text = "\n".join([f"- {skill}" for skill in selected_skills])
    embed.add_field(name="Vampiric Abilities", value=skills_text, inline=False)
    
    # Show initial record
    embed.add_field(name="Battle Record", value="0-0", inline=False)
    
    embed.set_footer(text="Use this ID for commands: ?show, ?train, ?fight")
    
    await ctx.send(embed=embed)

# Show command - Shows a vampire by ID
@bot.command(name='show')
async def show_character(ctx, character_id: str = None):
    """Show a vampire by ID. Usage: ?show <character_id>"""
    
    if character_id is None:
        await ctx.send("Usage: `?show <character_id>`\nExample: `?show 123456`")
        return
    
    # Check if vampire exists
    if character_id not in characters:
        await ctx.send(f"Vampire ID `{character_id}` not found!")
        return
    
    char = characters[character_id]
    
    # Display vampire
    embed = discord.Embed(
        title=char['name'],
        description=f"Owner: {char.get('username', 'Unknown')}\nID: `{char['character_id']}`\nRace: Vampire",
        color=discord.Color.dark_red()
    )
    
    embed.add_field(name="Blood Power", value=f"{char['power_level']}", inline=False)
    
    # Add rank
    rank = get_vampire_rank(char['power_level'])
    embed.add_field(name="Rank", value=f"{rank}", inline=False)
    
    skills_text = "\n".join([f"- {skill}" for skill in char['skills']])
    embed.add_field(name="Vampiric Abilities", value=skills_text, inline=False)
    
    # Show record
    wins = char.get('wins', 0)
    losses = char.get('losses', 0)
    embed.add_field(name="Battle Record", value=f"{wins}-{losses}", inline=False)
    
    await ctx.send(embed=embed)

# My Collection command - Shows all user's vampires in one comprehensive list
@bot.command(name='mycollection')
async def my_collection(ctx):
    """View your complete vampire collection with detailed stats"""
    
    user_id = str(ctx.author.id)
    
    # Find all vampires owned by user (including shared hybrids)
    user_vampires = [char for char in characters.values() if char.get('user_id') == user_id or char.get('shared_user_id') == user_id]
    
    if not user_vampires:
        await ctx.send("You don't have any vampires yet! Use `?make` to create one.")
        return
    
    # Sort by power level (highest first)
    user_vampires.sort(key=lambda x: x['power_level'], reverse=True)
    
    # Calculate collection statistics
    total_vampires = len(user_vampires)
    total_power = sum(v['power_level'] for v in user_vampires)
    avg_power = total_power // total_vampires
    total_wins = sum(v.get('wins', 0) for v in user_vampires)
    total_losses = sum(v.get('losses', 0) for v in user_vampires)
    
    # Count by rank
    rank_counts = {}
    for vamp in user_vampires:
        rank = get_vampire_rank(vamp['power_level'])
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    
    # Main collection embed
    main_embed = discord.Embed(
        title=f"🧛 {ctx.author.name}'s Vampire Collection",
        description=f"**Total Vampires:** {total_vampires}\n**Total Power:** {total_power}\n**Average Power:** {avg_power}\n**Overall Record:** {total_wins}-{total_losses}",
        color=discord.Color.dark_purple()
    )
    
    # Add rank distribution
    rank_text = ""
    for rank in ["Primordial", "Blood God", "Progenitor", "Ancient", "Elder", "Nightlord", "Stalker", "Fledgling"]:
        count = rank_counts.get(rank, 0)
        if count > 0:
            rank_text += f"{rank}: {count}\n"
    
    if rank_text:
        main_embed.add_field(name="Rank Distribution", value=rank_text, inline=False)
    
    await ctx.send(embed=main_embed)
    
    # Send vampire list in batches (10 per embed)
    for i in range(0, len(user_vampires), 10):
        batch = user_vampires[i:i+10]
        
        list_embed = discord.Embed(
            title=f"Vampire Collection (Page {i//10 + 1})",
            color=discord.Color.dark_red()
        )
        
        for vamp in batch:
            rank = get_vampire_rank(vamp['power_level'])
            wins = vamp.get('wins', 0)
            losses = vamp.get('losses', 0)
            
            # Check if hybrid
            hybrid_tag = " [HYBRID]" if vamp.get('is_hybrid', False) else ""
            
            # Build value text
            value_text = (
                f"**ID:** `{vamp['character_id']}`\n"
                f"**Rank:** {rank}\n"
                f"**Power:** {vamp['power_level']}\n"
                f"**Abilities:** {len(vamp['skills'])}\n"
                f"**Record:** {wins}-{losses}"
            )
            
            list_embed.add_field(
                name=f"{vamp['name']}{hybrid_tag}",
                value=value_text,
                inline=True
            )
        
        # Add footer with total pages
        total_pages = (len(user_vampires) + 9) // 10
        list_embed.set_footer(text=f"Page {i//10 + 1} of {total_pages} | Use ?show <id> for detailed view")
        
        await ctx.send(embed=list_embed)

# List command - Lists all vampires owned by user (kept for backwards compatibility)
@bot.command(name='list')
async def list_vampires(ctx):
    """List all your vampires (compact view)"""
    
    user_id = str(ctx.author.id)
    
    # Find all vampires owned by user
    user_vampires = [char for char in characters.values() if char.get('user_id') == user_id or char.get('shared_user_id') == user_id]
    
    if not user_vampires:
        await ctx.send("You don't have any vampires yet! Use `?make` to create one.")
        return
    
    # Sort by power level
    user_vampires.sort(key=lambda x: x['power_level'], reverse=True)
    
    embed = discord.Embed(
        title=f"{ctx.author.name}'s Vampires",
        description=f"Total: {len(user_vampires)} vampires | Use `?mycollection` for detailed view",
        color=discord.Color.dark_purple()
    )
    
    # Show first 10 vampires
    for vamp in user_vampires[:10]:
        rank = get_vampire_rank(vamp['power_level'])
        wins = vamp.get('wins', 0)
        losses = vamp.get('losses', 0)
        hybrid_tag = " [HYBRID]" if vamp.get('is_hybrid', False) else ""
        
        embed.add_field(
            name=f"{vamp['name']}{hybrid_tag}",
            value=f"ID: `{vamp['character_id']}` | {rank} | Power: {vamp['power_level']} | {wins}-{losses}",
            inline=False
        )
    
    if len(user_vampires) > 10:
        embed.set_footer(text=f"Showing 10 of {len(user_vampires)} vampires")
    
    await ctx.send(embed=embed)

# Rank command - Show vampire rank tiers
@bot.command(name='rank')
async def vampire_ranks(ctx):
    """Display vampire rank tiers and power requirements"""
    
    rank_embed = discord.Embed(
        title="VAMPIRE RANK TIERS",
        description="As vampires grow in power, they ascend through ancient ranks",
        color=discord.Color.dark_gold()
    )
    
    rank_embed.add_field(
        name="Fledgling",
        value="Power: 0-50\nNewly turned vampires, still learning their abilities",
        inline=False
    )
    
    rank_embed.add_field(
        name="Stalker",
        value="Power: 51-100\nExperienced hunters of the night",
        inline=False
    )
    
    rank_embed.add_field(
        name="Nightlord",
        value="Power: 101-200\nMasters of darkness and blood",
        inline=False
    )
    
    rank_embed.add_field(
        name="Elder",
        value="Power: 201-350\nCenturies-old vampires of immense power",
        inline=False
    )
    
    rank_embed.add_field(
        name="Ancient",
        value="Power: 351-500\nMillennia-old beings of legendary strength",
        inline=False
    )
    
    rank_embed.add_field(
        name="Progenitor",
        value="Power: 501-650\nThe first of their bloodline, wielding primeval might",
        inline=False
    )
    
    rank_embed.add_field(
        name="Blood God",
        value="Power: 651-800\nDeified vampires worshipped across realms",
        inline=False
    )
    
    rank_embed.add_field(
        name="Primordial",
        value="Power: 801-1000\nThe original vampires, older than recorded history",
        inline=False
    )
    
    await ctx.send(embed=rank_embed)

# Train command - Train your vampire to become more powerful
@bot.command(name='train')
async def train_vampire(ctx, character_id: str = None):
    """Train your vampire to increase their power! Usage: ?train <character_id>"""
    
    # Check if character ID was provided
    if character_id is None:
        await ctx.send("Usage: `?train <character_id>`\nExample: `?train 123456`\n\nUse `?list` to see your vampire IDs.")
        return
    
    # Check if vampire exists
    if character_id not in characters:
        await ctx.send(f"Vampire ID `{character_id}` not found!")
        return
    
    player_char = characters[character_id]
    user_id = str(ctx.author.id)
    
    # Verify ownership
    if player_char.get('user_id') != user_id and player_char.get('shared_user_id') != user_id:
        await ctx.send("You don't own this vampire!")
        return
    
    # Training embed
    training_embed = discord.Embed(
        title="TRAINING SESSION",
        description=f"{player_char['name']} begins intense training in the shadows...",
        color=discord.Color.blue()
    )
    
    await ctx.send(embed=training_embed)
    
    # 3 second delay for training
    await asyncio.sleep(3)
    
    # Random power increase (5 to 25)
    power_gain = random.randint(5, 25)
    old_power = player_char['power_level']
    new_power = old_power + power_gain
    
    # Cap at 1000
    if new_power > 1000:
        new_power = 1000
        power_gain = 1000 - old_power
    
    old_rank = get_vampire_rank(old_power)
    new_rank = get_vampire_rank(new_power)
    ranked_up = old_rank != new_rank
    
    player_char['power_level'] = new_power
    
    # Random chance to learn a new skill (20% chance)
    learned_new_skill = False
    new_skill = None
    
    if random.randint(1, 100) <= 20 and len(player_char['skills']) < 15:
        # Get skills the vampire doesn't have yet
        available_skills = [skill for skill in SKILLS.keys() if skill not in player_char['skills']]
        if available_skills:
            new_skill = random.choice(available_skills)
            player_char['skills'].append(new_skill)
            learned_new_skill = True
    
    # If hybrid, update shared vampire
    if player_char.get('is_hybrid', False):
        shared_user_id = player_char.get('shared_user_id')
        if shared_user_id:
            # Find the shared vampire by character_id
            for char_id, char in characters.items():
                if char.get('character_id') == player_char['character_id'] and char_id != character_id:
                    characters[char_id]['power_level'] = new_power
                    characters[char_id]['skills'] = player_char['skills']
    
    # Save updated vampire
    characters[character_id] = player_char
    save_characters(characters)
    
    # Results embed
    result_embed = discord.Embed(
        title="TRAINING COMPLETE",
        description=f"{player_char['name']} has grown stronger!",
        color=discord.Color.gold()
    )
    
    result_embed.add_field(
        name="Power Increase",
        value=f"{old_power} → {new_power} (+{power_gain})",
        inline=False
    )
    
    if ranked_up:
        result_embed.add_field(
            name="RANK UP!",
            value=f"{old_rank} → **{new_rank}**",
            inline=False
        )
    
    if learned_new_skill:
        result_embed.add_field(
            name="New Ability Learned!",
            value=f"{new_skill}",
            inline=False
        )
    
    result_embed.add_field(
        name="Total Abilities",
        value=f"{len(player_char['skills'])} abilities",
        inline=False
    )
    
    await ctx.send(embed=result_embed)

# Transfer command - Blood transfer ritual between two vampires
@bot.command(name='transfer')
async def blood_transfer(ctx, character_id_1: str = None, character_id_2: str = None):
    """Initiate a blood transfer ritual between two vampires. Usage: ?transfer <your_vampire_id> <target_vampire_id>"""
    
    if character_id_1 is None or character_id_2 is None:
        await ctx.send("Usage: `?transfer <your_vampire_id> <target_vampire_id>`\nExample: `?transfer 123456 789012`\n\nBoth vampires will be sacrificed to create a powerful hybrid!")
        return
    
    # Check if both vampires exist
    if character_id_1 not in characters:
        await ctx.send(f"Vampire ID `{character_id_1}` not found!")
        return
    
    if character_id_2 not in characters:
        await ctx.send(f"Vampire ID `{character_id_2}` not found!")
        return
    
    initiator_char = characters[character_id_1]
    target_char = characters[character_id_2]
    
    user_id = str(ctx.author.id)
    
    # Verify ownership of first vampire
    if initiator_char.get('user_id') != user_id and initiator_char.get('shared_user_id') != user_id:
        await ctx.send("You don't own the first vampire!")
        return
    
    # Both vampires must have different owners
    if initiator_char.get('user_id') == target_char.get('user_id'):
        await ctx.send("You cannot transfer with your own vampire! Both vampires must have different owners.")
        return
    
    target_user_id = target_char.get('user_id')
    
    # Create transfer request
    request_key = f"{character_id_1}_{character_id_2}"
    reverse_key = f"{character_id_2}_{character_id_1}"
    
    if reverse_key in transfer_requests:
        # Both agreed! Perform the transfer
        await ctx.send(f"Both vampire owners have agreed to the blood transfer ritual!")
        
        # Ritual embed
        ritual_embed = discord.Embed(
            title="BLOOD TRANSFER RITUAL",
            description=f"{initiator_char['name']} and {target_char['name']} begin the ancient blood ritual...\n\nTheir essences merge in darkness...",
            color=discord.Color.dark_purple()
        )
        
        ritual_embed.add_field(
            name=f"{initiator_char['name']}",
            value=f"Power: {initiator_char['power_level']} | Skills: {len(initiator_char['skills'])}",
            inline=True
        )
        
        ritual_embed.add_field(
            name=f"{target_char['name']}",
            value=f"Power: {target_char['power_level']} | Skills: {len(target_char['skills'])}",
            inline=True
        )
        
        await ctx.send(embed=ritual_embed)
        
        # 5 second ritual delay
        await asyncio.sleep(5)
        
        # Create new hybrid vampire
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        hybrid_name = f"{first_name} {last_name}"
        
        # Generate new ID for hybrid
        hybrid_id = generate_unique_id()
        
        # Combine powers
        combined_power = initiator_char['power_level'] + target_char['power_level']
        bonus = random.randint(50, 150)
        hybrid_power = min(combined_power + bonus, 1000)
        
        # Combine skills
        all_skills = list(set(initiator_char['skills'] + target_char['skills']))
        
        # Add 1-3 random new skills
        available_skills = [skill for skill in SKILLS.keys() if skill not in all_skills]
        if available_skills:
            num_new_skills = min(random.randint(1, 3), len(available_skills))
            new_skills = random.sample(available_skills, num_new_skills)
            all_skills.extend(new_skills)
        
        # Combine wins
        total_wins = initiator_char.get('wins', 0) + target_char.get('wins', 0)
        
        # Create hybrid vampire
        hybrid_data = {
            "character_id": hybrid_id,
            "name": hybrid_name,
            "username": f"{initiator_char.get('username', 'Unknown')} & {target_char.get('username', 'Unknown')}",
            "user_id": user_id,
            "shared_user_id": target_user_id,
            "power_level": hybrid_power,
            "skills": all_skills,
            "wins": total_wins,
            "losses": 0,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "is_hybrid": True
        }
        
        # Add old vampires to graveyard
        old_vamp1 = initiator_char.copy()
        old_vamp1['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        old_vamp1['killed_by'] = "Blood Transfer Ritual"
        
        old_vamp2 = target_char.copy()
        old_vamp2['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        old_vamp2['killed_by'] = "Blood Transfer Ritual"
        
        graveyard.append(old_vamp1)
        graveyard.append(old_vamp2)
        save_graveyard(graveyard)
        
        # Delete old vampires
        del characters[character_id_1]
        del characters[character_id_2]
        
        # Save hybrid vampire
        characters[hybrid_id] = hybrid_data
        save_characters(characters)
        
        # Clear the request
        del transfer_requests[reverse_key]
        
        # Get hybrid rank
        hybrid_rank = get_vampire_rank(hybrid_power)
        
        # Result embed
        result_embed = discord.Embed(
            title="HYBRID VAMPIRE BORN",
            description=f"The ritual is complete! {hybrid_name} emerges from the darkness!\n\nID: `{hybrid_id}`",
            color=discord.Color.gold()
        )
        
        result_embed.add_field(name="Hybrid Name", value=hybrid_name, inline=False)
        result_embed.add_field(name="Blood Power", value=f"{hybrid_power} (+{bonus} ritual bonus)", inline=False)
        result_embed.add_field(name="Rank", value=f"{hybrid_rank}", inline=False)
        result_embed.add_field(name="Total Abilities", value=f"{len(all_skills)} abilities", inline=False)
        result_embed.add_field(name="Battle Record", value=f"{total_wins}-0", inline=False)
        
        await ctx.send(embed=result_embed)
        
    else:
        # Create new request
        transfer_requests[request_key] = {
            "initiator": user_id,
            "target": target_user_id,
            "timestamp": datetime.now()
        }
        
        # Request embed
        request_embed = discord.Embed(
            title="BLOOD TRANSFER REQUEST",
            description=f"Blood transfer ritual initiated!",
            color=discord.Color.orange()
        )
        
        request_embed.add_field(
            name="Warning",
            value="Both vampires will be sacrificed to create a powerful hybrid vampire!",
            inline=False
        )
        
        request_embed.add_field(
            name=f"Vampire 1",
            value=f"{initiator_char['name']} (ID: `{character_id_1}`) - Power: {initiator_char['power_level']}",
            inline=True
        )
        
        request_embed.add_field(
            name=f"Vampire 2",
            value=f"{target_char['name']} (ID: `{character_id_2}`) - Power: {target_char['power_level']}",
            inline=True
        )
        
        request_embed.add_field(
            name="To Accept",
            value=f"The owner of {target_char['name']} must use `?transfer {character_id_2} {character_id_1}` to accept!",
            inline=False
        )
        
        await ctx.send(embed=request_embed)

# Fight command - Fight rank-appropriate vampire opponents with death chance
@bot.command(name='fight')
async def fight_character(ctx, character_id: str = None):
    """Fight a vampire opponent matched to your rank! Usage: ?fight <character_id>"""
    
    # Check if character ID was provided
    if character_id is None:
        await ctx.send("Usage: `?fight <character_id>`\nExample: `?fight 123456`\n\nUse `?list` to see your vampire IDs.")
        return
    
    # Check if vampire exists
    if character_id not in characters:
        await ctx.send(f"Vampire ID `{character_id}` not found!")
        return
    
    player_char = characters[character_id]
    user_id = str(ctx.author.id)
    
    # Verify ownership
    if player_char.get('user_id') != user_id and player_char.get('shared_user_id') != user_id:
        await ctx.send("You don't own this vampire!")
        return
    
    # Generate rank-appropriate AI vampire opponent
    min_power, max_power = get_opponent_power_range(player_char['power_level'])
    
    ai_first_name = random.choice(FIRST_NAMES)
    ai_last_name = random.choice(LAST_NAMES)
    ai_name = f"{ai_first_name} {ai_last_name}"
    ai_power_level = random.randint(min_power, max_power)
    
    # Higher rank opponents get more skills
    if ai_power_level <= 50:
        ai_num_skills = random.randint(3, 5)
    elif ai_power_level <= 100:
        ai_num_skills = random.randint(4, 6)
    elif ai_power_level <= 200:
        ai_num_skills = random.randint(5, 7)
    elif ai_power_level <= 350:
        ai_num_skills = random.randint(6, 8)
    elif ai_power_level <= 500:
        ai_num_skills = random.randint(7, 10)
    elif ai_power_level <= 650:
        ai_num_skills = random.randint(8, 12)
    elif ai_power_level <= 800:
        ai_num_skills = random.randint(10, 14)
    else:  # 801-1000
        ai_num_skills = random.randint(12, 15)
    
    ai_skills = random.sample(list(SKILLS.keys()), min(ai_num_skills, len(SKILLS)))
    
    # Calculate death chance
    death_chance = calculate_death_chance(player_char['power_level'], ai_power_level)
    
    # Battle intro embed
    battle_embed = discord.Embed(
        title="BLOOD BATTLE",
        description="Two vampires clash in the darkness!",
        color=discord.Color.purple()
    )
    
    battle_embed.add_field(
        name=f"{player_char['name']} (YOU)",
        value=f"Blood Power: {player_char['power_level']}\nRank: {get_vampire_rank(player_char['power_level'])}\nAbilities: {len(player_char['skills'])}",
        inline=True
    )
    
    battle_embed.add_field(
        name=f"{ai_name} (ENEMY)",
        value=f"Blood Power: {ai_power_level}\nRank: {get_vampire_rank(ai_power_level)}\nAbilities: {len(ai_skills)}",
        inline=True
    )
    
    battle_embed.add_field(
        name="Death Risk",
        value=f"{death_chance}% chance of permanent death if defeated",
        inline=False
    )
    
    await ctx.send(embed=battle_embed)
    
    # Simulate the battle
    await asyncio.sleep(2)
    
    battle_result = simulate_battle(
        player_char['name'], player_char['power_level'], player_char['skills'],
        ai_name, ai_power_level, ai_skills
    )
    
    # Group battle log by round to avoid duplication
    current_round = None
    round_actions = []
    
    for log_entry in battle_result['battle_log']:
        if log_entry['round'] != current_round:
            # Send previous round if exists
            if round_actions:
                round_text = ""
                for action in round_actions:
                    round_text += f"**{action['attacker']}** {action['action']}!\nDamage: {action['damage']} HP | {action['target']} HP: {action['target_hp']}\n\n"
                
                round_embed = discord.Embed(
                    title=f"Round {current_round}",
                    description=round_text,
                    color=discord.Color.orange()
                )
                
                await ctx.send(embed=round_embed)
                await asyncio.sleep(2)
            
            # Start new round
            current_round = log_entry['round']
            round_actions = []
        
        round_actions.append(log_entry)
    
    # Send last round
    if round_actions:
        round_text = ""
        for action in round_actions:
            round_text += f"**{action['attacker']}** {action['action']}!\nDamage: {action['damage']} HP | {action['target']} HP: {action['target_hp']}\n\n"
        
        round_embed = discord.Embed(
            title=f"Round {current_round}",
            description=round_text,
            color=discord.Color.orange()
        )
        
        await ctx.send(embed=round_embed)
        await asyncio.sleep(2)
    
    # Determine if player won
    player_wins = battle_result['winner'] == player_char['name']
    
    # Result embed
    if player_wins:
        # Update wins
        if 'wins' not in player_char:
            player_char['wins'] = 0
        player_char['wins'] += 1
        
        # If hybrid, update shared vampire
        if player_char.get('is_hybrid', False):
            for char_id, char in characters.items():
                if char.get('character_id') == player_char['character_id'] and char_id != character_id:
                    characters[char_id]['wins'] = player_char['wins']
        
        characters[character_id] = player_char
        save_characters(characters)
        
        result_embed = discord.Embed(
            title="VICTORY",
            description=f"{player_char['name']} has drained {ai_name} of their blood!",
            color=discord.Color.green()
        )
        
        result_embed.add_field(
            name="Battle Summary",
            value=f"{player_char['name']} emerged victorious with {battle_result['winner_hp']} HP remaining!",
            inline=False
        )
        
        # Show updated record
        wins = player_char.get('wins', 0)
        losses = player_char.get('losses', 0)
        result_embed.add_field(name="New Record", value=f"{wins}-{losses}", inline=False)
        
        await ctx.send(embed=result_embed)
    else:
        # Player lost - Roll for death
        death_roll = random.randint(1, 100)
        vampire_dies = death_roll <= death_chance
        
        if vampire_dies:
            # Vampire dies permanently
            result_embed = discord.Embed(
                title="PERMANENT DEATH",
                description=f"{player_char['name']} has been destroyed by {ai_name}!",
                color=discord.Color.dark_red()
            )
            
            # Show final record before deletion
            wins = player_char.get('wins', 0)
            losses = player_char.get('losses', 0)
            result_embed.add_field(name="Final Record", value=f"{wins}-{losses}", inline=False)
            
            result_embed.add_field(
                name="Death Roll",
                value=f"Rolled {death_roll} (Death at ≤{death_chance})",
                inline=False
            )
            
            result_embed.add_field(
                name="Battle Summary",
                value=f"{player_char['name']} has been staked through the heart and turned to ash...\n\nYour vampire has been destroyed. Use `?make` to create a new one.",
                inline=False
            )
            
            await ctx.send(embed=result_embed)
            
            # Add to graveyard before deleting
            dead_vampire = player_char.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = ai_name
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            
            # If hybrid, delete shared vampire
            if player_char.get('is_hybrid', False):
                for char_id in list(characters.keys()):
                    if characters[char_id].get('character_id') == player_char['character_id'] and char_id != character_id:
                        del characters[char_id]
            
            # Delete the vampire
            del characters[character_id]
            save_characters(characters)
            
        else:
            # Vampire survives!
            result_embed = discord.Embed(
                title="DEFEAT - BUT ALIVE",
                description=f"{player_char['name']} was defeated by {ai_name} but survived!",
                color=discord.Color.orange()
            )
            
            result_embed.add_field(
                name="Death Roll",
                value=f"Rolled {death_roll} (Death at ≤{death_chance}) - **You survived!**",
                inline=False
            )
            
            result_embed.add_field(
                name="Battle Summary",
                value=f"{player_char['name']} was defeated but managed to escape with their unlife intact!\n\nYou can fight again!",
                inline=False
            )
            
            # Update losses
            if 'losses' not in player_char:
                player_char['losses'] = 0
            player_char['losses'] += 1
            
            # If hybrid, update shared vampire
            if player_char.get('is_hybrid', False):
                for char_id, char in characters.items():
                    if char.get('character_id') == player_char['character_id'] and char_id != character_id:
                        characters[char_id]['losses'] = player_char['losses']
            
            characters[character_id] = player_char
            save_characters(characters)
            
            # Show updated record
            wins = player_char.get('wins', 0)
            losses = player_char.get('losses', 0)
            result_embed.add_field(name="New Record", value=f"{wins}-{losses}", inline=False)
            
            await ctx.send(embed=result_embed)

# Stats command - Shows world statistics
@bot.command(name='stats')
async def world_stats(ctx):
    """View world statistics of all vampires alive and dead"""
    
    # Load current data
    alive_vampires = load_characters()
    dead_vampires = load_graveyard()
    
    # Calculate stats
    total_alive = len(alive_vampires)
    total_dead = len(dead_vampires)
    total_vampires = total_alive + total_dead
    
    # Calculate total wins and losses
    total_wins = sum(char.get('wins', 0) for char in alive_vampires.values())
    total_losses = sum(char.get('losses', 0) for char in alive_vampires.values())
    
    # Main stats embed
    stats_embed = discord.Embed(
        title="VAMPIRE WORLD STATISTICS",
        description="Global vampire data across all realms",
        color=discord.Color.dark_purple()
    )
    
    stats_embed.add_field(name="Total Vampires Created", value=f"{total_vampires}", inline=True)
    stats_embed.add_field(name="Vampires Alive", value=f"{total_alive}", inline=True)
    stats_embed.add_field(name="Vampires Destroyed", value=f"{total_dead}", inline=True)
    stats_embed.add_field(name="Total Victories", value=f"{total_wins}", inline=True)
    stats_embed.add_field(name="Total Defeats", value=f"{total_losses}", inline=True)
    stats_embed.add_field(name="Total Battles", value=f"{total_wins + total_losses}", inline=True)
    
    await ctx.send(embed=stats_embed)
    
    # Combined embed with top living and recently fallen
    combined_embed = discord.Embed(
        title="VAMPIRE RANKINGS",
        color=discord.Color.blurple()
    )
    
    # Top 5 alive vampires (deduplicated)
    if alive_vampires:
        seen_ids = set()
        unique_vampires = []
        
        for vamp in alive_vampires.values():
            char_id = vamp.get('character_id')
            if char_id not in seen_ids:
                seen_ids.add(char_id)
                unique_vampires.append(vamp)
        
        alive_list = sorted(unique_vampires, key=lambda x: x.get('wins', 0), reverse=True)[:5]
        
        alive_text = "**TOP LIVING VAMPIRES**\nThe strongest vampires still walking the earth\n\n"
        for idx, vamp in enumerate(alive_list, 1):
            wins = vamp.get('wins', 0)
            losses = vamp.get('losses', 0)
            rank = get_vampire_rank(vamp['power_level'])
            hybrid_tag = " [HYBRID]" if vamp.get('is_hybrid', False) else ""
            alive_text += f"{idx}. **{vamp['name']}{hybrid_tag}**\nID: `{vamp['character_id']}` | {rank} | Power: {vamp['power_level']} | Record: {wins}-{losses}\n\n"
        
        combined_embed.add_field(name="\u200b", value=alive_text, inline=False)
    
    # Last 5 fallen vampires
    if dead_vampires:
        recent_dead = dead_vampires[-5:]
        recent_dead.reverse()
        
        dead_text = "**RECENTLY FALLEN VAMPIRES**\nThose who met their end in battle\n\n"
        for vamp in recent_dead:
            wins = vamp.get('wins', 0)
            losses = vamp.get('losses', 0)
            rank = get_vampire_rank(vamp['power_level'])
            dead_text += f"**{vamp['name']}**\nID: `{vamp['character_id']}` | {rank} | Power: {vamp['power_level']} | Record: {wins}-{losses}\nKilled by: {vamp.get('killed_by', 'Unknown')}\n\n"
        
        combined_embed.add_field(name="\u200b", value=dead_text, inline=False)
    
    await ctx.send(embed=combined_embed)

# Run the bot
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
