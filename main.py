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

# Work jobs for earning money
WORK_JOBS = [
    {"name": "Drug Runner", "min": 100, "max": 300},
    {"name": "Car Booster", "min": 150, "max": 400},
    {"name": "Corner Boy", "min": 80, "max": 250},
    {"name": "Lookout", "min": 50, "max": 150},
    {"name": "Package Delivery", "min": 120, "max": 350},
    {"name": "Chop Shop Worker", "min": 200, "max": 500},
    {"name": "Fence Stolen Goods", "min": 180, "max": 450},
    {"name": "Street Hustler", "min": 90, "max": 280},
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

# Check if user is admin
def is_admin(ctx):
    """Check if user has administrator permissions"""
    return ctx.author.guild_permissions.administrator

# Dynamic cooldown - bypasses for admins
def dynamic_cooldown(rate, per):
    async def predicate(ctx):
        # If admin, skip cooldown entirely
        if is_admin(ctx):
            return True
        return True
    
    def decorator(func):
        # Apply cooldown normally
        cooldown_decorator = commands.cooldown(rate, per, commands.BucketType.user)
        func = cooldown_decorator(func)
        
        # Override the cooldown check for admins
        original_predicate = func._buckets._cooldown
        
        def new_cooldown(message):
            # Check if user is admin
            if message.author.guild_permissions.administrator:
                # Return a bucket that never triggers cooldown
                class NoCooldownBucket:
                    def update_rate_limit(self, current=None):
                        return None
                    def reset(self):
                        pass
                    def get_tokens(self, current=None):
                        return 0
                    def get_retry_after(self, current=None):
                        return 0
                return NoCooldownBucket()
            # Return normal cooldown bucket for non-admins
            return original_predicate(message)
        
        func._buckets._cooldown = new_cooldown
        return func
    
    return decorator

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

# Make command - Creates a gang member
@bot.command(name='make')
@dynamic_cooldown(1, 10)
async def make_character(ctx):
    """Generate a gang member with a random name"""
    
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

# View command - Display all alive and dead characters
@bot.command(name='view')
@dynamic_cooldown(1, 10)
async def view_all_characters(ctx):
    """View all characters (alive and dead) including AI-generated rivals"""
    
    # Load current data
    all_alive = load_characters()
    all_dead = load_graveyard()
    
    # Create main embed
    main_embed = discord.Embed(
        title="LA GANG DATABASE",
        description="Complete record of all gang members - living and deceased",
        color=discord.Color.gold()
    )
    
    # ALIVE CHARACTERS SECTION
    if all_alive:
        alive_list = list(all_alive.values())
        # Sort by kills (highest first)
        alive_list.sort(key=lambda x: x.get('kills', 0), reverse=True)
        
        alive_text = ""
        for member in alive_list[:10]:  # Show top 10 alive
            in_jail = is_in_jail(member)
            status = "LOCKED UP" if in_jail else "FREE"
            
            alive_text += f"**{member['name']}**\n"
            alive_text += f"ID: `{member['character_id']}`\n"
            alive_text += f"Bodies: {member.get('kills', 0)} | Money: ${member.get('money', 0):,}\n"
            alive_text += f"Gang: {member.get('gang_affiliation', 'Unknown')}\n"
            alive_text += f"Status: {status}\n\n"
        
        if len(alive_list) > 10:
            alive_text += f"*+ {len(alive_list) - 10} more members alive...*"
        
        main_embed.add_field(
            name=f"ALIVE MEMBERS ({len(alive_list)})",
            value=alive_text if alive_text else "No living members",
            inline=False
        )
    else:
        main_embed.add_field(
            name="ALIVE MEMBERS (0)",
            value="No living members found",
            inline=False
        )
    
    # DEAD CHARACTERS SECTION
    if all_dead:
        # Sort by death date (most recent first)
        dead_list = sorted(all_dead, key=lambda x: x.get('death_date', ''), reverse=True)
        
        dead_text = ""
        for member in dead_list[:10]:  # Show 10 most recent deaths
            death_date = member.get('death_date', 'Unknown')
            try:
                date_obj = datetime.strptime(death_date, '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%b %d, %Y')
            except:
                formatted_date = death_date
            
            killed_by = member.get('killed_by', 'Unknown')
            
            dead_text += f"**{member['name']}**\n"
            dead_text += f"ID: `{member['character_id']}`\n"
            dead_text += f"Final Bodies: {member.get('kills', 0)} | Money: ${member.get('money', 0):,}\n"
            dead_text += f"Gang: {member.get('gang_affiliation', 'Unknown')}\n"
            dead_text += f"Killed by: {killed_by}\n"
            dead_text += f"Date: {formatted_date}\n\n"
        
        if len(dead_list) > 10:
            dead_text += f"*+ {len(dead_list) - 10} more bodies in the graveyard...*"
        
        main_embed.add_field(
            name=f"DECEASED MEMBERS ({len(dead_list)})",
            value=dead_text if dead_text else "No deceased members",
            inline=False
        )
    else:
        main_embed.add_field(
            name="DECEASED MEMBERS (0)",
            value="No bodies in the graveyard yet",
            inline=False
        )
    
    # STATISTICS SECTION
    total_alive = len(all_alive)
    total_dead = len(all_dead)
    total_overall = total_alive + total_dead
    
    # Calculate top killer (alive)
    top_killer_alive = None
    if all_alive:
        alive_sorted = sorted(all_alive.values(), key=lambda x: x.get('kills', 0), reverse=True)
        if alive_sorted and alive_sorted[0].get('kills', 0) > 0:
            top_killer_alive = alive_sorted[0]
    
    stats_text = f"Total Characters: {total_overall}\n"
    stats_text += f"Living: {total_alive}\n"
    stats_text += f"Deceased: {total_dead}\n"
    
    if top_killer_alive:
        stats_text += f"\nMost Dangerous (Alive): **{top_killer_alive['name']}** ({top_killer_alive.get('kills', 0)} bodies)"
    
    main_embed.add_field(
        name="STATISTICS",
        value=stats_text,
        inline=False
    )
    
    main_embed.set_footer(text="The streets keep records of everything")
    
    await ctx.send(embed=main_embed)

# Show command - Display user's gang members
@bot.command(name='show')
@dynamic_cooldown(1, 10)
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
    
    embed.set_footer(text="Commands: ?slide <id> | ?rob <id> | ?list <id> | ?work <id>")
    
    await ctx.send(embed=embed)

# List command - Show kill list for a character
@bot.command(name='list')
@dynamic_cooldown(1, 10)
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

# Work command - Earn money through street jobs
@bot.command(name='work')
@dynamic_cooldown(1, 10)
async def work(ctx, character_id: str = None):
    """Work a street job to earn money. Usage: ?work <character_id>"""
    
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
    job = random.choice(WORK_JOBS)
    earnings = random.randint(job['min'], job['max'])
    
    # Add money to character
    player_char['money'] = player_char.get('money', 0) + earnings
    
    # Save character data
    characters[character_id] = player_char
    save_characters(characters)
    
    # Create embed
    embed = discord.Embed(
        title="WORK COMPLETE",
        description=f"{player_char['name']} completed a job on the streets",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="Job",
        value=job['name'],
        inline=True
    )
    
    embed.add_field(
        name="Earnings",
        value=f"${earnings:,}",
        inline=True
    )
    
    embed.add_field(
        name="\u200b",
        value="\u200b",
        inline=False
    )
    
    embed.add_field(
        name="Updated Balance",
        value=f"${player_char['money']:,}",
        inline=False
    )
    
    embed.set_footer(text="Hustle hard on these streets")
    
    await ctx.send(embed=embed)

# Rob command - Rob local stores for money
@bot.command(name='rob')
@dynamic_cooldown(1, 10)
async def rob_store(ctx, character_id: str = None):
    """Rob a local store for money. Usage: ?rob <character_id>"""
    
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

# Slide command - Battle against rival gang members with JAIL SYSTEM based on kills
@bot.command(name='slide')
@dynamic_cooldown(1, 10)
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
                    value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED",
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
@dynamic_cooldown(1, 10)
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
                value=f"Body Count: {avenger_char.get('kills', 0)}\nMoney: ${avenger_char.get('money', 0):,}\nStatus: DECEASED",
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
