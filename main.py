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
        member_name = f"{first_name} {last_name}"
        
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
    character_name = f"{first_name} {last_name}"
    
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
        "kill_list": [],
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
        description=f"**{character_name}**\nA new soldier has joined the streets",
        color=gang_color
    )
    
    embed.add_field(
        name="Owner",
        value=ctx.author.name,
        inline=True
    )
    
    embed.add_field(
        name="Member ID",
        value=f"`{character_id}`",
        inline=True
    )
    
    embed.add_field(
        name="\u200b",
        value="\u200b",
        inline=False
    )
    
    embed.add_field(
        name="Gang Affiliation",
        value=gang_affiliation,
        inline=True
    )
    
    embed.add_field(
        name="Set",
        value=set_name,
        inline=True
    )
    
    embed.set_footer(text=f"Use ?slide {character_id} to get active")
    
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
        title=f"{ctx.author.name}'s Gang Roster",
        description=f"Total active members: {len(user_members)}",
        color=discord.Color.dark_purple()
    )
    
    for member in user_members:
        # Check jail status
        in_jail = is_in_jail(member)
        jail_status = "LOCKED UP" if in_jail else "FREE"
        
        kills = member.get('kills', 0)
        
        member_info = f"ID: `{member['character_id']}`\n"
        member_info += f"Bodies: {kills}\n"
        member_info += f"Gang: {member.get('gang_affiliation', 'Unknown')}\n"
        member_info += f"Set: {member.get('set_name', 'Unknown')}\n"
        member_info += f"Status: {jail_status}"
        
        if in_jail:
            remaining = get_jail_time_remaining(member)
            if remaining:
                minutes = int(remaining.total_seconds() // 60)
                seconds = int(remaining.total_seconds() % 60)
                member_info += f"\nRelease: {minutes}m {seconds}s"
        
        embed.add_field(
            name=f"{member['name']}",
            value=member_info,
            inline=True
        )
    
    embed.set_footer(text="Commands: ?crew | ?slide <id> [id2] [id3]... | ?list <id>")
    
    await ctx.send(embed=embed)

# List command - Show kill list for a character
@bot.command(name='list')
async def list_kills(ctx, character_id: str = None):
    """Display the kill list for a gang member. Usage: ?list <character_id>"""
    
    if character_id is None:
        await ctx.send("Usage: `?list <character_id>`\nExample: `?list 123456`")
        return
    
    if character_id not in characters:
        await ctx.send(f"Gang member ID `{character_id}` not found!")
        return
    
    player_char = characters[character_id]
    user_id = str(ctx.author.id)
    
    if player_char.get('user_id') != user_id:
        await ctx.send("You don't own this gang member!")
        return
    
    # Get kill list
    kill_list = player_char.get('kill_list', [])
    total_kills = player_char.get('kills', 0)
    
    # Get gang color
    gang_color = LA_GANGS.get(player_char.get('gang_affiliation', 'Crips'), {}).get('color', discord.Color.dark_red())
    
    # Create embed
    embed = discord.Embed(
        title=f"KILL LIST - {player_char['name']}",
        description=f"Total bodies: {total_kills}\nGang: {player_char.get('gang_affiliation', 'Unknown')}\nSet: {player_char.get('set_name', 'Unknown')}",
        color=gang_color
    )
    
    if kill_list:
        # Sort by date (most recent first)
        sorted_kills = sorted(kill_list, key=lambda x: x.get('date', ''), reverse=True)
        
        # Display kills (limit to 20 fields due to Discord embed limits)
        display_limit = 20
        
        for idx, kill in enumerate(sorted_kills):
            if idx >= display_limit:
                remaining = len(sorted_kills) - display_limit
                embed.add_field(
                    name="\u200b",
                    value=f"+ {remaining} more bodies not shown",
                    inline=False
                )
                break
            
            victim_name = kill.get('victim_name', 'Unknown')
            victim_gang = kill.get('victim_gang', 'Unknown')
            victim_set = kill.get('victim_set', 'Unknown')
            kill_date = kill.get('date', 'Unknown')
            kill_type = kill.get('type', 'slide')
            
            # Format date nicely
            try:
                date_obj = datetime.strptime(kill_date, '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%b %d, %Y at %I:%M %p')
            except:
                formatted_date = kill_date
            
            field_value = f"{victim_name}\n"
            field_value += f"Gang: {victim_gang}\n"
            field_value += f"Set: {victim_set}\n"
            field_value += f"Date: {formatted_date}"
            
            if kill_type == "revenge":
                field_value += "\nType: REVENGE"
            
            embed.add_field(
                name=f"Body #{idx + 1}",
                value=field_value,
                inline=True
            )
    else:
        embed.add_field(
            name="Status",
            value=f"{player_char['name']} is clean, no bodies caught yet",
            inline=False
        )
    
    embed.set_footer(text="Bodies caught in the streets")
    
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
        title="CREW WAR INITIATED",
        description=f"{ctx.author.name}'s crew encounters a rival {rival_gang} crew in enemy territory",
        color=rival_gang_color
    )
    
    # Player crew info
    player_crew_text = ""
    for member in available_members:
        player_crew_text += f"{member['name']} (Bodies: {member.get('kills', 0)})\n"
    
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
            rival_crew_text += f"{rival_member['name']}\n"
        elif idx == display_limit:
            remaining = len(rival_crew) - display_limit
            rival_crew_text += f"... and {remaining} more members\n"
            break
    
    intro_embed.add_field(
        name=f"ENEMY CREW - {rival_set} ({len(rival_crew)} members)",
        value=rival_crew_text,
        inline=False
    )
    
    # Crew size comparison
    size_diff = len(available_members) - len(rival_crew)
    if size_diff > 0:
        size_advantage = f"Numbers advantage: +{size_diff} members"
    elif size_diff < 0:
        size_advantage = f"Outnumbered by: {abs(size_diff)} members"
    else:
        size_advantage = "Equal numbers on both sides"
    
    intro_embed.add_field(
        name="Battle Assessment",
        value=size_advantage,
        inline=False
    )
    
    intro_embed.set_footer(text="The confrontation is about to begin...")
    
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
            description=f"{ctx.author.name}'s crew successfully defeated the {rival_set} and secured the territory",
            color=discord.Color.green()
        )
    else:
        outcome_embed = discord.Embed(
            title="CREW WAR DEFEAT",
            description=f"{ctx.author.name}'s crew was overwhelmed by the {rival_set} and forced to retreat",
            color=discord.Color.red()
        )
    
    # Show casualties
    if casualties:
        casualty_text = ""
        for member in casualties:
            casualty_text += f"{member['name']} (Bodies: {member.get('kills', 0)})\n"
            
            # Add to graveyard
            dead_member = member.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_set} Crew War"
            graveyard.append(dead_member)
            
            # Delete member
            del characters[member['character_id']]
        
        outcome_embed.add_field(
            name=f"CASUALTIES ({len(casualties)} members lost)",
            value=casualty_text,
            inline=False
        )
        
        save_graveyard(graveyard)
        save_characters(characters)
    else:
        outcome_embed.add_field(
            name="NO CASUALTIES",
            value="All crew members made it out alive",
            inline=False
        )
    
    # Update survivors
    if survivors:
        survivor_text = ""
        for member in survivors:
            characters[member['character_id']] = member
            survivor_text += f"{member['name']} (Bodies: {member.get('kills', 0)})\n"
        
        outcome_embed.add_field(
            name=f"SURVIVORS ({len(survivors)} members)",
            value=survivor_text,
            inline=False
        )
        
        save_characters(characters)
    
    outcome_embed.set_footer(text="The streets remember everything")
    
    await ctx.send(embed=outcome_embed)

