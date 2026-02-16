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

# Real LA gangs with real sets
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

GANG_RANKS = ["Recruit", "Soldier", "OG", "Shot Caller", "Boss"]

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

JAIL_SENTENCES = {
    "short": (1, 3),
    "medium": (4, 7),
    "long": (8, 14)
}


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
    players  = load_data(GANG_FILE)
    graveyard = load_data(GRAVEYARD_FILE)

    dead = player.copy()
    dead['killed_by']  = killed_by
    dead['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    graveyard[player['id']] = dead
    save_data(GRAVEYARD_FILE, graveyard)

    if player['id'] in players:
        del players[player['id']]
        save_data(GANG_FILE, players)

def send_to_prison(player, days):
    players = load_data(GANG_FILE)
    prison  = load_data(PRISON_FILE)

    inmate = player.copy()
    inmate['release_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    inmate['sentence_days'] = days

    prison[player['id']] = inmate
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
            inmate['heat']        = max(0, inmate.get('heat', 0) - 30)
            inmate['cash']        = max(0, inmate.get('cash', 0) - random.randint(100, 500))
            players[pid]          = inmate
            del prison[pid]
            released.append(inmate)

    save_data(PRISON_FILE, prison)
    save_data(GANG_FILE, players)
    return released


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
    """Create your gang member. Usage: ?start"""
    user_id = str(ctx.author.id)

    # Check graveyard
    graveyard = load_data(GRAVEYARD_FILE)
    for dead in graveyard.values():
        if dead.get('user_id') == user_id:
            await ctx.send(
                f"**{dead['name']}** is dead. You only get one life.\n"
                f"Killed by: {dead['killed_by']} on {dead['death_date'][:10]}."
            )
            return

    # Check prison
    prison = load_data(PRISON_FILE)
    for inmate in prison.values():
        if inmate.get('user_id') == user_id:
            days_left = max(0, inmate['sentence_days'] - days_since(inmate['release_date']))
            await ctx.send(
                f"**{inmate['name']}** is doing time. {days_left} day(s) left on their sentence."
            )
            return

    if get_player(user_id):
        await ctx.send("You already have a character. Use `?profile` to see them.")
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
        "days_in":    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    save_player(player)

    embed = discord.Embed(
        title=f"{name} - aka {hood_tag}",
        description=f"From the streets of {location}. Your story starts now.",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="Cash",     value=f"${player['cash']}", inline=True)
    embed.add_field(name="Rep",      value="0",                  inline=True)
    embed.add_field(name="Heat",     value="Cold",               inline=True)
    embed.add_field(name="Gang",     value="None - pick one with `?join`", inline=False)
    embed.set_footer(text=f"ID: {pid} | One life. Do not waste it.")

    await ctx.send(embed=embed)


@bot.command(name='join')
async def join_gang(ctx):
    """Join a real LA gang. Usage: ?join"""
    user_id = str(ctx.author.id)
    player  = get_player(user_id)

    if not player:
        await ctx.send("You do not have a character yet. Use `?start` first.")
        return

    if player.get('gang'):
        await ctx.send(f"You are already repping **{player['gang']}**. You ride or die with your set.")
        return

    gang_list = list(LA_GANGS.keys())
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
        msg = await bot.wait_for('message', check=check, timeout=30)
        choice = int(msg.content) - 1
        if choice < 0 or choice >= len(gang_list):
            await ctx.send("Invalid choice.")
            return

        chosen_gang = gang_list[choice]
        gang_info   = LA_GANGS[chosen_gang]

        player['gang'] = chosen_gang
        player['rep']  = player.get('rep', 0) + 25
        save_player(player)

        embed = discord.Embed(
            title=f"Welcome to {chosen_gang}",
            description=f"You are now repping {chosen_gang}. Do not embarrass the set.",
            color=discord.Color(gang_info['color'])
        )
        embed.add_field(name="Territory", value=gang_info['territory'],           inline=False)
        embed.add_field(name="Rivals",    value=", ".join(gang_info['rivals']) or "None listed", inline=False)
        embed.add_field(name="Allies",    value=", ".join(gang_info['allies']) or "None",        inline=False)
        embed.add_field(name="Your Rank", value="Recruit",                        inline=True)
        embed.add_field(name="Rep Bonus", value="+25 for joining",                inline=True)

        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("You took too long. Use `?join` again.")


@bot.command(name='profile')
async def profile(ctx, user: discord.Member = None):
    """View your profile or someone else's. Usage: ?profile or ?profile @user"""
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
    embed.add_field(name="Rank",    value=rank,                        inline=True)
    embed.add_field(name="Rep",     value=str(player.get('rep', 0)),   inline=True)
    embed.add_field(name="Cash",    value=f"${player.get('cash', 0)}", inline=True)
    embed.add_field(name="Heat",    value=heat,                        inline=True)
    embed.add_field(name="Kills",   value=str(player.get('kills', 0)), inline=True)
    embed.add_field(name="Arrests", value=str(player.get('arrests', 0)), inline=True)
    embed.set_footer(text=f"ID: {player['id']}")

    await ctx.send(embed=embed)


@bot.command(name='deal')
async def deal(ctx):
    """Hit the block and move some product. Usage: ?deal"""
    user_id = str(ctx.author.id)
    player  = get_player(user_id)

    if not player:
        await ctx.send("You do not have a character. Use `?start`.")
        return

    if not player.get('gang'):
        await ctx.send("You need to be in a gang before you can move product. Use `?join`.")
        return

    heat = player.get('heat', 0)

    if heat >= 80:
        await ctx.send(
            f"Your heat is at **{heat}** - you are a fugitive. "
            f"Lay low with `?laylow` before you do anything."
        )
        return

    await ctx.send(f"**{player['name']}** hits the block...")
    await asyncio.sleep(2)

    drug         = random.choice(DRUGS)
    outcome_roll = random.randint(1, 100)
    heat_gain    = random.randint(3, 10)

    # Police check - higher heat = higher chance of getting caught
    police_chance = int(heat * 0.4)
    caught        = random.randint(1, 100) <= police_chance

    if caught:
        sentence_type = random.choice(["short", "medium"])
        days          = random.randint(*JAIL_SENTENCES[sentence_type])
        player['arrests'] = player.get('arrests', 0) + 1
        player['heat']    = min(100, heat + 20)
        save_player(player)
        send_to_prison(player, days)

        embed = discord.Embed(
            title="BUSTED",
            description=random.choice(POLICE_OUTCOMES),
            color=discord.Color.red()
        )
        embed.add_field(name="Charge",    value="Possession with intent to distribute", inline=False)
        embed.add_field(name="Sentence",  value=f"{days} day(s)",                        inline=True)
        embed.add_field(name="Cash Lost", value=f"${min(player.get('cash', 0), random.randint(100, 500))}", inline=True)
        embed.set_footer(text="You are in prison. Use ?status to check your release date.")
        await ctx.send(embed=embed)
        return

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

    new_rank = get_rank(player['rep'])
    color    = discord.Color.green() if result == "clean" else discord.Color.orange() if result == "slow" else discord.Color.dark_grey()

    if result == "clean":
        desc = f"The {drug} moves fast. Fiends come through all night. Cash stacks up."
    elif result == "slow":
        desc = f"Slow night. The {drug} moves but the money is light."
    else:
        desc = f"Block is dry. Rollers been through. Nothing moves tonight."

    embed = discord.Embed(title="TRAP REPORT", description=desc, color=color)
    embed.add_field(name="Cash Earned", value=f"${cash_earned}", inline=True)
    embed.add_field(name="Rep Gained",  value=f"+{rep_gain}",    inline=True)
    embed.add_field(name="Heat",        value=f"+{heat_gain} ({get_heat_level(player['heat'])})", inline=True)
    embed.add_field(name="Total Cash",  value=f"${player['cash']}", inline=True)
    embed.add_field(name="Total Rep",   value=str(player['rep']),   inline=True)
    embed.add_field(name="Rank",        value=new_rank,              inline=True)

    await ctx.send(embed=embed)


@bot.command(name='rob')
async def rob(ctx):
    """Hit a lick. Usage: ?rob"""
    user_id = str(ctx.author.id)
    player  = get_player(user_id)

    if not player:
        await ctx.send("You do not have a character. Use `?start`.")
        return

    if not player.get('gang'):
        await ctx.send("Join a gang first with `?join`.")
        return

    heat = player.get('heat', 0)

    if heat >= 80:
        await ctx.send("Your heat is too high. Lay low first with `?laylow`.")
        return

    target = random.choice(ROB_TARGETS)
    await ctx.send(f"**{player['name']}** is moving on {target}...")
    await asyncio.sleep(2)

    success_chance = max(30, 70 - int(heat * 0.5))
    roll           = random.randint(1, 100)
    police_chance  = int(heat * 0.5)
    caught         = random.randint(1, 100) <= police_chance

    if caught:
        sentence_type = random.choice(["medium", "long"])
        days          = random.randint(*JAIL_SENTENCES[sentence_type])
        player['arrests'] = player.get('arrests', 0) + 1
        save_player(player)
        send_to_prison(player, days)

        embed = discord.Embed(
            title="CAUGHT IN THE ACT",
            description=random.choice(POLICE_OUTCOMES),
            color=discord.Color.red()
        )
        embed.add_field(name="Charge",   value="Armed robbery",   inline=False)
        embed.add_field(name="Sentence", value=f"{days} day(s)", inline=True)
        embed.set_footer(text="You are in prison.")
        await ctx.send(embed=embed)
        return

    if roll <= success_chance:
        cash_earned = random.randint(300, 1200)
        rep_gain    = random.randint(10, 30)
        heat_gain   = random.randint(15, 25)

        player['cash'] = player.get('cash', 0) + cash_earned
        player['rep']  = player.get('rep', 0) + rep_gain
        player['heat'] = min(100, player.get('heat', 0) + heat_gain)
        save_player(player)

        embed = discord.Embed(
            title="LICK SUCCESSFUL",
            description=f"You run up on {target} and take everything. Clean exit.",
            color=discord.Color.green()
        )
        embed.add_field(name="Cash Taken", value=f"${cash_earned}", inline=True)
        embed.add_field(name="Rep",        value=f"+{rep_gain}",    inline=True)
        embed.add_field(name="Heat",       value=f"+{heat_gain}",   inline=True)
    else:
        heat_gain = random.randint(10, 20)
        player['heat'] = min(100, player.get('heat', 0) + heat_gain)
        save_player(player)

        embed = discord.Embed(
            title="LICK FAILED",
            description=f"Something went wrong at {target}. You had to dip empty handed.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Cash",  value="$0",          inline=True)
        embed.add_field(name="Heat",  value=f"+{heat_gain}", inline=True)

    await ctx.send(embed=embed)


@bot.command(name='driveby')
async def drive_by(ctx, target_user: discord.Member = None):
    """Do a drive by on a rival gang member. Usage: ?driveby @user"""
    user_id = str(ctx.author.id)
    player  = get_player(user_id)

    if not player:
        await ctx.send("You do not have a character. Use `?start`.")
        return

    if not player.get('gang'):
        await ctx.send("You need to be in a gang. Use `?join`.")
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
        await ctx.send(f"{target_player['name']} is not in a gang. Pick a real target.")
        return

    if not is_rival(player['gang'], target_player['gang']):
        await ctx.send(
            f"**{target_player['gang']}** is not on your rival list. "
            f"You do not pop off on random sets."
        )
        return

    heat = player.get('heat', 0)
    if heat >= 80:
        await ctx.send("Your heat is too high. You cannot move right now.")
        return

    await ctx.send(f"**{player['name']}** pulls up on **{target_player['name']}**...")
    await asyncio.sleep(3)

    # Factor in rep difference
    attacker_power = player.get('rep', 0) + random.randint(1, 50)
    defender_power = target_player.get('rep', 0) + random.randint(1, 50)

    attacker_wins = attacker_power > defender_power

    heat_gain     = random.randint(25, 40)
    police_chance = int(heat * 0.4) + 20
    caught        = random.randint(1, 100) <= police_chance

    if attacker_wins:
        # Check if target dies
        death_roll   = random.randint(1, 100)
        target_dies  = death_roll <= 40

        rep_gain = random.randint(30, 80)
        player['rep']    = player.get('rep', 0) + rep_gain
        player['heat']   = min(100, player.get('heat', 0) + heat_gain)
        player['kills']  = player.get('kills', 0) + (1 if target_dies else 0)

        embed = discord.Embed(
            title="DRIVE BY - SUCCESSFUL HIT",
            description=random.choice(DRIVE_BY_OUTCOMES_WIN),
            color=discord.Color.green()
        )
        embed.add_field(name="Rep Gained", value=f"+{rep_gain}", inline=True)
        embed.add_field(name="Heat",       value=f"+{heat_gain}", inline=True)

        if target_dies:
            embed.add_field(
                name="TARGET DOWN",
                value=f"**{target_player['name']}** has been killed. They are gone forever.",
                inline=False
            )
            kill_player(target_player, f"{player['name']} ({player['gang']}) - Drive By")
        else:
            target_player['rep']  = max(0, target_player.get('rep', 0) - random.randint(10, 30))
            target_player['heat'] = min(100, target_player.get('heat', 0) + 10)
            save_player(target_player)
            embed.add_field(
                name="Target Status",
                value=f"**{target_player['name']}** survived but took heavy losses.",
                inline=False
            )

        save_player(player)

    else:
        rep_loss  = random.randint(10, 25)
        player['rep']  = max(0, player.get('rep', 0) - rep_loss)
        player['heat'] = min(100, player.get('heat', 0) + heat_gain)
        save_player(player)

        embed = discord.Embed(
            title="DRIVE BY - THEY SHOT BACK",
            description=random.choice(DRIVE_BY_OUTCOMES_LOSS),
            color=discord.Color.red()
        )
        embed.add_field(name="Rep Lost", value=f"-{rep_loss}",  inline=True)
        embed.add_field(name="Heat",     value=f"+{heat_gain}", inline=True)

        # Small chance you die on a failed drive by
        if random.randint(1, 100) <= 20:
            embed.add_field(
                name="YOU HAVE BEEN KILLED",
                value=f"**{player['name']}** did not make it back. Gone forever.",
                inline=False
            )
            await ctx.send(embed=embed)
            kill_player(player, f"{target_player['name']} ({target_player['gang']}) - Drive By Retaliation")
            return

    if caught:
        sentence_type = "long"
        days          = random.randint(*JAIL_SENTENCES[sentence_type])
        player['arrests'] = player.get('arrests', 0) + 1
        save_player(player)
        send_to_prison(player, days)

        embed.add_field(
            name="THEN THE POLICE CAME",
            value=f"LAPD locked you up right after. {days} days.",
            inline=False
        )

    await ctx.send(embed=embed)


@bot.command(name='laylow')
async def lay_low(ctx):
    """Lay low to reduce your heat. Usage: ?laylow"""
    user_id = str(ctx.author.id)
    player  = get_player(user_id)

    if not player:
        await ctx.send("You do not have a character. Use `?start`.")
        return

    heat = player.get('heat', 0)

    if heat == 0:
        await ctx.send("Your heat is already cold. You are good.")
        return

    await ctx.send(f"**{player['name']}** goes ghost for a while...")
    await asyncio.sleep(3)

    reduction       = random.randint(15, 35)
    new_heat        = max(0, heat - reduction)
    player['heat']  = new_heat
    save_player(player)

    embed = discord.Embed(
        title="LAYING LOW",
        description="You stay off the block. No moves. No noise. The heat starts to die down.",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="Heat Before", value=f"{heat} ({get_heat_level(heat)})",         inline=True)
    embed.add_field(name="Heat Now",    value=f"{new_heat} ({get_heat_level(new_heat)})", inline=True)
    embed.add_field(name="Reduced By",  value=str(reduction),                              inline=True)

    await ctx.send(embed=embed)


@bot.command(name='status')
async def status(ctx):
    """Check if you are in prison and how long is left. Usage: ?status"""
    user_id = str(ctx.author.id)
    prison  = load_data(PRISON_FILE)

    for inmate in prison.values():
        if inmate.get('user_id') == user_id:
            days_served = days_since(inmate['release_date'])
            days_left   = max(0, inmate['sentence_days'] - days_served)

            if days_left == 0:
                check_prison_release()
                await ctx.send(f"**{inmate['name']}** has served their time. Use any command to continue.")
                return

            embed = discord.Embed(
                title="DOING TIME",
                description=f"**{inmate['name']}** is locked up at county.",
                color=discord.Color.dark_grey()
            )
            embed.add_field(name="Sentence",     value=f"{inmate['sentence_days']} day(s)", inline=True)
            embed.add_field(name="Days Served",  value=str(days_served),                    inline=True)
            embed.add_field(name="Days Left",    value=str(days_left),                      inline=True)
            embed.add_field(name="Gang",         value=inmate.get('gang', 'None'),          inline=True)
            embed.set_footer(text="You cannot do anything until you are released.")
            await ctx.send(embed=embed)
            return

    player = get_player(user_id)
    if player:
        await ctx.send(f"**{player['name']}** is free. Heat: {get_heat_level(player.get('heat', 0))}. Use `?profile` for full stats.")
    else:
        graveyard = load_data(GRAVEYARD_FILE)
        for dead in graveyard.values():
            if dead.get('user_id') == user_id:
                await ctx.send(f"**{dead['name']}** is dead. Killed by {dead['killed_by']} on {dead['death_date'][:10]}. One life.")
                return
        await ctx.send("No character found. Use `?start`.")


@bot.command(name='streets')
async def streets(ctx):
    """See who is running the streets right now. Usage: ?streets"""
    players   = load_data(GANG_FILE)
    graveyard = load_data(GRAVEYARD_FILE)

    if not players:
        await ctx.send("The streets are empty right now.")
        return

    sorted_players = sorted(players.values(), key=lambda x: x.get('rep', 0), reverse=True)[:10]

    embed = discord.Embed(
        title="WHO IS RUNNING THE STREETS",
        description="Top earners by rep right now",
        color=discord.Color.dark_gold()
    )

    for i, p in enumerate(sorted_players, 1):
        gang      = p.get('gang') or "Unaffiliated"
        rank      = get_rank(p.get('rep', 0))
        gang_info = LA_GANGS.get(gang, {})
        embed.add_field(
            name=f"{i}. {p['name']} - {p['hood_name']}",
            value=f"{gang} | {rank} | Rep: {p.get('rep', 0)} | Cash: ${p.get('cash', 0)} | Kills: {p.get('kills', 0)}",
            inline=False
        )

    embed.set_footer(text=f"Graveyard count: {len(graveyard)} fallen")
    await ctx.send(embed=embed)


@bot.command(name='graveyard')
async def show_graveyard(ctx):
    """See who has been killed. Usage: ?graveyard"""
    graveyard = load_data(GRAVEYARD_FILE)

    if not graveyard:
        await ctx.send("Nobody has died yet.")
        return

    recent = sorted(graveyard.values(), key=lambda x: x.get('death_date', ''), reverse=True)[:10]

    embed = discord.Embed(
        title="THE GRAVEYARD",
        description="Those who did not make it",
        color=discord.Color.dark_grey()
    )

    for p in recent:
        embed.add_field(
            name=f"{p['name']} - {p.get('hood_name', '')}",
            value=(f"Gang: {p.get('gang') or 'Unaffiliated'} | "
                   f"Rep: {p.get('rep', 0)} | "
                   f"Kills: {p.get('kills', 0)}\n"
                   f"Killed by: {p.get('killed_by', 'Unknown')}\n"
                   f"Date: {p.get('death_date', '')[:10]}"),
            inline=False
        )

    await ctx.send(embed=embed)


@bot.command(name='cmds')
async def show_commands(ctx):
    """Show all commands. Usage: ?cmds"""
    embed = discord.Embed(
        title="GANG SIMULATOR COMMANDS",
        description="All commands available",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="?start",          value="Create your gang member",                   inline=False)
    embed.add_field(name="?join",           value="Join a real LA gang",                       inline=False)
    embed.add_field(name="?profile",        value="View your stats or someone else's",         inline=False)
    embed.add_field(name="?deal",           value="Hit the block and move product",            inline=False)
    embed.add_field(name="?rob",            value="Hit a lick for fast cash",                  inline=False)
    embed.add_field(name="?driveby @user",  value="Shoot on a rival gang member",              inline=False)
    embed.add_field(name="?laylow",         value="Reduce your heat level",                    inline=False)
    embed.add_field(name="?status",         value="Check prison status and time left",         inline=False)
    embed.add_field(name="?streets",        value="See who is running the streets",            inline=False)
    embed.add_field(name="?graveyard",      value="See all fallen gang members",               inline=False)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found!")
    else:
        print("Token found! Starting bot...")
        bot.run(TOKEN)
