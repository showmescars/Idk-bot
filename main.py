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

# Dynamic AI power calculation based on player power
def generate_ai_power(player_power):
    """Generate dynamic AI power that creates interesting fights"""
    
    # 40% chance: Slightly weaker opponent (60-90% of player power)
    # 30% chance: Equal match (90-110% of player power)
    # 20% chance: Stronger opponent (110-140% of player power)
    # 10% chance: Very strong opponent (140-180% of player power)
    
    roll = random.randint(1, 100)
    
    if roll <= 40:
        multiplier = random.uniform(0.6, 0.9)
    elif roll <= 70:
        multiplier = random.uniform(0.9, 1.1)
    elif roll <= 90:
        multiplier = random.uniform(1.1, 1.4)
    else:
        multiplier = random.uniform(1.4, 1.8)
    
    ai_power = int(player_power * multiplier)
    
    # Keep within bounds 10-100
    ai_power = max(10, min(100, ai_power))
    
    return ai_power

# Calculate death chance based on power difference and outcome
def calculate_death_chance(player_power, enemy_power, player_won):
    """Calculate death chance - higher when losing to stronger opponents"""
    
    if player_won:
        # Winners have lower death chance
        base_chance = 5
        power_diff = player_power - enemy_power
        if power_diff < 5:
            base_chance = 15
    else:
        # Losers face real danger
        base_chance = 35
        power_diff = enemy_power - player_power
        power_multiplier = power_diff / 10
        base_chance += power_multiplier
    
    # Cap between 5% and 75%
    death_chance = max(5, min(75, base_chance))
    
    return int(death_chance)

# Simulate instant battle
def simulate_battle(player_name, player_power, enemy_name, enemy_power):
    """Simulate an instant vampire battle"""
    
    # Calculate win probability based on power
    power_diff = player_power - enemy_power
    
    # Base 50% chance, adjusted by power difference
    # Each point of power difference = 2% change in odds
    win_probability = 50 + (power_diff * 2)
    
    # Cap between 10% and 90%
    win_probability = max(10, min(90, win_probability))
    
    # Roll for winner
    roll = random.randint(1, 100)
    player_won = roll <= win_probability
    
    return {
        "player_won": player_won,
        "win_probability": win_probability,
        "roll": roll
    }

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

# Make command - Creates a vampire
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
    
    # Generate random power level (10 to 100)
    power_level = random.randint(10, 100)
    
    # Create vampire data
    character_data = {
        "character_id": character_id,
        "name": character_name,
        "username": str(ctx.author),
        "user_id": user_id,
        "power_level": power_level,
        "wins": 0,
        "losses": 0,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save vampire
    characters[character_id] = character_data
    save_characters(characters)
    
    # Display new vampire
    embed = discord.Embed(
        title="Vampire Created",
        description=f"**{character_name}**",
        color=discord.Color.dark_red()
    )
    
    embed.add_field(name="Owner", value=ctx.author.name, inline=True)
    embed.add_field(name="ID", value=f"`{character_id}`", inline=True)
    embed.add_field(name="Power Level", value=f"{power_level}", inline=False)
    embed.add_field(name="Record", value="0-0", inline=False)
    
    embed.set_footer(text="A new vampire has risen from the darkness")
    
    await ctx.send(embed=embed)

# Fight command - Battle against AI vampires
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
    
    # Generate dynamic AI opponent
    ai_power = generate_ai_power(player_char['power_level'])
    
    ai_first_name = random.choice(FIRST_NAMES)
    ai_last_name = random.choice(LAST_NAMES)
    ai_name = f"{ai_first_name} {ai_last_name}"
    
    # Determine power difference for threat level
    power_diff = ai_power - player_char['power_level']
    
    if power_diff > 20:
        threat_level = "DANGEROUS OPPONENT"
        threat_color = discord.Color.dark_red()
    elif power_diff > 5:
        threat_level = "TOUGH CHALLENGER"
        threat_color = discord.Color.orange()
    elif power_diff > -5:
        threat_level = "EVEN MATCH"
        threat_color = discord.Color.gold()
    else:
        threat_level = "FAVORABLE MATCHUP"
        threat_color = discord.Color.green()
    
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
        value=f"Power: **{ai_power}**\nStatus: Wild Vampire",
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
            
            outcome_embed.set_footer(text="Your vampire is gone forever. Use ?make to create a new one")
            
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
