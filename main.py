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
    return ctx.author.guild_permissions.administrator

# Check if member is in jail
def is_in_jail(member):
    if 'jail_until' not in member:
        return False
    jail_until = datetime.strptime(member['jail_until'], '%Y-%m-%d %H:%M:%S')
    return datetime.now() < jail_until

# Get remaining jail time
def get_jail_time_remaining(member):
    if 'jail_until' not in member:
        return None
    jail_until = datetime.strptime(member['jail_until'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    if now >= jail_until:
        return None
    return jail_until - now

# Simulate instant street battle
def simulate_battle():
    roll = random.randint(1, 100)
    return {"player_won": roll <= 50, "roll": roll}

# Calculate death chance
def calculate_death_chance(player_won):
    return 15 if player_won else 40

# Generate a random rival name and gang
def generate_rival():
    rival_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    rival_gang = random.choice(list(LA_GANGS.keys()))
    rival_set = random.choice(LA_GANGS[rival_gang]['sets'])
    return rival_name, rival_gang, rival_set


# Handle random street event after a kill
async def trigger_post_kill_event(ctx, player_char, rival_name, rival_gang, rival_set, character_id):
    await asyncio.sleep(3)

    characters = load_characters()
    graveyard = load_graveyard()

    if character_id not in characters:
        return

    player_char = characters[character_id]

    event_roll = random.randint(1, 100)
    if event_roll > 40:
        return

    event_type = random.choice([
        "retaliation_crew",
        "witness_calls_police",
        "rival_solo_retaliation",
        "bounty_placed",
        "jumped_walking_home"
    ])

    if event_type == "retaliation_crew":
        num_attackers = random.randint(3, 6)
        attacker_names = [f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" for _ in range(num_attackers)]

        event_embed = discord.Embed(
            title="RETALIATION - RIVALS INCOMING",
            description=f"Word got back to the {rival_set} that {player_char['name']} just bodied one of theirs. A crew just pulled up looking for smoke.",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="CREW PULLING UP", value="\n".join(attacker_names), inline=False)
        event_embed.add_field(name="Rival Gang", value=f"{rival_gang} - {rival_set}", inline=True)
        event_embed.set_footer(text="They came for payback...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        survival_roll = random.randint(1, 100)
        survives = survival_roll <= 45
        death_roll = random.randint(1, 100)
        dies = death_roll <= 50 if not survives else death_roll <= 10

        if dies:
            death_embed = discord.Embed(
                title="OUTNUMBERED AND OUTGUNNED",
                description=f"{player_char['name']} was caught slipping by the retaliation crew and didn't make it out",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_set} Retaliation Crew"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            characters = load_characters()
            if character_id in characters:
                del characters[character_id]
                save_characters(characters)
            await ctx.send(embed=death_embed)
        else:
            survive_embed = discord.Embed(
                title="HELD IT DOWN",
                description=f"{player_char['name']} stood their ground against the retaliation crew and made it out",
                color=discord.Color.orange()
            )
            survive_embed.add_field(name="Outcome", value=f"Fought off {num_attackers} rivals and lived to tell the story", inline=False)
            survive_embed.set_footer(text="The streets respect the ones who hold it down")
            await ctx.send(embed=survive_embed)

    elif event_type == "witness_calls_police":
        event_embed = discord.Embed(
            title="WITNESS SNITCHED",
            description=f"Someone saw what {player_char['name']} did and called the police. Units are closing in.",
            color=discord.Color.blue()
        )
        event_embed.add_field(name="Police Response", value="Multiple units dispatched to the area based on witness description", inline=False)
        event_embed.set_footer(text="Can they escape in time...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        escape_roll = random.randint(1, 100)
        escapes = escape_roll <= 55

        if escapes:
            escape_embed = discord.Embed(
                title="CLEAN ESCAPE",
                description=f"{player_char['name']} heard the sirens and dipped before police could lock the area down",
                color=discord.Color.green()
            )
            escape_embed.add_field(name="Status", value="Made it back to the hood, police have no description", inline=False)
            await ctx.send(embed=escape_embed)
        else:
            jail_time = random.randint(15, 35)
            jail_embed = discord.Embed(
                title="CAUGHT BY POLICE",
                description=f"{player_char['name']} was picked up by police based on the witness description",
                color=discord.Color.orange()
            )
            jail_embed.add_field(name="Arrest Status", value=f"Booked and sentenced to {jail_time} minutes in county jail", inline=False)
            jail_until = datetime.now() + timedelta(minutes=jail_time)
            characters = load_characters()
            if character_id in characters:
                characters[character_id]['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
                save_characters(characters)
            await ctx.send(embed=jail_embed)

    elif event_type == "rival_solo_retaliation":
        solo_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        event_embed = discord.Embed(
            title="SOLO RETALIATION",
            description=f"{solo_name} from the {rival_set} just rolled up on {player_char['name']} alone. He came to handle business himself.",
            color=discord.Color.red()
        )
        event_embed.add_field(name="One on One", value=f"{solo_name} is out here solo, no backup - just him and his anger", inline=False)
        event_embed.set_footer(text="Settling it the old way...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle()
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(won)

        characters = load_characters()
        if character_id not in characters:
            return
        player_char = characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="HANDLED THE RETALIATION",
                description=f"{player_char['name']} bodied {solo_name} when he came for payback",
                color=discord.Color.green()
            )
            player_char['kills'] = player_char.get('kills', 0) + 1
            if 'kill_list' not in player_char:
                player_char['kill_list'] = []
            player_char['kill_list'].append({
                'victim_name': solo_name,
                'victim_gang': rival_gang,
                'victim_set': rival_set,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'retaliation_defense'
            })
            win_embed.add_field(name="Updated Bodies", value=f"Total Bodies: {player_char['kills']}", inline=False)
            characters[character_id] = player_char
            save_characters(characters)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="GOT CAUGHT LACKING",
                description=f"{solo_name} caught {player_char['name']} slipping and put him down",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{solo_name} ({rival_set}) Solo Retaliation"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del characters[character_id]
            save_characters(characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="GOT BEAT BUT SURVIVED",
                description=f"{solo_name} got the better of {player_char['name']} but let him live",
                color=discord.Color.orange()
            )
            loss_embed.add_field(name="Outcome", value="Lost the fight but made it out breathing", inline=False)
            await ctx.send(embed=loss_embed)

    elif event_type == "bounty_placed":
        bounty_amount = random.randint(500, 3000)
        event_embed = discord.Embed(
            title="BOUNTY ON YOUR HEAD",
            description=f"The {rival_set} put a ${bounty_amount:,} bounty on {player_char['name']} for the body",
            color=discord.Color.gold()
        )
        event_embed.add_field(name="Bounty Amount", value=f"${bounty_amount:,}", inline=True)
        event_embed.add_field(name="Placed By", value=f"{rival_set}", inline=True)
        event_embed.add_field(name="Warning", value=f"Everyone in the streets knows there is paper on {player_char['name']} - watch your back", inline=False)
        event_embed.set_footer(text="The price of putting in work")
        characters = load_characters()
        if character_id in characters:
            characters[character_id]['bounty'] = characters[character_id].get('bounty', 0) + bounty_amount
            save_characters(characters)
        await ctx.send(embed=event_embed)

    elif event_type == "jumped_walking_home":
        num_jumpers = random.randint(2, 5)
        event_embed = discord.Embed(
            title="JUMPED WALKING HOME",
            description=f"{player_char['name']} got rushed by {num_jumpers} opps on the way back from the hit",
            color=discord.Color.red()
        )
        event_embed.add_field(name="Ambush", value=f"They were waiting, knew the route - {num_jumpers} on one", inline=False)
        event_embed.set_footer(text="Nowhere to run...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        survival_roll = random.randint(1, 100)
        survives = survival_roll <= 50
        death_roll = random.randint(1, 100)
        dies = death_roll <= 35 if not survives else death_roll <= 8

        characters = load_characters()
        if character_id not in characters:
            return
        player_char = characters[character_id]

        if dies:
            death_embed = discord.Embed(
                title="JUMPED AND KILLED",
                description=f"{player_char['name']} was jumped and beaten to death by the crew",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_set} Jump (Post Kill)"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del characters[character_id]
            save_characters(characters)
            await ctx.send(embed=death_embed)
        elif survives:
            survive_embed = discord.Embed(
                title="FOUGHT THROUGH THE JUMP",
                description=f"{player_char['name']} got jumped but scrapped their way out and made it home",
                color=discord.Color.orange()
            )
            survive_embed.add_field(name="Outcome", value="Banged up but alive - made it back to the block", inline=False)
            await ctx.send(embed=survive_embed)
        else:
            survive_embed = discord.Embed(
                title="BARELY ESCAPED THE JUMP",
                description=f"{player_char['name']} broke away from the jump and ran before it got worse",
                color=discord.Color.orange()
            )
            survive_embed.add_field(name="Outcome", value="Took some hits but got away before things went fatal", inline=False)
            await ctx.send(embed=survive_embed)


async def trigger_passive_event(ctx, player_char, character_id):
    await asyncio.sleep(random.randint(8, 15))

    characters = load_characters()
    if character_id not in characters:
        return

    player_char = characters[character_id]
    graveyard = load_graveyard()
    char_gang = player_char.get('gang_affiliation', 'Unknown')

    event_roll = random.randint(1, 100)
    if event_roll > 30:
        return

    event_type = random.choice([
        "drive_by_on_block",
        "found_cash_on_street",
        "police_raid_area",
        "homie_in_trouble",
        "drug_deal_gone_wrong",
        "shot_at_while_walking",
        "rival_tags_your_hood",
        "unexpected_confrontation"
    ])

    if event_type == "drive_by_on_block":
        rival_name, rival_gang, rival_set = generate_rival()
        event_embed = discord.Embed(
            title="DRIVE BY ON THE BLOCK",
            description=f"Out of nowhere a car from the {rival_set} just sprayed the block where {player_char['name']} was posted",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="Shooter", value=f"{rival_name} - {rival_set}", inline=True)
        event_embed.add_field(name="Situation", value="Shots fired with no warning - had to react fast", inline=True)
        event_embed.set_footer(text="The block is never safe...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        hit_roll = random.randint(1, 100)
        gets_hit = hit_roll <= 30

        characters = load_characters()
        if character_id not in characters:
            return
        player_char = characters[character_id]

        if gets_hit:
            death_roll = random.randint(1, 100)
            if death_roll <= 50:
                death_embed = discord.Embed(
                    title="HIT BY THE DRIVE BY",
                    description=f"{player_char['name']} was struck by bullets in the drive by and didn't survive",
                    color=discord.Color.dark_red()
                )
                death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
                dead_member = player_char.copy()
                dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_member['killed_by'] = f"{rival_set} Drive By (Passive Event)"
                graveyard.append(dead_member)
                save_graveyard(graveyard)
                del characters[character_id]
                save_characters(characters)
                await ctx.send(embed=death_embed)
            else:
                wound_embed = discord.Embed(
                    title="WOUNDED BUT ALIVE",
                    description=f"{player_char['name']} got hit in the drive by but the wounds are not fatal",
                    color=discord.Color.orange()
                )
                wound_embed.add_field(name="Status", value="Took a bullet but survived - heading to get patched up", inline=False)
                await ctx.send(embed=wound_embed)
        else:
            safe_embed = discord.Embed(
                title="DOVE FOR COVER",
                description=f"{player_char['name']} hit the ground when the shots rang out and avoided getting hit",
                color=discord.Color.green()
            )
            safe_embed.add_field(name="Outcome", value="Bullets missed - made it out clean", inline=False)
            await ctx.send(embed=safe_embed)

    elif event_type == "found_cash_on_street":
        cash_found = random.randint(50, 500)
        characters = load_characters()
        if character_id not in characters:
            return
        player_char = characters[character_id]
        player_char['money'] = player_char.get('money', 0) + cash_found
        characters[character_id] = player_char
        save_characters(characters)
        event_embed = discord.Embed(
            title="FOUND SOMETHING ON THE STREET",
            description=f"{player_char['name']} was walking through the hood and found a dropped envelope",
            color=discord.Color.green()
        )
        event_embed.add_field(name="Contents", value=f"${cash_found:,} cash inside - no name, no questions", inline=True)
        event_embed.add_field(name="New Balance", value=f"${player_char['money']:,}", inline=True)
        event_embed.set_footer(text="Streets provide sometimes")
        await ctx.send(embed=event_embed)

    elif event_type == "police_raid_area":
        event_embed = discord.Embed(
            title="POLICE SWEEPING THE AREA",
            description=f"LAPD gang unit is doing a sweep through {player_char.get('set_name', 'the hood')} territory right now",
            color=discord.Color.blue()
        )
        event_embed.add_field(name="Police Activity", value="Multiple units rolling through, stopping and questioning everyone on the block", inline=False)
        event_embed.set_footer(text="Lay low or get caught up...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        caught_roll = random.randint(1, 100)
        characters = load_characters()
        if character_id not in characters:
            return
        player_char = characters[character_id]

        if caught_roll <= 20:
            jail_time = random.randint(5, 20)
            jail_embed = discord.Embed(
                title="SWEPT UP IN THE RAID",
                description=f"{player_char['name']} got caught in the police sweep and taken in",
                color=discord.Color.orange()
            )
            jail_embed.add_field(name="Detention", value=f"Held for {jail_time} minutes before being released", inline=False)
            jail_until = datetime.now() + timedelta(minutes=jail_time)
            characters[character_id]['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
            save_characters(characters)
            await ctx.send(embed=jail_embed)
        else:
            clear_embed = discord.Embed(
                title="STAYED LOW DURING THE SWEEP",
                description=f"{player_char['name']} saw the police coming and got off the block in time",
                color=discord.Color.green()
            )
            clear_embed.add_field(name="Outcome", value="Avoided the sweep - back to normal", inline=False)
            await ctx.send(embed=clear_embed)

    elif event_type == "homie_in_trouble":
        homie_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        rival_name, rival_gang, rival_set = generate_rival()
        event_embed = discord.Embed(
            title="HOMIE NEEDS BACKUP",
            description=f"{homie_name} from the {player_char.get('set_name', 'set')} just called - he is pinned down by {rival_set} and needs help right now",
            color=discord.Color.orange()
        )
        event_embed.add_field(name="The Call", value=f"{homie_name} is outnumbered and calling for backup in enemy territory", inline=False)
        event_embed.set_footer(text="You ride for your homies...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle()
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(won)

        characters = load_characters()
        if character_id not in characters:
            return
        player_char = characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="HOMIE SAVED",
                description=f"{player_char['name']} ran to the aid of {homie_name} and helped fight off the {rival_set}",
                color=discord.Color.green()
            )
            bonus_money = random.randint(100, 300)
            player_char['money'] = player_char.get('money', 0) + bonus_money
            win_embed.add_field(name="Loyalty Reward", value=f"{homie_name} hit {player_char['name']} with ${bonus_money:,} for pulling up", inline=False)
            characters[character_id] = player_char
            save_characters(characters)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="DIED RIDING FOR THE HOMIES",
                description=f"{player_char['name']} gave their life pulling up for {homie_name}",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_set} (Died Riding for Homies)"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del characters[character_id]
            save_characters(characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="BACKUP CAME BUT LOST THE FIGHT",
                description=f"{player_char['name']} pulled up for {homie_name} but they both had to retreat",
                color=discord.Color.orange()
            )
            loss_embed.add_field(name="Outcome", value=f"Both made it out alive but the {rival_set} held the block tonight", inline=False)
            await ctx.send(embed=loss_embed)

    elif event_type == "drug_deal_gone_wrong":
        rival_name, rival_gang, rival_set = generate_rival()
        event_embed = discord.Embed(
            title="DEAL WENT SIDEWAYS",
            description=f"{player_char['name']} was present when a deal in the hood went completely wrong",
            color=discord.Color.red()
        )
        event_embed.add_field(name="The Situation", value="Someone tried to rob the deal - shots fired, everyone scattering", inline=False)
        event_embed.set_footer(text="Wrong place wrong time...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        outcome_roll = random.randint(1, 100)
        characters = load_characters()
        if character_id not in characters:
            return
        player_char = characters[character_id]

        if outcome_roll <= 40:
            money_lost = random.randint(100, max(100, player_char.get('money', 100)))
            money_lost = min(money_lost, player_char.get('money', 0))
            player_char['money'] = max(0, player_char.get('money', 0) - money_lost)
            loss_embed = discord.Embed(
                title="ROBBED IN THE CHAOS",
                description=f"{player_char['name']} got robbed during the confusion",
                color=discord.Color.red()
            )
            loss_embed.add_field(name="Money Lost", value=f"${money_lost:,} taken", inline=True)
            loss_embed.add_field(name="New Balance", value=f"${player_char['money']:,}", inline=True)
            characters[character_id] = player_char
            save_characters(characters)
            await ctx.send(embed=loss_embed)
        elif outcome_roll <= 70:
            safe_embed = discord.Embed(
                title="GOT OUT OF THE CHAOS",
                description=f"{player_char['name']} dipped when the deal went wrong and avoided the fallout",
                color=discord.Color.green()
            )
            safe_embed.add_field(name="Outcome", value="Made it out clean - nothing lost", inline=False)
            await ctx.send(embed=safe_embed)
        else:
            profit = random.randint(200, 800)
            player_char['money'] = player_char.get('money', 0) + profit
            profit_embed = discord.Embed(
                title="CAME UP IN THE CHAOS",
                description=f"{player_char['name']} moved smart during the confusion and walked away with something",
                color=discord.Color.green()
            )
            profit_embed.add_field(name="Street Profit", value=f"${profit:,} picked up in the chaos", inline=True)
            profit_embed.add_field(name="New Balance", value=f"${player_char['money']:,}", inline=True)
            characters[character_id] = player_char
            save_characters(characters)
            await ctx.send(embed=profit_embed)

    elif event_type == "shot_at_while_walking":
        rival_name, rival_gang, rival_set = generate_rival()
        event_embed = discord.Embed(
            title="SHOTS FIRED WALKING HOME",
            description=f"{player_char['name']} was just walking through the hood when a car slowed down and opened fire",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="Attack", value=f"Believed to be from the {rival_set} - targeted shooting", inline=False)
        event_embed.set_footer(text="Can never fully relax out here...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        hit_roll = random.randint(1, 100)
        characters = load_characters()
        if character_id not in characters:
            return
        player_char = characters[character_id]

        if hit_roll <= 25:
            death_roll = random.randint(1, 100)
            if death_roll <= 45:
                death_embed = discord.Embed(
                    title="SHOT AND KILLED",
                    description=f"{player_char['name']} was hit and killed walking home from nowhere",
                    color=discord.Color.dark_red()
                )
                death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
                dead_member = player_char.copy()
                dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_member['killed_by'] = f"{rival_set} Shooting (Passive Street Event)"
                graveyard.append(dead_member)
                save_graveyard(graveyard)
                del characters[character_id]
                save_characters(characters)
                await ctx.send(embed=death_embed)
            else:
                wound_embed = discord.Embed(
                    title="SHOT BUT SURVIVED",
                    description=f"{player_char['name']} was hit but the wound is not fatal - got to the hospital in time",
                    color=discord.Color.orange()
                )
                wound_embed.add_field(name="Status", value="Wounded and recovering but alive", inline=False)
                await ctx.send(embed=wound_embed)
        else:
            miss_embed = discord.Embed(
                title="SHOTS MISSED",
                description=f"{player_char['name']} ducked behind a car and the shots missed - got away clean",
                color=discord.Color.green()
            )
            miss_embed.add_field(name="Outcome", value="Fast reflexes saved the day", inline=False)
            await ctx.send(embed=miss_embed)

    elif event_type == "rival_tags_your_hood":
        rival_name, rival_gang, rival_set = generate_rival()
        event_embed = discord.Embed(
            title="RIVALS TAGGED YOUR HOOD",
            description=f"{player_char['name']} woke up to find the {rival_set} had tagged over the {player_char.get('set_name', 'set')} graffiti all through the neighborhood",
            color=discord.Color.red()
        )
        event_embed.add_field(name="Disrespect", value=f"The {rival_set} crossed out the set's tags and put their own up - a direct challenge", inline=False)
        event_embed.add_field(name="Suspects", value=f"{rival_name} and crew from {rival_gang}", inline=True)
        event_embed.set_footer(text="Disrespect cannot go unanswered...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        response_roll = random.randint(1, 100)
        if response_roll <= 60:
            battle = simulate_battle()
            won = battle['player_won']
            death_roll = random.randint(1, 100)
            dies = death_roll <= calculate_death_chance(won)

            characters = load_characters()
            if character_id not in characters:
                return
            player_char = characters[character_id]

            if won and not dies:
                win_embed = discord.Embed(
                    title="CHECKED THEM FOR THE DISRESPECT",
                    description=f"{player_char['name']} went and found the {rival_set} crew responsible and made them pay for the disrespect",
                    color=discord.Color.green()
                )
                player_char['kills'] = player_char.get('kills', 0) + 1
                if 'kill_list' not in player_char:
                    player_char['kill_list'] = []
                player_char['kill_list'].append({
                    'victim_name': rival_name,
                    'victim_gang': rival_gang,
                    'victim_set': rival_set,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'type': 'hood_defense'
                })
                win_embed.add_field(name="Bodies", value=f"{player_char['kills']}", inline=True)
                characters[character_id] = player_char
                save_characters(characters)
                await ctx.send(embed=win_embed)
            elif dies:
                death_embed = discord.Embed(
                    title="DIED DEFENDING THE HOOD",
                    description=f"{player_char['name']} went to check the {rival_set} for the disrespect but walked into a setup",
                    color=discord.Color.dark_red()
                )
                death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
                dead_member = player_char.copy()
                dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_member['killed_by'] = f"{rival_name} ({rival_set}) Hood Defense"
                graveyard.append(dead_member)
                save_graveyard(graveyard)
                del characters[character_id]
                save_characters(characters)
                await ctx.send(embed=death_embed)
            else:
                loss_embed = discord.Embed(
                    title="COULDN'T CHECK THEM TODAY",
                    description=f"{player_char['name']} went to handle the disrespect but had to fall back",
                    color=discord.Color.orange()
                )
                loss_embed.add_field(name="Outcome", value="Survived but the disrespect is still out there", inline=False)
                characters[character_id] = player_char
                save_characters(characters)
                await ctx.send(embed=loss_embed)
        else:
            lay_low_embed = discord.Embed(
                title="LAID LOW",
                description=f"{player_char['name']} decided to let it slide for now and not walk into a potential setup",
                color=discord.Color.orange()
            )
            lay_low_embed.add_field(name="Decision", value="Chose not to react - playing it smart", inline=False)
            await ctx.send(embed=lay_low_embed)

    elif event_type == "unexpected_confrontation":
        rival_name, rival_gang, rival_set = generate_rival()
        event_embed = discord.Embed(
            title="UNEXPECTED RUN IN",
            description=f"{player_char['name']} was out handling regular business when they crossed paths with {rival_name} from the {rival_set}",
            color=discord.Color.orange()
        )
        event_embed.add_field(name="Chance Encounter", value="Nobody planned this - it just happened. Now what?", inline=False)
        event_embed.set_footer(text="The streets always got something waiting...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle()
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(won)

        characters = load_characters()
        if character_id not in characters:
            return
        player_char = characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="HANDLED THE RUN IN",
                description=f"{player_char['name']} came out on top in the unexpected confrontation with {rival_name}",
                color=discord.Color.green()
            )
            player_char['kills'] = player_char.get('kills', 0) + 1
            if 'kill_list' not in player_char:
                player_char['kill_list'] = []
            player_char['kill_list'].append({
                'victim_name': rival_name,
                'victim_gang': rival_gang,
                'victim_set': rival_set,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'unexpected_confrontation'
            })
            win_embed.add_field(name="Bodies", value=f"{player_char['kills']}", inline=True)
            characters[character_id] = player_char
            save_characters(characters)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="RUN IN TURNED FATAL",
                description=f"The chance encounter with {rival_name} ended with {player_char['name']} not making it home",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_name} ({rival_set}) Unexpected Confrontation"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del characters[character_id]
            save_characters(characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="LOST THE RUN IN BUT SURVIVED",
                description=f"{player_char['name']} came out on the losing end of the confrontation with {rival_name} but made it out alive",
                color=discord.Color.orange()
            )
            loss_embed.add_field(name="Outcome", value="Lost this one but lived to fight again", inline=False)
            characters[character_id] = player_char
            save_characters(characters)
            await ctx.send(embed=loss_embed)


characters = load_characters()
graveyard = load_graveyard()


@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('LA Gang Battle System Ready')


@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You're on cooldown. Try again in {error.retry_after:.1f} seconds.")
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        print(f"Error: {error}")


# Make command
@bot.command(name='make')
@commands.cooldown(1, 10, commands.BucketType.user)
async def make_character(ctx):
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)

    user_id = str(ctx.author.id)
    user_is_admin = is_admin(ctx)

    if not user_is_admin:
        user_members = [char for char in characters.values() if char.get('user_id') == user_id]
        if user_members:
            await ctx.send(f"You already have a gang member alive! You can only have one character at a time.\nUse `?show` to see your current member.")
            return

    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    character_name = f"{first_name} {last_name}"
    character_id = generate_unique_id()
    gang_affiliation = random.choice(list(LA_GANGS.keys()))
    gang_sets = LA_GANGS[gang_affiliation]['sets']
    set_name = random.choice(gang_sets)

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

    characters[character_id] = character_data
    save_characters(characters)

    gang_color = LA_GANGS[gang_affiliation]['color']

    embed = discord.Embed(
        title="GANG MEMBER CREATED",
        description=f"**{character_name}**\nA new soldier has joined the streets",
        color=gang_color
    )
    embed.add_field(name="Owner", value=ctx.author.name, inline=True)
    embed.add_field(name="Member ID", value=f"`{character_id}`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(name="Gang Affiliation", value=gang_affiliation, inline=True)
    embed.add_field(name="Set", value=set_name, inline=True)
    embed.set_footer(text=f"Use ?random {character_id} to trigger a street event")

    await ctx.send(embed=embed)


# Show command
@bot.command(name='show')
@commands.cooldown(1, 10, commands.BucketType.user)
async def show_members(ctx):
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)

    user_id = str(ctx.author.id)
    fresh_characters = load_characters()
    user_members = [char for char in fresh_characters.values() if char.get('user_id') == user_id]

    if not user_members:
        await ctx.send("You don't have any gang members! Use `?make` to create one.")
        return

    user_members.sort(key=lambda x: x.get('kills', 0), reverse=True)

    embed = discord.Embed(
        title=f"{ctx.author.name}'s Gang Roster",
        description=f"Total active members: {len(user_members)}",
        color=discord.Color.dark_purple()
    )

    for member in user_members:
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

        if member.get('bounty', 0) > 0:
            member_info += f"\nBounty: ${member['bounty']:,}"

        if member.get('police_heat'):
            member_info += f"\nPolice Heat: ACTIVE"

        embed.add_field(name=f"{member['name']}", value=member_info, inline=True)

    embed.set_footer(text="Commands: ?slide <id> | ?rob <id> | ?work <id> | ?list <id> | ?block <id> | ?hoodday <id> | ?random <id>")
    await ctx.send(embed=embed)


# List command
@bot.command(name='list')
@commands.cooldown(1, 10, commands.BucketType.user)
async def list_kills(ctx, character_id: str = None):
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)

    if character_id is None:
        await ctx.send("Usage: `?list <character_id>`\nExample: `?list 123456`")
        return

    fresh_characters = load_characters()

    if character_id not in fresh_characters:
        await ctx.send(f"Gang member ID `{character_id}` not found!")
        return

    player_char = fresh_characters[character_id]
    user_id = str(ctx.author.id)

    if player_char.get('user_id') != user_id:
        await ctx.send("You don't own this gang member!")
        return

    kill_list = player_char.get('kill_list', [])
    total_kills = player_char.get('kills', 0)
    gang_color = LA_GANGS.get(player_char.get('gang_affiliation', 'Crips'), {}).get('color', discord.Color.dark_red())

    embed = discord.Embed(
        title=f"KILL LIST - {player_char['name']}",
        description=f"Total bodies: {total_kills}\nGang: {player_char.get('gang_affiliation', 'Unknown')}\nSet: {player_char.get('set_name', 'Unknown')}",
        color=gang_color
    )

    if kill_list:
        sorted_kills = sorted(kill_list, key=lambda x: x.get('date', ''), reverse=True)
        display_limit = 20

        for idx, kill in enumerate(sorted_kills):
            if idx >= display_limit:
                remaining = len(sorted_kills) - display_limit
                embed.add_field(name="\u200b", value=f"+ {remaining} more bodies not shown", inline=False)
                break

            victim_name = kill.get('victim_name', 'Unknown')
            victim_gang = kill.get('victim_gang', 'Unknown')
            victim_set = kill.get('victim_set', 'Unknown')
            kill_date = kill.get('date', 'Unknown')
            kill_type = kill.get('type', 'slide')

            try:
                date_obj = datetime.strptime(kill_date, '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%b %d, %Y at %I:%M %p')
            except:
                formatted_date = kill_date

            field_value = f"{victim_name}\nGang: {victim_gang}\nSet: {victim_set}\nDate: {formatted_date}"

            type_labels = {
                'slide': 'SLIDE',
                'revenge': 'REVENGE',
                'retaliation_defense': 'RETALIATION DEFENSE',
                'creation_event': 'DAY ONE BODY',
                'old_beef': 'OLD BEEF',
                'hood_defense': 'HOOD DEFENSE',
                'unexpected_confrontation': 'STREET RUN IN'
            }
            field_value += f"\nType: {type_labels.get(kill_type, kill_type.upper())}"

            embed.add_field(name=f"Body #{idx + 1}", value=field_value, inline=True)
    else:
        embed.add_field(name="Status", value=f"{player_char['name']} is clean, no bodies caught yet", inline=False)

    embed.set_footer(text="Bodies caught in the streets")
    await ctx.send(embed=embed)


# Work command
@bot.command(name='work')
@commands.cooldown(1, 10, commands.BucketType.user)
async def work_job(ctx, character_id: str = None):
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)

    if character_id is None:
        await ctx.send("Usage: `?work <character_id>`\nExample: `?work 123456`")
        return

    fresh_characters = load_characters()

    if character_id not in fresh_characters:
        await ctx.send(f"Gang member ID `{character_id}` not found!")
        return

    player_char = fresh_characters[character_id]
    user_id = str(ctx.author.id)

    if player_char.get('user_id') != user_id:
        await ctx.send("You don't own this gang member!")
        return

    if is_in_jail(player_char):
        remaining = get_jail_time_remaining(player_char)
        if remaining:
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            await ctx.send(f"{player_char['name']} is currently locked up and will be released in {minutes}m {seconds}s")
            return

    job_name = random.choice(list(WORK_JOBS.keys()))
    job_info = WORK_JOBS[job_name]

    intro_embed = discord.Embed(
        title="CLOCKING IN",
        description=f"{player_char['name']} is heading to work",
        color=discord.Color.green()
    )
    intro_embed.add_field(name="Job", value=f"{job_name}\n{job_info['description']}", inline=False)
    intro_embed.add_field(name="Member", value=f"{player_char['name']}\nCurrent Money: ${player_char.get('money', 0):,}", inline=False)
    intro_embed.set_footer(text="Putting in work...")
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(2)

    earnings = random.randint(job_info['min'], job_info['max'])
    player_char['money'] = player_char.get('money', 0) + earnings

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
    outcome_embed.add_field(name="Job Completed", value=job_name, inline=True)
    outcome_embed.add_field(name="Earnings", value=f"${earnings:,}", inline=True)
    outcome_embed.add_field(name="\u200b", value="\u200b", inline=False)
    outcome_embed.add_field(name="Updated Balance", value=f"${player_char['money']:,}", inline=False)
    outcome_embed.set_footer(text="Honest work pays off")

    fresh_characters = load_characters()
    if character_id in fresh_characters:
        fresh_characters[character_id]['money'] = player_char['money']
        save_characters(fresh_characters)
        characters.update(fresh_characters)

    await ctx.send(embed=outcome_embed)


# Rob command
@bot.command(name='rob')
@commands.cooldown(1, 10, commands.BucketType.user)
async def rob_store(ctx, character_id: str = None):
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)

    if character_id is None:
        await ctx.send("Usage: `?rob <character_id>`\nExample: `?rob 123456`")
        return

    fresh_characters = load_characters()

    if character_id not in fresh_characters:
        await ctx.send(f"Gang member ID `{character_id}` not found!")
        return

    player_char = fresh_characters[character_id]
    user_id = str(ctx.author.id)

    if player_char.get('user_id') != user_id:
        await ctx.send("You don't own this gang member!")
        return

    if is_in_jail(player_char):
        remaining = get_jail_time_remaining(player_char)
        if remaining:
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            await ctx.send(f"{player_char['name']} is currently locked up and will be released in {minutes}m {seconds}s")
            return

    store_type = random.choice(list(STORE_TYPES.keys()))
    store_info = STORE_TYPES[store_type]
    store_name = f"{random.choice(['Main St', 'Broadway', 'Central Ave', 'Sunset Blvd', 'Crenshaw', 'Vermont Ave'])} {store_type}"

    intro_embed = discord.Embed(
        title="ROBBERY IN PROGRESS",
        description=f"{player_char['name']} is attempting to rob {store_name}",
        color=discord.Color.gold()
    )
    intro_embed.add_field(name="Target", value=f"{store_name}\nRisk Level: {store_info['risk'].upper()}", inline=True)
    intro_embed.add_field(name="Member", value=f"{player_char['name']}\nMoney: ${player_char.get('money', 0):,}", inline=True)
    intro_embed.set_footer(text="The heist is underway...")
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)

    robbery_roll = random.randint(1, 100)
    police_heat_bonus = 15 if player_char.get('police_heat') else 0
    robbery_success = robbery_roll <= 70

    money_stolen = 0
    if robbery_success:
        money_stolen = random.randint(store_info['min'], store_info['max'])

    caught_by_police = False
    jail_time = 0
    witnesses_present = False

    if robbery_success:
        if store_info['risk'] == "low":
            police_chance = 20 + police_heat_bonus
        elif store_info['risk'] == "medium":
            police_chance = 35 + police_heat_bonus
        elif store_info['risk'] == "high":
            police_chance = 50 + police_heat_bonus
        else:
            police_chance = 70 + police_heat_bonus

        police_roll = random.randint(1, 100)
        caught_by_police = police_roll <= police_chance

        if caught_by_police:
            witness_roll = random.randint(1, 100)
            witnesses_present = witness_roll <= 30
            jail_time = random.randint(20, 30) if witnesses_present else random.randint(5, 10)

    if robbery_success:
        if caught_by_police:
            outcome_embed = discord.Embed(
                title="ROBBERY SUCCESSFUL - BUT ARRESTED",
                description=f"{player_char['name']} successfully robbed {store_name} but was caught by police",
                color=discord.Color.orange()
            )
            outcome_embed.add_field(name="Money Stolen", value=f"${money_stolen:,}", inline=True)
            outcome_embed.add_field(name="Police Response", value="CAUGHT", inline=True)
            outcome_embed.add_field(name="\u200b", value="\u200b", inline=False)
            if witnesses_present:
                outcome_embed.add_field(name="WITNESSES PRESENT", value=f"Multiple witnesses identified {player_char['name']}\nSentence increased due to evidence", inline=False)
            outcome_embed.add_field(name="ARREST STATUS", value=f"Sentenced to {jail_time} minutes in county jail\nMoney confiscated by police", inline=False)
            jail_until = datetime.now() + timedelta(minutes=jail_time)
            fresh_characters = load_characters()
            if character_id in fresh_characters:
                fresh_characters[character_id]['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
                save_characters(fresh_characters)
                characters.update(fresh_characters)
        else:
            outcome_embed = discord.Embed(
                title="ROBBERY SUCCESSFUL",
                description=f"{player_char['name']} successfully robbed {store_name} and escaped",
                color=discord.Color.green()
            )
            outcome_embed.add_field(name="Money Stolen", value=f"${money_stolen:,}", inline=True)
            outcome_embed.add_field(name="Police Response", value="ESCAPED", inline=True)
            outcome_embed.add_field(name="\u200b", value="\u200b", inline=False)
            player_char['money'] = player_char.get('money', 0) + money_stolen
            outcome_embed.add_field(name="CLEAN GETAWAY", value=f"{player_char['name']} evaded police and made it back to the hood", inline=False)
            outcome_embed.add_field(name="Updated Balance", value=f"${player_char['money']:,}", inline=False)
            fresh_characters = load_characters()
            if character_id in fresh_characters:
                fresh_characters[character_id]['money'] = player_char['money']
                save_characters(fresh_characters)
                characters.update(fresh_characters)
    else:
        outcome_embed = discord.Embed(
            title="ROBBERY FAILED",
            description=f"{player_char['name']} failed to rob {store_name}",
            color=discord.Color.red()
        )
        outcome_embed.add_field(name="Result", value="The robbery went wrong before anything could be taken", inline=False)
        outcome_embed.add_field(name="Money Stolen", value="$0", inline=True)
        outcome_embed.add_field(name="Status", value="Fled the scene empty-handed", inline=True)

    outcome_embed.set_footer(text="Crime doesn't always pay")
    await ctx.send(embed=outcome_embed)


# Block command
@bot.command(name='block')
@commands.cooldown(1, 10, commands.BucketType.user)
async def block_party(ctx, character_id: str = None):
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)

    if character_id is None:
        await ctx.send("Usage: `?block <character_id>`\nExample: `?block 123456`")
        return

    fresh_characters = load_characters()

    if character_id not in fresh_characters:
        await ctx.send(f"Gang member ID `{character_id}` not found!")
        return

    player_char = fresh_characters[character_id]
    user_id = str(ctx.author.id)

    if player_char.get('user_id') != user_id:
        await ctx.send("You don't own this gang member!")
        return

    if is_in_jail(player_char):
        remaining = get_jail_time_remaining(player_char)
        if remaining:
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            await ctx.send(f"{player_char['name']} is currently locked up and will be released in {minutes}m {seconds}s")
            return

    char_gang = player_char.get('gang_affiliation', 'Unknown')
    char_set = player_char.get('set_name', 'Unknown')
    gang_color = LA_GANGS.get(char_gang, {}).get('color', discord.Color.purple())

    intro_embed = discord.Embed(
        title="BLOCK PARTY STARTING",
        description=f"{player_char['name']} is throwing a block party in {char_set} territory",
        color=gang_color
    )
    intro_embed.add_field(name="Host", value=f"{player_char['name']}", inline=True)
    intro_embed.add_field(name="Location", value=f"{char_set} turf", inline=True)
    intro_embed.add_field(name="\u200b", value="\u200b", inline=False)
    intro_embed.add_field(name="The Scene", value="Music bumping, homies gathered, BBQ going, everyone having a good time in the hood", inline=False)
    intro_embed.set_footer(text="The party is live...")
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)

    rival_roll = random.randint(1, 100)
    rival_shows_up = rival_roll <= 35

    if not rival_shows_up:
        outcome_embed = discord.Embed(
            title="BLOCK PARTY SUCCESS",
            description=f"The block party was a success! Everyone had a good time and no drama went down",
            color=discord.Color.green()
        )
        outcome_embed.add_field(name="Party Status", value="Everything stayed peaceful in the hood tonight", inline=False)
        outcome_embed.add_field(name=f"{player_char['name']}", value="Threw a legendary block party that the hood will remember", inline=False)
        outcome_embed.set_footer(text="Good vibes only")
        await ctx.send(embed=outcome_embed)
    else:
        available_gangs = [g for g in LA_GANGS.keys() if g != char_gang]
        if not available_gangs:
            available_gangs = list(LA_GANGS.keys())
        rival_gang = random.choice(available_gangs)
        rival_set = random.choice(LA_GANGS[rival_gang]['sets'])
        num_shooters = random.randint(2, 4)
        rival_names = [f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" for _ in range(num_shooters)]

        driveby_embed = discord.Embed(
            title="RIVAL GANG ALERT",
            description=f"A car full of {rival_set} members just rolled up on the block party!",
            color=discord.Color.red()
        )
        driveby_embed.add_field(name="Rival Gang", value=f"{rival_gang}", inline=True)
        driveby_embed.add_field(name="Set", value=f"{rival_set}", inline=True)
        driveby_embed.add_field(name="\u200b", value="\u200b", inline=False)
        driveby_embed.add_field(name="SHOOTERS SPOTTED", value="\n".join(rival_names), inline=False)
        driveby_embed.set_footer(text="Shots about to be fired...")
        await ctx.send(embed=driveby_embed)
        await asyncio.sleep(3)

        shooting_embed = discord.Embed(
            title="SHOTS FIRED!",
            description=f"The {rival_set} members opened fire on the block party!",
            color=discord.Color.dark_red()
        )
        shooting_embed.add_field(name="Drive-By Shooting", value="Bullets flying everywhere, people running for cover, chaos in the streets", inline=False)
        await ctx.send(embed=shooting_embed)
        await asyncio.sleep(3)

        bullet_roll = random.randint(1, 100)
        player_hit = bullet_roll <= 40

        if player_hit:
            fresh_characters = load_characters()
            if character_id not in fresh_characters:
                return
            player_char = fresh_characters[character_id]
            death_embed = discord.Embed(
                title="CAUGHT BY A BULLET",
                description=f"{player_char['name']} was hit during the drive-by shooting",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Fatal Outcome", value=f"{player_char['name']} caught a stray bullet during the shootout and didn't make it", inline=False)
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_set} Drive-By Shooting (Block Party)"
            graveyard = load_graveyard()
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            death_embed.set_footer(text="Wrong place, wrong time")
            await ctx.send(embed=death_embed)
        else:
            survive_embed = discord.Embed(
                title="SURVIVED THE SHOOTING",
                description=f"{player_char['name']} managed to avoid the bullets and survive the drive-by",
                color=discord.Color.orange()
            )
            survive_embed.add_field(name="Close Call", value=f"{player_char['name']} hit the ground and avoided getting hit", inline=False)
            await ctx.send(embed=survive_embed)
            await asyncio.sleep(2)

            police_roll = random.randint(1, 100)
            if police_roll <= 60:
                police_embed = discord.Embed(
                    title="POLICE ARRIVAL",
                    description="LAPD rolled up on the scene after the shooting",
                    color=discord.Color.blue()
                )
                police_embed.add_field(name="Police Response", value="Multiple units arrived on scene, investigating the shooting", inline=False)
                police_embed.add_field(name=f"{player_char['name']} Status", value="Questioned by police but not arrested - no jail time for being a victim", inline=False)
                police_embed.set_footer(text="Survived to see another day")
                await ctx.send(embed=police_embed)
            else:
                final_embed = discord.Embed(
                    title="ESCAPED CLEAN",
                    description=f"{player_char['name']} survived the shooting and got away before police arrived",
                    color=discord.Color.green()
                )
                final_embed.add_field(name="Status", value="Made it out alive, no police involvement", inline=False)
                final_embed.set_footer(text="Lucky to be alive")
                await ctx.send(embed=final_embed)


# Hoodday command
@bot.command(name='hoodday')
@commands.cooldown(1, 10, commands.BucketType.user)
async def hoodday(ctx, character_id: str = None):
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)

    if character_id is None:
        await ctx.send("Usage: `?hoodday <character_id>`\nExample: `?hoodday 123456`")
        return

    fresh_characters = load_characters()

    if character_id not in fresh_characters:
        await ctx.send(f"Gang member ID `{character_id}` not found!")
        return

    player_char = fresh_characters[character_id]
    user_id = str(ctx.author.id)

    if player_char.get('user_id') != user_id:
        await ctx.send("You don't own this gang member!")
        return

    if is_in_jail(player_char):
        remaining = get_jail_time_remaining(player_char)
        if remaining:
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            await ctx.send(f"{player_char['name']} is currently locked up and will be released in {minutes}m {seconds}s")
            return

    char_gang = player_char.get('gang_affiliation', 'Unknown')
    char_set = player_char.get('set_name', 'Unknown')
    gang_color = LA_GANGS.get(char_gang, {}).get('color', discord.Color.purple())
    num_members = random.randint(10, 20)

    intro_embed = discord.Embed(
        title="HOOD DAY CELEBRATION",
        description=f"{player_char['name']} has organized a massive hood celebration bringing the whole {char_set} together!",
        color=gang_color
    )
    intro_embed.add_field(name="Organizer", value=f"{player_char['name']}", inline=True)
    intro_embed.add_field(name="Gang", value=f"{char_gang}", inline=True)
    intro_embed.add_field(name="\u200b", value="\u200b", inline=False)
    intro_embed.add_field(name="Location", value=f"{char_set} territory - The whole hood is out", inline=True)
    intro_embed.add_field(name="Attendance", value=f"{num_members} gang members present", inline=True)
    intro_embed.add_field(name="\u200b", value="\u200b", inline=False)
    intro_embed.add_field(name="The Celebration", value="The whole hood is lit! DJ spinning, grills fired up, kids playing, OGs telling stories, lowriders cruising, everyone representing the set with pride", inline=False)
    intro_embed.set_footer(text="The entire hood is celebrating...")
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(4)

    trouble_roll = random.randint(1, 100)
    trouble_occurs = trouble_roll <= 10

    if not trouble_occurs:
        success_embed = discord.Embed(
            title="HOOD DAY SUCCESS",
            description=f"The hood day celebration was a massive success! The whole {char_set} came together for an unforgettable day",
            color=discord.Color.green()
        )
        success_embed.add_field(name="Celebration Status", value="Peace throughout the hood, everybody had a great time, no drama all day", inline=False)
        success_embed.add_field(name="Hood Unity", value=f"The {char_set} showed the whole city what unity looks like - {num_members} members strong", inline=False)
        success_embed.add_field(name=f"{player_char['name']}", value="Organized a legendary hood day that will be remembered for years to come", inline=False)
        success_embed.set_footer(text="Hood day for the books")
        await ctx.send(embed=success_embed)
    else:
        trouble_type_roll = random.randint(1, 100)
        rival_attack = trouble_type_roll <= 50

        if rival_attack:
            available_gangs = [g for g in LA_GANGS.keys() if g != char_gang]
            if not available_gangs:
                available_gangs = list(LA_GANGS.keys())
            rival_gang = random.choice(available_gangs)
            rival_set = random.choice(LA_GANGS[rival_gang]['sets'])
            num_shooters = random.randint(5, 8)
            rival_names = [f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" for _ in range(num_shooters)]

            rival_embed = discord.Embed(
                title="RIVAL GANG ATTACK",
                description=f"Multiple cars full of {rival_set} members just pulled up on the hood day celebration!",
                color=discord.Color.red()
            )
            rival_embed.add_field(name="Rival Gang", value=f"{rival_gang}", inline=True)
            rival_embed.add_field(name="Rival Set", value=f"{rival_set}", inline=True)
            rival_embed.add_field(name="\u200b", value="\u200b", inline=False)
            rival_embed.add_field(name="ATTACKERS SPOTTED", value="\n".join(rival_names[:5]) + (f"\n+ {len(rival_names) - 5} more..." if len(rival_names) > 5 else ""), inline=False)
            rival_embed.set_footer(text="This is a major attack...")
            await ctx.send(embed=rival_embed)
            await asyncio.sleep(3)

            shooting_embed = discord.Embed(
                title="MASSIVE SHOOTOUT!",
                description=f"The {rival_set} opened fire on the hood day! The {char_set} is firing back!",
                color=discord.Color.dark_red()
            )
            shooting_embed.add_field(name="All-Out War", value="Gunfire erupting from all directions, the entire celebration turned into a warzone", inline=False)
            await ctx.send(embed=shooting_embed)
            await asyncio.sleep(3)

            bullet_roll = random.randint(1, 100)
            player_hit = bullet_roll <= 25

            if player_hit:
                fresh_characters = load_characters()
                if character_id not in fresh_characters:
                    return
                player_char = fresh_characters[character_id]
                death_embed = discord.Embed(
                    title="FALLEN IN THE BATTLE",
                    description=f"{player_char['name']} was struck down during the massive shootout",
                    color=discord.Color.dark_red()
                )
                death_embed.add_field(name="Fatal Outcome", value=f"{player_char['name']} was hit during the chaos and didn't survive", inline=False)
                death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
                dead_member = player_char.copy()
                dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_member['killed_by'] = f"{rival_set} Attack (Hood Day Massacre)"
                graveyard = load_graveyard()
                graveyard.append(dead_member)
                save_graveyard(graveyard)
                del fresh_characters[character_id]
                save_characters(fresh_characters)
                characters.update(fresh_characters)
                death_embed.set_footer(text="The hood day turned tragic")
                await ctx.send(embed=death_embed)
            else:
                survive_embed = discord.Embed(
                    title="SURVIVED THE WAR",
                    description=f"{player_char['name']} made it through the massive shootout alive",
                    color=discord.Color.orange()
                )
                survive_embed.add_field(name="Battle Outcome", value=f"The {char_set} held their ground and the {rival_set} was driven off", inline=False)
                survive_embed.add_field(name=f"{player_char['name']} Status", value="Survived the attack but the hood day was ruined by the violence", inline=False)
                survive_embed.set_footer(text="Hood defended but at what cost")
                await ctx.send(embed=survive_embed)
        else:
            police_embed = discord.Embed(
                title="POLICE RAID",
                description="LAPD task force rolled up on the hood day celebration in force!",
                color=discord.Color.blue()
            )
            police_embed.add_field(name="Police Response", value="Multiple units, helicopters overhead, they're shutting down the whole celebration", inline=False)
            police_embed.add_field(name="The Scene", value="Cops are everywhere, people scattering, chaos as the party gets broken up", inline=False)
            await ctx.send(embed=police_embed)
            await asyncio.sleep(3)

            arrest_roll = random.randint(1, 100)
            if arrest_roll <= 30:
                arrest_embed = discord.Embed(
                    title="DETAINED BY POLICE",
                    description=f"{player_char['name']} was detained during the raid",
                    color=discord.Color.orange()
                )
                arrest_embed.add_field(name="Police Harassment", value=f"{player_char['name']} was questioned and searched but released after a few hours - no charges filed", inline=False)
                arrest_embed.add_field(name="Hood Day Outcome", value="The celebration was shut down but everyone made it home safe", inline=False)
                arrest_embed.set_footer(text="Hood day ended early")
                await ctx.send(embed=arrest_embed)
            else:
                escape_embed = discord.Embed(
                    title="ESCAPED THE RAID",
                    description=f"{player_char['name']} and most of the hood got away clean",
                    color=discord.Color.green()
                )
                escape_embed.add_field(name="Quick Escape", value=f"{player_char['name']} slipped away before police could lock anyone down", inline=False)
                escape_embed.add_field(name="Hood Day Outcome", value="Police broke up the party but everyone avoided arrest and made it home", inline=False)
                escape_embed.set_footer(text="Hood day shut down but no arrests")
                await ctx.send(embed=escape_embed)


# Slide command
@bot.command(name='slide')
@commands.cooldown(1, 10, commands.BucketType.user)
async def slide_on_opps(ctx, *character_ids):
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)

    if not character_ids:
        await ctx.send("Usage: `?slide <character_id> [character_id2] [character_id3]...`\nExample: `?slide 123456`")
        return

    user_id = str(ctx.author.id)
    fresh_characters = load_characters()
    valid_members = []
    invalid_ids = []
    not_owned = []
    in_jail_members = []

    for character_id in character_ids:
        if character_id not in fresh_characters:
            invalid_ids.append(character_id)
            continue
        player_char = fresh_characters[character_id]
        if player_char.get('user_id') != user_id:
            not_owned.append(character_id)
            continue
        if is_in_jail(player_char):
            remaining = get_jail_time_remaining(player_char)
            if remaining:
                minutes = int(remaining.total_seconds() // 60)
                seconds = int(remaining.total_seconds() % 60)
                in_jail_members.append(f"{player_char['name']} ({minutes}m {seconds}s)")
            continue
        valid_members.append(player_char)

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

    for idx, player_char in enumerate(valid_members):
        character_id = player_char['character_id']
        rival_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        available_gangs = [g for g in LA_GANGS.keys() if g != player_char.get('gang_affiliation')]
        if not available_gangs:
            available_gangs = list(LA_GANGS.keys())
        rival_gang = random.choice(available_gangs)
        rival_set = random.choice(LA_GANGS[rival_gang]['sets'])

        intro_embed = discord.Embed(
            title=f"SLIDING ON OPPS ({idx + 1}/{len(valid_members)})",
            description=f"Your member has spotted an enemy in rival territory",
            color=discord.Color.orange()
        )
        intro_embed.add_field(name="YOUR MEMBER", value=f"{player_char['name']}\nBodies: {player_char.get('kills', 0)}\nGang: {player_char.get('gang_affiliation', 'Unknown')}\nSet: {player_char.get('set_name', 'Unknown')}", inline=True)
        intro_embed.add_field(name="ENEMY SPOTTED", value=f"{rival_name}\nGang: {rival_gang}\nSet: {rival_set}", inline=True)
        intro_embed.set_footer(text="The confrontation is about to go down...")
        await ctx.send(embed=intro_embed)
        await asyncio.sleep(2)

        battle_result = simulate_battle()
        player_won = battle_result['player_won']
        death_chance = calculate_death_chance(player_won)
        death_roll = random.randint(1, 100)
        member_dies = death_roll <= death_chance
        jail_roll = random.randint(1, 100)
        goes_to_jail = False
        jail_minutes = 0

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            continue
        player_char = fresh_characters[character_id]

        if not member_dies and player_won:
            player_char['kills'] = player_char.get('kills', 0) + 1
            if 'kill_list' not in player_char:
                player_char['kill_list'] = []
            player_char['kill_list'].append({
                'victim_name': rival_name,
                'victim_gang': rival_gang,
                'victim_set': rival_set,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'slide'
            })
            jail_chance = 30
            goes_to_jail = jail_roll <= jail_chance
            if goes_to_jail:
                jail_minutes = player_char['kills']

        if player_won:
            if member_dies:
                outcome_embed = discord.Embed(
                    title="PYRRHIC VICTORY",
                    description=f"{player_char['name']} successfully eliminated {rival_name} but sustained fatal injuries in the process",
                    color=discord.Color.dark_red()
                )
                outcome_embed.add_field(name="Final Outcome", value=f"Despite winning the confrontation, {player_char['name']} succumbed to their wounds", inline=False)
                outcome_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
                dead_member = player_char.copy()
                dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_member['killed_by'] = f"{rival_name} ({rival_set}) - Fatal Wounds"
                graveyard = load_graveyard()
                graveyard.append(dead_member)
                save_graveyard(graveyard)
                del fresh_characters[character_id]
                save_characters(fresh_characters)
                characters.update(fresh_characters)
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
                outcome_embed.add_field(name="Updated Stats", value=f"Total Bodies: {player_char['kills']}\nMoney: ${player_char.get('money', 0):,}", inline=False)
                if goes_to_jail:
                    jail_until = datetime.now() + timedelta(minutes=jail_minutes)
                    player_char['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
                    outcome_embed.add_field(name="ARREST STATUS", value=f"Sentenced to {jail_minutes} minutes in county jail\nWill be released in {jail_minutes} minutes", inline=False)
                else:
                    outcome_embed.add_field(name="POLICE STATUS", value="Successfully evaded law enforcement and made it back safely", inline=False)

                fresh_characters[character_id] = player_char
                save_characters(fresh_characters)
                characters.update(fresh_characters)
        else:
            if member_dies:
                outcome_embed = discord.Embed(
                    title="CAUGHT SLIPPING",
                    description=f"{player_char['name']} was eliminated by {rival_name} from the {rival_set}",
                    color=discord.Color.dark_red()
                )
                outcome_embed.add_field(name="Final Words", value=f"{player_char['name']} was caught lacking deep in enemy territory and paid the ultimate price", inline=False)
                outcome_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
                dead_member = player_char.copy()
                dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_member['killed_by'] = f"{rival_name} ({rival_set})"
                graveyard = load_graveyard()
                graveyard.append(dead_member)
                save_graveyard(graveyard)
                del fresh_characters[character_id]
                save_characters(fresh_characters)
                characters.update(fresh_characters)
            else:
                outcome_embed = discord.Embed(
                    title="TOOK AN L - SURVIVED",
                    description=f"{player_char['name']} was defeated by {rival_name} but managed to escape alive",
                    color=discord.Color.orange()
                )
                outcome_embed.add_field(name="Outcome", value="Lost the confrontation but survived to fight another day", inline=False)
                outcome_embed.add_field(name="Current Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: ALIVE", inline=False)
                fresh_characters[character_id] = player_char
                save_characters(fresh_characters)
                characters.update(fresh_characters)

        outcome_embed.set_footer(text="The streets never forget")
        await ctx.send(embed=outcome_embed)

        if idx < len(valid_members) - 1:
            await asyncio.sleep(3)


# Revenge command
@bot.command(name='revenge')
@commands.cooldown(1, 10, commands.BucketType.user)
async def revenge_battle(ctx, dead_character_id: str = None, avenger_character_id: str = None):
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)

    if dead_character_id is None or avenger_character_id is None:
        await ctx.send("Usage: `?revenge <dead_member_id> <avenger_member_id>`\nExample: `?revenge 123456 789012`")
        return

    user_id = str(ctx.author.id)
    fresh_characters = load_characters()

    if avenger_character_id not in fresh_characters:
        await ctx.send(f"Avenger member ID `{avenger_character_id}` not found!")
        return

    avenger_char = fresh_characters[avenger_character_id]

    if avenger_char.get('user_id') != user_id:
        await ctx.send("You don't own this avenger!")
        return

    if is_in_jail(avenger_char):
        remaining = get_jail_time_remaining(avenger_char)
        if remaining:
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            await ctx.send(f"{avenger_char['name']} is currently locked up and will be released in {minutes}m {seconds}s")
            return

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

    killer_name = dead_member.get('killed_by', 'Unknown')

    if "Crew War" in killer_name:
        await ctx.send(f"{dead_member['name']} was killed in a crew war. Revenge is not available for crew war deaths.")
        return

    if "(Fatal Wounds)" in killer_name or "- Fatal Wounds" in killer_name:
        killer_name = killer_name.replace(" (Fatal Wounds)", "").replace(" - Fatal Wounds", "").strip()
        if "(" in killer_name and ")" in killer_name:
            killer_name = killer_name.split("(")[0].strip()

    rival_gang = "Unknown Gang"
    rival_set = "Unknown Set"
    if "(" in dead_member.get('killed_by', '') and ")" in dead_member.get('killed_by', ''):
        try:
            set_info = dead_member['killed_by'].split("(")[1].split(")")[0]
            rival_set = set_info
            for gang, info in LA_GANGS.items():
                if rival_set in info['sets']:
                    rival_gang = gang
                    break
        except:
            pass

    intro_embed = discord.Embed(
        title="REVENGE MISSION",
        description=f"Your member is on a mission to avenge a fallen homie",
        color=discord.Color.dark_red()
    )
    intro_embed.add_field(name="YOUR AVENGER", value=f"{avenger_char['name']}\nBodies: {avenger_char.get('kills', 0)}\nGang: {avenger_char.get('gang_affiliation', 'Unknown')}\nSet: {avenger_char.get('set_name', 'Unknown')}", inline=True)
    intro_embed.add_field(name="TARGET LOCATED", value=f"{killer_name}\nGang: {rival_gang}\nSet: {rival_set}", inline=True)
    intro_embed.add_field(name="\u200b", value="\u200b", inline=False)
    intro_embed.add_field(name="FALLEN HOMIE", value=f"{dead_member['name']}\nBodies: {dead_member.get('kills', 0)}\nDeath Date: {dead_member.get('death_date', 'Unknown')}", inline=False)
    intro_embed.set_footer(text="Blood calls for blood...")
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)

    battle_result = simulate_battle()
    player_won = battle_result['player_won']
    death_chance = calculate_death_chance(player_won)
    death_roll = random.randint(1, 100)
    member_dies = death_roll <= death_chance
    jail_roll = random.randint(1, 100)
    goes_to_jail = False
    jail_minutes = 0

    fresh_characters = load_characters()
    if avenger_character_id not in fresh_characters:
        return
    avenger_char = fresh_characters[avenger_character_id]

    if not member_dies and player_won:
        avenger_char['kills'] = avenger_char.get('kills', 0) + 1
        if 'kill_list' not in avenger_char:
            avenger_char['kill_list'] = []
        avenger_char['kill_list'].append({
            'victim_name': killer_name,
            'victim_gang': rival_gang,
            'victim_set': rival_set,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'revenge'
        })
        goes_to_jail = jail_roll <= 30
        if goes_to_jail:
            jail_minutes = avenger_char['kills']

    if player_won:
        if member_dies:
            outcome_embed = discord.Embed(
                title="REVENGE COMPLETE - ULTIMATE SACRIFICE",
                description=f"{avenger_char['name']} successfully eliminated {killer_name}, avenging {dead_member['name']}, but was fatally wounded in the process",
                color=discord.Color.dark_red()
            )
            outcome_embed.add_field(name="Final Moments", value=f"{avenger_char['name']} avenged their fallen homie but paid the ultimate price", inline=False)
            outcome_embed.add_field(name="Final Stats", value=f"Body Count: {avenger_char.get('kills', 0)}\nMoney: ${avenger_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_avenger = avenger_char.copy()
            dead_avenger['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_avenger['killed_by'] = f"{killer_name} (Revenge Mission - Fatal Wounds)"
            graveyard = load_graveyard()
            graveyard.append(dead_avenger)
            save_graveyard(graveyard)
            del fresh_characters[avenger_character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
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
            outcome_embed.add_field(name="Vengeance Delivered", value=f"{dead_member['name']} has been avenged - {killer_name} is no longer a threat", inline=False)
            outcome_embed.add_field(name="Updated Stats", value=f"Total Bodies: {avenger_char['kills']}\nMoney: ${avenger_char.get('money', 0):,}", inline=False)
            if goes_to_jail:
                jail_until = datetime.now() + timedelta(minutes=jail_minutes)
                avenger_char['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
                outcome_embed.add_field(name="ARREST STATUS", value=f"Sentenced to {jail_minutes} minutes in county jail", inline=False)
            else:
                outcome_embed.add_field(name="POLICE STATUS", value="Successfully evaded law enforcement after the revenge hit", inline=False)

            fresh_characters[avenger_character_id] = avenger_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
    else:
        if member_dies:
            outcome_embed = discord.Embed(
                title="REVENGE FAILED - ELIMINATED",
                description=f"{avenger_char['name']} was eliminated by {killer_name} during the revenge attempt",
                color=discord.Color.dark_red()
            )
            outcome_embed.add_field(name="Failed Mission", value=f"{avenger_char['name']} fell to the same killer who took {dead_member['name']}\n{dead_member['name']} remains unavenged", inline=False)
            outcome_embed.add_field(name="Final Stats", value=f"Body Count: {avenger_char.get('kills', 0)}\nMoney: ${avenger_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_avenger = avenger_char.copy()
            dead_avenger['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_avenger['killed_by'] = f"{killer_name} (Failed Revenge Mission)"
            graveyard = load_graveyard()
            graveyard.append(dead_avenger)
            save_graveyard(graveyard)
            del fresh_characters[avenger_character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
        else:
            outcome_embed = discord.Embed(
                title="REVENGE FAILED - RETREAT",
                description=f"{avenger_char['name']} was defeated by {killer_name} but managed to escape alive",
                color=discord.Color.orange()
            )
            outcome_embed.add_field(name="Failed Attempt", value=f"The revenge mission was unsuccessful but {avenger_char['name']} survived to try again\n{dead_member['name']} remains unavenged", inline=False)
            outcome_embed.add_field(name="Current Stats", value=f"Body Count: {avenger_char.get('kills', 0)}\nMoney: ${avenger_char.get('money', 0):,}\nStatus: ALIVE", inline=False)
            fresh_characters[avenger_character_id] = avenger_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)

    outcome_embed.set_footer(text="The cycle of violence continues")
    await ctx.send(embed=outcome_embed)


# Random command - manually trigger a street event
@bot.command(name='random')
@commands.cooldown(1, 30, commands.BucketType.user)
async def random_event(ctx, character_id: str = None):
    if is_admin(ctx):
        ctx.command.reset_cooldown(ctx)

    if character_id is None:
        await ctx.send("Usage: `?random <character_id>`\nExample: `?random 123456`")
        return

    fresh_characters = load_characters()

    if character_id not in fresh_characters:
        await ctx.send(f"Gang member ID `{character_id}` not found!")
        return

    player_char = fresh_characters[character_id]
    user_id = str(ctx.author.id)

    if player_char.get('user_id') != user_id:
        await ctx.send("You don't own this gang member!")
        return

    if is_in_jail(player_char):
        remaining = get_jail_time_remaining(player_char)
        if remaining:
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            await ctx.send(f"{player_char['name']} is currently locked up and will be released in {minutes}m {seconds}s")
            return

    graveyard = load_graveyard()
    char_gang = player_char.get('gang_affiliation', 'Unknown')

    event_type = random.choice([
        "drive_by_on_block",
        "found_cash_on_street",
        "police_raid_area",
        "homie_in_trouble",
        "drug_deal_gone_wrong",
        "shot_at_while_walking",
        "rival_tags_your_hood",
        "unexpected_confrontation",
        "retaliation_crew",
        "witness_calls_police",
        "rival_solo_retaliation",
        "bounty_placed",
        "jumped_walking_home",
        "rival_spots_new_member",
        "initiated_by_hood",
        "found_on_wrong_block",
        "old_beef_resurfaces",
        "police_already_watching"
    ])

    notify_embed = discord.Embed(
        title="STREET EVENT INCOMING",
        description=f"Something is about to go down for {player_char['name']} in the streets...",
        color=discord.Color.dark_gold()
    )
    notify_embed.set_footer(text="The streets never sleep")
    await ctx.send(embed=notify_embed)
    await asyncio.sleep(2)

    rival_name, rival_gang, rival_set = generate_rival()

    if event_type == "drive_by_on_block":
        event_embed = discord.Embed(
            title="DRIVE BY ON THE BLOCK",
            description=f"Out of nowhere a car from the {rival_set} just sprayed the block where {player_char['name']} was posted",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="Shooter", value=f"{rival_name} - {rival_set}", inline=True)
        event_embed.add_field(name="Situation", value="Shots fired with no warning - had to react fast", inline=True)
        event_embed.set_footer(text="The block is never safe...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        hit_roll = random.randint(1, 100)
        gets_hit = hit_roll <= 30

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if gets_hit:
            death_roll = random.randint(1, 100)
            if death_roll <= 50:
                death_embed = discord.Embed(
                    title="HIT BY THE DRIVE BY",
                    description=f"{player_char['name']} was struck by bullets in the drive by and didn't survive",
                    color=discord.Color.dark_red()
                )
                death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
                dead_member = player_char.copy()
                dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_member['killed_by'] = f"{rival_set} Drive By"
                graveyard.append(dead_member)
                save_graveyard(graveyard)
                del fresh_characters[character_id]
                save_characters(fresh_characters)
                characters.update(fresh_characters)
                await ctx.send(embed=death_embed)
            else:
                wound_embed = discord.Embed(
                    title="WOUNDED BUT ALIVE",
                    description=f"{player_char['name']} got hit in the drive by but the wounds are not fatal",
                    color=discord.Color.orange()
                )
                wound_embed.add_field(name="Status", value="Took a bullet but survived - heading to get patched up", inline=False)
                await ctx.send(embed=wound_embed)
        else:
            safe_embed = discord.Embed(
                title="DOVE FOR COVER",
                description=f"{player_char['name']} hit the ground when the shots rang out and avoided getting hit",
                color=discord.Color.green()
            )
            safe_embed.add_field(name="Outcome", value="Bullets missed - made it out clean", inline=False)
            await ctx.send(embed=safe_embed)

    elif event_type == "found_cash_on_street":
        cash_found = random.randint(50, 500)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]
        player_char['money'] = player_char.get('money', 0) + cash_found
        fresh_characters[character_id] = player_char
        save_characters(fresh_characters)
        characters.update(fresh_characters)
        event_embed = discord.Embed(
            title="FOUND SOMETHING ON THE STREET",
            description=f"{player_char['name']} was walking through the hood and found a dropped envelope",
            color=discord.Color.green()
        )
        event_embed.add_field(name="Contents", value=f"${cash_found:,} cash inside - no name, no questions", inline=True)
        event_embed.add_field(name="New Balance", value=f"${player_char['money']:,}", inline=True)
        event_embed.set_footer(text="Streets provide sometimes")
        await ctx.send(embed=event_embed)

    elif event_type == "police_raid_area":
        event_embed = discord.Embed(
            title="POLICE SWEEPING THE AREA",
            description=f"LAPD gang unit is doing a sweep through {player_char.get('set_name', 'the hood')} territory right now",
            color=discord.Color.blue()
        )
        event_embed.add_field(name="Police Activity", value="Multiple units rolling through, stopping and questioning everyone on the block", inline=False)
        event_embed.set_footer(text="Lay low or get caught up...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        caught_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if caught_roll <= 20:
            jail_time = random.randint(5, 20)
            jail_embed = discord.Embed(
                title="SWEPT UP IN THE RAID",
                description=f"{player_char['name']} got caught in the police sweep and taken in",
                color=discord.Color.orange()
            )
            jail_embed.add_field(name="Detention", value=f"Held for {jail_time} minutes before being released", inline=False)
            jail_until = datetime.now() + timedelta(minutes=jail_time)
            fresh_characters[character_id]['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=jail_embed)
        else:
            clear_embed = discord.Embed(
                title="STAYED LOW DURING THE SWEEP",
                description=f"{player_char['name']} saw the police coming and got off the block in time",
                color=discord.Color.green()
            )
            clear_embed.add_field(name="Outcome", value="Avoided the sweep - back to normal", inline=False)
            await ctx.send(embed=clear_embed)

    elif event_type == "homie_in_trouble":
        homie_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        event_embed = discord.Embed(
            title="HOMIE NEEDS BACKUP",
            description=f"{homie_name} from the {player_char.get('set_name', 'set')} just called - he is pinned down by {rival_set} and needs help right now",
            color=discord.Color.orange()
        )
        event_embed.add_field(name="The Call", value=f"{homie_name} is outnumbered and calling for backup in enemy territory", inline=False)
        event_embed.set_footer(text="You ride for your homies...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle()
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(won)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="HOMIE SAVED",
                description=f"{player_char['name']} ran to the aid of {homie_name} and helped fight off the {rival_set}",
                color=discord.Color.green()
            )
            bonus_money = random.randint(100, 300)
            player_char['money'] = player_char.get('money', 0) + bonus_money
            win_embed.add_field(name="Loyalty Reward", value=f"{homie_name} hit {player_char['name']} with ${bonus_money:,} for pulling up", inline=False)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="DIED RIDING FOR THE HOMIES",
                description=f"{player_char['name']} gave their life pulling up for {homie_name}",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_set} (Died Riding for Homies)"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="BACKUP CAME BUT LOST THE FIGHT",
                description=f"{player_char['name']} pulled up for {homie_name} but they both had to retreat",
                color=discord.Color.orange()
            )
            loss_embed.add_field(name="Outcome", value=f"Both made it out alive but the {rival_set} held the block tonight", inline=False)
            await ctx.send(embed=loss_embed)

    elif event_type == "drug_deal_gone_wrong":
        event_embed = discord.Embed(
            title="DEAL WENT SIDEWAYS",
            description=f"{player_char['name']} was present when a deal in the hood went completely wrong",
            color=discord.Color.red()
        )
        event_embed.add_field(name="The Situation", value="Someone tried to rob the deal - shots fired, everyone scattering", inline=False)
        event_embed.set_footer(text="Wrong place wrong time...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        outcome_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if outcome_roll <= 40:
            money_lost = random.randint(100, max(100, player_char.get('money', 100)))
            money_lost = min(money_lost, player_char.get('money', 0))
            player_char['money'] = max(0, player_char.get('money', 0) - money_lost)
            loss_embed = discord.Embed(
                title="ROBBED IN THE CHAOS",
                description=f"{player_char['name']} got robbed during the confusion",
                color=discord.Color.red()
            )
            loss_embed.add_field(name="Money Lost", value=f"${money_lost:,} taken", inline=True)
            loss_embed.add_field(name="New Balance", value=f"${player_char['money']:,}", inline=True)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=loss_embed)
        elif outcome_roll <= 70:
            safe_embed = discord.Embed(
                title="GOT OUT OF THE CHAOS",
                description=f"{player_char['name']} dipped when the deal went wrong and avoided the fallout",
                color=discord.Color.green()
            )
            safe_embed.add_field(name="Outcome", value="Made it out clean - nothing lost", inline=False)
            await ctx.send(embed=safe_embed)
        else:
            profit = random.randint(200, 800)
            player_char['money'] = player_char.get('money', 0) + profit
            profit_embed = discord.Embed(
                title="CAME UP IN THE CHAOS",
                description=f"{player_char['name']} moved smart during the confusion and walked away with something",
                color=discord.Color.green()
            )
            profit_embed.add_field(name="Street Profit", value=f"${profit:,} picked up in the chaos", inline=True)
            profit_embed.add_field(name="New Balance", value=f"${player_char['money']:,}", inline=True)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=profit_embed)

    elif event_type == "shot_at_while_walking":
        event_embed = discord.Embed(
            title="SHOTS FIRED WALKING HOME",
            description=f"{player_char['name']} was just walking through the hood when a car slowed down and opened fire",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="Attack", value=f"Believed to be from the {rival_set} - targeted shooting", inline=False)
        event_embed.set_footer(text="Can never fully relax out here...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        hit_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if hit_roll <= 25:
            death_roll = random.randint(1, 100)
            if death_roll <= 45:
                death_embed = discord.Embed(
                    title="SHOT AND KILLED",
                    description=f"{player_char['name']} was hit and killed walking home",
                    color=discord.Color.dark_red()
                )
                death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
                dead_member = player_char.copy()
                dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_member['killed_by'] = f"{rival_set} Shooting"
                graveyard.append(dead_member)
                save_graveyard(graveyard)
                del fresh_characters[character_id]
                save_characters(fresh_characters)
                characters.update(fresh_characters)
                await ctx.send(embed=death_embed)
            else:
                wound_embed = discord.Embed(
                    title="SHOT BUT SURVIVED",
                    description=f"{player_char['name']} was hit but the wound is not fatal - got to the hospital in time",
                    color=discord.Color.orange()
                )
                wound_embed.add_field(name="Status", value="Wounded and recovering but alive", inline=False)
                await ctx.send(embed=wound_embed)
        else:
            miss_embed = discord.Embed(
                title="SHOTS MISSED",
                description=f"{player_char['name']} ducked behind a car and the shots missed - got away clean",
                color=discord.Color.green()
            )
            miss_embed.add_field(name="Outcome", value="Fast reflexes saved the day", inline=False)
            await ctx.send(embed=miss_embed)

    elif event_type == "rival_tags_your_hood":
        event_embed = discord.Embed(
            title="RIVALS TAGGED YOUR HOOD",
            description=f"{player_char['name']} woke up to find the {rival_set} had tagged over the {player_char.get('set_name', 'set')} graffiti all through the neighborhood",
            color=discord.Color.red()
        )
        event_embed.add_field(name="Disrespect", value=f"The {rival_set} crossed out the set's tags and put their own up - a direct challenge", inline=False)
        event_embed.add_field(name="Suspects", value=f"{rival_name} and crew from {rival_gang}", inline=True)
        event_embed.set_footer(text="Disrespect cannot go unanswered...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        response_roll = random.randint(1, 100)
        if response_roll <= 60:
            battle = simulate_battle()
            won = battle['player_won']
            death_roll = random.randint(1, 100)
            dies = death_roll <= calculate_death_chance(won)

            fresh_characters = load_characters()
            if character_id not in fresh_characters:
                return
            player_char = fresh_characters[character_id]

            if won and not dies:
                win_embed = discord.Embed(
                    title="CHECKED THEM FOR THE DISRESPECT",
                    description=f"{player_char['name']} went and found the {rival_set} crew responsible and made them pay",
                    color=discord.Color.green()
                )
                player_char['kills'] = player_char.get('kills', 0) + 1
                if 'kill_list' not in player_char:
                    player_char['kill_list'] = []
                player_char['kill_list'].append({
                    'victim_name': rival_name,
                    'victim_gang': rival_gang,
                    'victim_set': rival_set,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'type': 'hood_defense'
                })
                win_embed.add_field(name="Bodies", value=f"{player_char['kills']}", inline=True)
                fresh_characters[character_id] = player_char
                save_characters(fresh_characters)
                characters.update(fresh_characters)
                await ctx.send(embed=win_embed)
            elif dies:
                death_embed = discord.Embed(
                    title="DIED DEFENDING THE HOOD",
                    description=f"{player_char['name']} went to check the {rival_set} but walked into a setup",
                    color=discord.Color.dark_red()
                )
                death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
                dead_member = player_char.copy()
                dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_member['killed_by'] = f"{rival_name} ({rival_set}) Hood Defense"
                graveyard.append(dead_member)
                save_graveyard(graveyard)
                del fresh_characters[character_id]
                save_characters(fresh_characters)
                characters.update(fresh_characters)
                await ctx.send(embed=death_embed)
            else:
                loss_embed = discord.Embed(
                    title="COULDN'T CHECK THEM TODAY",
                    description=f"{player_char['name']} went to handle the disrespect but had to fall back",
                    color=discord.Color.orange()
                )
                loss_embed.add_field(name="Outcome", value="Survived but the disrespect is still out there", inline=False)
                fresh_characters[character_id] = player_char
                save_characters(fresh_characters)
                characters.update(fresh_characters)
                await ctx.send(embed=loss_embed)
        else:
            lay_low_embed = discord.Embed(
                title="LAID LOW",
                description=f"{player_char['name']} decided to let it slide and not walk into a potential setup",
                color=discord.Color.orange()
            )
            lay_low_embed.add_field(name="Decision", value="Chose not to react - playing it smart", inline=False)
            await ctx.send(embed=lay_low_embed)

    elif event_type == "unexpected_confrontation":
        event_embed = discord.Embed(
            title="UNEXPECTED RUN IN",
            description=f"{player_char['name']} was out handling regular business when they crossed paths with {rival_name} from the {rival_set}",
            color=discord.Color.orange()
        )
        event_embed.add_field(name="Chance Encounter", value="Nobody planned this - it just happened. Now what?", inline=False)
        event_embed.set_footer(text="The streets always got something waiting...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle()
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(won)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="HANDLED THE RUN IN",
                description=f"{player_char['name']} came out on top in the confrontation with {rival_name}",
                color=discord.Color.green()
            )
            player_char['kills'] = player_char.get('kills', 0) + 1
            if 'kill_list' not in player_char:
                player_char['kill_list'] = []
            player_char['kill_list'].append({
                'victim_name': rival_name,
                'victim_gang': rival_gang,
                'victim_set': rival_set,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'unexpected_confrontation'
            })
            win_embed.add_field(name="Bodies", value=f"{player_char['kills']}", inline=True)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="RUN IN TURNED FATAL",
                description=f"The chance encounter with {rival_name} ended with {player_char['name']} not making it home",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_name} ({rival_set}) Unexpected Confrontation"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="LOST THE RUN IN BUT SURVIVED",
                description=f"{player_char['name']} came out on the losing end with {rival_name} but made it out alive",
                color=discord.Color.orange()
            )
            loss_embed.add_field(name="Outcome", value="Lost this one but lived to fight again", inline=False)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=loss_embed)

    elif event_type == "retaliation_crew":
        num_attackers = random.randint(3, 6)
        attacker_names = [f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" for _ in range(num_attackers)]
        event_embed = discord.Embed(
            title="RETALIATION CREW PULLING UP",
            description=f"A crew from the {rival_set} just pulled up looking for smoke with {player_char['name']}",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="CREW PULLING UP", value="\n".join(attacker_names), inline=False)
        event_embed.add_field(name="Rival Gang", value=f"{rival_gang} - {rival_set}", inline=True)
        event_embed.set_footer(text="They came for payback...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        survival_roll = random.randint(1, 100)
        survives = survival_roll <= 45
        death_roll = random.randint(1, 100)
        dies = death_roll <= 50 if not survives else death_roll <= 10

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if dies:
            death_embed = discord.Embed(
                title="OUTNUMBERED AND OUTGUNNED",
                description=f"{player_char['name']} was caught slipping by the crew and didn't make it out",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_set} Retaliation Crew"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            survive_embed = discord.Embed(
                title="HELD IT DOWN",
                description=f"{player_char['name']} stood their ground against the retaliation crew and made it out",
                color=discord.Color.orange()
            )
            survive_embed.add_field(name="Outcome", value=f"Fought off {num_attackers} rivals and lived to tell the story", inline=False)
            survive_embed.set_footer(text="The streets respect the ones who hold it down")
            await ctx.send(embed=survive_embed)

    elif event_type == "witness_calls_police":
        event_embed = discord.Embed(
            title="WITNESS SNITCHED",
            description=f"Someone in the streets snitched on {player_char['name']} and called the police. Units are closing in.",
            color=discord.Color.blue()
        )
        event_embed.add_field(name="Police Response", value="Multiple units dispatched to the area based on witness description", inline=False)
        event_embed.set_footer(text="Can they escape in time...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        escape_roll = random.randint(1, 100)
        escapes = escape_roll <= 55

        if escapes:
            escape_embed = discord.Embed(
                title="CLEAN ESCAPE",
                description=f"{player_char['name']} heard the sirens and dipped before police could lock the area down",
                color=discord.Color.green()
            )
            escape_embed.add_field(name="Status", value="Made it back to the hood, police have no description", inline=False)
            await ctx.send(embed=escape_embed)
        else:
            jail_time = random.randint(15, 35)
            jail_embed = discord.Embed(
                title="CAUGHT BY POLICE",
                description=f"{player_char['name']} was picked up by police based on the witness description",
                color=discord.Color.orange()
            )
            jail_embed.add_field(name="Arrest Status", value=f"Booked and sentenced to {jail_time} minutes in county jail", inline=False)
            jail_until = datetime.now() + timedelta(minutes=jail_time)
            fresh_characters = load_characters()
            if character_id in fresh_characters:
                fresh_characters[character_id]['jail_until'] = jail_until.strftime('%Y-%m-%d %H:%M:%S')
                save_characters(fresh_characters)
                characters.update(fresh_characters)
            await ctx.send(embed=jail_embed)

    elif event_type == "rival_solo_retaliation":
        solo_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        event_embed = discord.Embed(
            title="SOLO RETALIATION",
            description=f"{solo_name} from the {rival_set} just rolled up on {player_char['name']} alone to handle business",
            color=discord.Color.red()
        )
        event_embed.add_field(name="One on One", value=f"{solo_name} is out here solo, no backup - just him and his anger", inline=False)
        event_embed.set_footer(text="Settling it the old way...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle()
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(won)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="HANDLED THE RETALIATION",
                description=f"{player_char['name']} bodied {solo_name} when he came for payback",
                color=discord.Color.green()
            )
            player_char['kills'] = player_char.get('kills', 0) + 1
            if 'kill_list' not in player_char:
                player_char['kill_list'] = []
            player_char['kill_list'].append({
                'victim_name': solo_name,
                'victim_gang': rival_gang,
                'victim_set': rival_set,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'retaliation_defense'
            })
            win_embed.add_field(name="Updated Bodies", value=f"Total Bodies: {player_char['kills']}", inline=False)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="GOT CAUGHT LACKING",
                description=f"{solo_name} caught {player_char['name']} slipping and put him down",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{solo_name} ({rival_set}) Solo Retaliation"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="GOT BEAT BUT SURVIVED",
                description=f"{solo_name} got the better of {player_char['name']} but let him live",
                color=discord.Color.orange()
            )
            loss_embed.add_field(name="Outcome", value="Lost the fight but made it out breathing", inline=False)
            await ctx.send(embed=loss_embed)

    elif event_type == "bounty_placed":
        bounty_amount = random.randint(500, 3000)
        event_embed = discord.Embed(
            title="BOUNTY ON YOUR HEAD",
            description=f"The {rival_set} put a ${bounty_amount:,} bounty on {player_char['name']}",
            color=discord.Color.gold()
        )
        event_embed.add_field(name="Bounty Amount", value=f"${bounty_amount:,}", inline=True)
        event_embed.add_field(name="Placed By", value=f"{rival_set}", inline=True)
        event_embed.add_field(name="Warning", value=f"Everyone in the streets knows there is paper on {player_char['name']} - watch your back", inline=False)
        event_embed.set_footer(text="The price of putting in work")
        fresh_characters = load_characters()
        if character_id in fresh_characters:
            fresh_characters[character_id]['bounty'] = fresh_characters[character_id].get('bounty', 0) + bounty_amount
            save_characters(fresh_characters)
            characters.update(fresh_characters)
        await ctx.send(embed=event_embed)

    elif event_type == "jumped_walking_home":
        num_jumpers = random.randint(2, 5)
        event_embed = discord.Embed(
            title="JUMPED WALKING HOME",
            description=f"{player_char['name']} got rushed by {num_jumpers} opps on the way home",
            color=discord.Color.red()
        )
        event_embed.add_field(name="Ambush", value=f"They were waiting - {num_jumpers} on one", inline=False)
        event_embed.set_footer(text="Nowhere to run...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        survival_roll = random.randint(1, 100)
        survives = survival_roll <= 50
        death_roll = random.randint(1, 100)
        dies = death_roll <= 35 if not survives else death_roll <= 8

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if dies:
            death_embed = discord.Embed(
                title="JUMPED AND KILLED",
                description=f"{player_char['name']} was jumped and beaten to death by the crew",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_set} Jump"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        elif survives:
            survive_embed = discord.Embed(
                title="FOUGHT THROUGH THE JUMP",
                description=f"{player_char['name']} got jumped but scrapped their way out and made it home",
                color=discord.Color.orange()
            )
            survive_embed.add_field(name="Outcome", value="Banged up but alive - made it back to the block", inline=False)
            await ctx.send(embed=survive_embed)
        else:
            survive_embed = discord.Embed(
                title="BARELY ESCAPED THE JUMP",
                description=f"{player_char['name']} broke away from the jump and ran before it got worse",
                color=discord.Color.orange()
            )
            survive_embed.add_field(name="Outcome", value="Took some hits but got away before things went fatal", inline=False)
            await ctx.send(embed=survive_embed)

    elif event_type == "rival_spots_new_member":
        event_embed = discord.Embed(
            title="NEW FACE GETS NOTICED",
            description=f"Word traveled fast. {rival_name} from the {rival_set} knows {player_char['name']} is out here and is coming to send a message.",
            color=discord.Color.red()
        )
        event_embed.add_field(name="Threat", value=f"{rival_name} is coming to test {player_char['name']} before they get established", inline=False)
        event_embed.add_field(name="Enemy Info", value=f"Gang: {rival_gang}\nSet: {rival_set}", inline=True)
        event_embed.set_footer(text="The streets already know your name...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle()
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(won)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="PASSED THE TEST",
                description=f"{player_char['name']} handled {rival_name} and let the whole hood know they are not to be played with",
                color=discord.Color.green()
            )
            player_char['kills'] = player_char.get('kills', 0) + 1
            if 'kill_list' not in player_char:
                player_char['kill_list'] = []
            player_char['kill_list'].append({
                'victim_name': rival_name,
                'victim_gang': rival_gang,
                'victim_set': rival_set,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'creation_event'
            })
            win_embed.add_field(name="Bodies", value=f"{player_char['kills']}", inline=True)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="TAKEN OUT",
                description=f"{player_char['name']} got taken out by {rival_name} before they could establish themselves",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_name} ({rival_set})"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="ROUGH DAY",
                description=f"{player_char['name']} got tested and lost but survived. The streets already humbled them.",
                color=discord.Color.orange()
            )
            loss_embed.add_field(name="Outcome", value="Lost the fight but lived to learn from it", inline=False)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=loss_embed)

    elif event_type == "initiated_by_hood":
        char_set = player_char.get('set_name', 'the set')
        num_homies = random.randint(5, 12)
        event_embed = discord.Embed(
            title="INITIATION - GETTING JUMPED IN",
            description=f"Before {player_char['name']} can officially run with the {char_set}, they gotta get jumped in. {num_homies} homies are waiting.",
            color=discord.Color.purple()
        )
        event_embed.add_field(name="The Initiation", value=f"{num_homies} members of the {char_set} are about to put hands on {player_char['name']} for 60 seconds", inline=False)
        event_embed.set_footer(text="Everyone goes through it...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        survive_roll = random.randint(1, 100)
        if survive_roll <= 85:
            success_embed = discord.Embed(
                title="OFFICIALLY JUMPED IN",
                description=f"{player_char['name']} took the beat down and didn't fold. Now officially a member of the {char_set}.",
                color=discord.Color.green()
            )
            success_embed.add_field(name="Hood Status", value=f"Officially recognized by the {char_set} - welcome to the family", inline=False)
            success_embed.set_footer(text="One of us now")
            await ctx.send(embed=success_embed)
        else:
            fail_embed = discord.Embed(
                title="INITIATION GONE WRONG",
                description=f"{player_char['name']} couldn't handle the initiation and got seriously hurt",
                color=discord.Color.orange()
            )
            fail_embed.add_field(name="Outcome", value="Survived but in bad shape - still made it into the set but paid a heavy price", inline=False)
            await ctx.send(embed=fail_embed)

    elif event_type == "found_on_wrong_block":
        event_embed = discord.Embed(
            title="WRONG BLOCK",
            description=f"{player_char['name']} was on the wrong side of the map when {rival_name} from {rival_set} spotted them deep in enemy territory",
            color=discord.Color.red()
        )
        event_embed.add_field(name="Caught Out There", value=f"Deep in {rival_set} territory with no backup - this is a problem", inline=False)
        event_embed.set_footer(text="Nowhere to run on the wrong block...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle()
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= (calculate_death_chance(won) + 10)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="GOT OUT ALIVE",
                description=f"{player_char['name']} scrapped their way out of enemy territory",
                color=discord.Color.green()
            )
            win_embed.add_field(name="Outcome", value="Made it back to the hood - won't make that mistake again", inline=False)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="KILLED ON ENEMY TURF",
                description=f"{player_char['name']} was caught on the wrong block and paid the price",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_name} ({rival_set}) Wrong Block"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            escape_embed = discord.Embed(
                title="BARELY GOT OUT",
                description=f"{player_char['name']} got beat up on enemy turf but managed to limp back home",
                color=discord.Color.orange()
            )
            escape_embed.add_field(name="Outcome", value="Learned the hard way where the boundaries are", inline=False)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=escape_embed)

    elif event_type == "old_beef_resurfaces":
        event_embed = discord.Embed(
            title="OLD BEEF RESURFACES",
            description=f"Before {player_char['name']} could settle in, {rival_name} from the {rival_set} came around claiming there is already history between them.",
            color=discord.Color.dark_orange()
        )
        event_embed.add_field(name="The Situation", value=f"{rival_name} says the beef is from before and it's time to settle it", inline=False)
        event_embed.add_field(name="Enemy", value=f"{rival_gang} - {rival_set}", inline=True)
        event_embed.set_footer(text="Old beef never dies in the streets...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle()
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(won)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        player_char = fresh_characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="BEEF SQUASHED",
                description=f"{player_char['name']} handled {rival_name} and that old beef is officially dead",
                color=discord.Color.green()
            )
            player_char['kills'] = player_char.get('kills', 0) + 1
            if 'kill_list' not in player_char:
                player_char['kill_list'] = []
            player_char['kill_list'].append({
                'victim_name': rival_name,
                'victim_gang': rival_gang,
                'victim_set': rival_set,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'old_beef'
            })
            win_embed.add_field(name="Bodies", value=f"{player_char['kills']}", inline=True)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="OLD BEEF TOOK THEM OUT",
                description=f"{player_char['name']} couldn't shake the old history - {rival_name} settled it permanently",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Body Count: {player_char.get('kills', 0)}\nMoney: ${player_char.get('money', 0):,}\nStatus: DECEASED", inline=False)
            dead_member = player_char.copy()
            dead_member['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_member['killed_by'] = f"{rival_name} ({rival_set}) Old Beef"
            graveyard.append(dead_member)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="OLD BEEF STILL GOING",
                description=f"{player_char['name']} couldn't settle the beef today but is still breathing",
                color=discord.Color.orange()
            )
            loss_embed.add_field(name="Outcome", value="The beef is still alive - this is not over", inline=False)
            fresh_characters[character_id] = player_char
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=loss_embed)

    elif event_type == "police_already_watching":
        event_embed = discord.Embed(
            title="POLICE ALREADY ON YOU",
            description=f"The LAPD gang unit already has eyes on {player_char['name']}. They're watching every move.",
            color=discord.Color.blue()
        )
        event_embed.add_field(name="Surveillance", value="Gang detectives already building a file on the member", inline=False)
        event_embed.add_field(name="Warning", value="Any crime committed has a higher chance of getting caught for the next few runs", inline=False)
        event_embed.set_footer(text="They know your face before you know theirs")
        fresh_characters = load_characters()
        if character_id in fresh_characters:
            fresh_characters[character_id]['police_heat'] = True
            save_characters(fresh_characters)
            characters.update(fresh_characters)
        await ctx.send(embed=event_embed)


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
