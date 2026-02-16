import discord
from discord.ext import commands
import json
import os
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

GANG_FILE = 'gang.json'
PRISON_FILE = 'prison.json'
GRAVEYARD_FILE = 'graveyard.json'

LA_GANGS = {
    "Rollin 60s Crips": {
        "color": 0x0000FF,
        "territory": "West Adams, Hyde Park",
        "rivals": ["Inglewood Family Bloods", "Black P Stones", "Eight Tray Gangster Crips"],
        "allies": ["Rollin 90s Crips", "Rollin 40s Crips"]
    },
    "Eight Tray Gangster Crips": {
        "color": 0x0000FF,
        "territory": "Inglewood, Manchester",
        "rivals": ["Rollin 60s Crips", "Hoover Criminals", "Inglewood Family Bloods"],
        "allies": ["Tray Way Crips", "Gangster Crips"]
    },
    "Hoover Criminals": {
        "color": 0x0000FF,
        "territory": "South Central, Hoover Street",
        "rivals": ["Eight Tray Gangster Crips", "Rollin 60s Crips", "Slauson Village Crips"],
        "allies": []
    },
    "Grape Street Crips": {
        "color": 0x800080,
        "territory": "Watts, Jordan Downs",
        "rivals": ["Bounty Hunter Bloods", "PJ Watts Crips", "Watts Varrio Grape"],
        "allies": ["Rollin 60s Crips", "Watts Crips"]
    },
    "Inglewood Family Bloods": {
        "color": 0xFF0000,
        "territory": "Inglewood, Century Boulevard",
        "rivals": ["Rollin 60s Crips", "Eight Tray Gangster Crips", "Centinela Park Family Bloods"],
        "allies": ["Blood Stone Villains", "Crenshaw Mafia Bloods"]
    },
    "Black P Stones": {
        "color": 0xFF0000,
        "territory": "Crenshaw, Jefferson Park",
        "rivals": ["Rollin 60s Crips", "Rollin 20s Crips", "Rollin 30s Crips"],
        "allies": ["Inglewood Family Bloods", "Campanella Park Pirus"]
    },
    "Bounty Hunter Bloods": {
        "color": 0xFF0000,
        "territory": "Watts, Nickerson Gardens",
        "rivals": ["Grape Street Crips", "PJ Watts Crips", "Watts Crips"],
        "allies": ["Inglewood Family Bloods", "Black P Stones"]
    },
    "MS-13": {
        "color": 0x00FF00,
        "territory": "Pico-Union, Koreatown, Panorama City",
        "rivals": ["18th Street", "Mara Salvatrucha Rebels", "LAPD"],
        "allies": []
    },
    "18th Street": {
        "color": 0x00FF00,
        "territory": "Rampart, Pico-Union, MacArthur Park",
        "rivals": ["MS-13", "Clanton 14", "Columbia Lil Cycos"],
        "allies": []
    },
    "Clanton 14": {
        "color": 0x00FF00,
        "territory": "South Central, Hooper Avenue",
        "rivals": ["18th Street", "Florence 13", "Florencia 13"],
        "allies": ["White Fence", "Maravilla"]
    },
    "Florencia 13": {
        "color": 0x00FF00,
        "territory": "Florence, Firestone",
        "rivals": ["Clanton 14", "East Coast Crips", "Hoover Criminals"],
        "allies": ["Varrio Nuevo Estrada", "Watts Varrio Grape"]
    },
    "East Coast Crips": {
        "color": 0x0000FF,
        "territory": "Southeast LA, Watts",
        "rivals": ["Florencia 13", "Grape Street Crips", "Bounty Hunter Bloods"],
        "allies": ["Rollin 60s Crips", "Neighborhood Crips"]
    },
    "Crenshaw Mafia Bloods": {
        "color": 0xFF0000,
        "territory": "Crenshaw, Leimert Park",
        "rivals": ["Rollin 60s Crips", "Black P Stones", "Rollin 20s Crips"],
        "allies": ["Inglewood Family Bloods", "Blood Stone Villains"]
    },
    "Rollin 20s Crips": {
        "color": 0x0000FF,
        "territory": "West Adams, Arlington Heights",
        "rivals": ["Black P Stones", "Crenshaw Mafia Bloods", "Rollin 30s Crips"],
        "allies": ["Rollin 60s Crips", "Rollin 40s Crips"]
    },
    "Piru Street Boys": {
        "color": 0xFF0000,
        "territory": "Compton, Piru Street",
        "rivals": ["Compton Crips", "Kelly Park Crips", "Rollin 20s Bloods"],
        "allies": ["Tree Top Pirus", "Campanella Park Pirus"]
    },
    "Compton Crips": {
        "color": 0x0000FF,
        "territory": "Compton, Central Avenue",
        "rivals": ["Piru Street Boys", "Tree Top Pirus", "Compton Varrio 70s"],
        "allies": ["Kelly Park Crips", "Neighborhood Crips"]
    },
    "Avalon Gangster Crips": {
        "color": 0x0000FF,
        "territory": "South Central, Avalon Boulevard",
        "rivals": ["Florencia 13", "East Coast Crips", "Bounty Hunter Bloods"],
        "allies": ["Compton Crips", "Neighborhood Crips"]
    },
    "Blood Stone Villains": {
        "color": 0xFF0000,
        "territory": "Inglewood, Manchester Boulevard",
        "rivals": ["Eight Tray Gangster Crips", "Rollin 60s Crips", "Hoover Criminals"],
        "allies": ["Inglewood Family Bloods", "Crenshaw Mafia Bloods"]
    }
}

FIRST_NAMES = [
    "Darius", "Malik", "Jerome", "DeShawn", "Tremaine", "Jaylen", "Kendrick", "Marcus",
    "Devon", "Lamar", "Antoine", "Tyrese", "Dontae", "Rasheed", "Kareem", "Jamal",
    "Carlos", "Miguel", "Jose", "Luis", "Juan", "Ricardo", "Antonio", "Eduardo",
    "Damien", "Terrell", "Marquise", "Deon", "Kevon", "Trayvon", "Jalen", "Dwayne",
    "Cortez", "Reggie", "Leroy", "Cedric", "Alvin", "Bernard", "Clarence", "Derrick"
]

