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

# Lore generation components
ORIGINS = [
    "turned during the Black Plague in 14th century Europe",
    "awakened in ancient Egypt as a royal blood drinker",
    "created by a vampire council in medieval Transylvania",
    "born from a forbidden ritual in Victorian London",
    "transformed during the French Revolution's Reign of Terror",
    "emerged from the shadows of feudal Japan",
    "cursed by dark magic in the Scottish Highlands",
    "created in the catacombs beneath Rome",
    "turned during the American Civil War",
    "awakened in a Mayan temple centuries ago",
    "transformed in the Russian Empire during the Romanov dynasty",
    "born from blood magic in ancient Babylon",
    "turned by a vampire lord in Renaissance Italy",
    "created during the Spanish Inquisition",
    "awakened in the Byzantine Empire",
    "transformed in the Australian outback by an aboriginal vampire",
    "turned during the Viking Age in Scandinavia",
    "created in a Chinese monastery by an ancient master",
    "born from a blood pact in New Orleans",
    "awakened during the Salem witch trials"
]

PERSONALITIES = [
    "ruthless and calculating, showing no mercy to enemies",
    "noble and honorable, following an ancient code of conduct",
    "chaotic and unpredictable, thriving in madness",
    "cunning and strategic, always three steps ahead",
    "melancholic and haunted by centuries of existence",
    "savage and feral, barely controlling their bloodlust",
    "elegant and refined, preferring diplomacy over violence",
    "vengeful and obsessed with past wrongs",
    "philosophical and contemplative about immortality",
    "sadistic and cruel, enjoying the suffering of others",
    "protective and loyal to those they care about",
    "ambitious and power-hungry, seeking dominance",
    "isolated and withdrawn, avoiding vampire society",
    "seductive and manipulative, using charm as a weapon",
    "warrior-like and honorable in combat",
    "mysterious and enigmatic, keeping secrets close",
    "rebellious and defiant against vampire hierarchy",
    "ancient and wise, having seen empires rise and fall",
    "tragic and romantic, mourning lost humanity",
    "cold and emotionless, treating life as a game"
]

ABILITIES_LORE = [
    "mastered blood magic through decades of practice",
    "learned shadow manipulation from an ancient vampire",
    "developed supernatural speed through constant hunting",
    "gained hypnotic powers from a mystical artifact",
    "achieved regeneration by consuming powerful blood",
    "unlocked mind control through forbidden rituals",
    "inherited shapeshifting from their vampire sire",
    "acquired enhanced strength through trial by combat",
    "learned mist form transformation in the mountains",
    "developed venomous bite through genetic mutation",
    "gained telepathy from drinking a witch's blood",
    "mastered darkness manipulation in underground lairs",
    "achieved immortality through a blood curse",
    "learned fear inducement from a nightmare demon",
    "developed enhanced senses through centuries of survival",
    "gained death touch from consuming ancient vampire blood",
    "mastered blood wings through Egyptian blood magic",
    "unlocked corpse animation from necromantic studies",
    "developed crimson lightning through storm rituals",
    "achieved bloodfire mastery from volcanic sacrifice"
]

GOALS = [
    "seeking to build an empire of darkness",
    "hunting the vampire who turned them",
    "searching for a cure to vampirism",
    "protecting humanity from supernatural threats",
    "collecting ancient vampire artifacts",
    "destroying rival vampire covens",
    "seeking revenge for their mortal death",
    "trying to maintain their fading humanity",
    "building a vampire sanctuary",
    "searching for their lost love across centuries",
    "attempting to end their immortal existence",
    "seeking to become the most powerful vampire",
    "protecting their bloodline from extinction",
    "hunting down rogue vampires",
    "searching for the first vampire",
    "trying to unite all vampire clans",
    "seeking redemption for past sins",
    "collecting knowledge of all vampire bloodlines",
    "attempting to create a new vampire species",
    "searching for a way to walk in daylight"
]

WEAKNESSES = [
    "vulnerable to silver blessed by ancient priests",
    "weakened by running water from sacred rivers",
    "allergic to garlic grown in consecrated ground",
    "burned by sunlight, even reflected rays",
    "unable to cross thresholds without invitation",
    "repelled by religious symbols from their mortal faith",
    "weakened during new moon phases",
    "vulnerable to wooden stakes through the heart",
    "loses power in the presence of pure innocence",
    "weakened by the sound of church bells",
    "unable to see their reflection, causing disorientation",
    "burns when touching holy ground",
    "weakened by the blood of their human family",
    "vulnerable to fire from natural sources",
    "loses strength when starved of blood",
    "weakened by ancient vampire-killing weapons",
    "unable to enter homes of those they've wronged",
    "burns from holy water blessed by seven priests",
    "weakened by wolfsbane and mountain ash",
    "vulnerable to magic from their place of origin"
]

