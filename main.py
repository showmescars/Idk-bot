import discord
from discord.ext import commands
import json
import os
import random
import asyncio
from datetime import datetime, timedelta
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

# LA Gang Member Names (First Names)
FIRST_NAMES = [
    "Tyrone", "DeAndre", "Marcus", "Jamal", "Darius", "Andre", "Carlos", "Miguel",
    "Jose", "Luis", "Diego", "Ramon", "Francisco", "Juan", "Antonio", "Jesus",
    "Roberto", "Fernando", "Manuel", "Cesar", "Rico", "Hector", "Pablo", "Oscar",
    "Raymond", "Antoine", "Lamar", "Terrell", "Kevin", "Brandon", "Isaiah", "Elijah",
    "Xavier", "Dominic", "Vincent", "Anthony", "Michael", "Christopher", "Daniel", "David",
    "Jonathan", "Steven", "Richard", "Eric", "Angel", "Victor", "Marco", "Sergio",
    "Eduardo", "Armando", "Raul", "Jorge", "Alejandro", "Mario", "Pedro", "Alberto"
]

# LA Gang Surnames
LAST_NAMES = [
    "Williams", "Johnson", "Brown", "Jackson", "Davis", "Rodriguez", "Martinez", "Garcia",
    "Hernandez", "Lopez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Rivera",
    "Flores", "Gomez", "Diaz", "Cruz", "Reyes", "Morales", "Jimenez", "Ortiz",
    "Washington", "Thompson", "Harris", "Robinson", "Walker", "Green", "White", "Lewis",
    "King", "Wright", "Hill", "Scott", "Adams", "Baker", "Nelson", "Mitchell",
    "Carter", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards",
    "Collins", "Stewart", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell"
]

# Real LA Gang Affiliations
LA_GANGS = {
    "Crips": {
        "sets": [
            "Rollin 60s Crips", "Eight Tray Gangster Crips", "Grape Street Watts Crips",
            "Hoover Criminals", "Rollin 30s Harlem Crips", "Rollin 40s Crips",
            "Rollin 90s Crips", "Rollin 100s Crips", "Kitchen Crips", "Avalon Gangster Crips",
            "East Coast Crips", "Raymond Avenue Crips", "Westside Crips", "Main Street Crips",
            "PJ Watts Crips", "Fudge Town Mafia Crips", "Neighborhood Crips", "Long Beach Crips"
        ],
        "color": discord.Color.blue(),
        "territory": ["South Central", "Compton", "Long Beach", "Inglewood", "Watts"]
    },
    "Bloods": {
        "sets": [
            "Bounty Hunter Bloods", "Crenshaw Mafia Gangsters", "Black P Stones",
            "Fruit Town Pirus", "Inglewood Family Bloods", "Van Ness Gangster Brims",
            "Centinela Park Family", "Denver Lane Bloods", "Tree Top Pirus", "Campanella Park Pirus",
            "Athens Park Bloods", "Skyline Pirus", "Mad Swan Bloods", "9 Deuce Bishops",
            "Hacienda Village Bloods", "Lime Hood Pirus", "Queen Street Bloods", "Harvard Park Brims"
        ],
        "color": discord.Color.red(),
        "territory": ["Compton", "South LA", "Inglewood", "Pasadena", "West Athens"]
    },
    "Sureños": {
        "sets": [
            "18th Street Gang", "Mara Salvatrucha (MS-13)", "Florencia 13", "Eastside 13",
            "38th Street Gang", "White Fence", "Varrio Nuevo Estrada", "Harpys 13",
            "King Kobras", "Primera Flats", "Avenues", "Big Hazard", "Highland Park 13",
            "Clanton 14", "Barrio Van Nuys", "Vineland Boys", "Langdon Street", "Diamond Street"
        ],
        "color": discord.Color.from_rgb(0, 128, 255),
        "territory": ["East LA", "South LA", "Boyle Heights", "Highland Park", "Downtown LA"]
    },
    "Norteños": {
        "sets": [
            "Varrio North Side", "Pacoima 13", "Varrio Nuevo", "Varrio Panorama",
            "Blythe Street", "Vineland Boyz", "North Side Kings", "Barrio Mojados"
        ],
        "color": discord.Color.red(),
        "territory": ["San Fernando Valley", "Pacoima", "Panorama City", "North Hollywood"]
    }
}

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

