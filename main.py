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
STATS_FILE = 'game_stats.json'

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

# Store types and their potential payouts
STORE_TYPES = {
    "Gas Station": {"min": 200, "max": 800, "risk": "low"},
    "Liquor Store": {"min": 300, "max": 1000, "risk": "low"},
    "Convenience Store": {"min": 250, "max": 900, "risk": "low"},
    "Jewelry Store": {"min": 2000, "max": 5000, "risk": "high"},
    "Bank": {"min": 5000, "max": 15000, "risk": "extreme"},
    "Check Cashing": {"min": 1000, "max": 3000, "risk": "medium"},
    "Pharmacy": {"min": 800, "max": 2500, "risk": "medium"},
    "Electronics Store": {"min": 1500, "max": 4000, "risk": "high"}
}

# Work jobs and their payouts
WORK_JOBS = {
    "McDonald's": {"min": 50, "max": 120, "description": "Flipping burgers at the local Mickey D's"},
    "Walmart": {"min": 60, "max": 140, "description": "Stocking shelves and dealing with customers"},
    "Car Wash": {"min": 70, "max": 150, "description": "Washing cars in the hood"},
    "Pizza Delivery": {"min": 80, "max": 180, "description": "Delivering pizzas around the city"},
    "Uber Driver": {"min": 90, "max": 200, "description": "Driving people around LA"},
    "Construction": {"min": 100, "max": 250, "description": "Working construction downtown"},
    "Warehouse": {"min": 110, "max": 220, "description": "Loading and unloading at the warehouse"},
    "Security Guard": {"min": 95, "max": 190, "description": "Working security at a local business"},
    "Mechanic": {"min": 120, "max": 280, "description": "Fixing cars at the local shop"},
    "Food Truck": {"min": 85, "max": 175, "description": "Serving food from a food truck"}
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

# Load game stats
def load_game_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {
        "total_characters_created": 0,
        "total_deaths": 0,
        "total_kills": 0,
        "total_money_earned": 0,
        "total_robberies": 0,
        "successful_robberies": 0,
        "failed_robberies": 0,
        "total_arrests": 0,
        "total_work_shifts": 0,
        "total_slides": 0,
        "total_revenge_missions": 0,
        "successful_revenge": 0,
        "failed_revenge": 0,
        "total_block_parties": 0,
        "block_party_shootings": 0,
        "block_party_deaths": 0,
        "gang_stats": {
            "Crips": {"kills": 0, "deaths": 0},
            "Bloods": {"kills": 0, "deaths": 0},
            "Sureños": {"kills": 0, "deaths": 0},
            "Norteños": {"kills": 0, "deaths": 0}
        },
        "ai_kills": [],
        "player_kills": [],
        "recent_deaths": []
    }

# Save game stats
def save_game_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=4)

# Update stats for character creation
def update_stats_character_created():
    stats = load_game_stats()
    stats['total_characters_created'] += 1
    save_game_stats(stats)