LAST_NAMES = [
    "Washington", "Jackson", "Williams", "Johnson", "Davis", "Brown", "Jones", "Taylor",
    "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Rodriguez", "Lopez", "Gonzalez",
    "Robinson", "Clark", "Lewis", "Walker", "Hall", "Allen", "Young", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams",
    "Nelson", "Baker", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips"
]

HOOD_NAMES = [
    "Lil", "Big", "Young", "OG", "Baby", "Tiny", "Savage", "Ghost",
    "Slim", "Loc", "Crazy", "Menace", "Demon", "Shadow", "Ice", "Stone",
    "Trigger", "Speedy", "Joker", "Villain", "Monster", "Killer", "Draco", "Ace"
]

LOCATIONS = [
    "Crenshaw", "Compton", "Watts", "Inglewood", "South Central",
    "East LA", "Boyle Heights", "Pico-Union", "Hyde Park", "Florence",
    "Lynwood", "Carson", "Paramount", "Hawthorne", "Gardena"
]

FEMALE_NAMES = [
    "Keisha", "Tasha", "Shaniqua", "Destiny", "Brianna", "Latoya", "Monique", "Alicia",
    "Crystal", "Tamika", "Niecy", "Shayla", "Jasmine", "Unique", "Precious", "Diamond",
    "Maria", "Gabriela", "Yesenia", "Vanessa", "Selena", "Rosa", "Carmen", "Lupita",
    "Amber", "Tiffany", "Shawna", "Dominique", "Alexis", "Candice", "Porsha", "Tiara"
]

SMOKE_STRAINS = [
    "Runtz", "Gelato", "Backwood", "Loud", "Za", "Exotic", "Gas", "Cookies",
    "Purple Haze", "OG Kush", "Cali Weed", "Dank", "Top Shelf", "Reggie", "Dirt"
]

DRINK_OPTIONS = [
    "Hennessy", "Patron", "D'usse", "1942", "Ciroc", "Lean", "40oz",
    "Olde English", "Modelo", "Corona", "Bud", "Henny and Coke"
]

CARS = [
    "Chevy Impala", "Dodge Charger", "Cadillac Escalade", "Chevy Caprice",
    "BMW 5 Series", "Mercedes S Class", "Dodge Challenger", "Chevy Monte Carlo",
    "Buick Regal", "Ford Crown Vic", "Oldsmobile Cutlass", "Pontiac Grand Prix",
    "Chevy Tahoe", "GMC Yukon", "Lincoln Town Car"
]

JEWELRY = [
    "gold chain", "diamond watch", "grillz", "gold ring", "diamond chain",
    "gold bracelet", "pinky ring", "Cuban link", "Rolex", "AP watch"
]

CLOTHES = [
    "Dickies fit", "all blue Chucks", "all red Nikes", "white tee and khakis",
    "fresh Jordans", "Dior fit", "Amiri jeans", "Givenchy shirt", "Balmain jacket",
    "Lakers jersey", "Dodgers cap", "Crip blue hoodie", "Blood red hoodie"
]

DRUGS = ["weed", "crack", "pills", "meth", "dope"]

ROB_TARGETS = [
    "a corner store", "a rival dealer", "a gas station", "a trap house",
    "a stash house", "a local plug", "a dope boy", "a random mark"
]

DRIVE_BY_OUTCOMES_WIN = [
    "You pull up on the block and let it ring. Bodies drop. The block goes silent.",
    "The homies ride through and air it out. Rivals scatter. You own these streets.",
    "You catch them lacking at the trap. The hit is clean. Word spreads fast.",
    "Quick and quiet. In and out. One less problem on the block.",
    "They never saw you coming. The streets talk about it for weeks."
]

DRIVE_BY_OUTCOMES_LOSS = [
    "They were ready. Shots come back at you. You barely make it out.",
    "The hit goes wrong. Your car gets lit up. You dip but take damage.",
    "They had more shooters than expected. You fall back with losses.",
    "Someone snitched about the lick. They were waiting. You escape but the heat is up.",
    "The block was fortified. You ride out empty handed and shaken."
]

POLICE_OUTCOMES = [
    "Marked units roll up from both ends. You are surrounded.",
    "A helicopter locks onto you. Ground units move in fast.",
    "An undercover had eyes on you the whole time. You never saw it coming.",
    "LAPD SWAT kicks the door. It is over before it starts.",
    "A tip came in. The task force was waiting."
]

SMOKE_SESSIONS = [
    "You spark a backwood and lean back. The block gets quiet for a minute.",
    "You roll up a fat one with the homies. Smoke fills the car.",
    "You hit the blunt and pass it. For a minute everything is calm.",
    "You fire up some gas and zone out. The streets can wait.",
    "You and the gang smoke out on the porch. Just another night.",
    "You roll a wood by yourself on the steps. Nobody bothers you.",
    "The homie pulls out a zip of Za. You all smoke until the sun comes up."
]

DRUNK_SESSIONS = [
    "You crack open a bottle of Henny with the gang. Things get loud.",
    "You sip lean all night on the porch. Time slows down.",
    "You and the homies pop bottles at the spot. It gets wild.",
    "You pour up a four and zone. The block is yours tonight.",
    "You drink until the sun comes up. No problems tonight."
]

GIRL_ENCOUNTERS = [
    "She pulls up in a Honda Civic looking for a good time.",
    "You meet her at a kickback and she is feeling you hard.",
    "She been eyeing you from across the block for weeks. Tonight she comes through.",
    "You link with her at the motel off Crenshaw. No strings.",
    "She texts you at 2am. You already know what it is.",
    "You meet her at a party in Inglewood. She leaves with you.",
    "She is a rider. Been rocking with the hood for years. Tonight she is all yours."
]

GIRL_OUTCOMES = [
    "Good night. No cap.",
    "She is down for whatever. You have a real one for the night.",
    "You end up talking until the morning. She might be different.",
    "Quick and gone. That is all it was.",
    "She brings a friend. The night gets interesting.",
    "She is with it. You kick it until the sun comes up.",
    "She stays the night. The homies clown you in the morning."
]

FLEX_ITEMS = [
    ("a fresh pair of Jordans", 200, 15),
    ("a gold chain", 500, 25),
    ("a Rolex watch", 2000, 60),
    ("a Cuban link", 1500, 45),
    ("a diamond grill", 1000, 35),
    ("a Balmain fit", 800, 30),
    ("a Dodge Charger", 5000, 100),
    ("a Chevy Impala on 24s", 8000, 150),
    ("a AP watch", 3000, 80),
    ("a pinky ring with VVS", 2500, 70)
]