# Generate detailed lore
def generate_vampire_lore(vampire_name, power_level):
    """Generate detailed backstory for a vampire"""
    
    origin = random.choice(ORIGINS)
    personality = random.choice(PERSONALITIES)
    ability_source = random.choice(ABILITIES_LORE)
    goal = random.choice(GOALS)
    weakness = random.choice(WEAKNESSES)
    
    # Generate age based on power
    if power_level <= 400:
        age = random.randint(50, 200)
        experience = "relatively young vampire"
    elif power_level <= 1000:
        age = random.randint(200, 500)
        experience = "seasoned vampire"
    elif power_level <= 1600:
        age = random.randint(500, 1000)
        experience = "ancient vampire"
    else:
        age = random.randint(1000, 3000)
        experience = "primordial vampire"
    
    # Generate notable kills
    kills = random.randint(10, 500)
    
    # Generate territory
    territories = [
        "the Gothic ruins of Eastern Europe",
        "the underground catacombs of Paris",
        "the foggy streets of London",
        "the ancient forests of Transylvania",
        "the abandoned castles of Scotland",
        "the dark alleys of New York",
        "the bayous of Louisiana",
        "the mountain ranges of the Carpathians",
        "the hidden temples of Southeast Asia",
        "the frozen wastelands of Siberia",
        "the desert ruins of Egypt",
        "the volcanic caves of Iceland",
        "the rainforests of South America",
        "the underground cities beneath Rome",
        "the abandoned subway tunnels of Tokyo"
    ]
    territory = random.choice(territories)
    
    # Generate special trait
    traits = [
        "can sense fear in mortals from miles away",
        "has visions of future blood moons",
        "can communicate with nocturnal creatures",
        "leaves no trace of their presence",
        "can drain blood without touching their victim",
        "immune to most conventional vampire weaknesses",
        "can turn invisible during moonless nights",
        "has a hypnotic voice that compels obedience",
        "can sense other vampires' power levels",
        "never needs to feed more than once a month",
        "can walk in cloudy daylight for brief periods",
        "has memorized the names of all their victims",
        "can manipulate dreams of sleeping humans",
        "aged wine tastes like blood to them",
        "can smell vampire hunters from great distances"
    ]
    special_trait = random.choice(traits)
    
    # Determine lore bonus (knowledge of lore grants power boost)
    lore_bonus = random.randint(50, 150)
    
    lore_data = {
        "origin": origin,
        "age": age,
        "experience": experience,
        "personality": personality,
        "ability_source": ability_source,
        "goal": goal,
        "weakness": weakness,
        "kills": kills,
        "territory": territory,
        "special_trait": special_trait,
        "lore_bonus": lore_bonus,
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

# Generate completely random AI power (10-2000, super unpredictable)
def generate_ai_power():
    """Generate completely random AI power from 10 to 2000"""
    
    roll = random.randint(1, 100)
    
    if roll <= 50:
        return random.randint(10, 800)
    elif roll <= 75:
        return random.randint(801, 1400)
    elif roll <= 90:
        return random.randint(1401, 1800)
    else:
        return random.randint(1801, 2000)

# Generate completely random vampire power for new vampires (10-2000)
def generate_random_vampire_power():
    """Generate completely random power for new vampires"""
    
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

# Calculate gang death chance (lower than solo)
def calculate_gang_death_chance(player_won):
    """Calculate death chance for gang battles - lower risk due to group support"""
    
    if player_won:
        return random.randint(2, 8)
    else:
        return random.randint(15, 35)

# Simulate instant battle with lore bonus
def simulate_battle(player_name, player_power, enemy_name, enemy_power, lore_revealed=False):
    """Simulate an instant vampire battle"""
    
    # Apply lore bonus if revealed
    effective_player_power = player_power
    if lore_revealed:
        # Lore knowledge gives strategic advantage
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

# Generate AI gang with SUPER RANDOM size
def generate_ai_gang():
    """Generate a random AI vampire gang with SUPER RANDOM size (1-20 vampires)"""
    
    roll = random.randint(1, 100)
    
    if roll <= 30:
        gang_size = random.randint(1, 3)
    elif roll <= 55:
        gang_size = random.randint(4, 6)
    elif roll <= 75:
        gang_size = random.randint(7, 10)
    elif roll <= 90:
        gang_size = random.randint(11, 15)
    else:
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

# Make command - Creates a vampire with RANDOM power (10-2000)
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
    
    # Generate COMPLETELY RANDOM power level (10 to 2000)
    power_level = generate_random_vampire_power()
    
    # Generate vampire lore
    lore_data = generate_vampire_lore(character_name, power_level)
    
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
        "lore": lore_data,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save vampire
    characters[character_id] = character_data
    save_characters(characters)
    
    # Determine power tier for description
    if power_level <= 400:
        tier = "Fledgling"
        tier_color = discord.Color.dark_grey()
    elif power_level <= 1000:
        tier = "Experienced"
        tier_color = discord.Color.blue()
    elif power_level <= 1600:
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
    
    embed.add_field(
        name="Hidden Lore",
        value=f"Use `?lore {character_id}` to reveal their dark history and unlock combat bonuses",
        inline=False
    )
    
    embed.set_footer(text="A new vampire has risen from the darkness")
    
    await ctx.send(embed=embed)

# Lore command - Reveal detailed vampire backstory
@bot.command(name='lore')
async def reveal_lore(ctx, character_id: str = None):
    """Reveal the detailed lore of your vampire. Usage: ?lore <character_id>"""
    
    if character_id is None:
        await ctx.send("Usage: `?lore <character_id>`\nExample: `?lore 123456`")
        return
    
    # Check if vampire exists
    if character_id not in characters:
        await ctx.send(f"Vampire ID `{character_id}` not found!")
        return
    
    vampire = characters[character_id]
    user_id = str(ctx.author.id)
    
    # Verify ownership
    if vampire.get('user_id') != user_id:
        await ctx.send("You don't own this vampire!")
        return
    
    # Check if vampire has lore
    if 'lore' not in vampire:
        # Generate lore for old vampires
        lore_data = generate_vampire_lore(vampire['name'], vampire['power_level'])
        vampire['lore'] = lore_data
        characters[character_id] = vampire
        save_characters(characters)
    
    lore = vampire['lore']
    
    # Lore reveal animation
    reveal_embed = discord.Embed(
        title="UNCOVERING DARK HISTORY",
        description=f"Delving into the past of **{vampire['name']}**...\n\nAncient memories surface from the shadows...",
        color=discord.Color.dark_purple()
    )
    
    await ctx.send(embed=reveal_embed)
    await asyncio.sleep(3)
    
    # Mark lore as revealed (grants combat bonus)
    if not lore.get('lore_revealed', False):
        lore['lore_revealed'] = True
        vampire['lore'] = lore
        characters[character_id] = vampire
        save_characters(characters)
        
        newly_revealed = True
    else:
        newly_revealed = False
    
    # Main lore embed
    lore_embed = discord.Embed(
        title=f"THE LEGEND OF {vampire['name'].upper()}",
        description=f"**{lore['experience'].title()}** | Age: {lore['age']} years",
        color=discord.Color.dark_red()
    )
    
    lore_embed.add_field(
        name="ORIGIN",
        value=f"{vampire['name']} was {lore['origin']}. Through centuries of existence, they have become {lore['personality']}.",
        inline=False
    )
    
    lore_embed.add_field(
        name="POWERS",
        value=f"They {lore['ability_source']}, granting them supernatural abilities that strike fear into mortals and vampires alike.",
        inline=False
    )
    
    lore_embed.add_field(
        name="MOTIVATION",
        value=f"Currently, {vampire['name']} is {lore['goal']}.",
        inline=False
    )
    
    lore_embed.add_field(
        name="TERRITORY",
        value=f"They rule over {lore['territory']}, where they are both feared and respected.",
        inline=False
    )
    
    lore_embed.add_field(
        name="SPECIAL TRAIT",
        value=f"{vampire['name']} {lore['special_trait']}.",
        inline=False
    )
    
    lore_embed.add_field(
        name="BODY COUNT",
        value=f"Confirmed kills: **{lore['kills']}** victims",
        inline=True
    )
    
    lore_embed.add_field(
        name="WEAKNESS",
        value=f"Despite their power, they remain {lore['weakness']}.",
        inline=False
    )
    
    if newly_revealed:
        lore_embed.add_field(
            name="LORE BONUS UNLOCKED",
            value=f"Knowledge of {vampire['name']}'s history grants **5-15% power boost** in battles!\nEffective in both solo fights and gang wars.",
            inline=False
        )
    else:
        lore_embed.add_field(
            name="LORE BONUS ACTIVE",
            value=f"Combat bonus already unlocked: **5-15% power boost** in battles",
            inline=False
        )
    
    lore_embed.set_footer(text=f"Current Power: {vampire['power_level']} | Record: {vampire.get('wins', 0)}-{vampire.get('losses', 0)}")
    
    await ctx.send(embed=lore_embed)

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
        
        # Check lore status
        lore_revealed = False
        if 'lore' in vamp:
            lore_revealed = vamp['lore'].get('lore_revealed', False)
        
        # Determine tier
        power = vamp['power_level']
        if power <= 400:
            tier = "Fledgling"
        elif power <= 1000:
            tier = "Experienced"
        elif power <= 1600:
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
        lore_status = "Revealed" if lore_revealed else "Hidden"
        
        value_text = (
            f"**ID:** `{vamp['character_id']}`\n"
            f"**Power:** {vamp['power_level']}\n"
            f"**Tier:** {tier}\n"
            f"**Record:** {wins}-{losses}\n"
            f"**Status:** {status}\n"
            f"**Lore:** {lore_status}\n"
            f"**Rebirth:** {rebirth_eligible}"
        )
        
        embed.add_field(
            name=f"{vamp['name']}",
            value=value_text,
            inline=True
        )
    
    embed.set_footer(text="Use ?lore <id> to reveal backstory | ?gang for group battles | ?fight <id> for solo")
    
    await ctx.send(embed=embed)

# Gang command - Group battle with lore bonuses
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
    
    # Calculate total gang power with lore bonuses
    player_gang_power = 0
    lore_bonus_count = 0
    
    for vamp in user_vampires:
        base_power = vamp['power_level']
        if 'lore' in vamp and vamp['lore'].get('lore_revealed', False):
            # Apply lore bonus
            lore_bonus_multiplier = random.uniform(1.05, 1.15)
            effective_power = int(base_power * lore_bonus_multiplier)
            player_gang_power += effective_power
            lore_bonus_count += 1
        else:
            player_gang_power += base_power
    
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
        lore_indicator = " [LORE]" if 'lore' in vamp and vamp['lore'].get('lore_revealed', False) else ""
        player_gang_text += f"**{vamp['name']}**{lore_indicator} - Power: {vamp['power_level']}\n"
    
    intro_embed.add_field(
        name=f"YOUR GANG ({len(user_vampires)} vampires)",
        value=f"{player_gang_text}\n**Total Power: {player_gang_power}**",
        inline=False
    )
    
    if lore_bonus_count > 0:
        intro_embed.add_field(
            name="Lore Advantage",
            value=f"{lore_bonus_count} vampire(s) with revealed lore gain combat bonuses!",
            inline=False
        )
    
    # AI gang info - truncate if too large
    ai_gang_text = ""
    display_limit = 10
    
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
    
    if power_diff > 2000:
        threat_level = "EASY TARGET"
        threat_color = discord.Color.dark_green()
    elif power_diff > 1000:
        threat_level = "FAVORABLE MATCHUP"
        threat_color = discord.Color.green()
    elif power_diff > -1000:
        threat_level = "EVEN MATCH"
        threat_color = discord.Color.gold()
    elif power_diff > -2000:
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
        ai_gang_power,
        lore_revealed=True  # Gang has lore advantage if any member has it
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
        
        if battle_result.get('lore_bonus_applied'):
            outcome_embed.add_field(
                name="Lore Bonus Applied",
                value=f"Revealed lore provided strategic advantage in battle!",
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

# Fight command - Battle against AI vampires with lore bonus
@bot.command(name='fight')
async def fight_character(ctx, character_id: str = None):
    """Fight an AI vampire opponent. Usage: ?fight <character_id>"""
    
    if character_id is None:
        await ctx.send("Usage: `?fight <character_id>`\nExample: `?fight 123456`")
        return
    
    if character_id not in characters:
        await ctx.send(f"Vampire ID `{character_id}` not found!")
        return
    
    player_char = characters[character_id]
    user_id = str(ctx.author.id)
    
    if player_char.get('user_id') != user_id:
        await ctx.send("You don't own this vampire!")
        return
    
    # Check lore status
    lore_revealed = False
    if 'lore' in player_char:
        lore_revealed = player_char['lore'].get('lore_revealed', False)
    
    # Generate COMPLETELY RANDOM AI opponent (10-2000)
    ai_power = generate_ai_power()
    
    ai_first_name = random.choice(FIRST_NAMES)
    ai_last_name = random.choice(LAST_NAMES)
    ai_name = f"{ai_first_name} {ai_last_name}"
    
    # Determine power difference for threat level
    effective_power = player_char['power_level']
    if lore_revealed:
        effective_power = int(player_char['power_level'] * random.uniform(1.05, 1.15))
    
    power_diff = ai_power - effective_power
    
    if power_diff > 600:
        threat_level = "EXTREMELY DANGEROUS OPPONENT"
        threat_color = discord.Color.dark_red()
    elif power_diff > 300:
        threat_level = "DANGEROUS OPPONENT"
        threat_color = discord.Color.red()
    elif power_diff > 100:
        threat_level = "TOUGH CHALLENGER"
        threat_color = discord.Color.orange()
    elif power_diff > -100:
        threat_level = "EVEN MATCH"
        threat_color = discord.Color.gold()
    elif power_diff > -300:
        threat_level = "FAVORABLE MATCHUP"
        threat_color = discord.Color.green()
    else:
        threat_level = "EASY TARGET"
        threat_color = discord.Color.dark_green()
    
    # Determine AI tier
    if ai_power <= 400:
        ai_tier = "Fledgling"
    elif ai_power <= 1000:
        ai_tier = "Experienced"
    elif ai_power <= 1600:
        ai_tier = "Ancient"
    else:
        ai_tier = "Primordial"
    
    # Battle intro embed
    intro_embed = discord.Embed(
        title="BLOOD BATTLE",
        description=f"**{player_char['name']}** encounters **{ai_name}** in the darkness\n\n{threat_level}",
        color=threat_color
    )
    
    lore_indicator = " [LORE BONUS]" if lore_revealed else ""
    
    intro_embed.add_field(
        name=f"{player_char['name']} (YOU)",
        value=f"Power: **{player_char['power_level']}**{lore_indicator}\nRecord: {player_char.get('wins', 0)}-{player_char.get('losses', 0)}",
        inline=True
    )
    
    intro_embed.add_field(
        name=f"{ai_name} (ENEMY)",
        value=f"Power: **{ai_power}**\nTier: {ai_tier}",
        inline=True
    )
    
    if lore_revealed:
        intro_embed.add_field(
            name="Strategic Advantage",
            value="Knowledge of your vampire's lore grants combat bonus!",
            inline=False
        )
    
    intro_embed.set_footer(text="The battle begins...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)
    
    # Simulate the battle with lore bonus
    battle_result = simulate_battle(
        player_char['name'], 
        player_char['power_level'],
        ai_name,
        ai_power,
        lore_revealed=lore_revealed
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
            
            if not player_char.get('has_been_reborn', False):
                outcome_embed.set_footer(text=f"Use ?rebirth {character_id} to bring them back")
            else:
                outcome_embed.set_footer(text="This vampire has already been reborn once and cannot be resurrected again")
            
            dead_vampire = player_char.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = f"{ai_name} (Fatal Wounds)"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            
            del characters[character_id]
            save_characters(characters)
            
        else:
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
            
            if battle_result.get('lore_bonus_applied'):
                outcome_embed.add_field(
                    name="Lore Bonus Applied",
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
        if vampire_dies:
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
            
            if not player_char.get('has_been_reborn', False):
                outcome_embed.set_footer(text=f"Use ?rebirth {character_id} to bring them back")
            else:
                outcome_embed.set_footer(text="This vampire has already been reborn once and cannot be resurrected again")
            
            dead_vampire = player_char.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = ai_name
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            
            del characters[character_id]
            save_characters(characters)
            
        else:
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

# Revenge command - Battle the AI vampire that killed your vampire
@bot.command(name='revenge')
async def revenge_battle(ctx, dead_character_id: str = None, avenger_character_id: str = None):
    """Take revenge on the AI that killed your vampire. Usage: ?revenge <dead_vampire_id> <avenger_vampire_id>"""
    
    if dead_character_id is None or avenger_character_id is None:
        await ctx.send("Usage: `?revenge <dead_vampire_id> <avenger_vampire_id>`\nExample: `?revenge 123456 789012`\n\nUse the ID of your dead vampire and the ID of the vampire you want to use for revenge!")
        return
    
    user_id = str(ctx.author.id)
    
    # Check if avenger vampire exists and is owned by user
    if avenger_character_id not in characters:
        await ctx.send(f"Avenger vampire ID `{avenger_character_id}` not found!")
        return
    
    avenger_char = characters[avenger_character_id]
    
    if avenger_char.get('user_id') != user_id:
        await ctx.send("You don't own this avenger vampire!")
        return
    
    # Find the dead vampire in graveyard
    current_graveyard = load_graveyard()
    
    dead_vampire = None
    for vamp in current_graveyard:
        if vamp.get('character_id') == dead_character_id:
            dead_vampire = vamp
            break
    
    if dead_vampire is None:
        await ctx.send(f"No dead vampire with ID `{dead_character_id}` found in the graveyard!")
        return
    
    if dead_vampire.get('user_id') != user_id:
        await ctx.send("The dead vampire doesn't belong to you!")
        return
    
    # Check if the vampire was killed by an AI (not gang war or ritual)
    killer_name = dead_vampire.get('killed_by', 'Unknown')
    
    if killer_name == "Gang War":
        await ctx.send(f"**{dead_vampire['name']}** was killed in a gang war, not by a specific AI vampire. Revenge is not available for gang war deaths.")
        return
    
    if killer_name == "Blood Transfer Ritual":
        await ctx.send(f"**{dead_vampire['name']}** was sacrificed in a blood transfer ritual. Revenge is not available for ritual sacrifices.")
        return
    
    if "(Fatal Wounds)" in killer_name:
        # Extract the actual killer name
        killer_name = killer_name.replace(" (Fatal Wounds)", "").strip()
    
    # Recreate the AI opponent with the same name but new random power
    ai_power = generate_ai_power()
    
    # Check lore status of avenger
    lore_revealed = False
    if 'lore' in avenger_char:
        lore_revealed = avenger_char['lore'].get('lore_revealed', False)
    
    # Determine power difference for threat level
    effective_power = avenger_char['power_level']
    if lore_revealed:
        effective_power = int(avenger_char['power_level'] * random.uniform(1.05, 1.15))
    
    power_diff = ai_power - effective_power
    
    if power_diff > 600:
        threat_level = "EXTREMELY DANGEROUS OPPONENT"
        threat_color = discord.Color.dark_red()
    elif power_diff > 300:
        threat_level = "DANGEROUS OPPONENT"
        threat_color = discord.Color.red()
    elif power_diff > 100:
        threat_level = "TOUGH CHALLENGER"
        threat_color = discord.Color.orange()
    elif power_diff > -100:
        threat_level = "EVEN MATCH"
        threat_color = discord.Color.gold()
    elif power_diff > -300:
        threat_level = "FAVORABLE MATCHUP"
        threat_color = discord.Color.green()
    else:
        threat_level = "EASY TARGET"
        threat_color = discord.Color.dark_green()
    
    # Determine AI tier
    if ai_power <= 400:
        ai_tier = "Fledgling"
    elif ai_power <= 1000:
        ai_tier = "Experienced"
    elif ai_power <= 1600:
        ai_tier = "Ancient"
    else:
        ai_tier = "Primordial"
    
    # Revenge intro embed
    intro_embed = discord.Embed(
        title="REVENGE BATTLE",
        description=f"**{avenger_char['name']}** seeks vengeance for the death of **{dead_vampire['name']}**\n\nThe killer, **{killer_name}**, emerges from the shadows...\n\n{threat_level}",
        color=threat_color
    )
    
    lore_indicator = " [LORE BONUS]" if lore_revealed else ""
    
    intro_embed.add_field(
        name=f"{avenger_char['name']} (AVENGER)",
        value=f"Power: **{avenger_char['power_level']}**{lore_indicator}\nRecord: {avenger_char.get('wins', 0)}-{avenger_char.get('losses', 0)}",
        inline=True
    )
    
    intro_embed.add_field(
        name=f"{killer_name} (KILLER)",
        value=f"Power: **{ai_power}**\nTier: {ai_tier}",
        inline=True
    )
    
    intro_embed.add_field(
        name="Fallen Comrade",
        value=f"{dead_vampire['name']} (Power: {dead_vampire['power_level']})\nKilled on: {dead_vampire.get('death_date', 'Unknown')}",
        inline=False
    )
    
    if lore_revealed:
        intro_embed.add_field(
            name="Strategic Advantage",
            value="Knowledge of your vampire's lore grants combat bonus!",
            inline=False
        )
    
    intro_embed.set_footer(text="The battle for revenge begins...")
    
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)
    
    # Simulate the revenge battle with lore bonus
    battle_result = simulate_battle(
        avenger_char['name'], 
        avenger_char['power_level'],
        killer_name,
        ai_power,
        lore_revealed=lore_revealed
    )
    
    player_won = battle_result['player_won']
    
    # Calculate death chance
    death_chance = calculate_death_chance(
        avenger_char['power_level'],
        ai_power,
        player_won
    )
    
    # Roll for death
    death_roll = random.randint(1, 100)
    vampire_dies = death_roll <= death_chance
    
    # Outcome embed
    if player_won:
        if vampire_dies:
            outcome_embed = discord.Embed(
                title="REVENGE ACHIEVED - BUT AT A COST",
                description=f"**{avenger_char['name']}** destroyed **{killer_name}**, avenging **{dead_vampire['name']}**, but succumbed to fatal wounds",
                color=discord.Color.dark_red()
            )
            
            outcome_embed.add_field(
                name="Battle Odds",
                value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
                inline=False
            )
            
            if battle_result.get('lore_bonus_applied'):
                outcome_embed.add_field(
                    name="Lore Bonus Applied",
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
                value=f"{avenger_char['name']} fulfilled their vendetta but paid the ultimate price",
                inline=False
            )
            
            outcome_embed.add_field(
                name="Final Record",
                value=f"{avenger_char.get('wins', 0)}-{avenger_char.get('losses', 0)}",
                inline=False
            )
            
            if not avenger_char.get('has_been_reborn', False):
                outcome_embed.set_footer(text=f"Use ?rebirth {avenger_character_id} to bring them back")
            else:
                outcome_embed.set_footer(text="This vampire has already been reborn once and cannot be resurrected again")
            
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
                description=f"**{avenger_char['name']}** has destroyed **{killer_name}**, avenging **{dead_vampire['name']}**!",
                color=discord.Color.green()
            )
            
            outcome_embed.add_field(
                name="Battle Odds",
                value=f"Win Probability: {battle_result['win_probability']}%\nRolled: {battle_result['roll']}",
                inline=False
            )
            
            if battle_result.get('lore_bonus_applied'):
                outcome_embed.add_field(
                    name="Lore Bonus Applied",
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
                value=f"{dead_vampire['name']} has been avenged! {killer_name} has been destroyed!",
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
        if vampire_dies:
            outcome_embed = discord.Embed(
                title="REVENGE FAILED - PERMANENT DEATH",
                description=f"**{avenger_char['name']}** has been destroyed by **{killer_name}**\n\n{dead_vampire['name']} remains unavenged...",
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
                name="The End",
                value=f"{avenger_char['name']} fell to the same killer that destroyed {dead_vampire['name']}",
                inline=False
            )
            
            if not avenger_char.get('has_been_reborn', False):
                outcome_embed.set_footer(text=f"Use ?rebirth {avenger_character_id} to bring them back")
            else:
                outcome_embed.set_footer(text="This vampire has already been reborn once and cannot be resurrected again")
            
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
                description=f"**{avenger_char['name']}** was defeated by **{killer_name}** but managed to escape\n\n{dead_vampire['name']} remains unavenged...",
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
            
            outcome_embed.set_footer(text=f"{avenger_char['name']} fled into the shadows, wounded and defeated")
    
    await ctx.send(embed=outcome_embed)

# Transfer command - Sacrifice two vampires to create a hybrid
@bot.command(name='transfer')
async def transfer_vampires(ctx, vampire1_id: str = None, vampire2_id: str = None):
    """Sacrifice two of your vampires to create a powerful hybrid. Usage: ?transfer <id1> <id2>"""
    
    if vampire1_id is None or vampire2_id is None:
        await ctx.send("Usage: `?transfer <vampire1_id> <vampire2_id>`\nExample: `?transfer 123456 789012`\n\nBoth vampires will be sacrificed to create a powerful hybrid!")
        return
    
    if vampire1_id == vampire2_id:
        await ctx.send("You cannot transfer a vampire with itself!")
        return
    
    user_id = str(ctx.author.id)
    
    if vampire1_id not in characters:
        await ctx.send(f"Vampire ID `{vampire1_id}` not found!")
        return
    
    if vampire2_id not in characters:
        await ctx.send(f"Vampire ID `{vampire2_id}` not found!")
        return
    
    vampire1 = characters[vampire1_id]
    vampire2 = characters[vampire2_id]
    
    if vampire1.get('user_id') != user_id:
        await ctx.send(f"You don't own the vampire with ID `{vampire1_id}`!")
        return
    
    if vampire2.get('user_id') != user_id:
        await ctx.send(f"You don't own the vampire with ID `{vampire2_id}`!")
        return
    
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
    
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    hybrid_name = f"{first_name} {last_name}"
    
    hybrid_id = generate_unique_id()
    
    combined_power = vampire1['power_level'] + vampire2['power_level']
    ritual_bonus = random.randint(200, 600)
    hybrid_power = combined_power + ritual_bonus
    
    if hybrid_power > 2000:
        hybrid_power = 2000
        actual_bonus = 2000 - combined_power
    else:
        actual_bonus = ritual_bonus
    
    total_wins = vampire1.get('wins', 0) + vampire2.get('wins', 0)
    total_losses = 0
    
    has_been_reborn = vampire1.get('has_been_reborn', False) or vampire2.get('has_been_reborn', False)
    
    # Generate hybrid lore
    hybrid_lore = generate_vampire_lore(hybrid_name, hybrid_power)
    
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
        "lore": hybrid_lore,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
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
    
    del characters[vampire1_id]
    del characters[vampire2_id]
    
    characters[hybrid_id] = hybrid_data
    save_characters(characters)
    
    if hybrid_power <= 400:
        tier = "Fledgling"
        tier_color = discord.Color.dark_grey()
    elif hybrid_power <= 1000:
        tier = "Experienced"
        tier_color = discord.Color.blue()
    elif hybrid_power <= 1600:
        tier = "Ancient"
        tier_color = discord.Color.purple()
    else:
        tier = "Primordial"
        tier_color = discord.Color.gold()
    
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
    
    success_embed.add_field(
        name="New Lore",
        value=f"Use `?lore {hybrid_id}` to discover the hybrid's dark history",
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

# Rebirth command - Bring a dead vampire back to life with more power (ONE TIME ONLY)
@bot.command(name='rebirth')
async def rebirth_vampire(ctx, character_id: str = None):
    """Resurrect a fallen vampire with increased power (ONE TIME ONLY). Usage: ?rebirth <character_id>"""
    
    if character_id is None:
        await ctx.send("Usage: `?rebirth <character_id>`\nExample: `?rebirth 123456`")
        return
    
    user_id = str(ctx.author.id)
    
    current_graveyard = load_graveyard()
    
    dead_vampire = None
    graveyard_index = None
    
    for idx, vamp in enumerate(current_graveyard):
        if vamp.get('character_id') == character_id:
            dead_vampire = vamp
            graveyard_index = idx
            break
    
    if dead_vampire is None:
        await ctx.send(f"No dead vampire with ID `{character_id}` found in the graveyard!")
        return
    
    if dead_vampire.get('user_id') != user_id:
        await ctx.send("You don't own this vampire!")
        return
    
    if dead_vampire.get('has_been_reborn', False):
        await ctx.send(f"**{dead_vampire['name']}** has already been reborn once and cannot be resurrected again!\n\nEach vampire can only be reborn ONE time. Use `?make` to create a new vampire.")
        return
    
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
    
    base_boost = random.randint(200, 500)
    percentage_boost = int(dead_vampire['power_level'] * 0.15)
    total_boost = base_boost + percentage_boost
    
    new_power = dead_vampire['power_level'] + total_boost
    
    if new_power > 2000:
        new_power = 2000
        total_boost = 2000 - dead_vampire['power_level']
    
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
        "lore": dead_vampire.get('lore', {}),
        "original_id": character_id,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "reborn_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if dead_vampire.get('is_hybrid', False):
        reborn_data['parent1_name'] = dead_vampire.get('parent1_name')
        reborn_data['parent2_name'] = dead_vampire.get('parent2_name')
        reborn_data['parent1_id'] = dead_vampire.get('parent1_id')
        reborn_data['parent2_id'] = dead_vampire.get('parent2_id')
    
    characters[new_character_id] = reborn_data
    save_characters(characters)
    
    current_graveyard.pop(graveyard_index)
    save_graveyard(current_graveyard)
    
    if new_power <= 400:
        tier = "Fledgling"
        tier_color = discord.Color.dark_grey()
    elif new_power <= 1000:
        tier = "Experienced"
        tier_color = discord.Color.blue()
    elif new_power <= 1600:
        tier = "Ancient"
        tier_color = discord.Color.purple()
    else:
        tier = "Primordial"
        tier_color = discord.Color.gold()
    
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
    
    # Check if lore was revealed
    if 'lore' in dead_vampire and dead_vampire['lore'].get('lore_revealed', False):
        success_embed.add_field(
            name="Lore Preserved",
            value="Ancient knowledge retained through rebirth - combat bonus still active!",
            inline=False
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