# Update stats for death
def update_stats_death(victim_name, victim_gang, killer_name, killer_gang, death_type, is_ai_kill=False):
    stats = load_game_stats()
    stats['total_deaths'] += 1
    
    # Update gang stats
    if victim_gang in stats['gang_stats']:
        stats['gang_stats'][victim_gang]['deaths'] += 1
    if killer_gang and killer_gang in stats['gang_stats']:
        stats['gang_stats'][killer_gang]['kills'] += 1
    
    # Track death
    death_record = {
        'victim': victim_name,
        'victim_gang': victim_gang,
        'killer': killer_name,
        'killer_gang': killer_gang,
        'type': death_type,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    stats['recent_deaths'].insert(0, death_record)
    if len(stats['recent_deaths']) > 50:
        stats['recent_deaths'] = stats['recent_deaths'][:50]
    
    # Track AI kills vs player kills
    if is_ai_kill:
        stats['ai_kills'].insert(0, death_record)
        if len(stats['ai_kills']) > 50:
            stats['ai_kills'] = stats['ai_kills'][:50]
    else:
        stats['player_kills'].insert(0, death_record)
        if len(stats['player_kills']) > 50:
            stats['player_kills'] = stats['player_kills'][:50]
    
    save_game_stats(stats)

# Update stats for kill
def update_stats_kill():
    stats = load_game_stats()
    stats['total_kills'] += 1
    save_game_stats(stats)

# Update stats for robbery
def update_stats_robbery(success, money_earned=0):
    stats = load_game_stats()
    stats['total_robberies'] += 1
    if success:
        stats['successful_robberies'] += 1
        stats['total_money_earned'] += money_earned
    else:
        stats['failed_robberies'] += 1
    save_game_stats(stats)

# Update stats for arrest
def update_stats_arrest():
    stats = load_game_stats()
    stats['total_arrests'] += 1
    save_game_stats(stats)

# Update stats for work
def update_stats_work(money_earned):
    stats = load_game_stats()
    stats['total_work_shifts'] += 1
    stats['total_money_earned'] += money_earned
    save_game_stats(stats)

# Update stats for slide
def update_stats_slide():
    stats = load_game_stats()
    stats['total_slides'] += 1
    save_game_stats(stats)

# Update stats for revenge
def update_stats_revenge(success):
    stats = load_game_stats()
    stats['total_revenge_missions'] += 1
    if success:
        stats['successful_revenge'] += 1
    else:
        stats['failed_revenge'] += 1
    save_game_stats(stats)

# Update stats for block party
def update_stats_block_party(shooting_occurred, death_occurred):
    stats = load_game_stats()
    stats['total_block_parties'] += 1
    if shooting_occurred:
        stats['block_party_shootings'] += 1
    if death_occurred:
        stats['block_party_deaths'] += 1
    save_game_stats(stats)

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

# Check if user is admin
def is_admin(ctx):
    """Check if user has administrator permissions"""
    return ctx.author.guild_permissions.administrator

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

# Error handler for cooldowns
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You're on cooldown. Try again in {error.retry_after:.1f} seconds.")
    elif isinstance(error, commands.CheckFailure):
        pass  # Ignore check failures (like DM blocking)
    else:
        # Print error for debugging
        print(f"Error: {error}")

# View command - Display all game statistics
@bot.command(name='view')
@commands.cooldown(1, 10, commands.BucketType.user)
async def view_stats(ctx):
    """Display comprehensive game statistics"""
    
    # Reset cooldown for admins
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)
    
    stats = load_game_stats()
    current_characters = load_characters()
    current_graveyard = load_graveyard()
    
    # Main stats embed
    main_embed = discord.Embed(
        title="📊 LA GANG BATTLE STATISTICS",
        description="Complete overview of all game activity",
        color=discord.Color.gold()
    )
    
    # General Stats
    main_embed.add_field(
        name="👥 Character Stats",
        value=f"Created: {stats['total_characters_created']}\nAlive: {len(current_characters)}\nDead: {len(current_graveyard)}",
        inline=True
    )
    
    main_embed.add_field(
        name="💀 Death Stats",
        value=f"Total Deaths: {stats['total_deaths']}\nTotal Kills: {stats['total_kills']}\nBlock Party Deaths: {stats['block_party_deaths']}",
        inline=True
    )
    
    main_embed.add_field(
        name="💰 Money Stats",
        value=f"Total Earned: ${stats['total_money_earned']:,}\nWork Shifts: {stats['total_work_shifts']}\nRobberies: {stats['total_robberies']}",
        inline=True
    )
    
    # Action Stats
    main_embed.add_field(
        name="🔫 Combat Stats",
        value=f"Slides: {stats['total_slides']}\nRevenge Missions: {stats['total_revenge_missions']}\nSuccessful Revenge: {stats['successful_revenge']}",
        inline=True
    )
    
    main_embed.add_field(
        name="🏪 Robbery Stats",
        value=f"Successful: {stats['successful_robberies']}\nFailed: {stats['failed_robberies']}\nSuccess Rate: {(stats['successful_robberies'] / max(stats['total_robberies'], 1) * 100):.1f}%",
        inline=True
    )
    
    main_embed.add_field(
        name="👮 Law Enforcement",
        value=f"Total Arrests: {stats['total_arrests']}\nCurrently Jailed: {sum(1 for c in current_characters.values() if is_in_jail(c))}",
        inline=True
    )
    
    # Block Party Stats
    main_embed.add_field(
        name="🎉 Block Party Stats",
        value=f"Total Parties: {stats['total_block_parties']}\nShootings: {stats['block_party_shootings']}\nDeaths: {stats['block_party_deaths']}",
        inline=True
    )
    
    # Gang War Stats
    gang_stats_text = ""
    for gang, data in stats['gang_stats'].items():
        gang_stats_text += f"**{gang}**\nKills: {data['kills']} | Deaths: {data['deaths']}\n"
    
    main_embed.add_field(
        name="🏴 Gang Statistics",
        value=gang_stats_text if gang_stats_text else "No gang activity yet",
        inline=False
    )
    
    await ctx.send(embed=main_embed)
    
    # Recent Deaths Embed
    if stats['recent_deaths']:
        deaths_embed = discord.Embed(
            title="💀 RECENT DEATHS (Last 10)",
            color=discord.Color.dark_red()
        )
        
        for idx, death in enumerate(stats['recent_deaths'][:10]):
            field_value = f"**Victim:** {death['victim']} ({death['victim_gang']})\n"
            field_value += f"**Killer:** {death['killer']}\n"
            if death['killer_gang']:
                field_value += f"**Gang:** {death['killer_gang']}\n"
            field_value += f"**Type:** {death['type']}\n"
            field_value += f"**Time:** {death['timestamp']}"
            
            deaths_embed.add_field(
                name=f"Death #{idx + 1}",
                value=field_value,
                inline=True
            )
        
        await ctx.send(embed=deaths_embed)
    
    # AI Kills vs Player Kills
    kills_embed = discord.Embed(
        title="🎯 KILL BREAKDOWN",
        color=discord.Color.purple()
    )
    
    kills_embed.add_field(
        name="AI Kills",
        value=f"Total: {len(stats['ai_kills'])}\nPercentage: {(len(stats['ai_kills']) / max(stats['total_deaths'], 1) * 100):.1f}%",
        inline=True
    )
    
    kills_embed.add_field(
        name="Player Kills",
        value=f"Total: {len(stats['player_kills'])}\nPercentage: {(len(stats['player_kills']) / max(stats['total_deaths'], 1) * 100):.1f}%",
        inline=True
    )
    
    await ctx.send(embed=kills_embed)
    
    # Recent AI Kills
    if stats['ai_kills']:
        ai_kills_embed = discord.Embed(
            title="🤖 RECENT AI KILLS (Last 5)",
            description="Deaths caused by AI-controlled rivals",
            color=discord.Color.orange()
        )
        
        for idx, kill in enumerate(stats['ai_kills'][:5]):
            field_value = f"**Victim:** {kill['victim']} ({kill['victim_gang']})\n"
            field_value += f"**AI Killer:** {kill['killer']}\n"
            if kill['killer_gang']:
                field_value += f"**Gang:** {kill['killer_gang']}\n"
            field_value += f"**Type:** {kill['type']}\n"
            field_value += f"**Time:** {kill['timestamp']}"
            
            ai_kills_embed.add_field(
                name=f"AI Kill #{idx + 1}",
                value=field_value,
                inline=True
            )
        
        await ctx.send(embed=ai_kills_embed)
    
    # Top Killers (from alive characters)
    top_killers = sorted(current_characters.values(), key=lambda x: x.get('kills', 0), reverse=True)[:5]
    
    if top_killers:
        killers_embed = discord.Embed(
            title="🔝 TOP KILLERS (Alive)",
            color=discord.Color.red()
        )
        
        for idx, killer in enumerate(top_killers):
            if killer.get('kills', 0) > 0:
                field_value = f"**Gang:** {killer.get('gang_affiliation', 'Unknown')}\n"
                field_value += f"**Set:** {killer.get('set_name', 'Unknown')}\n"
                field_value += f"**Bodies:** {killer.get('kills', 0)}\n"
                field_value += f"**Money:** ${killer.get('money', 0):,}"
                
                killers_embed.add_field(
                    name=f"#{idx + 1} - {killer['name']}",
                    value=field_value,
                    inline=True
                )
        
        if killers_embed.fields:
            await ctx.send(embed=killers_embed)
    
    # Richest Players (from alive characters)
    richest = sorted(current_characters.values(), key=lambda x: x.get('money', 0), reverse=True)[:5]
    
    if richest:
        money_embed = discord.Embed(
            title="💵 RICHEST PLAYERS (Alive)",
            color=discord.Color.green()
        )
        
        for idx, rich_player in enumerate(richest):
            if rich_player.get('money', 0) > 0:
                field_value = f"**Gang:** {rich_player.get('gang_affiliation', 'Unknown')}\n"
                field_value += f"**Set:** {rich_player.get('set_name', 'Unknown')}\n"
                field_value += f"**Money:** ${rich_player.get('money', 0):,}\n"
                field_value += f"**Bodies:** {rich_player.get('kills', 0)}"
                
                money_embed.add_field(
                    name=f"#{idx + 1} - {rich_player['name']}",
                    value=field_value,
                    inline=True
                )
        
        if money_embed.fields:
            await ctx.send(embed=money_embed)