JAIL_SENTENCES = {
    "short":  (1, 3),
    "medium": (4, 7),
    "long":   (8, 14)
}

TATTOO_OPTIONS = [
    ("RIP tattoo on your neck", 100, 10),
    ("hood name on your chest", 150, 15),
    ("gang set on your arm", 200, 20),
    ("teardrops under your eye", 80, 8),
    ("full sleeve on your right arm", 500, 40),
    ("back piece of the hood", 800, 60),
    ("face tattoo", 300, 30),
    ("LA on your hand", 120, 12)
]

WEAPONS = [
    ("Glock 19", 500, 20),
    ("AK-47", 1500, 50),
    ("AR-15", 1800, 60),
    ("Draco", 2000, 70),
    ("Shotgun", 800, 30),
    ("Desert Eagle", 1200, 45),
    ("Mac-10", 900, 35),
    ("Uzi", 1100, 40)
]

GANG_RANKS = ["Recruit", "Soldier", "OG", "Shot Caller", "Boss"]

PRISON_EVENTS = [
    "You keep your head down and do your time clean.",
    "You get into a fight on the yard but handle it.",
    "You link with some homies from the hood doing time.",
    "You pick up a book and start reading. Time passes.",
    "You work out every day. You come out bigger than you went in.",
    "You get a visit from your girl. She is still holding it down.",
    "You hear about what happened on the block. It hurts to be locked up.",
    "You get into it with a rival on the yard. You handle your business."
]


def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def generate_id():
    players   = load_data(GANG_FILE)
    graveyard = load_data(GRAVEYARD_FILE)
    prison    = load_data(PRISON_FILE)
    existing  = (
        {p.get('id') for p in players.values()} |
        {p.get('id') for p in graveyard.values()} |
        {p.get('id') for p in prison.values()}
    )
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing:
            return new_id

def get_rank(rep):
    if rep < 100:    return "Recruit"
    elif rep < 300:  return "Soldier"
    elif rep < 600:  return "OG"
    elif rep < 1000: return "Shot Caller"
    else:            return "Boss"

def get_heat_level(heat):
    if heat < 20:   return "Cold"
    elif heat < 40: return "Warm"
    elif heat < 60: return "Hot"
    elif heat < 80: return "Burning"
    else:           return "Fugitive"

def is_rival(player_gang, target_gang):
    gang_data = LA_GANGS.get(player_gang, {})
    return target_gang in gang_data.get("rivals", [])

def days_since(date_str):
    then  = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    delta = datetime.now() - then
    return delta.days

def get_player(user_id):
    players = load_data(GANG_FILE)
    for p in players.values():
        if p.get('user_id') == user_id:
            return p
    return None

def save_player(player):
    players = load_data(GANG_FILE)
    players[player['id']] = player
    save_data(GANG_FILE, players)

