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
        "color": discord.Color.from_rgb(0, 128, 255),  # Blue
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

# Street Backgrounds/Origins
ORIGINS = [
    "grew up in the projects and joined the gang at 13",
    "lost family to gang violence and sought revenge through the streets",
    "was jumped into the set after proving themselves in a beatdown",
    "inherited the gang life from their OG father",
    "started tagging walls and earned respect through graffiti wars",
    "protected their block from rival gangs since childhood",
    "served time in county jail and came out with more connections",
    "moved from another city and had to earn their stripes",
    "was born into the gang life, third generation banger",
    "started selling on the corner and worked their way up",
    "got jumped in after their brother was killed by rivals",
    "earned respect by handling business no one else would",
    "came up robbing rival gang members in enemy territory",
    "was recruited after showing loyalty during a raid",
    "survived a drive-by and became a street legend",
    "built their reputation moving weight for the OGs",
    "earned their spot after doing dirt for the homies",
    "started banging after their hood got disrespected",
    "proved themselves in a shootout with rival gangs",
    "was born and raised in the heart of the hood"
]

# Gang Member Personalities
PERSONALITIES = [
    "ruthless and cold-blooded, shows no mercy to opps",
    "loyal to the set, would die for their homies",
    "hot-headed and unpredictable, quick to blast",
    "calculated and strategic, thinks before moving",
    "paranoid from years on the streets, trusts no one",
    "savage and fearless, first one to slide on enemies",
    "respected OG who commands authority",
    "young and reckless, trying to prove themselves",
    "quiet but deadly, lets their actions speak",
    "manipulative and cunning, plays chess not checkers",
    "protective of their hood and family",
    "ambitious and power-hungry, wants to run the set",
    "isolated and solo, doesn't roll with the crew much",
    "charismatic and influential, natural born leader",
    "war-ready soldier, always strapped and prepared",
    "mysterious and low-key, keeps things tight",
    "rebellious and defiant, doesn't follow orders well",
    "seasoned veteran who's seen it all",
    "troubled and conflicted about the gang life",
    "stone-cold killer with bodies on their name"
]

# Street Skills/Reputation
SKILLS_LORE = [
    "mastered the art of moving weight without getting caught",
    "earned a reputation for accuracy in drive-bys",
    "learned to evade police through years on the run",
    "gained respect through hand-to-hand combat skills",
    "developed a network of connections across the city",
    "became known for strategic planning of gang operations",
    "built an untouchable reputation through violence",
    "learned the streets from the best OGs in the game",
    "survived multiple attempts on their life",
    "gained influence through fear and intimidation",
    "mastered the code of the streets and gang politics",
    "developed street smarts through years of hustling",
    "earned stripes through loyalty during investigations",
    "became known for their ability to get money",
    "built respect through years of putting in work",
    "gained a reputation for keeping it real with the homies",
    "learned to navigate gang wars and truces",
    "became a go-to person for handling problems",
    "developed survival instincts from constant danger",
    "earned their name through countless street battles"
]

# Gang Member Goals/Motivations
GOALS = [
    "trying to make it out the hood and go legit",
    "seeking revenge for fallen homies",
    "trying to become an OG and lead the set",
    "protecting younger family members from the streets",
    "building a drug empire in their territory",
    "eliminating rival gang members from their hood",
    "avenging the death of their brother or sister",
    "trying to maintain control of their block",
    "seeking to expand their gang's territory",
    "looking for a way out but too deep in the game",
    "trying to end their life in the streets",
    "seeking to become the most feared in the city",
    "protecting their family's legacy in the gang",
    "hunting down snitches and informants",
    "searching for the person who killed their homie",
    "trying to unite rival sets for peace",
    "seeking redemption for past sins",
    "building respect through any means necessary",
    "trying to create generational wealth from the streets",
    "seeking to survive another day in the concrete jungle"
]

# Weaknesses/Vulnerabilities
WEAKNESSES = [
    "has an outstanding warrant and avoids police",
    "is being watched by gang task force detectives",
    "has family members being threatened by rivals",
    "is addicted to the lifestyle and can't leave",
    "owes money to dangerous people",
    "is on parole and one mistake means life",
    "has PTSD from years of violence",
    "is weakened by old gunshot wounds",
    "is being hunted by multiple rival gangs",
    "is under federal investigation",
    "has lost trust in some of their own homies",
    "is targeted due to their high-profile reputation",
    "can't enter certain areas without getting killed",
    "is vulnerable due to predictable routines",
    "is compromised by personal relationships",
    "is weakened by substance abuse",
    "is haunted by the people they've killed",
    "is vulnerable during visits to incarcerated homies",
    "is at risk due to social media exposure",
    "is weakened by loyalty to unreliable allies"
]

# Generate detailed gang member backstory
def generate_gang_lore(member_name, power_level, gang_affiliation, set_name):
    """Generate detailed backstory for a gang member"""
    
    origin = random.choice(ORIGINS)
    personality = random.choice(PERSONALITIES)
    skill_source = random.choice(SKILLS_LORE)
    goal = random.choice(GOALS)
    weakness = random.choice(WEAKNESSES)
    
    # Generate age and experience based on power
    if power_level <= 400:
        age = random.randint(16, 22)
        experience = "young hustler trying to earn stripes"
    elif power_level <= 1000:
        age = random.randint(23, 30)
        experience = "seasoned banger with respect on the streets"
    elif power_level <= 1600:
        age = random.randint(31, 45)
        experience = "OG with years of experience"
    else:
        age = random.randint(46, 65)
        experience = "legendary shot-caller"
    
    # Generate body count
    bodies = random.randint(0, 15)
    
    # Generate territory control
    gang_info = LA_GANGS.get(gang_affiliation, {})
    territories = gang_info.get('territory', ["Unknown Territory"])
    territory = random.choice(territories)
    
    # Generate street reputation trait
    traits = [
        "known for never backing down from a fight",
        "has a sixth sense for detecting undercover cops",
        "can navigate the entire city blindfolded",
        "never leaves witnesses behind",
        "has informants in rival gangs",
        "is untouchable due to political connections",
        "can disappear without a trace when needed",
        "has a reputation that precedes them everywhere",
        "can read people's intentions instantly",
        "never gets caught lacking or slipping",
        "controls drug distribution in their area",
        "has bodies buried that no one knows about",
        "can manipulate gang politics masterfully",
        "survived multiple hits from professional killers",
        "is respected even by rival gang members"
    ]
    special_trait = random.choice(traits)
    
    lore_data = {
        "origin": origin,
        "age": age,
        "experience": experience,
        "personality": personality,
        "skill_source": skill_source,
        "goal": goal,
        "weakness": weakness,
        "bodies": bodies,
        "territory": territory,
        "special_trait": special_trait,
        "gang_affiliation": gang_affiliation,
        "set_name": set_name,
        "lore_revealed": False
    }
    
    return lore_data

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