# Make command - Creates a gang member
@bot.command(name='make')
@commands.cooldown(1, 10, commands.BucketType.user)
async def make_character(ctx):
    """Generate a gang member with a random name"""
    
    # Reset cooldown for admins
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)
    
    user_id = str(ctx.author.id)
    
    # Check if user is admin
    user_is_admin = is_admin(ctx)
    
    # If not admin, check if they already have a living character
    if not user_is_admin:
        user_members = [char for char in characters.values() if char.get('user_id') == user_id]
        if user_members:
            await ctx.send(f"You already have a gang member alive! You can only have one character at a time.\nUse `?show` to see your current member.")
            return
    
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
        "money": 0,
        "kill_list": [],
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save gang member
    characters[character_id] = character_data
    save_characters(characters)
    
    # Update stats
    update_stats_character_created()
    
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
@commands.cooldown(1, 10, commands.BucketType.user)
async def show_members(ctx):
    """Display all your gang members"""
    
    # Reset cooldown for admins
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)
    
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
        money = member.get('money', 0)
        
        member_info = f"ID: `{member['character_id']}`\n"
        member_info += f"Bodies: {kills}\n"
        member_info += f"Money: ${money:,}\n"
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
    
    embed.set_footer(text="Commands: ?slide <id> | ?rob <id> | ?work <id> | ?list <id>")
    
    await ctx.send(embed=embed)