def kill_player(player, killed_by):
    players   = load_data(GANG_FILE)
    graveyard = load_data(GRAVEYARD_FILE)
    dead              = player.copy()
    dead['killed_by'] = killed_by
    dead['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    graveyard[player['id']] = dead
    save_data(GRAVEYARD_FILE, graveyard)
    if player['id'] in players:
        del players[player['id']]
        save_data(GANG_FILE, players)

def send_to_prison(player, days):
    players = load_data(GANG_FILE)
    prison  = load_data(PRISON_FILE)
    inmate                  = player.copy()
    inmate['release_date']  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    inmate['sentence_days'] = days
    prison[player['id']]    = inmate
    save_data(PRISON_FILE, prison)
    if player['id'] in players:
        del players[player['id']]
        save_data(GANG_FILE, players)

def check_prison_release():
    prison  = load_data(PRISON_FILE)
    players = load_data(GANG_FILE)
    released = []
    for pid, inmate in list(prison.items()):
        days_served = days_since(inmate['release_date'])
        if days_served >= inmate['sentence_days']:
            inmate['heat']  = max(0, inmate.get('heat', 0) - 30)
            inmate['cash']  = max(0, inmate.get('cash', 0) - random.randint(100, 500))
            players[pid]    = inmate
            del prison[pid]
            released.append(inmate)
    save_data(PRISON_FILE, prison)
    save_data(GANG_FILE, players)
    return released

def is_in_prison(user_id):
    prison = load_data(PRISON_FILE)
    for inmate in prison.values():
        if inmate.get('user_id') == user_id:
            return inmate
    return None

def is_dead(user_id):
    graveyard = load_data(GRAVEYARD_FILE)
    for dead in graveyard.values():
        if dead.get('user_id') == user_id:
            return dead
    return None

async def check_blocked(ctx):
    user_id = str(ctx.author.id)
    dead    = is_dead(user_id)
    if dead:
        await ctx.send(f"**{dead['name']}** is dead. One life. It is over.")
        return True
    inmate = is_in_prison(user_id)
    if inmate:
        days_left = max(0, inmate['sentence_days'] - days_since(inmate['release_date']))
        if days_left > 0:
            await ctx.send(f"**{inmate['name']}** is locked up. {days_left} day(s) left. Use `?status`.")
            return True
        else:
            check_prison_release()
    return False


@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Gang Simulator Ready')

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs.")
        return False
    return True


@bot.command(name='start')
async def start(ctx):
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return

    if get_player(user_id):
        await ctx.send("You already have a character. Use `?profile`.")
        return

    name     = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    hood_tag = random.choice(HOOD_NAMES)
    location = random.choice(LOCATIONS)
    pid      = generate_id()

    player = {
        "id":         pid,
        "name":       name,
        "hood_name":  hood_tag,
        "user_id":    user_id,
        "username":   str(ctx.author),
        "gang":       None,
        "rank":       "Recruit",
        "rep":        0,
        "cash":       random.randint(50, 200),
        "heat":       0,
        "location":   location,
        "kills":      0,
        "arrests":    0,
        "weapon":     None,
        "car":        None,
        "tattoos":    [],
        "body_count": 0,
        "times_high": 0,
        "times_drunk": 0,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    save_player(player)

    embed = discord.Embed(
        title=f"{name} - aka {hood_tag}",
        description=f"From the streets of {location}. Your story starts now.",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="Cash",  value=f"${player['cash']}", inline=True)
    embed.add_field(name="Rep",   value="0",                  inline=True)
    embed.add_field(name="Heat",  value="Cold",               inline=True)
    embed.add_field(name="Gang",  value="None - use `?join`", inline=False)
    embed.set_footer(text=f"ID: {pid} | One life. Do not waste it.")
    await ctx.send(embed=embed)


@bot.command(name='join')
async def join_gang(ctx):
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return
    if player.get('gang'):
        await ctx.send(f"You are already repping **{player['gang']}**. Ride or die.")
        return

    gang_list      = list(LA_GANGS.keys())
    gang_list_text = "\n".join(f"`{i+1}.` {g}" for i, g in enumerate(gang_list))

    embed = discord.Embed(
        title="Pick Your Set",
        description=f"Type the number of the gang you want to join.\n\n{gang_list_text}",
        color=discord.Color.dark_grey()
    )
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        msg    = await bot.wait_for('message', check=check, timeout=30)
        choice = int(msg.content) - 1
        if choice < 0 or choice >= len(gang_list):
            await ctx.send("Invalid choice.")
            return

        chosen_gang       = gang_list[choice]
        gang_info         = LA_GANGS[chosen_gang]
        player['gang']    = chosen_gang
        player['rep']     = player.get('rep', 0) + 25
        save_player(player)

        embed = discord.Embed(
            title=f"Welcome to {chosen_gang}",
            description=f"You are now repping {chosen_gang}. Do not embarrass the set.",
            color=discord.Color(gang_info['color'])
        )
        embed.add_field(name="Territory", value=gang_info['territory'],                        inline=False)
        embed.add_field(name="Rivals",    value=", ".join(gang_info['rivals']) or "None",      inline=False)
        embed.add_field(name="Allies",    value=", ".join(gang_info['allies']) or "None",      inline=False)
        embed.add_field(name="Rank",      value="Recruit",                                     inline=True)
        embed.add_field(name="Rep Bonus", value="+25",                                         inline=True)
        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("Took too long. Use `?join` again.")


@bot.command(name='profile')
async def profile(ctx, user: discord.Member = None):
    target  = user or ctx.author
    user_id = str(target.id)
    player  = get_player(user_id)

    if not player:
        await ctx.send(f"No character found for {target.name}.")
        return

    gang      = player.get('gang') or "Unaffiliated"
    rank      = get_rank(player.get('rep', 0))
    heat      = get_heat_level(player.get('heat', 0))
    gang_info = LA_GANGS.get(gang, {})
    color     = discord.Color(gang_info.get('color', 0x555555))

    embed = discord.Embed(
        title=f"{player['name']} - aka {player['hood_name']}",
        description=f"From {player['location']} | Repping {gang}",
        color=color
    )
    embed.add_field(name="Rank",       value=rank,                              inline=True)
    embed.add_field(name="Rep",        value=str(player.get('rep', 0)),         inline=True)
    embed.add_field(name="Cash",       value=f"${player.get('cash', 0)}",       inline=True)
    embed.add_field(name="Heat",       value=heat,                              inline=True)
    embed.add_field(name="Kills",      value=str(player.get('kills', 0)),       inline=True)
    embed.add_field(name="Arrests",    value=str(player.get('arrests', 0)),     inline=True)
    embed.add_field(name="Weapon",     value=player.get('weapon') or "None",    inline=True)
    embed.add_field(name="Car",        value=player.get('car') or "None",       inline=True)
    embed.add_field(name="Body Count", value=str(player.get('body_count', 0)),  inline=True)
    embed.add_field(name="Times High", value=str(player.get('times_high', 0)),  inline=True)
    embed.add_field(name="Times Drunk",value=str(player.get('times_drunk', 0)), inline=True)
    if player.get('tattoos'):
        embed.add_field(name="Tattoos", value=", ".join(player['tattoos'][:3]), inline=False)
    embed.set_footer(text=f"ID: {player['id']}")
    await ctx.send(embed=embed)


@bot.command(name='deal')
async def deal(ctx):
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return
    if not player.get('gang'):
        await ctx.send("Join a gang first with `?join`.")
        return

    heat = player.get('heat', 0)
    if heat >= 80:
        await ctx.send("Heat is too high. Use `?laylow` first.")
        return

    await ctx.send(f"**{player['name']}** hits the block...")
    await asyncio.sleep(2)

    drug          = random.choice(DRUGS)
    heat_gain     = random.randint(3, 10)
    police_chance = int(heat * 0.4)
    caught        = random.randint(1, 100) <= police_chance

    if caught:
        sentence_type     = random.choice(["short", "medium"])
        days              = random.randint(*JAIL_SENTENCES[sentence_type])
        player['arrests'] = player.get('arrests', 0) + 1
        player['heat']    = min(100, heat + 20)
        save_player(player)
        send_to_prison(player, days)

        embed = discord.Embed(title="BUSTED", description=random.choice(POLICE_OUTCOMES), color=discord.Color.red())
        embed.add_field(name="Charge",   value="Possession with intent",    inline=False)
        embed.add_field(name="Sentence", value=f"{days} day(s)",            inline=True)
        embed.set_footer(text="Use ?status to check release date.")
        await ctx.send(embed=embed)
        return

    outcome_roll = random.randint(1, 100)
    if outcome_roll <= 60:
        cash_earned = random.randint(150, 500)
        rep_gain    = random.randint(5, 15)
        result      = "clean"
    elif outcome_roll <= 85:
        cash_earned = random.randint(50, 149)
        rep_gain    = random.randint(1, 5)
        result      = "slow"
    else:
        cash_earned = 0
        rep_gain    = 0
        heat_gain  += random.randint(5, 15)
        result      = "dry"

    player['cash'] = player.get('cash', 0) + cash_earned
    player['rep']  = player.get('rep', 0) + rep_gain
    player['heat'] = min(100, player.get('heat', 0) + heat_gain)
    save_player(player)

    desc  = (f"The {drug} moves fast. Cash stacks up." if result == "clean" else
             f"Slow night. The {drug} moves but money is light." if result == "slow" else
             f"Block is dry. Nothing moves tonight.")
    color = discord.Color.green() if result == "clean" else discord.Color.orange() if result == "slow" else discord.Color.dark_grey()

    embed = discord.Embed(title="TRAP REPORT", description=desc, color=color)
    embed.add_field(name="Earned",    value=f"${cash_earned}",                           inline=True)
    embed.add_field(name="Rep",       value=f"+{rep_gain}",                              inline=True)
    embed.add_field(name="Heat",      value=f"+{heat_gain} ({get_heat_level(player['heat'])})", inline=True)
    embed.add_field(name="Cash",      value=f"${player['cash']}",                        inline=True)
    embed.add_field(name="Total Rep", value=str(player['rep']),                          inline=True)
    embed.add_field(name="Rank",      value=get_rank(player['rep']),                     inline=True)
    await ctx.send(embed=embed)


@bot.command(name='rob')
async def rob(ctx):
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return
    if not player.get('gang'):
        await ctx.send("Join a gang first with `?join`.")
        return

    heat = player.get('heat', 0)
    if heat >= 80:
        await ctx.send("Heat is too high. Use `?laylow` first.")
        return

    target = random.choice(ROB_TARGETS)
    await ctx.send(f"**{player['name']}** is moving on {target}...")
    await asyncio.sleep(2)

    success_chance = max(30, 70 - int(heat * 0.5))
    roll           = random.randint(1, 100)
    police_chance  = int(heat * 0.5)
    caught         = random.randint(1, 100) <= police_chance

    if caught:
        days              = random.randint(*JAIL_SENTENCES[random.choice(["medium", "long"])])
        player['arrests'] = player.get('arrests', 0) + 1
        save_player(player)
        send_to_prison(player, days)

        embed = discord.Embed(title="CAUGHT IN THE ACT", description=random.choice(POLICE_OUTCOMES), color=discord.Color.red())
        embed.add_field(name="Charge",   value="Armed robbery",  inline=False)
        embed.add_field(name="Sentence", value=f"{days} day(s)", inline=True)
        await ctx.send(embed=embed)
        return

    if roll <= success_chance:
        cash_earned    = random.randint(300, 1200)
        rep_gain       = random.randint(10, 30)
        heat_gain      = random.randint(15, 25)
        player['cash'] = player.get('cash', 0) + cash_earned
        player['rep']  = player.get('rep', 0) + rep_gain
        player['heat'] = min(100, player.get('heat', 0) + heat_gain)
        save_player(player)

        embed = discord.Embed(title="LICK SUCCESSFUL", description=f"You run up on {target} and take everything.", color=discord.Color.green())
        embed.add_field(name="Cash",  value=f"${cash_earned}", inline=True)
        embed.add_field(name="Rep",   value=f"+{rep_gain}",    inline=True)
        embed.add_field(name="Heat",  value=f"+{heat_gain}",   inline=True)
    else:
        heat_gain      = random.randint(10, 20)
        player['heat'] = min(100, player.get('heat', 0) + heat_gain)
        save_player(player)

        embed = discord.Embed(title="LICK FAILED", description=f"Something went wrong at {target}. You dipped empty handed.", color=discord.Color.orange())
        embed.add_field(name="Heat", value=f"+{heat_gain}", inline=True)

    await ctx.send(embed=embed)


@bot.command(name='driveby')
async def drive_by(ctx, target_user: discord.Member = None):
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)

    if not player:
        await ctx.send("Use `?start` first.")
        return
    if not player.get('gang'):
        await ctx.send("Join a gang first with `?join`.")
        return
    if target_user is None:
        await ctx.send("Usage: `?driveby @user`")
        return
    if target_user.id == ctx.author.id:
        await ctx.send("You cannot drive by yourself.")
        return

    target_player = get_player(str(target_user.id))
    if not target_player:
        await ctx.send(f"{target_user.name} does not have a character.")
        return
    if not target_player.get('gang'):
        await ctx.send(f"{target_player['name']} is not in a gang.")
        return
    if not is_rival(player['gang'], target_player['gang']):
        await ctx.send(f"**{target_player['gang']}** is not on your rival list.")
        return

    heat = player.get('heat', 0)
    if heat >= 80:
        await ctx.send("Heat is too high. You cannot move right now.")
        return

    await ctx.send(f"**{player['name']}** pulls up on **{target_player['name']}**...")
    await asyncio.sleep(3)

    weapon_bonus    = 20 if player.get('weapon') else 0
    attacker_power  = player.get('rep', 0) + random.randint(1, 50) + weapon_bonus
    defender_power  = target_player.get('rep', 0) + random.randint(1, 50)
    attacker_wins   = attacker_power > defender_power
    heat_gain       = random.randint(25, 40)
    police_chance   = int(heat * 0.4) + 20
    caught          = random.randint(1, 100) <= police_chance

    if attacker_wins:
        death_roll   = random.randint(1, 100)
        target_dies  = death_roll <= 40
        rep_gain     = random.randint(30, 80)
        player['rep']   = player.get('rep', 0) + rep_gain
        player['heat']  = min(100, player.get('heat', 0) + heat_gain)
        player['kills'] = player.get('kills', 0) + (1 if target_dies else 0)

        embed = discord.Embed(title="DRIVE BY - HIT", description=random.choice(DRIVE_BY_OUTCOMES_WIN), color=discord.Color.green())
        embed.add_field(name="Rep", value=f"+{rep_gain}", inline=True)
        embed.add_field(name="Heat", value=f"+{heat_gain}", inline=True)

        if target_dies:
            embed.add_field(name="TARGET DOWN", value=f"**{target_player['name']}** is dead. Gone forever.", inline=False)
            kill_player(target_player, f"{player['name']} ({player['gang']}) - Drive By")
        else:
            target_player['rep']  = max(0, target_player.get('rep', 0) - random.randint(10, 30))
            target_player['heat'] = min(100, target_player.get('heat', 0) + 10)
            save_player(target_player)
            embed.add_field(name="Target", value=f"**{target_player['name']}** survived but took losses.", inline=False)

        save_player(player)
    else:
        rep_loss       = random.randint(10, 25)
        player['rep']  = max(0, player.get('rep', 0) - rep_loss)
        player['heat'] = min(100, player.get('heat', 0) + heat_gain)

        embed = discord.Embed(title="DRIVE BY - THEY SHOT BACK", description=random.choice(DRIVE_BY_OUTCOMES_LOSS), color=discord.Color.red())
        embed.add_field(name="Rep Lost", value=f"-{rep_loss}",  inline=True)
        embed.add_field(name="Heat",     value=f"+{heat_gain}", inline=True)

        if random.randint(1, 100) <= 20:
            embed.add_field(name="YOU GOT KILLED", value=f"**{player['name']}** did not make it back. Gone forever.", inline=False)
            await ctx.send(embed=embed)
            kill_player(player, f"{target_player['name']} ({target_player['gang']}) - Drive By Retaliation")
            return

        save_player(player)

    if caught:
        days              = random.randint(*JAIL_SENTENCES["long"])
        player['arrests'] = player.get('arrests', 0) + 1
        save_player(player)
        send_to_prison(player, days)
        embed.add_field(name="THEN LAPD CAME", value=f"Locked up right after. {days} days.", inline=False)

    await ctx.send(embed=embed)


@bot.command(name='smoke')
async def smoke(ctx):
    """Light up and kick back. Usage: ?smoke"""
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return

    strain = random.choice(SMOKE_STRAINS)
    session = random.choice(SMOKE_SESSIONS)

    # Smoking reduces heat slightly and gives a small vibe boost
    heat_reduction = random.randint(3, 8)
    rep_gain       = random.randint(1, 5)
    player['heat']       = max(0, player.get('heat', 0) - heat_reduction)
    player['rep']        = player.get('rep', 0) + rep_gain
    player['times_high'] = player.get('times_high', 0) + 1
    save_player(player)

    embed = discord.Embed(
        title="SMOKING SESSION",
        description=f"You spark some **{strain}**. {session}",
        color=discord.Color.dark_green()
    )
    embed.add_field(name="Heat",       value=f"-{heat_reduction} ({get_heat_level(player['heat'])})", inline=True)
    embed.add_field(name="Vibe",       value=f"+{rep_gain} rep",                                      inline=True)
    embed.add_field(name="Times High", value=str(player['times_high']),                               inline=True)
    await ctx.send(embed=embed)


@bot.command(name='drink')
async def drink(ctx):
    """Pour up and get loose. Usage: ?drink"""
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return

    drink_choice   = random.choice(DRINK_OPTIONS)
    session        = random.choice(DRUNK_SESSIONS)
    heat_reduction = random.randint(2, 6)
    rep_gain       = random.randint(1, 4)

    # Small chance drinking gets you into trouble
    trouble = random.randint(1, 100) <= 15
    player['heat']        = max(0, player.get('heat', 0) - heat_reduction)
    player['rep']         = player.get('rep', 0) + rep_gain
    player['times_drunk'] = player.get('times_drunk', 0) + 1

    if trouble:
        heat_add       = random.randint(5, 15)
        player['heat'] = min(100, player.get('heat', 0) + heat_add)
        trouble_text   = f"\nYou got drunk and started wilding. Heat went up +{heat_add}."
    else:
        trouble_text = ""

    save_player(player)

    embed = discord.Embed(
        title="POUR UP",
        description=f"You crack open some **{drink_choice}**. {session}{trouble_text}",
        color=discord.Color.dark_magenta()
    )
    embed.add_field(name="Heat",        value=f"-{heat_reduction} ({get_heat_level(player['heat'])})", inline=True)
    embed.add_field(name="Vibe",        value=f"+{rep_gain} rep",                                      inline=True)
    embed.add_field(name="Times Drunk", value=str(player['times_drunk']),                              inline=True)
    await ctx.send(embed=embed)


@bot.command(name='hoes')
async def hoes(ctx):
    """Link with a girl for the night. Usage: ?hoes"""
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return

    cash = player.get('cash', 0)
    cost = random.randint(50, 200)

    if cash < cost:
        await ctx.send(f"You are broke. You need at least ${cost} to be out here like that.")
        return

    girl    = random.choice(FEMALE_NAMES)
    encounter = random.choice(GIRL_ENCOUNTERS)
    outcome   = random.choice(GIRL_OUTCOMES)
    rep_gain  = random.randint(2, 8)

    player['cash']       = cash - cost
    player['rep']        = player.get('rep', 0) + rep_gain
    player['body_count'] = player.get('body_count', 0) + 1

    # Small chance she sets you up
    setup = random.randint(1, 100) <= 10
    if setup:
        cash_lost      = random.randint(100, 500)
        heat_gain      = random.randint(5, 15)
        player['cash'] = max(0, player.get('cash', 0) - cash_lost)
        player['heat'] = min(100, player.get('heat', 0) + heat_gain)
        setup_text     = f"\n\nShe set you up. Lost ${cash_lost} and heat went up +{heat_gain}. Never trust a new face."
    else:
        setup_text = ""

    save_player(player)

    embed = discord.Embed(
        title=f"LINKING WITH {girl.upper()}",
        description=f"{encounter}\n\n{outcome}{setup_text}",
        color=discord.Color.dark_magenta()
    )
    embed.add_field(name="Spent",      value=f"${cost}",                inline=True)
    embed.add_field(name="Rep",        value=f"+{rep_gain}",            inline=True)
    embed.add_field(name="Body Count", value=str(player['body_count']), inline=True)
    await ctx.send(embed=embed)


@bot.command(name='flex')
async def flex(ctx):
    """Spend cash on drip, chains, and cars. Usage: ?flex"""
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return

    items_text = "\n".join(f"`{i+1}.` {item[0]} - ${item[1]}" for i, item in enumerate(FLEX_ITEMS))
    embed = discord.Embed(
        title="WHAT ARE YOU COPPING",
        description=f"Your cash: ${player.get('cash', 0)}\n\n{items_text}\n\nType the number to buy.",
        color=discord.Color.dark_grey()
    )
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        msg    = await bot.wait_for('message', check=check, timeout=30)
        choice = int(msg.content) - 1
        if choice < 0 or choice >= len(FLEX_ITEMS):
            await ctx.send("Invalid choice.")
            return

        item_name, item_cost, rep_gain = FLEX_ITEMS[choice]

        if player.get('cash', 0) < item_cost:
            await ctx.send(f"You cannot afford that. You need ${item_cost}.")
            return

        player['cash'] = player.get('cash', 0) - item_cost
        player['rep']  = player.get('rep', 0) + rep_gain

        # If it is a car update the car field
        if "Chevy" in item_name or "Dodge" in item_name or "BMW" in item_name or "Mercedes" in item_name or "Lincoln" in item_name or "Cadillac" in item_name or "Impala" in item_name or "Charger" in item_name:
            player['car'] = item_name

        save_player(player)

        embed = discord.Embed(
            title="COPPED",
            description=f"You just bought **{item_name}**. The streets notice.",
            color=discord.Color.gold()
        )
        embed.add_field(name="Spent",    value=f"${item_cost}",         inline=True)
        embed.add_field(name="Rep",      value=f"+{rep_gain}",          inline=True)
        embed.add_field(name="Cash Left",value=f"${player['cash']}",    inline=True)
        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("Took too long. Use `?flex` again.")


@bot.command(name='getstrapped')
async def get_strapped(ctx):
    """Buy a weapon to boost your power. Usage: ?getstrapped"""
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return

    weapons_text = "\n".join(f"`{i+1}.` {w[0]} - ${w[1]}" for i, w in enumerate(WEAPONS))
    embed = discord.Embed(
        title="WHAT ARE YOU GRABBING",
        description=f"Your cash: ${player.get('cash', 0)}\n\n{weapons_text}\n\nType the number to buy.",
        color=discord.Color.dark_grey()
    )
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        msg    = await bot.wait_for('message', check=check, timeout=30)
        choice = int(msg.content) - 1
        if choice < 0 or choice >= len(WEAPONS):
            await ctx.send("Invalid choice.")
            return

        weapon_name, weapon_cost, rep_gain = WEAPONS[choice]

        if player.get('cash', 0) < weapon_cost:
            await ctx.send(f"You cannot afford that. Need ${weapon_cost}.")
            return

        player['cash']   = player.get('cash', 0) - weapon_cost
        player['rep']    = player.get('rep', 0) + rep_gain
        player['weapon'] = weapon_name
        save_player(player)

        embed = discord.Embed(
            title="STRAPPED UP",
            description=f"You just grabbed a **{weapon_name}**. Now you are dangerous.",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Weapon",    value=weapon_name,           inline=True)
        embed.add_field(name="Spent",     value=f"${weapon_cost}",     inline=True)
        embed.add_field(name="Rep",       value=f"+{rep_gain}",        inline=True)
        embed.add_field(name="Cash Left", value=f"${player['cash']}",  inline=True)
        embed.set_footer(text="Your weapon gives you a bonus in drive bys.")
        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("Took too long. Use `?getstrapped` again.")


@bot.command(name='tattoo')
async def get_tattoo(ctx):
    """Get inked up. Usage: ?tattoo"""
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return

    tattoo_text = "\n".join(f"`{i+1}.` {t[0]} - ${t[1]}" for i, t in enumerate(TATTOO_OPTIONS))
    embed = discord.Embed(
        title="WHAT ARE YOU GETTING",
        description=f"Your cash: ${player.get('cash', 0)}\n\n{tattoo_text}\n\nType the number.",
        color=discord.Color.dark_grey()
    )
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        msg    = await bot.wait_for('message', check=check, timeout=30)
        choice = int(msg.content) - 1
        if choice < 0 or choice >= len(TATTOO_OPTIONS):
            await ctx.send("Invalid choice.")
            return

        tattoo_name, tattoo_cost, rep_gain = TATTOO_OPTIONS[choice]

        if player.get('cash', 0) < tattoo_cost:
            await ctx.send(f"You cannot afford that. Need ${tattoo_cost}.")
            return

        if tattoo_name in player.get('tattoos', []):
            await ctx.send("You already have that tattoo.")
            return

        player['cash'] = player.get('cash', 0) - tattoo_cost
        player['rep']  = player.get('rep', 0) + rep_gain
        if 'tattoos' not in player:
            player['tattoos'] = []
        player['tattoos'].append(tattoo_name)
        save_player(player)

        embed = discord.Embed(
            title="FRESH INK",
            description=f"You just got **{tattoo_name}**. The hood knows who you are.",
            color=discord.Color.dark_grey()
        )
        embed.add_field(name="Spent",      value=f"${tattoo_cost}",          inline=True)
        embed.add_field(name="Rep",        value=f"+{rep_gain}",             inline=True)
        embed.add_field(name="Total Tats", value=str(len(player['tattoos'])), inline=True)
        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("Took too long. Use `?tattoo` again.")


@bot.command(name='kickback')
async def kickback(ctx):
    """Throw a kickback at the spot. Usage: ?kickback"""
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return

    cost = random.randint(200, 600)
    if player.get('cash', 0) < cost:
        await ctx.send(f"You need at least ${cost} to throw a kickback. Get your money up.")
        return

    await ctx.send(f"**{player['name']}** is throwing a kickback at the spot...")
    await asyncio.sleep(2)

    strain      = random.choice(SMOKE_STRAINS)
    drink_choice = random.choice(DRINK_OPTIONS)
    rep_gain    = random.randint(20, 50)
    heat_gain   = random.randint(5, 15)

    player['cash']        = player.get('cash', 0) - cost
    player['rep']         = player.get('rep', 0) + rep_gain
    player['heat']        = min(100, player.get('heat', 0) + heat_gain)
    player['times_high']  = player.get('times_high', 0) + 1
    player['times_drunk'] = player.get('times_drunk', 0) + 1

    # Small chance kickback gets raided
    raided = random.randint(1, 100) <= 20
    if raided:
        days              = random.randint(*JAIL_SENTENCES["short"])
        player['arrests'] = player.get('arrests', 0) + 1
        save_player(player)
        send_to_prison(player, days)

        embed = discord.Embed(
            title="KICKBACK GOT RAIDED",
            description=f"The spot was lit. {strain} in the air, {drink_choice} everywhere. Then LAPD kicked the door.",
            color=discord.Color.red()
        )
        embed.add_field(name="Spent",    value=f"${cost}",      inline=True)
        embed.add_field(name="Sentence", value=f"{days} day(s)", inline=True)
        await ctx.send(embed=embed)
        return

    save_player(player)

    embed = discord.Embed(
        title="KICKBACK WAS LIVE",
        description=f"The spot was packed. {strain} in rotation, {drink_choice} on deck. The whole hood came through.",
        color=discord.Color.dark_purple()
    )
    embed.add_field(name="Spent", value=f"${cost}",      inline=True)
    embed.add_field(name="Rep",   value=f"+{rep_gain}",  inline=True)
    embed.add_field(name="Heat",  value=f"+{heat_gain}", inline=True)
    await ctx.send(embed=embed)


@bot.command(name='laylow')
async def lay_low(ctx):
    user_id = str(ctx.author.id)
    if await check_blocked(ctx): return
    player = get_player(user_id)
    if not player:
        await ctx.send("Use `?start` first.")
        return

    heat = player.get('heat', 0)
    if heat == 0:
        await ctx.send("Your heat is already cold.")
        return

    await ctx.send(f"**{player['name']}** goes ghost...")
    await asyncio.sleep(3)

    reduction      = random.randint(15, 35)
    new_heat       = max(0, heat - reduction)
    player['heat'] = new_heat
    save_player(player)

    embed = discord.Embed(
        title="LAYING LOW",
        description="You stay off the block. No moves. No noise. Heat dies down.",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="Before", value=f"{heat} ({get_heat_level(heat)})",         inline=True)
    embed.add_field(name="Now",    value=f"{new_heat} ({get_heat_level(new_heat)})", inline=True)
    embed.add_field(name="Drop",   value=str(reduction),                              inline=True)
    await ctx.send(embed=embed)


@bot.command(name='status')
async def status(ctx):
    user_id = str(ctx.author.id)
    prison  = load_data(PRISON_FILE)

    for inmate in prison.values():
        if inmate.get('user_id') == user_id:
            days_served = days_since(inmate['release_date'])
            days_left   = max(0, inmate['sentence_days'] - days_served)

            if days_left == 0:
                check_prison_release()
                await ctx.send(f"**{inmate['name']}** has served their time. You are out.")
                return

            prison_event = random.choice(PRISON_EVENTS)
            embed = discord.Embed(
                title="DOING TIME",
                description=f"**{inmate['name']}** is locked up.\n\n{prison_event}",
                color=discord.Color.dark_grey()
            )
            embed.add_field(name="Sentence",    value=f"{inmate['sentence_days']} day(s)", inline=True)
            embed.add_field(name="Days Served", value=str(days_served),                    inline=True)
            embed.add_field(name="Days Left",   value=str(days_left),                      inline=True)
            embed.set_footer(text="You cannot do anything until you are released.")
            await ctx.send(embed=embed)
            return

    player = get_player(user_id)
    if player:
        await ctx.send(f"**{player['name']}** is free. Heat: {get_heat_level(player.get('heat', 0))}. Use `?profile` for full stats.")
    else:
        dead = is_dead(user_id)
        if dead:
            await ctx.send(f"**{dead['name']}** is dead. Killed by {dead['killed_by']}. One life.")
        else:
            await ctx.send("No character found. Use `?start`.")


@bot.command(name='streets')
async def streets(ctx):
    players   = load_data(GANG_FILE)
    graveyard = load_data(GRAVEYARD_FILE)
    if not players:
        await ctx.send("The streets are empty.")
        return

    sorted_players = sorted(players.values(), key=lambda x: x.get('rep', 0), reverse=True)[:10]

    embed = discord.Embed(
        title="WHO IS RUNNING THE STREETS",
        description="Top players by rep",
        color=discord.Color.dark_gold()
    )
    for i, p in enumerate(sorted_players, 1):
        gang = p.get('gang') or "Unaffiliated"
        rank = get_rank(p.get('rep', 0))
        embed.add_field(
            name=f"{i}. {p['name']} - {p['hood_name']}",
            value=f"{gang} | {rank} | Rep: {p.get('rep', 0)} | Cash: ${p.get('cash', 0)} | Kills: {p.get('kills', 0)}",
            inline=False
        )
    embed.set_footer(text=f"Graveyard: {len(graveyard)} fallen")
    await ctx.send(embed=embed)


@bot.command(name='graveyard')
async def show_graveyard(ctx):
    graveyard = load_data(GRAVEYARD_FILE)
    if not graveyard:
        await ctx.send("Nobody has died yet.")
        return

    recent = sorted(graveyard.values(), key=lambda x: x.get('death_date', ''), reverse=True)[:10]

    embed = discord.Embed(title="THE GRAVEYARD", description="Those who did not make it", color=discord.Color.dark_grey())
    for p in recent:
        embed.add_field(
            name=f"{p['name']} - {p.get('hood_name', '')}",
            value=(f"Gang: {p.get('gang') or 'Unaffiliated'} | Rep: {p.get('rep', 0)} | Kills: {p.get('kills', 0)}\n"
                   f"Killed by: {p.get('killed_by', 'Unknown')}\n"
                   f"Date: {p.get('death_date', '')[:10]}"),
            inline=False
        )
    await ctx.send(embed=embed)


@bot.command(name='cmds')
async def show_commands(ctx):
    embed = discord.Embed(title="GANG SIMULATOR COMMANDS", color=discord.Color.dark_grey())
    embed.add_field(name="?start",        value="Create your character",                    inline=False)
    embed.add_field(name="?join",         value="Join a real LA gang",                      inline=False)
    embed.add_field(name="?profile",      value="View your stats or someone elses",         inline=False)
    embed.add_field(name="?deal",         value="Move product on the block",                inline=False)
    embed.add_field(name="?rob",          value="Hit a lick",                               inline=False)
    embed.add_field(name="?driveby @user",value="Shoot on a rival gang member",             inline=False)
    embed.add_field(name="?smoke",        value="Light up and chill",                       inline=False)
    embed.add_field(name="?drink",        value="Pour up",                                  inline=False)
    embed.add_field(name="?hoes",         value="Link with a girl for the night",           inline=False)
    embed.add_field(name="?flex",         value="Cop drip, chains, and cars",               inline=False)
    embed.add_field(name="?getstrapped",  value="Buy a weapon",                             inline=False)
    embed.add_field(name="?tattoo",       value="Get inked up",                             inline=False)
    embed.add_field(name="?kickback",     value="Throw a kickback at the spot",             inline=False)
    embed.add_field(name="?laylow",       value="Reduce your heat",                         inline=False)
    embed.add_field(name="?status",       value="Check prison time remaining",              inline=False)
    embed.add_field(name="?streets",      value="Top 10 players by rep",                   inline=False)
    embed.add_field(name="?graveyard",    value="See all fallen members",                   inline=False)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found!")
    else:
        print("Token found! Starting bot...")
        bot.run(TOKEN)
