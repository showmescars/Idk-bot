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

# Vampire name pools
FIRST_NAMES = [
    "Dracula", "Vladislav", "Carmilla", "Lestat", "Akasha", "Armand", "Blade", "Selene",
    "Viktor", "Marcus", "Lucian", "Sonja", "Aro", "Caius", "Demetri", "Jane",
    "Alec", "Elijah", "Klaus", "Rebekah", "Kol", "Finn", "Alaric", "Damon",
    "Stefan", "Katherine", "Silas", "Qetsiyah", "Amara", "Niklaus", "Mikael", "Esther",
    "Freya", "Dahlia", "Lucien", "Tristan", "Aurora", "Rayna", "Julian", "Lily",
    "Valerie", "Nora", "Mary", "Beau", "Oscar", "Malcolm", "Sage", "Maddox",
    "Atticus", "Greta", "Antoinette", "Cassandra", "Ezra", "Morgana", "Dorian"
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

# Generate completely random AI power (10-1000, super unpredictable)
def generate_ai_power():
    """Generate completely random AI power from 10 to 1000"""
    
    # 60% chance: Low to mid tier (10-400)
    # 25% chance: High tier (401-700)
    # 10% chance: Very high tier (701-900)
    # 5% chance: God tier (901-1000)
    
    roll = random.randint(1, 100)
    
    if roll <= 60:
        # Low to mid tier
        return random.randint(10, 400)
    elif roll <= 85:
        # High tier
        return random.randint(401, 700)
    elif roll <= 95:
        # Very high tier
        return random.randint(701, 900)
    else:
        # God tier
        return random.randint(901, 1000)

# Generate completely random vampire power for new vampires (10-1000)
def generate_random_vampire_power():
    """Generate completely random power for new vampires"""
    
    # 50% chance: Fledgling (10-200)
    # 30% chance: Experienced (201-500)
    # 15% chance: Ancient (501-800)
    # 5% chance: Primordial (801-1000)
    
    roll = random.randint(1, 100)
    
    if roll <= 50:
        # Fledgling
        return random.randint(10, 200)
    elif roll <= 80:
        # Experienced
        return random.randint(201, 500)
    elif roll <= 95:
        # Ancient
        return random.randint(501, 800)
    else:
        # Primordial
        return random.randint(801, 1000)

# Calculate death chance based on power difference and outcome
def calculate_death_chance(player_power, enemy_power, player_won):
    """Calculate death chance - higher when losing to stronger opponents"""
    
    if player_won:
        # Winners have lower death chance
        base_chance = 5
        power_diff = player_power - enemy_power
        
        # Even when winning, very close fights are dangerous
        if power_diff < 50:
            base_chance = 15
    else:
        # Losers face real danger
        base_chance = 35
        power_diff = enemy_power - player_power
        
        # The stronger the opponent, the more likely you die
        power_multiplier = power_diff / 100
        base_chance += power_multiplier
    
    # Cap between 5% and 80%
    death_chance = max(5, min(80, base_chance))
    
    return int(death_chance)

# Calculate gang death chance (lower than solo)
def calculate_gang_death_chance(player_won):
    """Calculate death chance for gang battles - lower risk due to group support"""
    
    if player_won:
        # Winners have very low death chance
        return random.randint(2, 8)
    else:
        # Losers still have decent survival chance due to gang escape
        return random.randint(15, 35)

# Simulate instant battle
def simulate_battle(player_name, player_power, enemy_name, enemy_power):
    """Simulate an instant vampire battle"""
    
    # Calculate win probability based on power
    power_diff = player_power - enemy_power
    
    # Base 50% chance, adjusted by power difference
    # Each 10 points of power difference = 1% change in odds
    win_probability = 50 + (power_diff / 10)
    
    # Cap between 5% and 95%
    win_probability = max(5, min(95, win_probability))
    
    # Roll for winner
    roll = random.randint(1, 100)
    player_won = roll <= win_probability
    
    return {
        "player_won": player_won,
        "win_probability": int(win_probability),
        "roll": roll
    }

# Generate AI gang with SUPER RANDOM size
def generate_ai_gang():
    """Generate a random AI vampire gang with SUPER RANDOM size (1-20 vampires)"""
    
    # SUPER RANDOM gang size distribution
    # 30% chance: Small gang (1-3 vampires)
    # 25% chance: Medium gang (4-6 vampires)
    # 20% chance: Large gang (7-10 vampires)
    # 15% chance: Huge gang (11-15 vampires)
    # 10% chance: MASSIVE gang (16-20 vampires)
    
    roll = random.randint(1, 100)
    
    if roll <= 30:
        # Small gang
        gang_size = random.randint(1, 3)
    elif roll <= 55:
        # Medium gang
        gang_size = random.randint(4, 6)
    elif roll <= 75:
        # Large gang
        gang_size = random.randint(7, 10)
    elif roll <= 90:
        # Huge gang
        gang_size = random.randint(11, 15)
    else:
        # MASSIVE gang
        gang_size = random.randint(16, 20)
    
    ai_gang = []
    
    for _ in range(gang_size):
        ai_first_name = random.choice(FIRST_NAMES)
        ai_last_name = random.choice(LAST_NAMES)
        ai_name = f"{ai_first_name} {ai_last_name}"
        ai_power = generate_ai_power()
        
        ai_gang.append({
            "name": ai_name,
            "power": ai_power
        })
    
    return ai_gang

characters = load_characters()
graveyard = load_graveyard()

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Vampire Battle System Ready')

# Check to block DM commands
@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True

# Make command - Creates a vampire with RANDOM power (10-1000)
@bot.command(name='make')
async def make_character(ctx):
    """Generate a vampire with a random name and power level"""
    
    user_id = str(ctx.author.id)
    
    # Generate random vampire name
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    character_name = f"{first_name} {last_name}"
    
    # Generate unique character ID
    character_id = generate_unique_id()
    
    # Generate COMPLETELY RANDOM power level (10 to 1000)
    power_level = generate_random_vampire_power()
    
    # Create vampire data
    character_data = {
        "character_id": character_id,
        "name": character_name,
        "username": str(ctx.author),
        "user_id": user_id,
        "power_level": power_level,
        "wins": 0,
        "losses": 0,
        "has_been_reborn": False,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save vampire
    characters[character_id] = character_data
    save_characters(characters)
    
    # Determine power tier for description
    if power_level <= 200:
        tier = "Fledgling"
        tier_color = discord.Color.dark_grey()
    elif power_level <= 500:
        tier = "Experienced"
        tier_color = discord.Color.blue()
    elif power_level <= 800:
        tier = "Ancient"
        tier_color = discord.Color.purple()
    else:
        tier = "Primordial"
        tier_color = discord.Color.gold()
    
    # Display new vampire
    embed = discord.Embed(
        title="Vampire Created",
        description=f"**{character_name}**",
        color=tier_color
    )
    
    embed.add_field(name="Owner", value=ctx.author.name, inline=True)
    embed.add_field(name="ID", value=f"`{character_id}`", inline=True)
    embed.add_field(name="Power Level", value=f"{power_level}", inline=False)
    embed.add_field(name="Tier", value=tier, inline=True)
    embed.add_field(name="Record", value="0-0", inline=True)
    
    embed.set_footer(text="A new vampire has risen from the darkness")
    
    await ctx.send(embed=embed)

# Show command - Display user's vampires
@bot.command(name='show')
async def show_vampires(ctx):
    """Display all your vampires"""
    
    user_id = str(ctx.author.id)
    
    # Find all vampires owned by user
    user_vampires = [char for char in characters.values() if char.get('user_id') == user_id]
    
    if not user_vampires:
        await ctx.send("You don't have any vampires! Use `?make` to create one.")
        return
    
    # Sort by power level (highest first)
    user_vampires.sort(key=lambda x: x['power_level'], reverse=True)
    
    # Main embed
    embed = discord.Embed(
        title=f"{ctx.author.name}'s Vampires",
        description=f"Total Vampires: {len(user_vampires)}",
        color=discord.Color.dark_purple()
    )
    
    for vamp in user_vampires:
        # Build vampire info
        wins = vamp.get('wins', 0)
        losses = vamp.get('losses', 0)
        has_been_reborn = vamp.get('has_been_reborn', False)
        is_hybrid = vamp.get('is_hybrid', False)
        
        # Determine tier
        power = vamp['power_level']
        if power <= 200:
            tier = "Fledgling"
        elif power <= 500:
            tier = "Experienced"
        elif power <= 800:
            tier = "Ancient"
        else:
            tier = "Primordial"
        
        # Status indicators
        if is_hybrid:
            status = "HYBRID"
        elif has_been_reborn:
            status = "REBORN"
        else:
            status = "Original"
        
        rebirth_eligible = "No" if has_been_reborn else "Yes"
        
        value_text = (
            f"**ID:** `{vamp['character_id']}`\n"
            f"**Power:** {vamp['power_level']}\n"
            f"**Tier:** {tier}\n"
            f"**Record:** {wins}-{losses}\n"
            f"**Status:** {status}\n"
            f"**Rebirth Eligible:** {rebirth_eligible}"
        )
        
        embed.add_field(
            name=f"{vamp['name']}",
            value=value_text,
            inline=True
        )
    
    embed.set_footer(text="Use ?gang to battle as a group | Use ?fight <id> for solo battles")
    
    await ctx.send(embed=embed)

# Gang command - Group battle with all user's vampires vs SUPER RANDOM AI gang
@bot.command(name='gang')
async def gang_battle(ctx):
    """Battle as a gang with ALL your vampires against a RANDOM sized AI gang (1-20 vampires)"""
    
    user_id = str(ctx.author.id)
    
    # Find all vampires owned by user
    user_vampires = [char for char in characters.values() if char.get('user_id') == user_id]
    
    if not user_vampires:
        await ctx.send("You don't have any vampires! Use `?make` to create one.")
        return
    
    if len(user_vampires) < 2:
        await ctx.send("You need at least 2 vampires to form a gang! Use `?make` to create more vampires.")
        return
    
    # Calculate total gang power
    player_gang_power = sum(vamp['power_level'] for vamp in user_vampires)
    
    # Generate SUPER RANDOM AI gang (1-20 vampires)
    ai_gang = generate_ai_gang()
    ai_gang_power = sum(ai['power'] for ai in ai_gang)
    
    # Gang intro embed
    intro_embed = discord.Embed(
        title="GANG WAR",
        description=f"**{ctx.author.name}'s Gang** encounters a rival vampire gang in the shadows!",
        color=discord.Color.dark_purple()
    )
    
    # Player gang info
    player_gang_text = ""
    for vamp in user_vampires:
        player_gang_text += f"**{vamp['name']}** - Power: {vamp['power_level']}\n"
    
    intro_embed.add_field(
        name=f"YOUR GANG ({len(user_vampires)} vampires)",
        value=f"{player_gang_text}\n**Total Power: {player_gang_power}**",
        inline=False
    )
    
    # AI gang info - truncate if too large
    ai_gang_text = ""
    display_limit = 10  # Show first 10, then summarize rest
    
    for idx, ai_vamp in enumerate(ai_gang):
        if idx < display_limit:
            ai_gang_text += f"**{ai_vamp['name']}** - Power: {ai_vamp['power']}\n"
        elif idx == display_limit:
            remaining = len(ai_gang) - display_limit
            ai_gang_text += f"... and {remaining} more vampires\n"
            break
    
    intro_embed.add_field(
        name=f"ENEMY GANG ({len(ai_gang)} vampires)",
        value=f"{ai_gang_text}\n**Total Power: {ai_gang_power}**",
        inline=False
    )
    
    # Power difference
    power_diff = player_gang_power - ai_gang_power
    
    if power_diff > 1000:
        threat_level = "EASY TARGET"
        threat_color = discord.Color.dark_green()
    elif power_diff > 500:
        threat_level = "FAVORABLE MATCHUP"
        threat_color = discord.Color.green()
    elif power_diff > -500:
        threat_level = "EVEN MATCH"
        threat_color = discord.Color.gold()
    elif power_diff > -1000:
        threat_level = "DANGEROUS GANG"
        threat_color = discord.Color.orange()
    else:
        threat_level = "EXTREMELY DANGEROUS GANG"
        threat_color = discord.Color.dark_red()
    
    intro_embed.add_field(
        name="Threat Level",
        value=threat_level,
        inline=False
    )
    
    # Gang size comparison
    size_diff = len(user_vampires) - len(ai_gang)
    if size_diff > 0:
        size_advantage = f"You outnumber them by {size_diff} vampires"
    elif size_diff < 0:
        size_advantage = f"They outnumber you by {abs(size_diff)} vampires"
    else:
        size_advantage = "Equal numbers"
    
    intro_embed.add_field(
        name="Numbers",
        value=size_advantage,
        inline=False
    )
    
    intro_embed.set_footer(text="The gang war begins...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(4)
    
    # Simulate the gang battle
    battle_result = simulate_battle(
        f"{ctx.author.name}'s Gang",
        player_gang_power,
        "Enemy Gang",
        ai_gang_power
    )
    
    player_won = battle_result['player_won']
    
    # Calculate death chance (lower for gang battles)
    death_chance = calculate_gang_death_chance(player_won)
    
    # Determine casualties
    casualties = []
    survivors = []
    
    for vamp in user_vampires:
        death_roll = random.randint(1, 100)
        vampire_dies = death_roll <= death_chance
        
        if vampire_dies:
            casualties.append(vamp)
        else:
            survivors.append(vamp)
    
    # Outcome embed
    if player_won:
        outcome_embed = discord.Embed(
            title="GANG WAR VICTORY",
            description=f"**{ctx.author.name}'s Gang** has defeated the enemy gang of {len(ai_gang)} vampires!",
            color=discord.Color.green()
        )
        
        outcome_embed.add_field(
            name="Battle Odds",
            value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
            inline=False
        )
        
    else:
        outcome_embed = discord.Embed(
            title="GANG WAR DEFEAT",
            description=f"**{ctx.author.name}'s Gang** was defeated by the enemy gang of {len(ai_gang)} vampires!",
            color=discord.Color.red()
        )
        
        outcome_embed.add_field(
            name="Battle Odds",
            value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
            inline=False
        )
    
    # Show casualties
    if casualties:
        casualty_text = ""
        for vamp in casualties:
            casualty_text += f"{vamp['name']} (Power: {vamp['power_level']})\n"
            
            # Add to graveyard
            dead_vampire = vamp.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = "Gang War"
            graveyard.append(dead_vampire)
            
            # Delete vampire
            del characters[vamp['character_id']]
        
        outcome_embed.add_field(
            name=f"CASUALTIES ({len(casualties)} vampires)",
            value=casualty_text,
            inline=False
        )
        
        save_graveyard(graveyard)
        save_characters(characters)
    else:
        outcome_embed.add_field(
            name="CASUALTIES",
            value="All gang members survived!",
            inline=False
        )
    
    # Update survivors
    if survivors:
        survivor_text = ""
        for vamp in survivors:
            if player_won:
                vamp['wins'] = vamp.get('wins', 0) + 1
            else:
                vamp['losses'] = vamp.get('losses', 0) + 1
            
            characters[vamp['character_id']] = vamp
            survivor_text += f"{vamp['name']} (Power: {vamp['power_level']}) - Record: {vamp['wins']}-{vamp['losses']}\n"
        
        outcome_embed.add_field(
            name=f"SURVIVORS ({len(survivors)} vampires)",
            value=survivor_text,
            inline=False
        )
        
        save_characters(characters)
    
    # Show rebirth info if applicable
    rebirth_ids = []
    for vamp in casualties:
        if not vamp.get('has_been_reborn', False):
            rebirth_ids.append(vamp['character_id'])
    
    if rebirth_ids:
        rebirth_text = "Fallen gang members can be reborn:\n"
        for char_id in rebirth_ids:
            rebirth_text += f"`?rebirth {char_id}`\n"
        outcome_embed.set_footer(text=rebirth_text)
    
    await ctx.send(embed=outcome_embed)

# Transfer command - Sacrifice two vampires to create a hybrid
@bot.command(name='transfer')
async def transfer_vampires(ctx, vampire1_id: str = None, vampire2_id: str = None):
    """Sacrifice two of your vampires to create a powerful hybrid. Usage: ?transfer <id1> <id2>"""
    
    # Check if both IDs were provided
    if vampire1_id is None or vampire2_id is None:
        await ctx.send("Usage: `?transfer <vampire1_id> <vampire2_id>`\nExample: `?transfer 123456 789012`\n\nBoth vampires will be sacrificed to create a powerful hybrid!")
        return
    
    # Check if trying to transfer same vampire
    if vampire1_id == vampire2_id:
        await ctx.send("You cannot transfer a vampire with itself!")
        return
    
    user_id = str(ctx.author.id)
    
    # Check if both vampires exist
    if vampire1_id not in characters:
        await ctx.send(f"Vampire ID `{vampire1_id}` not found!")
        return
    
    if vampire2_id not in characters:
        await ctx.send(f"Vampire ID `{vampire2_id}` not found!")
        return
    
    vampire1 = characters[vampire1_id]
    vampire2 = characters[vampire2_id]
    
    # Verify ownership of both vampires
    if vampire1.get('user_id') != user_id:
        await ctx.send(f"You don't own the vampire with ID `{vampire1_id}`!")
        return
    
    if vampire2.get('user_id') != user_id:
        await ctx.send(f"You don't own the vampire with ID `{vampire2_id}`!")
        return
    
    # Transfer ritual intro
    ritual_embed = discord.Embed(
        title="BLOOD TRANSFER RITUAL",
        description=f"**{vampire1['name']}** and **{vampire2['name']}** begin the forbidden ritual...\n\nTheir blood mingles in darkness...",
        color=discord.Color.dark_purple()
    )
    
    ritual_embed.add_field(
        name=f"{vampire1['name']}",
        value=f"Power: {vampire1['power_level']}\nRecord: {vampire1.get('wins', 0)}-{vampire1.get('losses', 0)}",
        inline=True
    )
    
    ritual_embed.add_field(
        name=f"{vampire2['name']}",
        value=f"Power: {vampire2['power_level']}\nRecord: {vampire2.get('wins', 0)}-{vampire2.get('losses', 0)}",
        inline=True
    )
    
    ritual_embed.set_footer(text="Both vampires will be sacrificed...")
    
    await ctx.send(embed=ritual_embed)
    await asyncio.sleep(4)
    
    # Generate new hybrid vampire
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    hybrid_name = f"{first_name} {last_name}"
    
    # Generate new ID for hybrid
    hybrid_id = generate_unique_id()
    
    # Calculate hybrid power
    # Combine both powers + massive bonus (100-300)
    combined_power = vampire1['power_level'] + vampire2['power_level']
    ritual_bonus = random.randint(100, 300)
    hybrid_power = combined_power + ritual_bonus
    
    # Cap at 1000
    if hybrid_power > 1000:
        hybrid_power = 1000
        actual_bonus = 1000 - combined_power
    else:
        actual_bonus = ritual_bonus
    
    # Combine wins (keep total victories)
    total_wins = vampire1.get('wins', 0) + vampire2.get('wins', 0)
    
    # Hybrid starts with 0 losses (fresh start)
    total_losses = 0
    
    # Check if either vampire was reborn
    has_been_reborn = vampire1.get('has_been_reborn', False) or vampire2.get('has_been_reborn', False)
    
    # Create hybrid vampire
    hybrid_data = {
        "character_id": hybrid_id,
        "name": hybrid_name,
        "username": str(ctx.author),
        "user_id": user_id,
        "power_level": hybrid_power,
        "wins": total_wins,
        "losses": total_losses,
        "has_been_reborn": has_been_reborn,
        "is_hybrid": True,
        "parent1_name": vampire1['name'],
        "parent2_name": vampire2['name'],
        "parent1_id": vampire1_id,
        "parent2_id": vampire2_id,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Add sacrificed vampires to graveyard
    dead_vamp1 = vampire1.copy()
    dead_vamp1['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dead_vamp1['killed_by'] = "Blood Transfer Ritual"
    
    dead_vamp2 = vampire2.copy()
    dead_vamp2['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dead_vamp2['killed_by'] = "Blood Transfer Ritual"
    
    current_graveyard = load_graveyard()
    current_graveyard.append(dead_vamp1)
    current_graveyard.append(dead_vamp2)
    save_graveyard(current_graveyard)
    
    # Delete old vampires
    del characters[vampire1_id]
    del characters[vampire2_id]
    
    # Save hybrid vampire
    characters[hybrid_id] = hybrid_data
    save_characters(characters)
    
    # Determine hybrid tier
    if hybrid_power <= 200:
        tier = "Fledgling"
        tier_color = discord.Color.dark_grey()
    elif hybrid_power <= 500:
        tier = "Experienced"
        tier_color = discord.Color.blue()
    elif hybrid_power <= 800:
        tier = "Ancient"
        tier_color = discord.Color.purple()
    else:
        tier = "Primordial"
        tier_color = discord.Color.gold()
    
    # Success embed
    success_embed = discord.Embed(
        title="HYBRID VAMPIRE BORN",
        description=f"The ritual is complete! **{hybrid_name}** emerges from the crimson flames!",
        color=tier_color
    )
    
    success_embed.add_field(
        name="Hybrid Name",
        value=hybrid_name,
        inline=False
    )
    
    success_embed.add_field(
        name="New ID",
        value=f"`{hybrid_id}`",
        inline=False
    )
    
    success_embed.add_field(
        name="Power Fusion",
        value=f"{vampire1['power_level']} + {vampire2['power_level']} + {actual_bonus} (ritual bonus) = **{hybrid_power}**",
        inline=False
    )
    
    success_embed.add_field(
        name="Tier",
        value=tier,
        inline=True
    )
    
    success_embed.add_field(
        name="Combined Victories",
        value=f"Total Wins: {total_wins}",
        inline=True
    )
    
    success_embed.add_field(
        name="Sacrificed",
        value=f"{vampire1['name']}\n{vampire2['name']}",
        inline=False
    )
    
    if has_been_reborn:
        success_embed.add_field(
            name="WARNING",
            value="This hybrid inherited rebirth status and CANNOT be reborn if killed",
            inline=False
        )
    else:
        success_embed.add_field(
            name="Rebirth Status",
            value="This hybrid can be reborn once if killed",
            inline=False
        )
    
    success_embed.set_footer(text="A new apex predator has been created")
    
    await ctx.send(embed=success_embed)

# Fight command - Battle against AI vampires with COMPLETELY RANDOM power
@bot.command(name='fight')
async def fight_character(ctx, character_id: str = None):
    """Fight an AI vampire opponent. Usage: ?fight <character_id>"""
    
    # Check if character ID was provided
    if character_id is None:
        await ctx.send("Usage: `?fight <character_id>`\nExample: `?fight 123456`")
        return
    
    # Check if vampire exists
    if character_id not in characters:
        await ctx.send(f"Vampire ID `{character_id}` not found!")
        return
    
    player_char = characters[character_id]
    user_id = str(ctx.author.id)
    
    # Verify ownership
    if player_char.get('user_id') != user_id:
        await ctx.send("You don't own this vampire!")
        return
    
    # Generate COMPLETELY RANDOM AI opponent (10-1000)
    ai_power = generate_ai_power()
    
    ai_first_name = random.choice(FIRST_NAMES)
    ai_last_name = random.choice(LAST_NAMES)
    ai_name = f"{ai_first_name} {ai_last_name}"
    
    # Determine power difference for threat level
    power_diff = ai_power - player_char['power_level']
    
    if power_diff > 300:
        threat_level = "EXTREMELY DANGEROUS OPPONENT"
        threat_color = discord.Color.dark_red()
    elif power_diff > 150:
        threat_level = "DANGEROUS OPPONENT"
        threat_color = discord.Color.red()
    elif power_diff > 50:
        threat_level = "TOUGH CHALLENGER"
        threat_color = discord.Color.orange()
    elif power_diff > -50:
        threat_level = "EVEN MATCH"
        threat_color = discord.Color.gold()
    elif power_diff > -150:
        threat_level = "FAVORABLE MATCHUP"
        threat_color = discord.Color.green()
    else:
        threat_level = "EASY TARGET"
        threat_color = discord.Color.dark_green()
    
    # Determine AI tier
    if ai_power <= 200:
        ai_tier = "Fledgling"
    elif ai_power <= 500:
        ai_tier = "Experienced"
    elif ai_power <= 800:
        ai_tier = "Ancient"
    else:
        ai_tier = "Primordial"
    
    # Battle intro embed
    intro_embed = discord.Embed(
        title="BLOOD BATTLE",
        description=f"**{player_char['name']}** encounters **{ai_name}** in the darkness\n\n{threat_level}",
        color=threat_color
    )
    
    intro_embed.add_field(
        name=f"{player_char['name']} (YOU)",
        value=f"Power: **{player_char['power_level']}**\nRecord: {player_char.get('wins', 0)}-{player_char.get('losses', 0)}",
        inline=True
    )
    
    intro_embed.add_field(
        name=f"{ai_name} (ENEMY)",
        value=f"Power: **{ai_power}**\nTier: {ai_tier}",
        inline=True
    )
    
    intro_embed.set_footer(text="The battle begins...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)
    
    # Simulate the battle
    battle_result = simulate_battle(
        player_char['name'], 
        player_char['power_level'],
        ai_name,
        ai_power
    )
    
    player_won = battle_result['player_won']
    
    # Calculate death chance
    death_chance = calculate_death_chance(
        player_char['power_level'],
        ai_power,
        player_won
    )
    
    # Roll for death
    death_roll = random.randint(1, 100)
    vampire_dies = death_roll <= death_chance
    
    # Outcome embed
    if player_won:
        if vampire_dies:
            # Rare case: won but died from injuries
            outcome_embed = discord.Embed(
                title="PYRRHIC VICTORY",
                description=f"**{player_char['name']}** defeated **{ai_name}**, but succumbed to fatal wounds",
                color=discord.Color.dark_red()
            )
            
            outcome_embed.add_field(
                name="Death Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Final Moments",
                value=f"Despite victory, {player_char['name']} collapses into ash",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Final Record",
                value=f"{player_char.get('wins', 0)}-{player_char.get('losses', 0)}",
                inline=False
            )
            
            # Check rebirth eligibility
            if not player_char.get('has_been_reborn', False):
                outcome_embed.set_footer(text=f"Use ?rebirth {character_id} to bring them back")
            else:
                outcome_embed.set_footer(text="This vampire has already been reborn once and cannot be resurrected again")
            
            # Add to graveyard
            dead_vampire = player_char.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = f"{ai_name} (Fatal Wounds)"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            
            # Delete vampire
            del characters[character_id]
            save_characters(characters)
            
        else:
            # Victory and survival
            outcome_embed = discord.Embed(
                title="VICTORY",
                description=f"**{player_char['name']}** has defeated **{ai_name}**",
                color=discord.Color.green()
            )
            
            outcome_embed.add_field(
                name="Battle Odds",
                value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Survival Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less) - SURVIVED",
                inline=False
            )
            
            # Update wins
            player_char['wins'] = player_char.get('wins', 0) + 1
            characters[character_id] = player_char
            save_characters(characters)
            
            outcome_embed.add_field(
                name="New Record",
                value=f"{player_char['wins']}-{player_char.get('losses', 0)}",
                inline=False
            )
            
    else:
        # Player lost
        if vampire_dies:
            # Permanent death
            outcome_embed = discord.Embed(
                title="PERMANENT DEATH",
                description=f"**{player_char['name']}** has been destroyed by **{ai_name}**",
                color=discord.Color.dark_red()
            )
            
            outcome_embed.add_field(
                name="Battle Odds",
                value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Death Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Final Record",
                value=f"{player_char.get('wins', 0)}-{player_char.get('losses', 0)}",
                inline=False
            )
            
            outcome_embed.add_field(
                name="The End",
                value=f"{player_char['name']} has been staked through the heart and turned to ash",
                inline=False
            )
            
            # Check rebirth eligibility
            if not player_char.get('has_been_reborn', False):
                outcome_embed.set_footer(text=f"Use ?rebirth {character_id} to bring them back")
            else:
                outcome_embed.set_footer(text="This vampire has already been reborn once and cannot be resurrected again")
            
            # Add to graveyard
            dead_vampire = player_char.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = ai_name
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            
            # Delete vampire
            del characters[character_id]
            save_characters(characters)
            
        else:
            # Defeated but survived
            outcome_embed = discord.Embed(
                title="DEFEAT - BUT ALIVE",
                description=f"**{player_char['name']}** was defeated by **{ai_name}** but managed to escape",
                color=discord.Color.orange()
            )
            
            outcome_embed.add_field(
                name="Battle Odds",
                value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Survival Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less) - SURVIVED",
                inline=False
            )
            
            # Update losses
            player_char['losses'] = player_char.get('losses', 0) + 1
            characters[character_id] = player_char
            save_characters(characters)
            
            outcome_embed.add_field(
                name="New Record",
                value=f"{player_char.get('wins', 0)}-{player_char['losses']}",
                inline=False
            )
            
            outcome_embed.set_footer(text="Your vampire fled into the shadows, wounded but alive")
    
    await ctx.send(embed=outcome_embed)

# Rebirth command - Bring a dead vampire back to life with more power (ONE TIME ONLY)
@bot.command(name='rebirth')
async def rebirth_vampire(ctx, character_id: str = None):
    """Resurrect a fallen vampire with increased power (ONE TIME ONLY). Usage: ?rebirth <character_id>"""
    
    # Check if character ID was provided
    if character_id is None:
        await ctx.send("Usage: `?rebirth <character_id>`\nExample: `?rebirth 123456`")
        return
    
    user_id = str(ctx.author.id)
    
    # Load current graveyard
    current_graveyard = load_graveyard()
    
    # Find the dead vampire
    dead_vampire = None
    graveyard_index = None
    
    for idx, vamp in enumerate(current_graveyard):
        if vamp.get('character_id') == character_id:
            dead_vampire = vamp
            graveyard_index = idx
            break
    
    # Check if vampire was found in graveyard
    if dead_vampire is None:
        await ctx.send(f"No dead vampire with ID `{character_id}` found in the graveyard!")
        return
    
    # Verify ownership
    if dead_vampire.get('user_id') != user_id:
        await ctx.send("You don't own this vampire!")
        return
    
    # Check if vampire has already been reborn
    if dead_vampire.get('has_been_reborn', False):
        await ctx.send(f"**{dead_vampire['name']}** has already been reborn once and cannot be resurrected again!\n\nEach vampire can only be reborn ONE time. Use `?make` to create a new vampire.")
        return
    
    # Rebirth ritual embed
    ritual_embed = discord.Embed(
        title="REBIRTH RITUAL",
        description=f"Ancient blood magic awakens **{dead_vampire['name']}** from eternal slumber...",
        color=discord.Color.dark_purple()
    )
    
    ritual_embed.add_field(
        name="Former Power",
        value=f"{dead_vampire['power_level']}",
        inline=True
    )
    
    ritual_embed.add_field(
        name="Previous Record",
        value=f"{dead_vampire.get('wins', 0)}-{dead_vampire.get('losses', 0)}",
        inline=True
    )
    
    ritual_embed.set_footer(text="The ritual begins...")
    
    await ctx.send(embed=ritual_embed)
    await asyncio.sleep(3)
    
    # Calculate power boost
    # Base boost: 100-250 power
    # Additional 15% of original power
    base_boost = random.randint(100, 250)
    percentage_boost = int(dead_vampire['power_level'] * 0.15)
    total_boost = base_boost + percentage_boost
    
    new_power = dead_vampire['power_level'] + total_boost
    
    # Cap at 1000
    if new_power > 1000:
        new_power = 1000
        total_boost = 1000 - dead_vampire['power_level']
    
    # Create reborn vampire with new ID
    new_character_id = generate_unique_id()
    
    reborn_data = {
        "character_id": new_character_id,
        "name": dead_vampire['name'],
        "username": dead_vampire.get('username'),
        "user_id": user_id,
        "power_level": new_power,
        "wins": dead_vampire.get('wins', 0),
        "losses": dead_vampire.get('losses', 0),
        "has_been_reborn": True,
        "is_hybrid": dead_vampire.get('is_hybrid', False),
        "original_id": character_id,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "reborn_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Preserve hybrid parent info if applicable
    if dead_vampire.get('is_hybrid', False):
        reborn_data['parent1_name'] = dead_vampire.get('parent1_name')
        reborn_data['parent2_name'] = dead_vampire.get('parent2_name')
        reborn_data['parent1_id'] = dead_vampire.get('parent1_id')
        reborn_data['parent2_id'] = dead_vampire.get('parent2_id')
    
    # Save reborn vampire
    characters[new_character_id] = reborn_data
    save_characters(characters)
    
    # Remove from graveyard
    current_graveyard.pop(graveyard_index)
    save_graveyard(current_graveyard)
    
    # Determine new tier
    if new_power <= 200:
        tier = "Fledgling"
        tier_color = discord.Color.dark_grey()
    elif new_power <= 500:
        tier = "Experienced"
        tier_color = discord.Color.blue()
    elif new_power <= 800:
        tier = "Ancient"
        tier_color = discord.Color.purple()
    else:
        tier = "Primordial"
        tier_color = discord.Color.gold()
    
    # Success embed
    success_embed = discord.Embed(
        title="RESURRECTION COMPLETE",
        description=f"**{dead_vampire['name']}** rises from the ashes, reborn with ancient power!",
        color=tier_color
    )
    
    success_embed.add_field(
        name="New ID",
        value=f"`{new_character_id}`",
        inline=False
    )
    
    success_embed.add_field(
        name="Power Increase",
        value=f"{dead_vampire['power_level']} → **{new_power}** (+{total_boost})",
        inline=False
    )
    
    success_embed.add_field(
        name="New Tier",
        value=tier,
        inline=True
    )
    
    success_embed.add_field(
        name="Retained Record",
        value=f"{dead_vampire.get('wins', 0)}-{dead_vampire.get('losses', 0)}",
        inline=True
    )
    
    success_embed.add_field(
        name="WARNING",
        value="This vampire has used their ONE rebirth. If they die again, they cannot be resurrected.",
        inline=False
    )
    
    success_embed.set_footer(text="Your vampire has returned stronger than ever")
    
    await ctx.send(embed=success_embed)

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