# List command - Show kill list for a character
@bot.command(name='list')
@commands.cooldown(1, 10, commands.BucketType.user)
async def list_kills(ctx, character_id: str = None):
    """Display the kill list for a gang member. Usage: ?list <character_id>"""
    
    # Reset cooldown for admins
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)
    
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

# Work command - Work legitimate jobs for money
@bot.command(name='work')
@commands.cooldown(1, 10, commands.BucketType.user)
async def work_job(ctx, character_id: str = None):
    """Work a legitimate job to earn money. Usage: ?work <character_id>"""
    
    # Reset cooldown for admins
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)
    
    if character_id is None:
        await ctx.send("Usage: `?work <character_id>`\nExample: `?work 123456`")
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
            await ctx.send(f"{player_char['name']} is currently locked up and will be released in {minutes}m {seconds}s")
            return
    
    # Pick a random job
    job_name = random.choice(list(WORK_JOBS.keys()))
    job_info = WORK_JOBS[job_name]
    
    # Intro embed
    intro_embed = discord.Embed(
        title="CLOCKING IN",
        description=f"{player_char['name']} is heading to work",
        color=discord.Color.green()
    )
    
    intro_embed.add_field(
        name="Job",
        value=f"{job_name}\n{job_info['description']}",
        inline=False
    )
    
    intro_embed.add_field(
        name="Member",
        value=f"{player_char['name']}\nCurrent Money: ${player_char.get('money', 0):,}",
        inline=False
    )
    
    intro_embed.set_footer(text="Putting in work...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(2)
    
    # Calculate earnings
    earnings = random.randint(job_info['min'], job_info['max'])
    
    # Add money to character
    player_char['money'] = player_char.get('money', 0) + earnings
    
    # Update stats
    update_stats_work(earnings)
    
    # Work outcomes (flavor text)
    work_outcomes = [
        f"{player_char['name']} put in a solid shift and earned their pay",
        f"{player_char['name']} grinded through the day and got paid",
        f"{player_char['name']} clocked in, did the work, and clocked out",
        f"{player_char['name']} handled business and collected the check",
        f"{player_char['name']} stayed focused and earned that bread",
        f"{player_char['name']} kept it professional and got the bag"
    ]
    
    outcome_embed = discord.Embed(
        title="SHIFT COMPLETE",
        description=random.choice(work_outcomes),
        color=discord.Color.green()
    )
    
    outcome_embed.add_field(
        name="Job Completed",
        value=job_name,
        inline=True
    )
    
    outcome_embed.add_field(
        name="Earnings",
        value=f"${earnings:,}",
        inline=True
    )
    
    outcome_embed.add_field(
        name="\u200b",
        value="\u200b",
        inline=False
    )
    
    outcome_embed.add_field(
        name="Updated Balance",
        value=f"${player_char['money']:,}",
        inline=False
    )
    
    outcome_embed.set_footer(text="Honest work pays off")
    
    # Save character data
    characters[character_id] = player_char
    save_characters(characters)
    
    await ctx.send(embed=outcome_embed)

# Rob command - Rob local stores for money
@bot.command(name='rob')
@commands.cooldown(1, 10, commands.BucketType.user)
async def rob_store(ctx, character_id: str = None):
    """Rob a local store for money. Usage: ?rob <character_id>"""
    
    # Reset cooldown for admins
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)
    
    if character_id is None:
        await ctx.send("Usage: `?rob <character_id>`\nExample: `?rob 123456`")
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
            await ctx.send(f"{player_char['name']} is currently locked up and will be released in {minutes}m {seconds}s")
            return
    
    # Pick a random store type
    store_type = random.choice(list(STORE_TYPES.keys()))
    store_info = STORE_TYPES[store_type]
    
    # Generate random store name
    store_name = f"{random.choice(['Main St', 'Broadway', 'Central Ave', 'Sunset Blvd', 'Crenshaw', 'Vermont Ave'])} {store_type}"
    
    # Intro embed
    intro_embed = discord.Embed(
        title="ROBBERY IN PROGRESS",
        description=f"{player_char['name']} is attempting to rob {store_name}",
        color=discord.Color.gold()
    )
    
    intro_embed.add_field(
        name="Target",
        value=f"{store_name}\nRisk Level: {store_info['risk'].upper()}",
        inline=True
    )
    
    intro_embed.add_field(
        name="Member",
        value=f"{player_char['name']}\nMoney: ${player_char.get('money', 0):,}",
        inline=True
    )
    
    intro_embed.set_footer(text="The heist is underway...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)
    
    # Determine success of robbery (70% success rate)
    robbery_roll = random.randint(1, 100)
    robbery_success = robbery_roll <= 70
    
    # Calculate money stolen if successful
    money_stolen = 0
    if robbery_success:
        money_stolen = random.randint(store_info['min'], store_info['max'])
    
    # Police response system
    caught_by_police = False
    jail_time = 0
    witnesses_present = False
    
    if robbery_success:
        # Base police chance depends on store risk
        if store_info['risk'] == "low":
            police_chance = 20
        elif store_info['risk'] == "medium":
            police_chance = 35
        elif store_info['risk'] == "high":
            police_chance = 50
        else:  # extreme
            police_chance = 70
        
        police_roll = random.randint(1, 100)
        caught_by_police = police_roll <= police_chance
        
        if caught_by_police:
            # Check for witnesses (30% chance)
            witness_roll = random.randint(1, 100)
            witnesses_present = witness_roll <= 30
            
            if witnesses_present:
                # 20-30 minutes with witnesses
                jail_time = random.randint(20, 30)
            else:
                # 5-10 minutes without witnesses
                jail_time = random.randint(5, 10)
            
            # Update stats for arrest
            update_stats_arrest()
    
    # Update robbery stats
    update_stats_robbery(robbery_success and not caught_by_police, money_stolen if not caught_by_police else 0)
    
    # Outcome embed
    if robbery_success:
        if caught_by_police:
            outcome_embed = discord.Embed(
                title="ROBBERY SUCCESSFUL - BUT ARRESTED",
                description=f"{player_char['name']} successfully robbed {store_name} but was caught by police",
                color=discord.Color.orange()
            )
            
            outcome_embed.add_field(
                name="Money Stolen",
                value=f"${money_stolen:,}",
                inline=True
            )
            
            outcome_embed.add_field(
                name="Police Response",
                value="CAUGHT",
                inline=True
            )
            
            outcome_embed.add_field(
                name="\u200b",
                value="\u200b",
                inline=False
            )
            
            if witnesses_present:
                outcome_embed.add_field(
                    name="WITNESSES PRESENT",
                    value=f"Multiple witnesses at the scene identified {player_char['name']}\nSentence increased due to evidence",
                    inline=False
                )
            
            outcome_embed.add_field(
                name="ARREST STATUS",
                value=f"Sentenced to {jail_time} minutes in county jail\nMoney confiscated by police",
                inline=False
            )
            
            # Set jail time
            jail_until = datetime.now() + timedelta(minutes=jail_time)
            player_char['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
            
            # Don't add money since it was confiscated
            
        else:
            outcome_embed = discord.Embed(
                title="ROBBERY SUCCESSFUL",
                description=f"{player_char['name']} successfully robbed {store_name} and escaped",
                color=discord.Color.green()
            )
            
            outcome_embed.add_field(
                name="Money Stolen",
                value=f"${money_stolen:,}",
                inline=True
            )
            
            outcome_embed.add_field(
                name="Police Response",
                value="ESCAPED",
                inline=True
            )
            
            outcome_embed.add_field(
                name="\u200b",
                value="\u200b",
                inline=False
            )
            
            # Add money to character
            player_char['money'] = player_char.get('money', 0) + money_stolen
            
            outcome_embed.add_field(
                name="CLEAN GETAWAY",
                value=f"{player_char['name']} successfully evaded police and made it back to the hood",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Updated Balance",
                value=f"${player_char['money']:,}",
                inline=False
            )
    else:
        outcome_embed = discord.Embed(
            title="ROBBERY FAILED",
            description=f"{player_char['name']} failed to rob {store_name}",
            color=discord.Color.red()
        )
        
        outcome_embed.add_field(
            name="Result",
            value="The robbery went wrong and the target was alerted before anything could be taken",
            inline=False
        )
        
        outcome_embed.add_field(
            name="Money Stolen",
            value="$0",
            inline=True
        )
        
        outcome_embed.add_field(
            name="Status",
            value="Fled the scene empty-handed",
            inline=True
        )
    
    outcome_embed.set_footer(text="Crime doesn't always pay")
    
    # Save character data
    characters[character_id] = player_char
    save_characters(characters)
    
    await ctx.send(embed=outcome_embed)

# Block command - Throw a block party with chance of rival shootup
@bot.command(name='block')
@commands.cooldown(1, 10, commands.BucketType.user)
async def block_party(ctx, character_id: str = None):
    """Throw a block party in the hood. Usage: ?block <character_id>"""
    
    # Reset cooldown for admins
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)
    
    if character_id is None:
        await ctx.send("Usage: `?block <character_id>`\nExample: `?block 123456`")
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
            await ctx.send(f"{player_char['name']} is currently locked up and will be released in {minutes}m {seconds}s")
            return
    
    # Get character's gang info
    char_gang = player_char.get('gang_affiliation', 'Unknown')
    char_set = player_char.get('set_name', 'Unknown')
    gang_color = LA_GANGS.get(char_gang, {}).get('color', discord.Color.purple())
    
    # Intro embed
    intro_embed = discord.Embed(
        title="BLOCK PARTY STARTING",
        description=f"{player_char['name']} is throwing a block party in {char_set} territory",
        color=gang_color
    )
    
    intro_embed.add_field(
        name="Host",
        value=f"{player_char['name']}",
        inline=True
    )
    
    intro_embed.add_field(
        name="Location",
        value=f"{char_set} turf",
        inline=True
    )
    
    intro_embed.add_field(
        name="\u200b",
        value="\u200b",
        inline=False
    )
    
    intro_embed.add_field(
        name="The Scene",
        value="Music bumping, homies gathered, BBQ going, everyone having a good time in the hood",
        inline=False
    )
    
    intro_embed.set_footer(text="The party is live...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)
    
    # 35% chance of rival gang showing up
    rival_roll = random.randint(1, 100)
    rival_shows_up = rival_roll <= 35
    
    if not rival_shows_up:
        # Peaceful party
        outcome_embed = discord.Embed(
            title="BLOCK PARTY SUCCESS",
            description=f"The block party was a success! Everyone had a good time and no drama went down",
            color=discord.Color.green()
        )
        
        outcome_embed.add_field(
            name="Party Status",
            value="Everything stayed peaceful in the hood tonight",
            inline=False
        )
        
        outcome_embed.add_field(
            name=f"{player_char['name']}",
            value="Threw a legendary block party that the hood will remember",
            inline=False
        )
        
        outcome_embed.set_footer(text="Good vibes only")
        
        # Update stats
        update_stats_block_party(False, False)
        
        await ctx.send(embed=outcome_embed)
    else:
        # Rival gang drives by
        # Generate rival gang (different from player's gang)
        available_gangs = [g for g in LA_GANGS.keys() if g != char_gang]
        if not available_gangs:
            available_gangs = list(LA_GANGS.keys())
        
        rival_gang = random.choice(available_gangs)
        rival_sets = LA_GANGS[rival_gang]['sets']
        rival_set = random.choice(rival_sets)
        
        # Generate 2-4 rival shooters
        num_shooters = random.randint(2, 4)
        rival_names = []
        for _ in range(num_shooters):
            rival_first = random.choice(FIRST_NAMES)
            rival_last = random.choice(LAST_NAMES)
            rival_names.append(f"{rival_first} {rival_last}")
        
        # Drive by alert
        driveby_embed = discord.Embed(
            title="RIVAL GANG ALERT",
            description=f"A car full of {rival_set} members just rolled up on the block party!",
            color=discord.Color.red()
        )
        
        driveby_embed.add_field(
            name="Rival Gang",
            value=f"{rival_gang}",
            inline=True
        )
        
        driveby_embed.add_field(
            name="Set",
            value=f"{rival_set}",
            inline=True
        )
        
        driveby_embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=False
        )
        
        driveby_embed.add_field(
            name="SHOOTERS SPOTTED",
            value="\n".join(rival_names),
            inline=False
        )
        
        driveby_embed.set_footer(text="Shots about to be fired...")
        
        await ctx.send(embed=driveby_embed)
        await asyncio.sleep(3)
        
        # SHOOTING STARTS
        shooting_embed = discord.Embed(
            title="SHOTS FIRED!",
            description=f"The {rival_set} members opened fire on the block party!",
            color=discord.Color.dark_red()
        )
        
        shooting_embed.add_field(
            name="Drive-By Shooting",
            value="Bullets flying everywhere, people running for cover, chaos in the streets",
            inline=False
        )
        
        await ctx.send(embed=shooting_embed)
        await asyncio.sleep(3)
        
        # 40% chance player gets hit by a bullet
        bullet_roll = random.randint(1, 100)
        player_hit = bullet_roll <= 40
        
        if player_hit:
            # Player caught a bullet and dies
            death_embed = discord.Embed(
                title="CAUGHT BY A BULLET",
                description=f"{player_char['name']} was hit during the drive-by shooting",
                color=discord.Color.dark_red()
            )
            
            death_embed.add_field(
                name="Fatal Outcome",
                value=f"{player_char['name']} caught a stray bullet during the shootout and didn't make it",
                inline=False
            )
            
            death_embed.add_field(
                name="Final Stats",
                value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED",
                inline=False
            )
            
            # Update stats - AI kill
            update_stats_death(
                player_char['name'],
                char_gang,
                f"{rival_set} Drive-By Shooting",
                rival_gang,
                "block_party",
                is_ai_kill=True
            )
            update_stats_block_party(True, True)
            
            # Add to graveyard
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_set} Drive-By Shooting (Block Party)"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            
            # Remove from characters
            del characters[character_id]
            save_characters(characters)
            
            death_embed.set_footer(text="Wrong place, wrong time")
            
            await ctx.send(embed=death_embed)
        else:
            # Player survives but police show up
            survive_embed = discord.Embed(
                title="SURVIVED THE SHOOTING",
                description=f"{player_char['name']} managed to avoid the bullets and survive the drive-by",
                color=discord.Color.orange()
            )
            
            survive_embed.add_field(
                name="Close Call",
                value=f"{player_char['name']} hit the ground and avoided getting hit",
                inline=False
            )
            
            # Update stats
            update_stats_block_party(True, False)
            
            await ctx.send(embed=survive_embed)
            await asyncio.sleep(2)
            
            # Police response (60% chance)
            police_roll = random.randint(1, 100)
            police_show = police_roll <= 60
            
            if police_show:
                police_embed = discord.Embed(
                    title="POLICE ARRIVAL",
                    description="LAPD rolled up on the scene after the shooting",
                    color=discord.Color.blue()
                )
                
                police_embed.add_field(
                    name="Police Response",
                    value="Multiple units arrived on scene, investigating the shooting",
                    inline=False
                )
                
                police_embed.add_field(
                    name=f"{player_char['name']} Status",
                    value="Questioned by police but not arrested - no jail time for being a victim",
                    inline=False
                )
                
                police_embed.set_footer(text="Survived to see another day")
                
                await ctx.send(embed=police_embed)
            else:
                final_embed = discord.Embed(
                    title="ESCAPED CLEAN",
                    description=f"{player_char['name']} survived the shooting and got away before police arrived",
                    color=discord.Color.green()
                )
                
                final_embed.add_field(
                    name="Status",
                    value="Made it out alive, no police involvement",
                    inline=False
                )
                
                final_embed.set_footer(text="Lucky to be alive")
                
                await ctx.send(embed=final_embed)
            
            # Save character (no changes needed, just survived)
            characters[character_id] = player_char
            save_characters(characters)

