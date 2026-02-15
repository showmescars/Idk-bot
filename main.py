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

# Vampire abilities pool
SKILLS = [
    "Blood Manipulation", "Shadow Travel", "Hypnotic Gaze", "Supernatural Speed",
    "Enhanced Strength", "Regeneration", "Mist Form", "Bat Transformation",
    "Mind Control", "Night Vision", "Wall Crawling", "Blood Drain",
    "Immortality", "Shapeshifting", "Feral Claws", "Venomous Bite",
    "Telepathy", "Superhuman Agility", "Blood Sense", "Darkness Manipulation",
    "Charm", "Fear Inducement", "Enhanced Senses", "Undead Resilience",
    "Thrall Creation", "Blood Healing", "Vampiric Speed", "Death Touch",
    "Soul Drain", "Crimson Lightning", "Bloodlust Rage", "Eternal Youth",
    "Mesmerize", "Bloodfire", "Cursed Bite", "Nightmare Inducement",
    "Blood Wings", "Lunar Empowerment", "Corpse Animation", "Dark Pact"
]

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

# Make command - Creates a vampire
@bot.command(name='make')
async def make_character(ctx):
    """Generate a unique vampire with random abilities and power level"""
    
    user_id = str(ctx.author.id)
    
    # Check if user already has a vampire
    if user_id in characters:
        char = characters[user_id]
        
        # Display existing vampire
        embed = discord.Embed(
            title=char['name'],
            description=f"Owner: {ctx.author.name}\nID: `{char['character_id']}`\nRace: Vampire",
            color=discord.Color.dark_red()
        )
        
        embed.add_field(name="Blood Power", value=f"{char['power_level']}", inline=False)
        
        skills_text = "\n".join([f"- {skill}" for skill in char['skills']])
        embed.add_field(name="Vampiric Abilities", value=skills_text, inline=False)
        
        # Show record
        wins = char.get('wins', 0)
        losses = char.get('losses', 0)
        embed.add_field(name="Battle Record", value=f"{wins}W - {losses}L", inline=False)
        
        await ctx.send(embed=embed)
        return
    
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
    selected_skills = random.sample(SKILLS, num_skills)
    
    # Create vampire data
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
    
    # Save vampire
    characters[user_id] = character_data
    save_characters(characters)
    
    # Display new vampire
    embed = discord.Embed(
        title=character_name,
        description=f"Owner: {ctx.author.name}\nID: `{character_id}`\nRace: Vampire",
        color=discord.Color.dark_red()
    )
    
    embed.add_field(name="Blood Power", value=f"{power_level}", inline=False)
    
    skills_text = "\n".join([f"- {skill}" for skill in selected_skills])
    embed.add_field(name="Vampiric Abilities", value=skills_text, inline=False)
    
    # Show initial record
    embed.add_field(name="Battle Record", value="0W - 0L", inline=False)
    
    await ctx.send(embed=embed)

# Show command - Shows your vampire
@bot.command(name='show')
async def show_character(ctx):
    """Show your vampire"""
    
    user_id = str(ctx.author.id)
    
    # Check if user has a vampire
    if user_id not in characters:
        await ctx.send("You don't have a vampire yet! Use `?make` to create one.")
        return
    
    char = characters[user_id]
    
    # Display vampire
    embed = discord.Embed(
        title=char['name'],
        description=f"Owner: {ctx.author.name}\nID: `{char['character_id']}`\nRace: Vampire",
        color=discord.Color.dark_red()
    )
    
    embed.add_field(name="Blood Power", value=f"{char['power_level']}", inline=False)
    
    skills_text = "\n".join([f"- {skill}" for skill in char['skills']])
    embed.add_field(name="Vampiric Abilities", value=skills_text, inline=False)
    
    # Show record
    wins = char.get('wins', 0)
    losses = char.get('losses', 0)
    embed.add_field(name="Battle Record", value=f"{wins}W - {losses}L", inline=False)
    
    await ctx.send(embed=embed)