# Generate completely random street power (10-2000)
def generate_street_power():
    """Generate completely random street power from 10 to 2000"""
    
    roll = random.randint(1, 100)
    
    if roll <= 50:
        return random.randint(10, 800)
    elif roll <= 75:
        return random.randint(801, 1400)
    elif roll <= 90:
        return random.randint(1401, 1800)
    else:
        return random.randint(1801, 2000)

# Generate completely random gang member power (10-2000)
def generate_random_member_power():
    """Generate completely random power for new gang members"""
    
    roll = random.randint(1, 100)
    
    if roll <= 45:
        return random.randint(10, 400)
    elif roll <= 75:
        return random.randint(401, 1000)
    elif roll <= 90:
        return random.randint(1001, 1600)
    else:
        return random.randint(1601, 2000)

# Calculate death chance based on power difference and outcome
def calculate_death_chance(player_power, enemy_power, player_won):
    """Calculate death chance - higher when losing to stronger opponents"""
    
    if player_won:
        base_chance = 5
        power_diff = player_power - enemy_power
        
        if power_diff < 100:
            base_chance = 15
    else:
        base_chance = 35
        power_diff = enemy_power - player_power
        
        power_multiplier = power_diff / 200
        base_chance += power_multiplier
    
    death_chance = max(5, min(80, base_chance))
    
    return int(death_chance)

# Calculate crew death chance (lower than solo)
def calculate_crew_death_chance(player_won):
    """Calculate death chance for crew battles - lower risk due to backup"""
    
    if player_won:
        return random.randint(2, 8)
    else:
        return random.randint(15, 35)