# Slide command - Battle against rival gang members with JAIL SYSTEM based on kills
@bot.command(name='slide')
@commands.cooldown(1, 10, commands.BucketType.user)
async def slide_on_opps(ctx, *character_ids):
    """Slide on rival gang members. Usage: ?slide <character_id> [character_id2] [character_id3]..."""
    
    # Reset cooldown for admins
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)
    
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
        
        # Update slide stats
        update_stats_slide()
        
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
            
            # Update kill stats
            update_stats_kill()
            
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
            
            # Record this as a player kill (not AI)
            update_stats_death(
                rival_name,
                rival_gang,
                player_char['name'],
                player_char.get('gang_affiliation'),
                'slide',
                is_ai_kill=False
            )
            
            # 30% chance of getting caught after killing someone
            jail_chance = 30
            goes_to_jail = jail_roll <= jail_chance
            
            if goes_to_jail:
                # Jail time = number of kills in minutes
                jail_minutes = player_char['kills']
                update_stats_arrest()
        
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
                    value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED",
                    inline=False
                )
                
                # Update death stats - AI kill
                update_stats_death(
                    player_char['name'],
                    player_char.get('gang_affiliation'),
                    f"{rival_name} ({rival_set})",
                    rival_gang,
                    'slide_fatal_wounds',
                    is_ai_kill=True
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
                    value=f"Total Bodies: {player_char['kills']}\nMoney: ${player_char.get('money', 0):,}",
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
                    value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED",
                    inline=False
                )
                
                # Update death stats - AI kill
                update_stats_death(
                    player_char['name'],
                    player_char.get('gang_affiliation'),
                    f"{rival_name} ({rival_set})",
                    rival_gang,
                    'slide_loss',
                    is_ai_kill=True
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
                    value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: ALIVE",
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
@commands.cooldown(1, 10, commands.BucketType.user)
async def revenge_battle(ctx, dead_character_id: str = None, avenger_character_id: str = None):
    """Take revenge on the rival that killed your gang member. Usage: ?revenge <dead_member_id> <avenger_member_id>"""
    
    # Reset cooldown for admins
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)
    
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
        
        # Update kill stats
        update_stats_kill()
        
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
        
        # Record as player kill
        update_stats_death(
            killer_name,
            rival_gang,
            avenger_char['name'],
            avenger_char.get('gang_affiliation'),
            'revenge',
            is_ai_kill=False
        )
        
        # 30% chance of getting caught
        jail_chance = 30
        goes_to_jail = jail_roll <= jail_chance
        
        if goes_to_jail:
            # Jail time = number of kills in minutes
            jail_minutes = avenger_char['kills']
            update_stats_arrest()
    
    # Update revenge stats
    update_stats_revenge(player_won and not member_dies)
    
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
                value=f"Body Count: {avenger_char.get('kills', 0)}\nMoney: ${avenger_char.get('money', 0):,}\nStatus: DECEASED",
                inline=False
            )
            
            # Update death stats - AI kill
            update_stats_death(
                avenger_char['name'],
                avenger_char.get('gang_affiliation'),
                f"{killer_name}",
                rival_gang,
                'revenge_fatal_wounds',
                is_ai_kill=True
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
                value=f"Total Bodies: {avenger_char['kills']}\nMoney: ${avenger_char.get('money', 0):,}",
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
                value=f"Body Count: {avenger_char.get('kills', 0)}\nMoney: ${avenger_char.get('money', 0):,}\nStatus: DECEASED",
                inline=False
            )
            
            # Update death stats - AI kill
            update_stats_death(
                avenger_char['name'],
                avenger_char.get('gang_affiliation'),
                f"{killer_name}",
                rival_gang,
                'revenge_failed',
                is_ai_kill=True
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
                value=f"Body Count: {avenger_char.get('kills', 0)}\nMoney: ${avenger_char.get('money', 0):,}\nStatus: ALIVE",
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