# Slide command - Battle against rival gang members with JAIL SYSTEM based on kills
@bot.command(name='slide')
async def slide_on_opps(ctx, *character_ids):
    """Slide on rival gang members. Usage: ?slide <character_id> [character_id2] [character_id3]..."""
    
    if not character_ids:
        await ctx.send("Usage: `?slide <character_id> [character_id2] [character_id3]...`\nExample: `?slide 123456` or `?slide 123456 789012 345678`")
        return
    
    user_id = str(ctx.author.id)
    
    # Validate all character IDs
    valid_members = []
    invalid_ids = []
    not_owned = []
    in_jail_members = []
    
    for character_id in character_ids:
        if character_id not in characters:
            invalid_ids.append(character_id)
            continue
        
        player_char = characters[character_id]
        
        if player_char.get('user_id') != user_id:
            not_owned.append(character_id)
            continue
        
        # Check if member is in jail
        if is_in_jail(player_char):
            remaining = get_jail_time_remaining(player_char)
            if remaining:
                minutes = int(remaining.total_seconds() // 60)
                seconds = int(remaining.total_seconds() % 60)
                in_jail_members.append(f"{player_char['name']} ({minutes}m {seconds}s)")
            continue
        
        valid_members.append(player_char)
    
    # Show errors if any
    if invalid_ids:
        await ctx.send(f"Invalid member IDs: {', '.join(invalid_ids)}")
        return
    
    if not_owned:
        await ctx.send(f"You don't own these members: {', '.join(not_owned)}")
        return
    
    if in_jail_members:
        await ctx.send(f"The following members are locked up:\n" + "\n".join(in_jail_members))
        return
    
    if not valid_members:
        await ctx.send("No valid members available to slide!")
        return
    
    # Now process each member's slide
    for idx, player_char in enumerate(valid_members):
        character_id = player_char['character_id']
        
        # Generate rival
        rival_first_name = random.choice(FIRST_NAMES)
        rival_last_name = random.choice(LAST_NAMES)
        rival_name = f"{rival_first_name} {rival_last_name}"
        
        # Generate rival gang affiliation (different from player if possible)
        available_gangs = [g for g in LA_GANGS.keys() if g != player_char.get('gang_affiliation')]
        if not available_gangs:
            available_gangs = list(LA_GANGS.keys())
        
        rival_gang = random.choice(available_gangs)
        rival_sets = LA_GANGS[rival_gang]['sets']
        rival_set = random.choice(rival_sets)
        
        # Battle intro embed
        intro_embed = discord.Embed(
            title=f"SLIDING ON OPPS ({idx + 1}/{len(valid_members)})",
            description=f"Your member has spotted an enemy in rival territory",
            color=discord.Color.orange()
        )
        
        intro_embed.add_field(
            name="YOUR MEMBER",
            value=f"{player_char['name']}\nBodies: {player_char.get('kills', 0)}\nGang: {player_char.get('gang_affiliation', 'Unknown')}\nSet: {player_char.get('set_name', 'Unknown')}",
            inline=True
        )
        
        intro_embed.add_field(
            name="ENEMY SPOTTED",
            value=f"{rival_name}\nGang: {rival_gang}\nSet: {rival_set}",
            inline=True
        )
        
        intro_embed.set_footer(text="The confrontation is about to go down...")
        
        await ctx.send(embed=intro_embed)
        await asyncio.sleep(2)
        
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
            
            # Add to kill list
            if 'kill_list' not in player_char:
                player_char['kill_list'] = []
            
            player_char['kill_list'].append({
                'victim_name': rival_name,
                'victim_gang': rival_gang,
                'victim_set': rival_set,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'slide'
            })
            
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
                    title="PYRRHIC VICTORY",
                    description=f"{player_char['name']} successfully eliminated {rival_name} but sustained fatal injuries in the process",
                    color=discord.Color.dark_red()
                )
                
                outcome_embed.add_field(
                    name="Final Outcome",
                    value=f"Despite winning the confrontation, {player_char['name']} succumbed to their wounds",
                    inline=False
                )
                
                outcome_embed.add_field(
                    name="Final Stats",
                    value=f"Body Count: {player_char.get('kills', 0)}\nStatus: DECEASED",
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
                        title="BODY CAUGHT - ARRESTED",
                        description=f"{player_char['name']} eliminated {rival_name} from the {rival_set} but was caught by law enforcement",
                        color=discord.Color.orange()
                    )
                else:
                    outcome_embed = discord.Embed(
                        title="BODY CAUGHT",
                        description=f"{player_char['name']} successfully eliminated {rival_name} from the {rival_set}",
                        color=discord.Color.green()
                    )
                
                outcome_embed.add_field(
                    name="Updated Stats",
                    value=f"Total Bodies: {player_char['kills']}",
                    inline=False
                )
                
                if goes_to_jail:
                    # Set jail time
                    jail_until = datetime.now() + timedelta(minutes=jail_minutes)
                    player_char['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
                    
                    outcome_embed.add_field(
                        name="ARREST STATUS",
                        value=f"Sentenced to {jail_minutes} minutes in county jail\nWill be released in {jail_minutes} minutes",
                        inline=False
                    )
                else:
                    outcome_embed.add_field(
                        name="POLICE STATUS",
                        value="Successfully evaded law enforcement and made it back safely",
                        inline=False
                    )
                
                characters[character_id] = player_char
                save_characters(characters)
                
        else:
            if member_dies:
                outcome_embed = discord.Embed(
                    title="CAUGHT SLIPPING",
                    description=f"{player_char['name']} was eliminated by {rival_name} from the {rival_set}",
                    color=discord.Color.dark_red()
                )
                
                outcome_embed.add_field(
                    name="Final Words",
                    value=f"{player_char['name']} was caught lacking deep in enemy territory and paid the ultimate price",
                    inline=False
                )
                
                outcome_embed.add_field(
                    name="Final Stats",
                    value=f"Body Count: {player_char.get('kills', 0)}\nStatus: DECEASED",
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
                    title="TOOK AN L - SURVIVED",
                    description=f"{player_char['name']} was defeated by {rival_name} but managed to escape alive",
                    color=discord.Color.orange()
                )
                
                outcome_embed.add_field(
                    name="Outcome",
                    value="Lost the confrontation but survived to fight another day",
                    inline=False
                )
                
                outcome_embed.add_field(
                    name="Current Stats",
                    value=f"Body Count: {player_char.get('kills', 0)}\nStatus: ALIVE",
                    inline=False
                )
                
                characters[character_id] = player_char
                save_characters(characters)
        
        outcome_embed.set_footer(text="The streets never forget")
        
        await ctx.send(embed=outcome_embed)
        
        # Add delay between slides if there are multiple members
        if idx < len(valid_members) - 1:
            await asyncio.sleep(3)

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
            await ctx.send(f"{avenger_char['name']} is currently locked up and will be released in {minutes}m {seconds}s")
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
        await ctx.send(f"{dead_member['name']} was killed in a crew war, not by a specific rival. Revenge is not available for crew war deaths.")
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
        description=f"Your member is on a mission to avenge a fallen homie",
        color=discord.Color.dark_red()
    )
    
    intro_embed.add_field(
        name="YOUR AVENGER",
        value=f"{avenger_char['name']}\nBodies: {avenger_char.get('kills', 0)}\nGang: {avenger_char.get('gang_affiliation', 'Unknown')}\nSet: {avenger_char.get('set_name', 'Unknown')}",
        inline=True
    )
    
    intro_embed.add_field(
        name="TARGET LOCATED",
        value=f"{killer_name}\nGang: {rival_gang}\nSet: {rival_set}",
        inline=True
    )
    
    intro_embed.add_field(
        name="\u200b",
        value="\u200b",
        inline=False
    )
    
    intro_embed.add_field(
        name="FALLEN HOMIE",
        value=f"{dead_member['name']}\nBodies: {dead_member.get('kills', 0)}\nDeath Date: {dead_member.get('death_date', 'Unknown')}",
        inline=False
    )
    
    intro_embed.set_footer(text="Blood calls for blood...")
    
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
        
        # Add to kill list
        if 'kill_list' not in avenger_char:
            avenger_char['kill_list'] = []
        
        avenger_char['kill_list'].append({
            'victim_name': killer_name,
            'victim_gang': rival_gang,
            'victim_set': rival_set,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'revenge'
        })
        
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
                title="REVENGE COMPLETE - ULTIMATE SACRIFICE",
                description=f"{avenger_char['name']} successfully eliminated {killer_name}, avenging {dead_member['name']}, but was fatally wounded in the process",
                color=discord.Color.dark_red()
            )
            
            outcome_embed.add_field(
                name="Final Moments",
                value=f"{avenger_char['name']} avenged their fallen homie but paid the ultimate price for vengeance",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Final Stats",
                value=f"Body Count: {avenger_char.get('kills', 0)}\nStatus: DECEASED",
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
                    title="REVENGE COMPLETE - ARRESTED",
                    description=f"{avenger_char['name']} successfully eliminated {killer_name}, avenging {dead_member['name']}, but was caught by law enforcement",
                    color=discord.Color.orange()
                )
            else:
                outcome_embed = discord.Embed(
                    title="REVENGE COMPLETE",
                    description=f"{avenger_char['name']} successfully eliminated {killer_name}, avenging {dead_member['name']}",
                    color=discord.Color.green()
                )
            
            outcome_embed.add_field(
                name="Vengeance Delivered",
                value=f"{dead_member['name']} has been avenged - {killer_name} is no longer a threat",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Updated Stats",
                value=f"Total Bodies: {avenger_char['kills']}",
                inline=False
            )
            
            if goes_to_jail:
                jail_until = datetime.now() + timedelta(minutes=jail_minutes)
                avenger_char['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
                
                outcome_embed.add_field(
                    name="ARREST STATUS",
                    value=f"Sentenced to {jail_minutes} minutes in county jail\nWill be released in {jail_minutes} minutes",
                    inline=False
                )
            else:
                outcome_embed.add_field(
                    name="POLICE STATUS",
                    value="Successfully evaded law enforcement after the revenge hit",
                    inline=False
                )
            
            characters[avenger_character_id] = avenger_char
            save_characters(characters)
            
    else:
        if member_dies:
            outcome_embed = discord.Embed(
                title="REVENGE FAILED - ELIMINATED",
                description=f"{avenger_char['name']} was eliminated by {killer_name} during the revenge attempt",
                color=discord.Color.dark_red()
            )
            
            outcome_embed.add_field(
                name="Failed Mission",
                value=f"{avenger_char['name']} fell to the same killer who took {dead_member['name']}\n{dead_member['name']} remains unavenged",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Final Stats",
                value=f"Body Count: {avenger_char.get('kills', 0)}\nStatus: DECEASED",
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
                description=f"{avenger_char['name']} was defeated by {killer_name} but managed to escape alive",
                color=discord.Color.orange()
            )
            
            outcome_embed.add_field(
                name="Failed Attempt",
                value=f"The revenge mission was unsuccessful but {avenger_char['name']} survived to try again another day\n{dead_member['name']} remains unavenged",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Current Stats",
                value=f"Body Count: {avenger_char.get('kills', 0)}\nStatus: ALIVE",
                inline=False
            )
            
            characters[avenger_character_id] = avenger_char
            save_characters(characters)
    
    outcome_embed.set_footer(text="The cycle of violence continues")
    
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