# Simulate instant street battle with lore bonus
def simulate_battle(player_name, player_power, enemy_name, enemy_power, lore_revealed=False):
    """Simulate an instant street battle"""
    
    # Apply lore bonus if revealed
    effective_player_power = player_power
    if lore_revealed:
        # Street knowledge gives tactical advantage
        lore_bonus_multiplier = random.uniform(1.05, 1.15)  # 5-15% power boost
        effective_player_power = int(player_power * lore_bonus_multiplier)
    
    # Calculate win probability based on power
    power_diff = effective_player_power - enemy_power
    
    # Base 50% chance, adjusted by power difference
    win_probability = 50 + (power_diff / 20)
    
    # Cap between 5% and 95%
    win_probability = max(5, min(95, win_probability))
    
    # Roll for winner
    roll = random.randint(1, 100)
    player_won = roll <= win_probability
    
    return {
        "player_won": player_won,
        "win_probability": int(win_probability),
        "roll": roll,
        "lore_bonus_applied": lore_revealed,
        "effective_power": effective_player_power if lore_revealed else player_power
    }

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
        member_power = generate_street_power()
        
        rival_crew.append({
            "name": member_name,
            "power": member_power,
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

# Make command - Creates a gang member with RANDOM power (10-2000)
@bot.command(name='make')
async def make_character(ctx):
    """Generate a gang member with a random name and street power"""
    
    user_id = str(ctx.author.id)
    
    # Generate random gang member name
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    # Add street nickname
    nickname = last_name[:3].upper()
    character_name = f"{first_name} '{nickname}' {last_name}"
    
    # Generate unique character ID
    character_id = generate_unique_id()
    
    # Generate COMPLETELY RANDOM power level (10 to 2000)
    power_level = generate_random_member_power()
    
    # Randomly assign gang affiliation
    gang_affiliation = random.choice(list(LA_GANGS.keys()))
    gang_sets = LA_GANGS[gang_affiliation]['sets']
    set_name = random.choice(gang_sets)
    
    # Generate gang member lore
    lore_data = generate_gang_lore(character_name, power_level, gang_affiliation, set_name)
    
    # Create gang member data
    character_data = {
        "character_id": character_id,
        "name": character_name,
        "username": str(ctx.author),
        "user_id": user_id,
        "power_level": power_level,
        "wins": 0,
        "losses": 0,
        "has_been_reborn": False,
        "gang_affiliation": gang_affiliation,
        "set_name": set_name,
        "lore": lore_data,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save gang member
    characters[character_id] = character_data
    save_characters(characters)
    
    # Determine power tier for description
    if power_level <= 400:
        tier = "Young Hustler"
        tier_color = discord.Color.dark_grey()
    elif power_level <= 1000:
        tier = "Seasoned Banger"
        tier_color = discord.Color.blue()
    elif power_level <= 1600:
        tier = "OG"
        tier_color = discord.Color.purple()
    else:
        tier = "Shot Caller"
        tier_color = discord.Color.gold()
    
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
    embed.add_field(name="Street Power", value=f"{power_level}", inline=False)
    embed.add_field(name="Gang Affiliation", value=f"{gang_affiliation}", inline=True)
    embed.add_field(name="Set", value=f"{set_name}", inline=True)
    embed.add_field(name="Rank", value=tier, inline=True)
    embed.add_field(name="Record", value="0-0", inline=True)
    
    embed.add_field(
        name="Hidden Background",
        value=f"Use `?lore {character_id}` to reveal their street history and unlock combat bonuses",
        inline=False
    )
    
    embed.set_footer(text="A new soldier hit the streets")
    
    await ctx.send(embed=embed)

# Lore command - Reveal detailed gang member backstory
@bot.command(name='lore')
async def reveal_lore(ctx, character_id: str = None):
    """Reveal the detailed lore of your gang member. Usage: ?lore <character_id>"""
    
    if character_id is None:
        await ctx.send("Usage: `?lore <character_id>`\nExample: `?lore 123456`")
        return
    
    # Check if gang member exists
    if character_id not in characters:
        await ctx.send(f"Gang member ID `{character_id}` not found!")
        return
    
    member = characters[character_id]
    user_id = str(ctx.author.id)
    
    # Verify ownership
    if member.get('user_id') != user_id:
        await ctx.send("You don't own this gang member!")
        return
    
    # Check if member has lore
    if 'lore' not in member:
        # Generate lore for old members
        lore_data = generate_gang_lore(
            member['name'], 
            member['power_level'],
            member.get('gang_affiliation', 'Crips'),
            member.get('set_name', 'Unknown Set')
        )
        member['lore'] = lore_data
        characters[character_id] = member
        save_characters(characters)
    
    lore = member['lore']
    
    # Lore reveal animation
    reveal_embed = discord.Embed(
        title="DIGGING UP THE HISTORY",
        description=f"Uncovering the street story of **{member['name']}**...\n\nThe streets remember everything...",
        color=discord.Color.dark_purple()
    )
    
    await ctx.send(embed=reveal_embed)
    await asyncio.sleep(3)
    
    # Mark lore as revealed (grants combat bonus)
    if not lore.get('lore_revealed', False):
        lore['lore_revealed'] = True
        member['lore'] = lore
        characters[character_id] = member
        save_characters(characters)
        
        newly_revealed = True
    else:
        newly_revealed = False
    
    # Get gang color
    gang_color = LA_GANGS.get(member.get('gang_affiliation', 'Crips'), {}).get('color', discord.Color.red())
    
    # Main lore embed
    lore_embed = discord.Embed(
        title=f"THE STORY OF {member['name'].upper()}",
        description=f"**{lore['experience'].title()}** | Age: {lore['age']} years old",
        color=gang_color
    )
    
    lore_embed.add_field(
        name="ORIGIN",
        value=f"{member['name']} {lore['origin']}. Through years in the streets, they became {lore['personality']}.",
        inline=False
    )
    
    lore_embed.add_field(
        name="GANG AFFILIATION",
        value=f"**{member.get('gang_affiliation', 'Unknown')}** - {member.get('set_name', 'Unknown Set')}",
        inline=False
    )
    
    lore_embed.add_field(
        name="STREET REPUTATION",
        value=f"They {lore['skill_source']}, earning respect and fear throughout the city.",
        inline=False
    )
    
    lore_embed.add_field(
        name="MOTIVATION",
        value=f"Currently, {member['name']} is {lore['goal']}.",
        inline=False
    )
    
    lore_embed.add_field(
        name="TERRITORY",
        value=f"They control operations in {lore['territory']}, where their word is law.",
        inline=False
    )
    
    lore_embed.add_field(
        name="SPECIAL TRAIT",
        value=f"{member['name']} {lore['special_trait']}.",
        inline=False
    )
    
    lore_embed.add_field(
        name="BODY COUNT",
        value=f"Alleged bodies: **{lore['bodies']}** (never convicted)",
        inline=True
    )
    
    lore_embed.add_field(
        name="WEAKNESS",
        value=f"Despite their power, they {lore['weakness']}.",
        inline=False
    )
    
    if newly_revealed:
        lore_embed.add_field(
            name="STREET KNOWLEDGE UNLOCKED",
            value=f"Knowledge of {member['name']}'s history grants **5-15% power boost** in battles!\nEffective in both solo fights and crew wars.",
            inline=False
        )
    else:
        lore_embed.add_field(
            name="STREET KNOWLEDGE ACTIVE",
            value=f"Combat bonus already unlocked: **5-15% power boost** in battles",
            inline=False
        )
    
    lore_embed.set_footer(text=f"Current Street Power: {member['power_level']} | Record: {member.get('wins', 0)}-{member.get('losses', 0)}")
    
    await ctx.send(embed=lore_embed)

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
    
    # Sort by power level (highest first)
    user_members.sort(key=lambda x: x['power_level'], reverse=True)
    
    # Main embed
    embed = discord.Embed(
        title=f"{ctx.author.name}'s Gang Members",
        description=f"Total Members: {len(user_members)}",
        color=discord.Color.dark_purple()
    )
    
    for member in user_members:
        # Build member info
        wins = member.get('wins', 0)
        losses = member.get('losses', 0)
        has_been_reborn = member.get('has_been_reborn', False)
        is_merged = member.get('is_merged', False)
        
        # Check lore status
        lore_revealed = False
        if 'lore' in member:
            lore_revealed = member['lore'].get('lore_revealed', False)
        
        # Determine tier
        power = member['power_level']
        if power <= 400:
            tier = "Young Hustler"
        elif power <= 1000:
            tier = "Seasoned Banger"
        elif power <= 1600:
            tier = "OG"
        else:
            tier = "Shot Caller"
        
        # Status indicators
        if is_merged:
            status = "MERGED"
        elif has_been_reborn:
            status = "CAME BACK"
        else:
            status = "Original"
        
        rebirth_eligible = "No" if has_been_reborn else "Yes"
        lore_status = "Known" if lore_revealed else "Unknown"
        
        value_text = (
            f"**ID:** `{member['character_id']}`\n"
            f"**Power:** {member['power_level']}\n"
            f"**Rank:** {tier}\n"
            f"**Gang:** {member.get('gang_affiliation', 'Unknown')}\n"
            f"**Set:** {member.get('set_name', 'Unknown')}\n"
            f"**Record:** {wins}-{losses}\n"
            f"**Status:** {status}\n"
            f"**History:** {lore_status}\n"
            f"**Can Revive:** {rebirth_eligible}"
        )
        
        embed.add_field(
            name=f"{member['name']}",
            value=value_text,
            inline=True
        )
    
    embed.set_footer(text="Use ?lore <id> to reveal history | ?crew for crew battles | ?slide <id> for solo")
    
    await ctx.send(embed=embed)

# Crew command - Group battle with lore bonuses
@bot.command(name='crew')
async def crew_battle(ctx):
    """Battle as a crew with ALL your gang members against a RANDOM sized rival crew (1-20 members)"""
    
    user_id = str(ctx.author.id)
    
    # Find all gang members owned by user
    user_members = [char for char in characters.values() if char.get('user_id') == user_id]
    
    if not user_members:
        await ctx.send("You don't have any gang members! Use `?make` to create one.")
        return
    
    if len(user_members) < 2:
        await ctx.send("You need at least 2 gang members to form a crew! Use `?make` to recruit more.")
        return
    
    # Calculate total crew power with lore bonuses
    player_crew_power = 0
    lore_bonus_count = 0
    
    for member in user_members:
        base_power = member['power_level']
        if 'lore' in member and member['lore'].get('lore_revealed', False):
            # Apply lore bonus
            lore_bonus_multiplier = random.uniform(1.05, 1.15)
            effective_power = int(base_power * lore_bonus_multiplier)
            player_crew_power += effective_power
            lore_bonus_count += 1
        else:
            player_crew_power += base_power
    
    # Generate SUPER RANDOM rival crew (1-20 members)
    rival_crew, rival_gang, rival_set = generate_rival_crew()
    rival_crew_power = sum(rival['power'] for rival in rival_crew)
    
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
    for member in user_members:
        lore_indicator = " [STREET KNOWLEDGE]" if 'lore' in member and member['lore'].get('lore_revealed', False) else ""
        player_crew_text += f"**{member['name']}**{lore_indicator} - Power: {member['power_level']}\n"
    
    intro_embed.add_field(
        name=f"YOUR CREW ({len(user_members)} members)",
        value=f"{player_crew_text}\n**Total Power: {player_crew_power}**",
        inline=False
    )
    
    if lore_bonus_count > 0:
        intro_embed.add_field(
            name="Street Knowledge Advantage",
            value=f"{lore_bonus_count} member(s) with revealed history gain combat bonuses!",
            inline=False
        )
    
    # Rival crew info - truncate if too large
    rival_crew_text = ""
    display_limit = 10
    
    for idx, rival_member in enumerate(rival_crew):
        if idx < display_limit:
            rival_crew_text += f"**{rival_member['name']}** - Power: {rival_member['power']}\n"
        elif idx == display_limit:
            remaining = len(rival_crew) - display_limit
            rival_crew_text += f"... and {remaining} more members\n"
            break
    
    intro_embed.add_field(
        name=f"RIVAL CREW - {rival_set} ({len(rival_crew)} members)",
        value=f"{rival_crew_text}\n**Total Power: {rival_crew_power}**",
        inline=False
    )
    
    # Power difference
    power_diff = player_crew_power - rival_crew_power
    
    if power_diff > 2000:
        threat_level = "EASY TARGET"
        threat_color = discord.Color.dark_green()
    elif power_diff > 1000:
        threat_level = "FAVORABLE ODDS"
        threat_color = discord.Color.green()
    elif power_diff > -1000:
        threat_level = "EVEN MATCH"
        threat_color = discord.Color.gold()
    elif power_diff > -2000:
        threat_level = "DANGEROUS SITUATION"
        threat_color = discord.Color.orange()
    else:
        threat_level = "EXTREMELY DANGEROUS"
        threat_color = discord.Color.dark_red()
    
    intro_embed.add_field(
        name="Threat Assessment",
        value=threat_level,
        inline=False
    )
    
    # Crew size comparison
    size_diff = len(user_members) - len(rival_crew)
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
    battle_result = simulate_battle(
        f"{ctx.author.name}'s Crew",
        player_crew_power,
        f"{rival_set}",
        rival_crew_power,
        lore_revealed=True  # Crew has advantage if any member has it
    )
    
    player_won = battle_result['player_won']
    
    # Calculate death chance (lower for crew battles)
    death_chance = calculate_crew_death_chance(player_won)
    
    # Determine casualties
    casualties = []
    survivors = []
    
    for member in user_members:
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
            name="Battle Odds",
            value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
            inline=False
        )
        
        if battle_result.get('lore_bonus_applied'):
            outcome_embed.add_field(
                name="Street Knowledge Applied",
                value=f"Revealed history provided tactical advantage in battle!",
                inline=False
            )
        
    else:
        outcome_embed = discord.Embed(
            title="CREW WAR DEFEAT",
            description=f"**{ctx.author.name}'s Crew** was defeated by the {rival_set} crew of {len(rival_crew)} members!",
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
        for member in casualties:
            casualty_text += f"{member['name']} (Power: {member['power_level']})\n"
            
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
            if player_won:
                member['wins'] = member.get('wins', 0) + 1
            else:
                member['losses'] = member.get('losses', 0) + 1
            
            characters[member['character_id']] = member
            survivor_text += f"{member['name']} (Power: {member['power_level']}) - Record: {member['wins']}-{member['losses']}\n"
        
        outcome_embed.add_field(
            name=f"SURVIVORS ({len(survivors)} members)",
            value=survivor_text,
            inline=False
        )
        
        save_characters(characters)
    
    # Show revival info if applicable
    revival_ids = []
    for member in casualties:
        if not member.get('has_been_reborn', False):
            revival_ids.append(member['character_id'])
    
    if revival_ids:
        revival_text = "Fallen crew members can be brought back:\n"
        for char_id in revival_ids:
            revival_text += f"`?revive {char_id}`\n"
        outcome_embed.set_footer(text=revival_text)
    
    await ctx.send(embed=outcome_embed)

# Slide command - Battle against rival gang members with lore bonus
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
    
    # Check lore status
    lore_revealed = False
    if 'lore' in player_char:
        lore_revealed = player_char['lore'].get('lore_revealed', False)
    
    # Generate COMPLETELY RANDOM rival (10-2000)
    rival_power = generate_street_power()
    
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
    
    # Determine power difference for threat level
    effective_power = player_char['power_level']
    if lore_revealed:
        effective_power = int(player_char['power_level'] * random.uniform(1.05, 1.15))
    
    power_diff = rival_power - effective_power
    
    if power_diff > 600:
        threat_level = "EXTREMELY DANGEROUS OPP"
        threat_color = discord.Color.dark_red()
    elif power_diff > 300:
        threat_level = "DANGEROUS OPP"
        threat_color = discord.Color.red()
    elif power_diff > 100:
        threat_level = "TOUGH OPPOSITION"
        threat_color = discord.Color.orange()
    elif power_diff > -100:
        threat_level = "EVEN MATCH"
        threat_color = discord.Color.gold()
    elif power_diff > -300:
        threat_level = "FAVORABLE ODDS"
        threat_color = discord.Color.green()
    else:
        threat_level = "EASY TARGET"
        threat_color = discord.Color.dark_green()
    
    # Determine rival tier
    if rival_power <= 400:
        rival_tier = "Young Hustler"
    elif rival_power <= 1000:
        rival_tier = "Seasoned Banger"
    elif rival_power <= 1600:
        rival_tier = "OG"
    else:
        rival_tier = "Shot Caller"
    
    # Get gang colors
    player_gang_color = LA_GANGS.get(player_char.get('gang_affiliation', 'Crips'), {}).get('color', discord.Color.blue())
    rival_gang_color = LA_GANGS.get(rival_gang, {}).get('color', discord.Color.red())
    
    # Battle intro embed
    intro_embed = discord.Embed(
        title="SLIDING ON OPPS",
        description=f"**{player_char['name']}** spots **{rival_name}** in enemy territory\n\n{threat_level}",
        color=threat_color
    )
    
    lore_indicator = " [STREET KNOWLEDGE]" if lore_revealed else ""
    
    intro_embed.add_field(
        name=f"{player_char['name']} (YOU)",
        value=f"Power: **{player_char['power_level']}**{lore_indicator}\nGang: {player_char.get('gang_affiliation', 'Unknown')}\nSet: {player_char.get('set_name', 'Unknown')}\nRecord: {player_char.get('wins', 0)}-{player_char.get('losses', 0)}",
        inline=True
    )
    
    intro_embed.add_field(
        name=f"{rival_name} (OPP)",
        value=f"Power: **{rival_power}**\nGang: {rival_gang}\nSet: {rival_set}\nRank: {rival_tier}",
        inline=True
    )
    
    if lore_revealed:
        intro_embed.add_field(
            name="Tactical Advantage",
            value="Street knowledge grants combat bonus!",
            inline=False
        )
    
    intro_embed.set_footer(text="The confrontation begins...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)
    
    # Simulate the battle with lore bonus
    battle_result = simulate_battle(
        player_char['name'], 
        player_char['power_level'],
        rival_name,
        rival_power,
        lore_revealed=lore_revealed
    )
    
    player_won = battle_result['player_won']
    
    # Calculate death chance
    death_chance = calculate_death_chance(
        player_char['power_level'],
        rival_power,
        player_won
    )
    
    # Roll for death
    death_roll = random.randint(1, 100)
    member_dies = death_roll <= death_chance
    
    # Outcome embed
    if player_won:
        if member_dies:
            outcome_embed = discord.Embed(
                title="CAUGHT A BODY BUT PAID THE PRICE",
                description=f"**{player_char['name']}** eliminated **{rival_name}**, but was fatally wounded",
                color=discord.Color.dark_red()
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
            
            outcome_embed.add_field(
                name="Final Record",
                value=f"{player_char.get('wins', 0)}-{player_char.get('losses', 0)}",
                inline=False
            )
            
            if not player_char.get('has_been_reborn', False):
                outcome_embed.set_footer(text=f"Use ?revive {character_id} to bring them back")
            else:
                outcome_embed.set_footer(text="This member already came back once and cannot be revived again")
            
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_name} ({rival_set}) - Fatal Wounds"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            
            del characters[character_id]
            save_characters(characters)
            
        else:
            outcome_embed = discord.Embed(
                title="BODY CAUGHT",
                description=f"**{player_char['name']}** has eliminated **{rival_name}** from {rival_set}",
                color=discord.Color.green()
            )
            
            outcome_embed.add_field(
                name="Battle Odds",
                value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
                inline=False
            )
            
            if battle_result.get('lore_bonus_applied'):
                outcome_embed.add_field(
                    name="Street Knowledge Applied",
                    value=f"Effective Power: {battle_result['effective_power']} (boosted from {player_char['power_level']})",
                    inline=False
                )
            
            outcome_embed.add_field(
                name="Survival Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less) - SURVIVED",
                inline=False
            )
            
            player_char['wins'] = player_char.get('wins', 0) + 1
            characters[character_id] = player_char
            save_characters(characters)
            
            outcome_embed.add_field(
                name="New Record",
                value=f"{player_char['wins']}-{player_char.get('losses', 0)}",
                inline=False
            )
            
    else:
        if member_dies:
            outcome_embed = discord.Embed(
                title="CAUGHT SLIPPING",
                description=f"**{player_char['name']}** was eliminated by **{rival_name}** from {rival_set}",
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
                name="RIP",
                value=f"{player_char['name']} was caught lacking in enemy territory",
                inline=False
            )
            
            if not player_char.get('has_been_reborn', False):
                outcome_embed.set_footer(text=f"Use ?revive {character_id} to bring them back")
            else:
                outcome_embed.set_footer(text="This member already came back once and cannot be revived again")
            
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
                name="Battle Odds",
                value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Survival Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less) - SURVIVED",
                inline=False
            )
            
            player_char['losses'] = player_char.get('losses', 0) + 1
            characters[character_id] = player_char
            save_characters(characters)
            
            outcome_embed.add_field(
                name="New Record",
                value=f"{player_char.get('wins', 0)}-{player_char['losses']}",
                inline=False
            )
            
            outcome_embed.set_footer(text="Your member got away but took an L")
    
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
    
    # Check if the member was killed by a rival (not crew war or merge)
    killer_name = dead_member.get('killed_by', 'Unknown')
    
    if "Crew War" in killer_name:
        await ctx.send(f"**{dead_member['name']}** was killed in a crew war, not by a specific rival. Revenge is not available for crew war deaths.")
        return
    
    if "Merge Operation" in killer_name or "Blood Merge" in killer_name:
        await ctx.send(f"**{dead_member['name']}** was sacrificed in a merge operation. Revenge is not available for merges.")
        return
    
    if "(Fatal Wounds)" in killer_name or "- Fatal Wounds" in killer_name:
        # Extract the actual killer name
        killer_name = killer_name.replace(" (Fatal Wounds)", "").replace(" - Fatal Wounds", "").strip()
        # Try to extract set name if present
        if "(" in killer_name and ")" in killer_name:
            killer_name = killer_name.split("(")[0].strip()
    
    # Recreate the rival with the same name but new random power
    rival_power = generate_street_power()
    
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
    
    # Check lore status of avenger
    lore_revealed = False
    if 'lore' in avenger_char:
        lore_revealed = avenger_char['lore'].get('lore_revealed', False)
    
    # Determine power difference for threat level
    effective_power = avenger_char['power_level']
    if lore_revealed:
        effective_power = int(avenger_char['power_level'] * random.uniform(1.05, 1.15))
    
    power_diff = rival_power - effective_power
    
    if power_diff > 600:
        threat_level = "EXTREMELY DANGEROUS OPP"
        threat_color = discord.Color.dark_red()
    elif power_diff > 300:
        threat_level = "DANGEROUS OPP"
        threat_color = discord.Color.red()
    elif power_diff > 100:
        threat_level = "TOUGH OPPOSITION"
        threat_color = discord.Color.orange()
    elif power_diff > -100:
        threat_level = "EVEN MATCH"
        threat_color = discord.Color.gold()
    elif power_diff > -300:
        threat_level = "FAVORABLE ODDS"
        threat_color = discord.Color.green()
    else:
        threat_level = "EASY TARGET"
        threat_color = discord.Color.dark_green()
    
    # Determine rival tier
    if rival_power <= 400:
        rival_tier = "Young Hustler"
    elif rival_power <= 1000:
        rival_tier = "Seasoned Banger"
    elif rival_power <= 1600:
        rival_tier = "OG"
    else:
        rival_tier = "Shot Caller"
    
    # Revenge intro embed
    intro_embed = discord.Embed(
        title="REVENGE MISSION",
        description=f"**{avenger_char['name']}** seeks vengeance for **{dead_member['name']}**\n\nThe killer, **{killer_name}**, has been located...\n\n{threat_level}",
        color=threat_color
    )
    
    lore_indicator = " [STREET KNOWLEDGE]" if lore_revealed else ""
    
    intro_embed.add_field(
        name=f"{avenger_char['name']} (AVENGER)",
        value=f"Power: **{avenger_char['power_level']}**{lore_indicator}\nGang: {avenger_char.get('gang_affiliation', 'Unknown')}\nRecord: {avenger_char.get('wins', 0)}-{avenger_char.get('losses', 0)}",
        inline=True
    )
    
    intro_embed.add_field(
        name=f"{killer_name} (KILLER)",
        value=f"Power: **{rival_power}**\nGang: {rival_gang}\nSet: {rival_set}\nRank: {rival_tier}",
        inline=True
    )
    
    intro_embed.add_field(
        name="Fallen Homie",
        value=f"{dead_member['name']} (Power: {dead_member['power_level']})\nKilled on: {dead_member.get('death_date', 'Unknown')}",
        inline=False
    )
    
    if lore_revealed:
        intro_embed.add_field(
            name="Tactical Advantage",
            value="Street knowledge grants combat bonus!",
            inline=False
        )
    
    intro_embed.set_footer(text="The revenge mission begins...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)
    
    # Simulate the revenge battle with lore bonus
    battle_result = simulate_battle(
        avenger_char['name'], 
        avenger_char['power_level'],
        killer_name,
        rival_power,
        lore_revealed=lore_revealed
    )
    
    player_won = battle_result['player_won']
    
    # Calculate death chance
    death_chance = calculate_death_chance(
        avenger_char['power_level'],
        rival_power,
        player_won
    )
    
    # Roll for death
    death_roll = random.randint(1, 100)
    member_dies = death_roll <= death_chance
    
    # Outcome embed
    if player_won:
        if member_dies:
            outcome_embed = discord.Embed(
                title="REVENGE COMPLETE - BUT AT A COST",
                description=f"**{avenger_char['name']}** eliminated **{killer_name}**, avenging **{dead_member['name']}**, but was fatally wounded",
                color=discord.Color.dark_red()
            )
            
            outcome_embed.add_field(
                name="Battle Odds",
                value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
                inline=False
            )
            
            if battle_result.get('lore_bonus_applied'):
                outcome_embed.add_field(
                    name="Street Knowledge Applied",
                    value=f"Effective Power: {battle_result['effective_power']} (boosted from {avenger_char['power_level']})",
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
            
            outcome_embed.add_field(
                name="Final Record",
                value=f"{avenger_char.get('wins', 0)}-{avenger_char.get('losses', 0)}",
                inline=False
            )
            
            if not avenger_char.get('has_been_reborn', False):
                outcome_embed.set_footer(text=f"Use ?revive {avenger_character_id} to bring them back")
            else:
                outcome_embed.set_footer(text="This member already came back once and cannot be revived again")
            
            dead_avenger = avenger_char.copy()
            dead_avenger['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_avenger['killed_by'] = f"{killer_name} (Revenge Mission - Fatal Wounds)"
            graveyard.append(dead_avenger)
            save_graveyard(graveyard)
            
            del characters[avenger_character_id]
            save_characters(characters)
            
        else:
            outcome_embed = discord.Embed(
                title="REVENGE COMPLETE",
                description=f"**{avenger_char['name']}** has eliminated **{killer_name}**, avenging **{dead_member['name']}**!",
                color=discord.Color.green()
            )
            
            outcome_embed.add_field(
                name="Battle Odds",
                value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
                inline=False
            )
            
            if battle_result.get('lore_bonus_applied'):
                outcome_embed.add_field(
                    name="Street Knowledge Applied",
                    value=f"Effective Power: {battle_result['effective_power']} (boosted from {avenger_char['power_level']})",
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
            
            avenger_char['wins'] = avenger_char.get('wins', 0) + 1
            characters[avenger_character_id] = avenger_char
            save_characters(characters)
            
            outcome_embed.add_field(
                name="New Record",
                value=f"{avenger_char['wins']}-{avenger_char.get('losses', 0)}",
                inline=False
            )
            
    else:
        if member_dies:
            outcome_embed = discord.Embed(
                title="REVENGE FAILED - ELIMINATED",
                description=f"**{avenger_char['name']}** was eliminated by **{killer_name}**\n\n{dead_member['name']} remains unavenged...",
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
                value=f"{avenger_char.get('wins', 0)}-{avenger_char.get('losses', 0)}",
                inline=False
            )
            
            outcome_embed.add_field(
                name="RIP",
                value=f"{avenger_char['name']} fell to the same killer that got {dead_member['name']}",
                inline=False
            )
            
            if not avenger_char.get('has_been_reborn', False):
                outcome_embed.set_footer(text=f"Use ?revive {avenger_character_id} to bring them back")
            else:
                outcome_embed.set_footer(text="This member already came back once and cannot be revived again")
            
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
                name="Battle Odds",
                value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Survival Roll",
                value=f"Rolled **{death_roll}** (Death at {death_chance}% or less) - SURVIVED",
                inline=False
            )
            
            avenger_char['losses'] = avenger_char.get('losses', 0) + 1
            characters[avenger_character_id] = avenger_char
            save_characters(characters)
            
            outcome_embed.add_field(
                name="New Record",
                value=f"{avenger_char.get('wins', 0)}-{avenger_char['losses']}",
                inline=False
            )
            
            outcome_embed.set_footer(text=f"{avenger_char['name']} got away but took an L")
    
    await ctx.send(embed=outcome_embed)

# Merge command - Combine two gang members to create a more powerful member
@bot.command(name='merge')
async def merge_members(ctx, member1_id: str = None, member2_id: str = None):
    """Merge two gang members to create a more powerful member. Usage: ?merge <id1> <id2>"""
    
    if member1_id is None or member2_id is None:
        await ctx.send("Usage: `?merge <member1_id> <member2_id>`\nExample: `?merge 123456 789012`\n\nBoth members will be merged to create a more powerful gang member!")
        return
    
    if member1_id == member2_id:
        await ctx.send("You cannot merge a member with themselves!")
        return
    
    user_id = str(ctx.author.id)
    
    if member1_id not in characters:
        await ctx.send(f"Gang member ID `{member1_id}` not found!")
        return
    
    if member2_id not in characters:
        await ctx.send(f"Gang member ID `{member2_id}` not found!")
        return
    
    member1 = characters[member1_id]
    member2 = characters[member2_id]
    
    if member1.get('user_id') != user_id:
        await ctx.send(f"You don't own the member with ID `{member1_id}`!")
        return
    
    if member2.get('user_id') != user_id:
        await ctx.send(f"You don't own the member with ID `{member2_id}`!")
        return
    
    ritual_embed = discord.Embed(
        title="BLOOD MERGE OPERATION",
        description=f"**{member1['name']}** and **{member2['name']}** begin the merge ritual...\n\nTwo become one...",
        color=discord.Color.dark_purple()
    )
    
    ritual_embed.add_field(
        name=f"{member1['name']}",
        value=f"Power: {member1['power_level']}\nGang: {member1.get('gang_affiliation', 'Unknown')}\nRecord: {member1.get('wins', 0)}-{member1.get('losses', 0)}",
        inline=True
    )
    
    ritual_embed.add_field(
        name=f"{member2['name']}",
        value=f"Power: {member2['power_level']}\nGang: {member2.get('gang_affiliation', 'Unknown')}\nRecord: {member2.get('wins', 0)}-{member2.get('losses', 0)}",
        inline=True
    )
    
    ritual_embed.set_footer(text="Both members will be sacrificed...")
    
    await ctx.send(embed=ritual_embed)
    await asyncio.sleep(4)
    
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    nickname = last_name[:3].upper()
    merged_name = f"{first_name} '{nickname}' {last_name}"
    
    merged_id = generate_unique_id()
    
    combined_power = member1['power_level'] + member2['power_level']
    merge_bonus = random.randint(200, 600)
    merged_power = combined_power + merge_bonus
    
    if merged_power > 2000:
        merged_power = 2000
        actual_bonus = 2000 - combined_power
    else:
        actual_bonus = merge_bonus
    
    total_wins = member1.get('wins', 0) + member2.get('wins', 0)
    total_losses = 0
    
    has_been_reborn = member1.get('has_been_reborn', False) or member2.get('has_been_reborn', False)
    
    # Use gang affiliation from stronger member
    if member1['power_level'] > member2['power_level']:
        merged_gang = member1.get('gang_affiliation', 'Crips')
        merged_set = member1.get('set_name', 'Unknown Set')
    else:
        merged_gang = member2.get('gang_affiliation', 'Crips')
        merged_set = member2.get('set_name', 'Unknown Set')
    
    # Generate merged member lore
    merged_lore = generate_gang_lore(merged_name, merged_power, merged_gang, merged_set)
    
    merged_data = {
        "character_id": merged_id,
        "name": merged_name,
        "username": str(ctx.author),
        "user_id": user_id,
        "power_level": merged_power,
        "wins": total_wins,
        "losses": total_losses,
        "has_been_reborn": has_been_reborn,
        "is_merged": True,
        "parent1_name": member1['name'],
        "parent2_name": member2['name'],
        "parent1_id": member1_id,
        "parent2_id": member2_id,
        "gang_affiliation": merged_gang,
        "set_name": merged_set,
        "lore": merged_lore,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    dead_member1 = member1.copy()
    dead_member1['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dead_member1['killed_by'] = "Blood Merge Operation"
    
    dead_member2 = member2.copy()
    dead_member2['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dead_member2['killed_by'] = "Blood Merge Operation"
    
    current_graveyard = load_graveyard()
    current_graveyard.append(dead_member1)
    current_graveyard.append(dead_member2)
    save_graveyard(current_graveyard)
    
    del characters[member1_id]
    del characters[member2_id]
    
    characters[merged_id] = merged_data
    save_characters(characters)
    
    if merged_power <= 400:
        tier = "Young Hustler"
        tier_color = discord.Color.dark_grey()
    elif merged_power <= 1000:
        tier = "Seasoned Banger"
        tier_color = discord.Color.blue()
    elif merged_power <= 1600:
        tier = "OG"
        tier_color = discord.Color.purple()
    else:
        tier = "Shot Caller"
        tier_color = discord.Color.gold()
    
    # Get gang color
    gang_color = LA_GANGS.get(merged_gang, {}).get('color', discord.Color.blue())
    
    success_embed = discord.Embed(
        title="MERGED GANG MEMBER CREATED",
        description=f"The merge is complete! **{merged_name}** emerges as a more powerful member!",
        color=gang_color
    )
    
    success_embed.add_field(
        name="Merged Name",
        value=merged_name,
        inline=False
    )
    
    success_embed.add_field(
        name="New ID",
        value=f"`{merged_id}`",
        inline=False
    )
    
    success_embed.add_field(
        name="Power Fusion",
        value=f"{member1['power_level']} + {member2['power_level']} + {actual_bonus} (merge bonus) = **{merged_power}**",
        inline=False
    )
    
    success_embed.add_field(
        name="Gang Affiliation",
        value=f"{merged_gang} - {merged_set}",
        inline=False
    )
    
    success_embed.add_field(
        name="Rank",
        value=tier,
        inline=True
    )
    
    success_embed.add_field(
        name="Combined Wins",
        value=f"Total Wins: {total_wins}",
        inline=True
    )
    
    success_embed.add_field(
        name="Sacrificed",
        value=f"{member1['name']}\n{member2['name']}",
        inline=False
    )
    
    success_embed.add_field(
        name="New History",
        value=f"Use `?lore {merged_id}` to discover the merged member's street story",
        inline=False
    )
    
    if has_been_reborn:
        success_embed.add_field(
            name="WARNING",
            value="This merged member inherited revival status and CANNOT be revived if killed",
            inline=False
        )
    else:
        success_embed.add_field(
            name="Revival Status",
            value="This merged member can be revived once if killed",
            inline=False
        )
    
    success_embed.set_footer(text="A more powerful soldier has been created")
    
    await ctx.send(embed=success_embed)

# Revive command - Bring a dead gang member back with more power (ONE TIME ONLY)
@bot.command(name='revive')
async def revive_member(ctx, character_id: str = None):
    """Revive a fallen gang member with increased power (ONE TIME ONLY). Usage: ?revive <character_id>"""
    
    if character_id is None:
        await ctx.send("Usage: `?revive <character_id>`\nExample: `?revive 123456`")
        return
    
    user_id = str(ctx.author.id)
    
    current_graveyard = load_graveyard()
    
    dead_member = None
    graveyard_index = None
    
    for idx, member in enumerate(current_graveyard):
        if member.get('character_id') == character_id:
            dead_member = member
            graveyard_index = idx
            break
    
    if dead_member is None:
        await ctx.send(f"No dead member with ID `{character_id}` found in the graveyard!")
        return
    
    if dead_member.get('user_id') != user_id:
        await ctx.send("You don't own this member!")
        return
    
    if dead_member.get('has_been_reborn', False):
        await ctx.send(f"**{dead_member['name']}** already came back once and cannot be revived again!\n\nEach member can only be revived ONE time. Use `?make` to create a new member.")
        return
    
    ritual_embed = discord.Embed(
        title="REVIVAL OPERATION",
        description=f"Street doctors work to bring back **{dead_member['name']}** from the dead...",
        color=discord.Color.dark_purple()
    )
    
    ritual_embed.add_field(
        name="Former Power",
        value=f"{dead_member['power_level']}",
        inline=True
    )
    
    ritual_embed.add_field(
        name="Previous Record",
        value=f"{dead_member.get('wins', 0)}-{dead_member.get('losses', 0)}",
        inline=True
    )
    
    ritual_embed.set_footer(text="The operation begins...")
    
    await ctx.send(embed=ritual_embed)
    await asyncio.sleep(3)
    
    base_boost = random.randint(200, 500)
    percentage_boost = int(dead_member['power_level'] * 0.15)
    total_boost = base_boost + percentage_boost
    
    new_power = dead_member['power_level'] + total_boost
    
    if new_power > 2000:
        new_power = 2000
        total_boost = 2000 - dead_member['power_level']
    
    new_character_id = generate_unique_id()
    
    revived_data = {
        "character_id": new_character_id,
        "name": dead_member['name'],
        "username": dead_member.get('username'),
        "user_id": user_id,
        "power_level": new_power,
        "wins": dead_member.get('wins', 0),
        "losses": dead_member.get('losses', 0),
        "has_been_reborn": True,
        "is_merged": dead_member.get('is_merged', False),
        "gang_affiliation": dead_member.get('gang_affiliation', 'Crips'),
        "set_name": dead_member.get('set_name', 'Unknown Set'),
        "lore": dead_member.get('lore', {}),
        "original_id": character_id,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "revived_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if dead_member.get('is_merged', False):
        revived_data['parent1_name'] = dead_member.get('parent1_name')
        revived_data['parent2_name'] = dead_member.get('parent2_name')
        revived_data['parent1_id'] = dead_member.get('parent1_id')
        revived_data['parent2_id'] = dead_member.get('parent2_id')
    
    characters[new_character_id] = revived_data
    save_characters(characters)
    
    current_graveyard.pop(graveyard_index)
    save_graveyard(current_graveyard)
    
    if new_power <= 400:
        tier = "Young Hustler"
        tier_color = discord.Color.dark_grey()
    elif new_power <= 1000:
        tier = "Seasoned Banger"
        tier_color = discord.Color.blue()
    elif new_power <= 1600:
        tier = "OG"
        tier_color = discord.Color.purple()
    else:
        tier = "Shot Caller"
        tier_color = discord.Color.gold()
    
    # Get gang color
    gang_color = LA_GANGS.get(revived_data['gang_affiliation'], {}).get('color', discord.Color.blue())
    
    success_embed = discord.Embed(
        title="REVIVAL SUCCESSFUL",
        description=f"**{dead_member['name']}** is back on the streets, stronger than ever!",
        color=gang_color
    )
    
    success_embed.add_field(
        name="New ID",
        value=f"`{new_character_id}`",
        inline=False
    )
    
    success_embed.add_field(
        name="Power Increase",
        value=f"{dead_member['power_level']} → **{new_power}** (+{total_boost})",
        inline=False
    )
    
    success_embed.add_field(
        name="New Rank",
        value=tier,
        inline=True
    )
    
    success_embed.add_field(
        name="Retained Record",
        value=f"{dead_member.get('wins', 0)}-{dead_member.get('losses', 0)}",
        inline=True
    )
    
    # Check if lore was revealed
    if 'lore' in dead_member and dead_member['lore'].get('lore_revealed', False):
        success_embed.add_field(
            name="Street Knowledge Preserved",
            value="Street history retained - combat bonus still active!",
            inline=False
        )
    
    success_embed.add_field(
        name="WARNING",
        value="This member has used their ONE revival. If they die again, they cannot be brought back.",
        inline=False
    )
    
    success_embed.set_footer(text="Your member is back in the game")
    
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