# Fight command - Fight random vampire opponents
@bot.command(name='fight')
async def fight_character(ctx, character_id: str = None):
    """Fight a random vampire - you can win or lose! Usage: ?fight <character_id>"""
    
    # Check if character ID was provided
    if character_id is None:
        await ctx.send("Usage: `?fight <character_id>`\nExample: `?fight 123456`\n\nUse `?show` to see your vampire ID.")
        return
    
    user_id = str(ctx.author.id)
    
    # Check if user has a vampire
    if user_id not in characters:
        await ctx.send("You don't have a vampire yet! Use `?make` to create one.")
        return
    
    player_char = characters[user_id]
    
    # Verify the character ID matches
    if player_char['character_id'] != character_id:
        await ctx.send(f"Invalid vampire ID! Your vampire ID is `{player_char['character_id']}`")
        return
    
    # Generate random AI vampire opponent
    ai_first_name = random.choice(FIRST_NAMES)
    ai_last_name = random.choice(LAST_NAMES)
    ai_name = f"{ai_first_name} {ai_last_name}"
    ai_power_level = random.randint(10, 100)
    ai_num_skills = random.randint(3, 5)
    ai_skills = random.sample(SKILLS, ai_num_skills)
    
    # Battle embed - show both vampires
    battle_embed = discord.Embed(
        title="BLOOD BATTLE",
        description="Two vampires clash in the darkness!",
        color=discord.Color.purple()
    )
    
    battle_embed.add_field(
        name=f"{player_char['name']} (YOU)",
        value=f"Blood Power: {player_char['power_level']}\nAbilities: {', '.join(player_char['skills'][:2])}...",
        inline=True
    )
    
    battle_embed.add_field(
        name=f"{ai_name} (ENEMY VAMPIRE)",
        value=f"Blood Power: {ai_power_level}\nAbilities: {', '.join(ai_skills[:2])}...",
        inline=True
    )
    
    await ctx.send(embed=battle_embed)
    
    # 4 second delay before showing results
    await asyncio.sleep(4)
    
    # Calculate win chance based on power levels
    player_power = player_char['power_level']
    total_power = player_power + ai_power_level
    player_win_chance = (player_power / total_power) * 100
    
    # Add some randomness (30% random factor)
    random_factor = random.randint(-15, 15)
    final_win_chance = max(10, min(90, player_win_chance + random_factor))
    
    # Determine winner
    roll = random.randint(1, 100)
    player_wins = roll <= final_win_chance
    
    # Result embed
    if player_wins:
        # Update wins
        if 'wins' not in player_char:
            player_char['wins'] = 0
        player_char['wins'] += 1
        characters[user_id] = player_char
        save_characters(characters)
        
        result_embed = discord.Embed(
            title="VICTORY",
            description=f"{player_char['name']} has drained {ai_name} of their blood!",
            color=discord.Color.green()
        )
        
        result_embed.add_field(name="Your Blood Power", value=f"{player_power}", inline=True)
        result_embed.add_field(name="Enemy Blood Power", value=f"{ai_power_level}", inline=True)
        result_embed.add_field(name="Win Chance", value=f"{final_win_chance:.1f}%", inline=True)
        result_embed.add_field(
            name="Battle Summary",
            value=f"{player_char['name']} emerged victorious from the blood battle and survives to hunt another night!",
            inline=False
        )
        
        # Show updated record
        wins = player_char.get('wins', 0)
        losses = player_char.get('losses', 0)
        result_embed.add_field(name="New Record", value=f"{wins}W - {losses}L", inline=False)
        
        await ctx.send(embed=result_embed)
    else:
        result_embed = discord.Embed(
            title="DEFEAT",
            description=f"{player_char['name']} has been destroyed by {ai_name}!",
            color=discord.Color.red()
        )
        
        result_embed.add_field(name="Your Blood Power", value=f"{player_power}", inline=True)
        result_embed.add_field(name="Enemy Blood Power", value=f"{ai_power_level}", inline=True)
        result_embed.add_field(name="Win Chance", value=f"{final_win_chance:.1f}%", inline=True)
        
        # Show final record before deletion
        wins = player_char.get('wins', 0)
        losses = player_char.get('losses', 0)
        result_embed.add_field(name="Final Record", value=f"{wins}W - {losses}L", inline=False)
        
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
        
        # Delete the vampire
        del characters[user_id]
        save_characters(characters)

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
    total_losses = sum(char.get('wins', 0) for char in dead_vampires)
    
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
    
    # Show top 5 alive vampires by wins
    if alive_vampires:
        alive_list = sorted(alive_vampires.values(), key=lambda x: x.get('wins', 0), reverse=True)[:5]
        
        alive_embed = discord.Embed(
            title="TOP LIVING VAMPIRES",
            description="The strongest vampires still walking the earth",
            color=discord.Color.green()
        )
        
        for idx, vamp in enumerate(alive_list, 1):
            wins = vamp.get('wins', 0)
            losses = vamp.get('losses', 0)
            alive_embed.add_field(
                name=f"{idx}. {vamp['name']}",
                value=f"ID: `{vamp['character_id']}` | Power: {vamp['power_level']} | Record: {wins}W-{losses}L",
                inline=False
            )
        
        await ctx.send(embed=alive_embed)
    
    # Show last 5 fallen vampires
    if dead_vampires:
        recent_dead = dead_vampires[-5:]
        recent_dead.reverse()
        
        dead_embed = discord.Embed(
            title="RECENTLY FALLEN VAMPIRES",
            description="Those who met their end in battle",
            color=discord.Color.dark_red()
        )
        
        for vamp in recent_dead:
            wins = vamp.get('wins', 0)
            losses = vamp.get('losses', 0)
            dead_embed.add_field(
                name=f"{vamp['name']}",
                value=f"ID: `{vamp['character_id']}` | Power: {vamp['power_level']} | Record: {wins}W-{losses}L\nKilled by: {vamp.get('killed_by', 'Unknown')}",
                inline=False
            )
        
        await ctx.send(embed=dead_embed)

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