# Check if member is in jail
def is_in_jail(member):
    """Check if a gang member is currently in jail"""
    if 'jail_until' not in member:
        return False
    
    jail_until = datetime.strptime(member['jail_until'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    
    return now < jail_until

# Get remaining jail time
def get_jail_time_remaining(member):
    """Get the remaining jail time for a member"""
    if 'jail_until' not in member:
        return None
    
    jail_until = datetime.strptime(member['jail_until'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    
    if now >= jail_until:
        return None
    
    remaining = jail_until - now
    return remaining

# Simulate instant street battle
def simulate_battle():
    """Simulate an instant street battle - completely random 50/50"""
    roll = random.randint(1, 100)
    player_won = roll <= 50
    
    return {
        "player_won": player_won,
        "roll": roll
    }

# Calculate death chance
def calculate_death_chance(player_won):
    """Calculate death chance"""
    if player_won:
        return 15
    else:
        return 40

# Calculate crew death chance (lower than solo)
def calculate_crew_death_chance(player_won):
    """Calculate death chance for crew battles - lower risk due to backup"""
    if player_won:
        return random.randint(5, 10)
    else:
        return random.randint(20, 35)

# Generate rival gang crew with SUPER RANDOM size
def generate_rival_crew():
    """Generate a random rival gang crew with SUPER RANDOM size (1-20 members)"""
    
    roll = random.randint(1, 100)
    
    if roll <= 30:
        crew_size = random.randint(1, 3)
    elif roll <= 55:
        crew_size = random.randint(4, 6)
    elif roll <= 75:
        crew_size = random.randint(7, 10)
    elif roll <= 90:
        crew_size = random.randint(11, 15)
    else:
        crew_size = random.randint(16, 20)
    
    # Pick random rival gang
    rival_gang = random.choice(list(LA_GANGS.keys()))
    gang_sets = LA_GANGS[rival_gang]['sets']
    rival_set = random.choice(gang_sets)
    
    rival_crew = []
    
    for _ in range(crew_size):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        member_name = f"{first_name} '{last_name[:3].upper()}' {last_name}"
        
        rival_crew.append({
            "name": member_name,
            "gang": rival_gang,
            "set": rival_set
        })
    
    return rival_crew, rival_gang, rival_set

characters = load_characters()
graveyard = load_graveyard()

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('LA Gang Battle System Ready')

# Check to block DM commands
@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True

# Make command - Creates a gang member
@bot.command(name='make')
async def make_character(ctx):
    """Generate a gang member with a random name"""
    
    user_id = str(ctx.author.id)
    
    # Generate random gang member name
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    nickname = last_name[:3].upper()
    character_name = f"{first_name} '{nickname}' {last_name}"
    
    # Generate unique character ID
    character_id = generate_unique_id()
    
    # Randomly assign gang affiliation
    gang_affiliation = random.choice(list(LA_GANGS.keys()))
    gang_sets = LA_GANGS[gang_affiliation]['sets']
    set_name = random.choice(gang_sets)
    
    # Create gang member data
    character_data = {
        "character_id": character_id,
        "name": character_name,
        "username": str(ctx.author),
        "user_id": user_id,
        "gang_affiliation": gang_affiliation,
        "set_name": set_name,
        "kills": 0,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save gang member
    characters[character_id] = character_data
    save_characters(characters)
    
    # Get gang color
    gang_color = LA_GANGS[gang_affiliation]['color']
    
    # Display new gang member
    embed = discord.Embed(
        title="GANG MEMBER CREATED",
        description=f"**{character_name}**",
        color=gang_color
    )
    
    embed.add_field(name="Owner", value=ctx.author.name, inline=True)
    embed.add_field(name="ID", value=f"`{character_id}`", inline=True)
    embed.add_field(name="Gang Affiliation", value=f"{gang_affiliation}", inline=True)
    embed.add_field(name="Set", value=f"{set_name}", inline=True)
    
    embed.set_footer(text="A new soldier hit the streets")
    
    await ctx.send(embed=embed)

# Show command - Display user's gang members
@bot.command(name='show')
async def show_members(ctx):
    """Display all your gang members"""
    
    user_id = str(ctx.author.id)
    
    # Find all gang members owned by user
    user_members = [char for char in characters.values() if char.get('user_id') == user_id]
    
    if not user_members:
        await ctx.send("You don't have any gang members! Use `?make` to create one.")
        return
    
    # Sort by kills (highest first)
    user_members.sort(key=lambda x: x.get('kills', 0), reverse=True)
    
    # Main embed
    embed = discord.Embed(
        title=f"{ctx.author.name}'s Gang Members",
        description=f"Total Members: {len(user_members)}",
        color=discord.Color.dark_purple()
    )
    
    for member in user_members:
        # Check jail status
        in_jail = is_in_jail(member)
        jail_status = "LOCKED UP" if in_jail else "FREE"
        
        kills = member.get('kills', 0)
        
        value_text = (
            f"**ID:** `{member['character_id']}`\n"
            f"**Kills:** {kills}\n"
            f"**Gang:** {member.get('gang_affiliation', 'Unknown')}\n"
            f"**Set:** {member.get('set_name', 'Unknown')}\n"
            f"**Status:** {jail_status}"
        )
        
        if in_jail:
            remaining = get_jail_time_remaining(member)
            if remaining:
                minutes = int(remaining.total_seconds() // 60)
                seconds = int(remaining.total_seconds() % 60)
                value_text += f"\n**Time Left:** {minutes}m {seconds}s"
        
        embed.add_field(
            name=f"{member['name']}",
            value=value_text,
            inline=True
        )
    
    embed.set_footer(text="Use ?crew for crew battles | ?slide <id> for solo")
    
    await ctx.send(embed=embed)

# Crew command - Group battle
@bot.command(name='crew')
async def crew_battle(ctx):
    """Battle as a crew with ALL your gang members against a RANDOM sized rival crew (1-20 members)"""
    
    user_id = str(ctx.author.id)
    
    # Find all gang members owned by user
    user_members = [char for char in characters.values() if char.get('user_id') == user_id]
    
    if not user_members:
        await ctx.send("You don't have any gang members! Use `?make` to create one.")
        return
    
    # Filter out members in jail
    available_members = [m for m in user_members if not is_in_jail(m)]
    
    if not available_members:
        await ctx.send("All your gang members are locked up! Wait for them to get out of jail.")
        return
    
    if len(available_members) < 2:
        await ctx.send("You need at least 2 free gang members to form a crew! Use `?make` to recruit more or wait for members to get out of jail.")
        return
    
    # Generate SUPER RANDOM rival crew (1-20 members)
    rival_crew, rival_gang, rival_set = generate_rival_crew()
    
    # Get rival gang color
    rival_gang_color = LA_GANGS.get(rival_gang, {}).get('color', discord.Color.red())
    
    # Crew intro embed
    intro_embed = discord.Embed(
        title="CREW WAR",
        description=f"**{ctx.author.name}'s Crew** encounters a rival {rival_gang} crew in enemy territory!",
        color=rival_gang_color
    )
    
    # Player crew info
    player_crew_text = ""
    for member in available_members:
        player_crew_text += f"**{member['name']}** - Kills: {member.get('kills', 0)}\n"
    
    intro_embed.add_field(
        name=f"YOUR CREW ({len(available_members)} members)",
        value=player_crew_text,
        inline=False
    )
    
    # Rival crew info - truncate if too large
    rival_crew_text = ""
    display_limit = 10
    
    for idx, rival_member in enumerate(rival_crew):
        if idx < display_limit:
            rival_crew_text += f"**{rival_member['name']}**\n"
        elif idx == display_limit:
            remaining = len(rival_crew) - display_limit
            rival_crew_text += f"... and {remaining} more members\n"
            break
    
    intro_embed.add_field(
        name=f"RIVAL CREW - {rival_set} ({len(rival_crew)} members)",
        value=rival_crew_text,
        inline=False
    )
    
    # Crew size comparison
    size_diff = len(available_members) - len(rival_crew)
    if size_diff > 0:
        size_advantage = f"You outnumber them by {size_diff} members"
    elif size_diff < 0:
        size_advantage = f"They outnumber you by {abs(size_diff)} members"
    else:
        size_advantage = "Equal numbers"
    
    intro_embed.add_field(
        name="Numbers",
        value=size_advantage,
        inline=False
    )
    
    intro_embed.set_footer(text="The crew war begins...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(4)
    
    # Simulate the crew battle
    battle_result = simulate_battle()
    player_won = battle_result['player_won']
    
    # Calculate death chance (lower for crew battles)
    death_chance = calculate_crew_death_chance(player_won)
    
    # Determine casualties
    casualties = []
    survivors = []
    
    for member in available_members:
        death_roll = random.randint(1, 100)
        member_dies = death_roll <= death_chance
        
        if member_dies:
            casualties.append(member)
        else:
            survivors.append(member)
    
    # Outcome embed
    if player_won:
        outcome_embed = discord.Embed(
            title="CREW WAR VICTORY",
            description=f"**{ctx.author.name}'s Crew** has defeated the {rival_set} crew of {len(rival_crew)} members!",
            color=discord.Color.green()
        )
        
        outcome_embed.add_field(
            name="Battle Result",
            value=f"Rolled: {battle_result['roll']} (50 or less to win)",
            inline=False
        )
        
    else:
        outcome_embed = discord.Embed(
            title="CREW WAR DEFEAT",
            description=f"**{ctx.author.name}'s Crew** was defeated by the {rival_set} crew of {len(rival_crew)} members!",
            color=discord.Color.red()
        )
        
        outcome_embed.add_field(
            name="Battle Result",
            value=f"Rolled: {battle_result['roll']} (50 or less to win)",
            inline=False
        )
    
    # Show casualties
    if casualties:
        casualty_text = ""
        for member in casualties:
            casualty_text += f"{member['name']} (Kills: {member.get('kills', 0)})\n"
            
            # Add to graveyard
            dead_member = member.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_set} Crew War"
            graveyard.append(dead_member)
            
            # Delete member
            del characters[member['character_id']]
        
        outcome_embed.add_field(
            name=f"CASUALTIES ({len(casualties)} members)",
            value=casualty_text,
            inline=False
        )
        
        save_graveyard(graveyard)
        save_characters(characters)
    else:
        outcome_embed.add_field(
            name="CASUALTIES",
            value="All crew members survived!",
            inline=False
        )
    
    # Update survivors
    if survivors:
        survivor_text = ""
        for member in survivors:
            characters[member['character_id']] = member
            survivor_text += f"{member['name']} (Kills: {member.get('kills', 0)})\n"
        
        outcome_embed.add_field(
            name=f"SURVIVORS ({len(survivors)} members)",
            value=survivor_text,
            inline=False
        )
        
        save_characters(characters)
    
    await ctx.send(embed=outcome_embed)

# Slide command - Battle against rival gang members with JAIL SYSTEM based on kills
@bot.command(name='slide')
async def slide_on_opps(ctx, character_id: str = None):
    """Slide on rival gang members. Usage: ?slide <character_id>"""
    
    if character_id is None:
        await ctx.send("Usage: `?slide <character_id>`\nExample: `?slide 123456`")
        return
    
    if character_id not in characters:
        await ctx.send(f"Gang member ID `{character_id}` not found!")
        return
    
    player_char = characters[character_id]
    user_id = str(ctx.author.id)
    
    if player_char.get('user_id') != user_id:
        await ctx.send("You don't own this gang member!")
        return
    
    # Check if member is in jail
    if is_in_jail(player_char):
        remaining = get_jail_time_remaining(player_char)
        if remaining:
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            await ctx.send(f"**{player_char['name']}** is locked up! They'll be out in **{minutes}m {seconds}s**.")
            return
    
    # Generate rival
    rival_first_name = random.choice(FIRST_NAMES)
    rival_last_name = random.choice(LAST_NAMES)
    rival_nickname = rival_last_name[:3].upper()
    rival_name = f"{rival_first_name} '{rival_nickname}' {rival_last_name}"
    
    # Generate rival gang affiliation (different from player if possible)
    available_gangs = [g for g in LA_GANGS.keys() if g != player_char.get('gang_affiliation')]
    if not available_gangs:
        available_gangs = list(LA_GANGS.keys())
    
    rival_gang = random.choice(available_gangs)
    rival_sets = LA_GANGS[rival_gang]['sets']
    rival_set = random.choice(rival_sets)
    
    # Battle intro embed
    intro_embed = discord.Embed(
        title="SLIDING ON OPPS",
        description=f"**{player_char['name']}** spots **{rival_name}** in enemy territory",
        color=discord.Color.orange()
    )
    
    intro_embed.add_field(
        name=f"{player_char['name']} (YOU)",
        value=f"Kills: {player_char.get('kills', 0)}\nGang: {player_char.get('gang_affiliation', 'Unknown')}\nSet: {player_char.get('set_name', 'Unknown')}",
        inline=True
    )
    
    intro_embed.add_field(
        name=f"{rival_name} (OPP)",
        value=f"Gang: {rival_gang}\nSet: {rival_set}",
        inline=True
    )
    
    intro_embed.set_footer(text="The confrontation begins...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)
    
    # Simulate the battle
    battle_result = simulate_battle()
    player_won = battle_result['player_won']
    
    # Calculate death chance
    death_chance = calculate_death_chance(player_won)
    
    # Roll for death
    death_roll = random.randint(1, 100)
    member_dies = death_roll <= death_chance
    
    # JAIL SYSTEM - Roll for jail if member survives and wins
    jail_roll = random.randint(1, 100)
    goes_to_jail = False
    jail_minutes = 0
    
    if not member_dies and player_won:
        # Increment kill count
        player_char['kills'] = player_char.get('kills', 0) + 1
        
        # 30% chance of getting caught after killing someone
        jail_chance = 30
        goes_to_jail = jail_roll <= jail_chance
        
        if goes_to_jail:
            # Jail time = number of kills in minutes
            jail_minutes = player_char['kills']
    
    # Outcome embed
    if player_won:
        if member_dies:
            outcome_embed = discord.Embed(
                title="CAUGHT A BODY BUT PAID THE PRICE",
                description=f"**{player_char['name']}** eliminated **{rival_name}**, but was fatally wounded",
                color=discord.Color.dark_red()
            )
            
            outcome_embed.add_field(
                name="Battle Result",
                value=f"Rolled: {battle_result['roll']} (50 or less to win)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Death Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Final Moments",
                value=f"Despite the victory, {player_char['name']} didn't make it",
                inline=False
            )
            
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_name} ({rival_set}) - Fatal Wounds"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            
            del characters[character_id]
            save_characters(characters)
            
        else:
            if goes_to_jail:
                outcome_embed = discord.Embed(
                    title="BODY CAUGHT - BUT LOCKED UP",
                    description=f"**{player_char['name']}** eliminated **{rival_name}** from {rival_set} but got arrested!",
                    color=discord.Color.orange()
                )
            else:
                outcome_embed = discord.Embed(
                    title="BODY CAUGHT",
                    description=f"**{player_char['name']}** has eliminated **{rival_name}** from {rival_set}",
                    color=discord.Color.green()
                )
            
            outcome_embed.add_field(
                name="Battle Result",
                value=f"Rolled: {battle_result['roll']} (50 or less to win)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Survival Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less) - SURVIVED",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Kill Count",
                value=f"Total Kills: **{player_char['kills']}**",
                inline=False
            )
            
            if goes_to_jail:
                # Set jail time
                jail_until = datetime.now() + timedelta(minutes=jail_minutes)
                player_char['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
                
                outcome_embed.add_field(
                    name="ARRESTED",
                    value=f"Locked up for **{jail_minutes} minutes**",
                    inline=False
                )
            else:
                outcome_embed.add_field(
                    name="EVADED POLICE",
                    value=f"Got away clean!",
                    inline=False
                )
            
            characters[character_id] = player_char
            save_characters(characters)
            
    else:
        if member_dies:
            outcome_embed = discord.Embed(
                title="CAUGHT SLIPPING",
                description=f"**{player_char['name']}** was eliminated by **{rival_name}** from {rival_set}",
                color=discord.Color.dark_red()
            )
            
            outcome_embed.add_field(
                name="Battle Result",
                value=f"Rolled: {battle_result['roll']} (50 or less to win)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Death Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="RIP",
                value=f"{player_char['name']} was caught lacking in enemy territory\nFinal Kill Count: {player_char.get('kills', 0)}",
                inline=False
            )
            
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_name} ({rival_set})"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            
            del characters[character_id]
            save_characters(characters)
            
        else:
            outcome_embed = discord.Embed(
                title="TOOK AN L BUT SURVIVED",
                description=f"**{player_char['name']}** was defeated by **{rival_name}** but managed to escape",
                color=discord.Color.orange()
            )
            
            outcome_embed.add_field(
                name="Battle Result",
                value=f"Rolled: {battle_result['roll']} (50 or less to win)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Survival Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less) - SURVIVED",
                inline=False
            )
            
            characters[character_id] = player_char
            save_characters(characters)
    
    await ctx.send(embed=outcome_embed)

# Revenge command - Battle the rival that killed your gang member
@bot.command(name='revenge')
async def revenge_battle(ctx, dead_character_id: str = None, avenger_character_id: str = None):
    """Take revenge on the rival that killed your gang member. Usage: ?revenge <dead_member_id> <avenger_member_id>"""
    
    if dead_character_id is None or avenger_character_id is None:
        await ctx.send("Usage: `?revenge <dead_member_id> <avenger_member_id>`\nExample: `?revenge 123456 789012`\n\nUse the ID of your dead member and the ID of the member you want to use for revenge!")
        return
    
    user_id = str(ctx.author.id)
    
    # Check if avenger exists and is owned by user
    if avenger_character_id not in characters:
        await ctx.send(f"Avenger member ID `{avenger_character_id}` not found!")
        return
    
    avenger_char = characters[avenger_character_id]
    
    if avenger_char.get('user_id') != user_id:
        await ctx.send("You don't own this avenger!")
        return
    
    # Check if avenger is in jail
    if is_in_jail(avenger_char):
        remaining = get_jail_time_remaining(avenger_char)
        if remaining:
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            await ctx.send(f"**{avenger_char['name']}** is locked up! They'll be out in **{minutes}m {seconds}s**.")
            return
    
    # Find the dead member in graveyard
    current_graveyard = load_graveyard()
    
    dead_member = None
    for member in current_graveyard:
        if member.get('character_id') == dead_character_id:
            dead_member = member
            break
    
    if dead_member is None:
        await ctx.send(f"No dead member with ID `{dead_character_id}` found in the graveyard!")
        return
    
    if dead_member.get('user_id') != user_id:
        await ctx.send("The dead member doesn't belong to you!")
        return
    
    # Check if the member was killed by a rival (not crew war)
    killer_name = dead_member.get('killed_by', 'Unknown')
    
    if "Crew War" in killer_name:
        await ctx.send(f"**{dead_member['name']}** was killed in a crew war, not by a specific rival. Revenge is not available for crew war deaths.")
        return
    
    if "(Fatal Wounds)" in killer_name or "- Fatal Wounds" in killer_name:
        # Extract the actual killer name
        killer_name = killer_name.replace(" (Fatal Wounds)", "").replace(" - Fatal Wounds", "").strip()
        # Try to extract set name if present
        if "(" in killer_name and ")" in killer_name:
            killer_name = killer_name.split("(")[0].strip()
    
    # Try to extract rival gang/set from killer name
    rival_gang = "Unknown Gang"
    rival_set = "Unknown Set"
    if "(" in dead_member.get('killed_by', '') and ")" in dead_member.get('killed_by', ''):
        try:
            set_info = dead_member['killed_by'].split("(")[1].split(")")[0]
            rival_set = set_info
            # Try to match to known gangs
            for gang, info in LA_GANGS.items():
                if rival_set in info['sets']:
                    rival_gang = gang
                    break
        except:
            pass
    
    # Revenge intro embed
    intro_embed = discord.Embed(
        title="REVENGE MISSION",
        description=f"**{avenger_char['name']}** seeks vengeance for **{dead_member['name']}**\n\nThe killer, **{killer_name}**, has been located...",
        color=discord.Color.dark_red()
    )
    
    intro_embed.add_field(
        name=f"{avenger_char['name']} (AVENGER)",
        value=f"Kills: {avenger_char.get('kills', 0)}\nGang: {avenger_char.get('gang_affiliation', 'Unknown')}",
        inline=True
    )
    
    intro_embed.add_field(
        name=f"{killer_name} (KILLER)",
        value=f"Gang: {rival_gang}\nSet: {rival_set}",
        inline=True
    )
    
    intro_embed.add_field(
        name="Fallen Homie",
        value=f"{dead_member['name']} (Kills: {dead_member.get('kills', 0)})\nKilled on: {dead_member.get('death_date', 'Unknown')}",
        inline=False
    )
    
    intro_embed.set_footer(text="The revenge mission begins...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)
    
    # Simulate the revenge battle
    battle_result = simulate_battle()
    player_won = battle_result['player_won']
    
    # Calculate death chance
    death_chance = calculate_death_chance(player_won)
    
    # Roll for death
    death_roll = random.randint(1, 100)
    member_dies = death_roll <= death_chance
    
    # JAIL SYSTEM - Roll for jail if member survives and wins
    jail_roll = random.randint(1, 100)
    goes_to_jail = False
    jail_minutes = 0
    
    if not member_dies and player_won:
        # Increment kill count
        avenger_char['kills'] = avenger_char.get('kills', 0) + 1
        
        # 30% chance of getting caught
        jail_chance = 30
        goes_to_jail = jail_roll <= jail_chance
        
        if goes_to_jail:
            # Jail time = number of kills in minutes
            jail_minutes = avenger_char['kills']
    
    # Outcome embed
    if player_won:
        if member_dies:
            outcome_embed = discord.Embed(
                title="REVENGE COMPLETE - BUT AT A COST",
                description=f"**{avenger_char['name']}** eliminated **{killer_name}**, avenging **{dead_member['name']}**, but was fatally wounded",
                color=discord.Color.dark_red()
            )
            
            outcome_embed.add_field(
                name="Battle Result",
                value=f"Rolled: {battle_result['roll']} (50 or less to win)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Death Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Final Moments",
                value=f"{avenger_char['name']} avenged their fallen homie but paid the ultimate price",
                inline=False
            )
            
            dead_avenger = avenger_char.copy()
            dead_avenger['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_avenger['killed_by'] = f"{killer_name} (Revenge Mission - Fatal Wounds)"
            graveyard.append(dead_avenger)
            save_graveyard(graveyard)
            
            del characters[avenger_character_id]
            save_characters(characters)
            
        else:
            if goes_to_jail:
                outcome_embed = discord.Embed(
                    title="REVENGE COMPLETE - BUT LOCKED UP",
                    description=f"**{avenger_char['name']}** eliminated **{killer_name}**, avenging **{dead_member['name']}**, but got arrested!",
                    color=discord.Color.orange()
                )
            else:
                outcome_embed = discord.Embed(
                    title="REVENGE COMPLETE",
                    description=f"**{avenger_char['name']}** has eliminated **{killer_name}**, avenging **{dead_member['name']}**!",
                    color=discord.Color.green()
                )
            
            outcome_embed.add_field(
                name="Battle Result",
                value=f"Rolled: {battle_result['roll']} (50 or less to win)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Survival Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less) - SURVIVED",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Vengeance",
                value=f"{dead_member['name']} has been avenged! {killer_name} is dead!",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Kill Count",
                value=f"Total Kills: **{avenger_char['kills']}**",
                inline=False
            )
            
            if goes_to_jail:
                jail_until = datetime.now() + timedelta(minutes=jail_minutes)
                avenger_char['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
                
                outcome_embed.add_field(
                    name="ARRESTED",
                    value=f"Locked up for **{jail_minutes} minute(s)**",
                    inline=False
                )
            else:
                outcome_embed.add_field(
                    name="EVADED POLICE",
                    value=f"Got away clean!",
                    inline=False
                )
            
            characters[avenger_character_id] = avenger_char
            save_characters(characters)
            
    else:
        if member_dies:
            outcome_embed = discord.Embed(
                title="REVENGE FAILED - ELIMINATED",
                description=f"**{avenger_char['name']}** was eliminated by **{killer_name}**\n\n{dead_member['name']} remains unavenged...",
                color=discord.Color.dark_red()
            )
            
            outcome_embed.add_field(
                name="Battle Result",
                value=f"Rolled: {battle_result['roll']} (50 or less to win)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Death Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="RIP",
                value=f"{avenger_char['name']} fell to the same killer that got {dead_member['name']}",
                inline=False
            )
            
            dead_avenger = avenger_char.copy()
            dead_avenger['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_avenger['killed_by'] = f"{killer_name} (Failed Revenge Mission)"
            graveyard.append(dead_avenger)
            save_graveyard(graveyard)
            
            del characters[avenger_character_id]
            save_characters(characters)
            
        else:
            outcome_embed = discord.Embed(
                title="REVENGE FAILED - RETREAT",
                description=f"**{avenger_char['name']}** was defeated by **{killer_name}** but managed to escape\n\n{dead_member['name']} remains unavenged...",
                color=discord.Color.orange()
            )
            
            outcome_embed.add_field(
                name="Battle Result",
                value=f"Rolled: {battle_result['roll']} (50 or less to win)",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Survival Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less) - SURVIVED",
                inline=False
            )
            
            characters[avenger_character_id] = avenger_char
            save_characters(characters)
    
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
