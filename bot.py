import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import os
import asyncio
import time
from keep_alive import keep_alive


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# ─────────────────────────────────────────────
# STATUS SYSTEM
# ─────────────────────────────────────────────

STATUS_TAGS = {
    "BEAST":       "Goes harder than anyone. Earned it in blood.",
    "GHOST":       "Moves unseen. Never caught lacking.",
    "MARKED":      "Enemies know the name. Got a target on their back.",
    "SNITCH":      "Word on the street is they talked. Trust is gone.",
    "LOCKED":      "Been through the system and came out harder.",
    "CURSED":      "Bad luck follows this one everywhere.",
    "LOYAL":       "Ride or die. Set comes before everything.",
    "FALLEN":      "Took too many Ls. Reputation in the dirt.",
    "RISEN":       "Came back from nothing. Streets respect the comeback.",
    "UNTOUCHABLE": "Never took a loss. Still perfect.",
}


def evaluate_status(member):
    kills = member.get('kills', 0)
    deaths = member.get('deaths', 0)
    times_jailed = member.get('times_jailed', 0)
    times_snitched = member.get('times_snitched', 0)
    missions_survived = member.get('missions_survived', 0)

    tags = []
    if times_snitched > 0:
        tags.append("SNITCH")
    if kills >= 15 and deaths == 0:
        tags.append("UNTOUCHABLE")
    elif kills >= 10:
        tags.append("BEAST")
    if missions_survived >= 5 and times_jailed == 0:
        tags.append("GHOST")
    if deaths >= 3:
        tags.append("CURSED")
    if times_jailed >= 3:
        tags.append("LOCKED")
    if kills >= 5 and deaths >= 2:
        tags.append("MARKED")
    if kills == 0 and deaths >= 2:
        tags.append("FALLEN")
    if member.get('came_back_from_zero'):
        tags.append("RISEN")
    if times_jailed == 0 and deaths == 0 and kills >= 3:
        tags.append("LOYAL")

    priority = ["SNITCH", "UNTOUCHABLE", "BEAST", "GHOST", "CURSED", "LOCKED", "MARKED", "FALLEN", "RISEN", "LOYAL"]
    tags = sorted(tags, key=lambda t: priority.index(t) if t in priority else 99)
    return tags[:2]


def format_status_line(member):
    tags = evaluate_status(member)
    return "  ".join([f"[{t}]" for t in tags]) if tags else "--"


# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────

STREET_NAMES = [
    "Big Loc", "Joker", "Tiny", "Demon", "Ghost", "Cisco", "Drowsy", "Spanky",
    "Travieso", "Sleepy", "Boxer", "Dopey", "Scrappy", "Sinner", "Cartoon",
    "Psycho", "Casper", "Smiley", "Termite", "Coyote", "Grumpy", "Stomper",
    "Danger", "Vicious", "Puppet", "Trigger", "Mosco", "Huero", "Flaco",
    "Gordo", "Speedy", "Terminator", "Mugsy", "Sniper", "Looney", "Crazy",
    "Silent", "Savage", "Bandit", "Sinister", "Diablo", "Capone", "Scarface",
    "Hitman", "Naughty", "Shadow", "Youngsta", "Wino", "Sad Eyes", "Pnut",
    "Lil Menace", "Lil Creep", "Lil Caps", "Lil Diablo", "Lil Wicked",
    "Lil Payaso", "Lil Evil", "Lil Trigg", "Lil Psycho", "Lil Casper",
    "Lil Smiley", "Lil Monster", "Lil Lobo", "Lil Pnut", "Lil Wino",
    "Lil Coyote", "Lil Grumpy", "Lil Chino", "Lil Stomper", "Lil Danger",
    "Lil Vicious", "Lil Puppet", "Lil Sad Eyes", "Lil Trigger", "Lil Mosco",
    "Lil Huero", "Lil Flaco", "Lil Gordo", "Lil Speedy", "Lil Terminator",
    "Lil Mugsy", "Lil Sniper", "Lil Looney", "Lil Crazy", "Lil Silent",
    "Lil Savage", "Lil Bandit", "Lil Sinister", "Lil Capone", "Lil Scarface",
    "Lil Hitman", "Lil Naughty",
    "Creeper", "Vulture", "Venom", "Reaper", "Cobra", "Phantom", "Wraith",
    "Raider", "Chaos", "Menace", "Havoc", "Reckless", "Infamous", "Renegade",
    "Outlaw", "Maverick", "Rebel", "Diesel", "Bruiser", "Crusher", "Tank",
    "Boulder", "Razor", "Blade", "Cutthroat", "Buckshot", "Hollow", "Gauge",
    "Caliber", "Barrel", "Hammer", "Spike", "Cleaver", "Machete", "Crowbar",
    "Wrench", "Knuckles", "Fist", "Brawler", "Slugger", "Mauler", "Bonebreaker",
    "Jawbreaker", "Headbuster", "Kneecap", "Ribcracker", "Necksnap", "Backbreaker",
    "Undertaker", "Gravedigger", "Casket", "Tombstone", "Cipher", "Riddle",
    "Maze", "Dusty", "Rusty", "Crusty", "Grimey", "Murk", "Smoky",
    "Thunder", "Lightning", "Tempest", "Cyclone", "Tornado", "Hurricane",
    "Avalanche", "Rubble", "Ruins", "Wreckage", "Bones", "Skull",
    "Fracture", "Shatter", "Detonate", "Ignite", "Blaze", "Inferno",
    "Ember", "Ash", "Scorch", "Burn", "Flare", "Bolt", "Spark",
    "Toxic", "Plague", "Fever", "Blackout", "Blindside", "Ambush",
    "Deadzone", "Killzone", "Warzone", "Bunker", "Warden", "Lawless",
    "Feral", "Rabid", "Predator", "Apex", "Alpha", "Omega", "Titan",
    "Colossus", "Juggernaut", "Sledge", "Devastate", "Obliterate", "Annihilate",
    "Eliminate", "Vanquish", "Dominate", "Crush", "Steamroll", "Purge",
    "Scar", "Mark", "Cipher Zero", "Ghost Rider", "Night Crawler", "Street King",
    "Block God", "Corner Lord", "Trap Star", "Hustle King", "Grind Lord",
    "Bankroll", "Guap", "Offshore", "Fugitive", "Exile", "Outcast",
    "Phantom Pain", "Ghost Protocol", "Dark Matter", "Anomaly", "Glitch",
    "Corrupt", "Virus", "Payload", "Detonator", "Trigger Man", "Hitlist",
    "Bounty", "Verdict", "Sentence", "Conviction", "Alibi", "Evidence",
    "Felony", "Override", "Dispatch", "Deploy", "Advance", "Flank",
    "Tactic", "Operation", "Objective", "Infiltrate", "Breach", "Lockdown",
    "Standoff", "Deadlock", "Choke", "Silence", "Whisper", "Echo",
    "Amplify", "Distort", "Warp", "Twist", "Disfigure", "Mutilate",
]

LA_GANGS = [
    {"name": "Rollin 60s Crips", "hood": "West Adams, LA"},
    {"name": "Grape Street Watts Crips", "hood": "Watts, LA"},
    {"name": "Eight Tray Gangster Crips", "hood": "South LA"},
    {"name": "Compton Crips", "hood": "Compton, LA"},
    {"name": "Bounty Hunter Bloods", "hood": "Watts, LA"},
    {"name": "Piru Street Boys", "hood": "Compton, LA"},
    {"name": "Inglewood Family Bloods", "hood": "Inglewood, LA"},
    {"name": "Brims", "hood": "South LA"},
    {"name": "MS-13", "hood": "Pico-Union, LA"},
    {"name": "18th Street Gang", "hood": "Rampart, LA"},
    {"name": "Florencia 13", "hood": "Florence, LA"},
    {"name": "Avenues", "hood": "Northeast LA"},
    {"name": "White Fence", "hood": "East LA"},
    {"name": "Varrio Nuevo Estrada", "hood": "Boyle Heights, LA"},
    {"name": "East Coast Crips", "hood": "South LA"},
    {"name": "Hoover Criminals", "hood": "South LA"},
    {"name": "Nutty Blocc Crips", "hood": "Compton, LA"},
    {"name": "Crenshaw Mafia Bloods", "hood": "Crenshaw, LA"},
    {"name": "Black P Stones", "hood": "Exposition Park, LA"},
    {"name": "Pueblo Bishops Bloods", "hood": "Watts, LA"},
    {"name": "Harpys 13", "hood": "East LA"},
    {"name": "Clanton 14", "hood": "South LA"},
    {"name": "Temple Street", "hood": "Echo Park, LA"},
    {"name": "Rampart Villains", "hood": "Rampart, LA"},
    {"name": "Compton Avenue Crips", "hood": "Compton, LA"},
    {"name": "Elm Street Piru", "hood": "Compton, LA"},
    {"name": "Tree Top Piru", "hood": "Compton, LA"},
    {"name": "Fruit Town Piru", "hood": "Compton, LA"},
    {"name": "Westside Crips", "hood": "West LA"},
    {"name": "Mona Park Crips", "hood": "Compton, LA"},
    {"name": "Palmer Blocc Crips", "hood": "Compton, LA"},
    {"name": "Santana Blocc Crips", "hood": "Compton, LA"},
    {"name": "Acacia Blocc Crips", "hood": "Compton, LA"},
    {"name": "Kelly Park Crips", "hood": "Compton, LA"},
    {"name": "Tragniew Park Crips", "hood": "Compton, LA"},
    {"name": "Leuders Park Piru", "hood": "Compton, LA"},
    {"name": "Mob Piru", "hood": "Compton, LA"},
    {"name": "Lime Hood Piru", "hood": "Compton, LA"},
    {"name": "Richland Farms Crips", "hood": "Compton, LA"},
    {"name": "Dominguez Varrio 13", "hood": "Compton, LA"},
    {"name": "Compton Varrio Tortilla Flats", "hood": "Compton, LA"},
    {"name": "CV70s", "hood": "Compton, LA"},
    {"name": "Spook Town Crips", "hood": "Watts, LA"},
    {"name": "Nickerson Gardens Bloods", "hood": "Watts, LA"},
    {"name": "Jordan Downs Grape Street", "hood": "Watts, LA"},
    {"name": "Hacienda Village Bloods", "hood": "Watts, LA"},
    {"name": "Imperial Courts Crips", "hood": "Watts, LA"},
    {"name": "Watts Varrio Grape", "hood": "Watts, LA"},
    {"name": "Front Hood Watts Crips", "hood": "Watts, LA"},
    {"name": "Rollin 20s Bloods", "hood": "West Adams, LA"},
    {"name": "Rollin 30s Harlem Crips", "hood": "West Adams, LA"},
    {"name": "Rollin 40s Crips", "hood": "West Adams, LA"},
    {"name": "Rollin 90s Crips", "hood": "South LA"},
    {"name": "Rollin 100s Crips", "hood": "South LA"},
    {"name": "111 Neighborhood Crips", "hood": "South LA"},
    {"name": "113 Stoner Crips", "hood": "South LA"},
    {"name": "Avalon Gangster Crips", "hood": "South LA"},
    {"name": "Main Street Crips", "hood": "South LA"},
    {"name": "Raymond Avenue Crips", "hood": "South LA"},
    {"name": "Fudge Town Mafia Crips", "hood": "South LA"},
    {"name": "Weirdos Crips", "hood": "South LA"},
    {"name": "Swan Bloods", "hood": "South LA"},
    {"name": "Athens Park Bloods", "hood": "South LA"},
    {"name": "Denver Lane Bloods", "hood": "South LA"},
    {"name": "Van Ness Gangster Brims", "hood": "South LA"},
    {"name": "Harvard Park Brims", "hood": "South LA"},
    {"name": "Menlo Crips", "hood": "South LA"},
    {"name": "Figueroa Boys", "hood": "South LA"},
    {"name": "Shotgun Crips", "hood": "South LA"},
    {"name": "Original Swamp Crips", "hood": "South LA"},
    {"name": "Neighborhood Crips", "hood": "South LA"},
    {"name": "Six Pacc Crips", "hood": "South LA"},
    {"name": "Underground Crips", "hood": "South LA"},
    {"name": "Florencia 13 Southside", "hood": "South LA"},
    {"name": "La Mirada Locos 13", "hood": "East LA"},
    {"name": "Maravilla", "hood": "East LA"},
    {"name": "Varrio Nuevo Estrada Locos", "hood": "Boyle Heights, LA"},
    {"name": "Primera Flats", "hood": "East LA"},
    {"name": "Cuatro Flats", "hood": "East LA"},
    {"name": "Big Hazard", "hood": "East LA"},
    {"name": "Lil Valley Hoods", "hood": "East LA"},
    {"name": "El Hoyo Maravilla", "hood": "East LA"},
    {"name": "Indiana Dukes", "hood": "East LA"},
    {"name": "Eastside Wilmas", "hood": "East LA"},
    {"name": "Barrio Mojados", "hood": "East LA"},
    {"name": "Barrio Van Nuys 13", "hood": "Van Nuys, LA"},
    {"name": "Canoga Park Alabama", "hood": "Canoga Park, LA"},
    {"name": "Langdon Street Locos", "hood": "San Fernando Valley, LA"},
    {"name": "Pacoima Flats", "hood": "Pacoima, LA"},
    {"name": "Vineland Boyz", "hood": "Sun Valley, LA"},
    {"name": "Toonerville Rifa 13", "hood": "Atwater Village, LA"},
    {"name": "Columbia Lil Cycos 13", "hood": "Westlake, LA"},
    {"name": "Diamond Street Locos", "hood": "Silver Lake, LA"},
    {"name": "Mara Salvatrucha Westside", "hood": "Westside, LA"},
    {"name": "Rockwood Street Locos", "hood": "Echo Park, LA"},
    {"name": "Glendale Locos 13", "hood": "Glendale, LA"},
    {"name": "Burbank Locos", "hood": "Burbank, LA"},
    {"name": "Azusa 13", "hood": "Azusa, LA"},
    {"name": "Duarte Vario 13", "hood": "Duarte, LA"},
    {"name": "Norwalk Locos 13", "hood": "Norwalk, LA"},
    {"name": "Whittier Varrio Locos", "hood": "Whittier, LA"},
    {"name": "Santa Fe Springs 13", "hood": "Santa Fe Springs, LA"},
    {"name": "South Side Whittier", "hood": "Whittier, LA"},
    {"name": "Paragons", "hood": "South Gate, LA"},
    {"name": "South Gate Locos", "hood": "South Gate, LA"},
    {"name": "Lynwood Vario Tortilla Flats", "hood": "Lynwood, LA"},
    {"name": "Lynwood Bloods", "hood": "Lynwood, LA"},
    {"name": "Paramount Locos 13", "hood": "Paramount, LA"},
    {"name": "Bellflower Locos", "hood": "Bellflower, LA"},
    {"name": "Artesia Crips", "hood": "Artesia, LA"},
    {"name": "Carson Crips", "hood": "Carson, LA"},
    {"name": "Varrio Carson 13", "hood": "Carson, LA"},
    {"name": "Westside Wilmas", "hood": "Wilmington, LA"},
    {"name": "Varrio Wilmington 13", "hood": "Wilmington, LA"},
    {"name": "Eastside Longos", "hood": "Long Beach, LA"},
    {"name": "West Side Longos", "hood": "Long Beach, LA"},
    {"name": "Insane Long Beach Crips", "hood": "Long Beach, LA"},
    {"name": "Rollin 20s Long Beach Crips", "hood": "Long Beach, LA"},
    {"name": "Long Beach Insane Crips", "hood": "Long Beach, LA"},
    {"name": "Sons of Samoa", "hood": "Carson, LA"},
    {"name": "Tongan Crip Gang", "hood": "Carson, LA"},
    {"name": "Samoan Crips", "hood": "Hawthorne, LA"},
    {"name": "Hawthorne Piru", "hood": "Hawthorne, LA"},
    {"name": "Lawndale Bloods", "hood": "Lawndale, LA"},
    {"name": "Gardena Shotgun Crips", "hood": "Gardena, LA"},
    {"name": "Gardena Paybacc Crips", "hood": "Gardena, LA"},
    {"name": "Varrio Gardena 13", "hood": "Gardena, LA"},
    {"name": "Inglewood Crips", "hood": "Inglewood, LA"},
    {"name": "Queen Street Bloods", "hood": "Inglewood, LA"},
    {"name": "Crenshaw Mafia Gang", "hood": "Crenshaw, LA"},
    {"name": "Black P Stone Jungles", "hood": "Hyde Park, LA"},
    {"name": "Jungle Boys", "hood": "Baldwin Hills, LA"},
    {"name": "Westside Piru", "hood": "Compton, LA"},
    {"name": "Westside Pomona Crips", "hood": "Pomona, LA"},
    {"name": "Eastside Pomona Crips", "hood": "Pomona, LA"},
    {"name": "Pomona Varrio 12", "hood": "Pomona, LA"},
    {"name": "12th Street Sharkies", "hood": "Pomona, LA"},
    {"name": "Ontario Varrio Sur", "hood": "Ontario, LA"},
    {"name": "Montebello Park Gang", "hood": "Montebello, LA"},
    {"name": "Lomas Varrio 70", "hood": "Montebello, LA"},
    {"name": "Barrio El Sereno", "hood": "El Sereno, LA"},
    {"name": "Eastside Alvas", "hood": "El Sereno, LA"},
    {"name": "Varrio Nuevo Aliso", "hood": "Aliso Village, LA"},
    {"name": "Pico Viejo Locos", "hood": "Pico-Union, LA"},
    {"name": "Drifters", "hood": "Pico-Union, LA"},
    {"name": "Crazy Riders", "hood": "Mid-City, LA"},
    {"name": "Mid City Stoners 13", "hood": "Mid-City, LA"},
    {"name": "Jefferson Park Locos", "hood": "Jefferson Park, LA"},
    {"name": "Adams 11 Locos", "hood": "Adams, LA"},
    {"name": "Country Club Drive Locos", "hood": "South LA"},
    {"name": "Malditos 13", "hood": "Lincoln Heights, LA"},
    {"name": "Lincoln Heights Locos", "hood": "Lincoln Heights, LA"},
    {"name": "Eastside Clover", "hood": "Glassel Park, LA"},
    {"name": "Glassel Park Boys", "hood": "Glassel Park, LA"},
    {"name": "Cypress Park Locos", "hood": "Cypress Park, LA"},
    {"name": "Arroyo Boys", "hood": "Highland Park, LA"},
    {"name": "Highland Park Gang", "hood": "Highland Park, LA"},
    {"name": "San Fer 13", "hood": "San Fernando, LA"},
    {"name": "Sylmar Locotes", "hood": "Sylmar, LA"},
    {"name": "Pacas 13", "hood": "Panorama City, LA"},
    {"name": "Panorama City Locos", "hood": "Panorama City, LA"},
    {"name": "North Hollywood Locos", "hood": "North Hollywood, LA"},
    {"name": "Blythe Street Gang", "hood": "Panorama City, LA"},
    {"name": "Barrio Van Nuys Locos", "hood": "Van Nuys, LA"},
]

gangs = {}
active_gang_owners = set()

SENTENCE_TIERS = [
    {"label": "2 years",  "minutes": 2},
    {"label": "5 years",  "minutes": 5},
    {"label": "10 years", "minutes": 10},
    {"label": "15 years", "minutes": 15},
    {"label": "25 years", "minutes": 25},
    {"label": "40 years", "minutes": 40},
    {"label": "50 years", "minutes": 50},
]
SENTENCE_WEIGHTS = [30, 25, 20, 12, 8, 3, 2]

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def is_admin(message):
    member = message.author
    if isinstance(member, discord.Member):
        return member.guild_permissions.administrator
    return False


def user_has_active_gang(user_id):
    return any(g['owner_id'] == user_id and g['alive'] for g in gangs.values())


def generate_code():
    while True:
        code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
        if code not in gangs:
            return code


def generate_ai_members(count=5):
    available = list(STREET_NAMES)
    random.shuffle(available)
    names = available[:min(count, len(available))]
    members = []
    for name in names:
        members.append({
            "name": name,
            "rep": random.randint(10, 200),
            "alive": True,
            "kills": 0,
            "deaths": 0,
            "times_jailed": 0,
            "times_snitched": 0,
            "missions_survived": 0,
            "came_back_from_zero": False,
            "jail_until": None,
            "jail_sentence": None,
        })
    return members


def get_alive_members(gang):
    return [m for m in gang.get('members', []) if m['alive']]


def get_free_members(gang):
    now = time.time()
    return [
        m for m in gang.get('members', [])
        if m['alive'] and (m.get('jail_until') is None or now >= m['jail_until'])
    ]


def get_gang_bodies(gang):
    return sum(m.get('kills', 0) for m in gang.get('members', []))


def get_gang_deaths(gang):
    return sum(m.get('deaths', 0) for m in gang.get('members', []))


def check_and_mark_dead(code):
    gang = gangs[code]
    if len(get_alive_members(gang)) == 0:
        gang['alive'] = False
        owner_id = gang['owner_id']
        if not user_has_active_gang(owner_id):
            active_gang_owners.discard(owner_id)


def send_to_jail(member):
    tier = random.choices(SENTENCE_TIERS, weights=SENTENCE_WEIGHTS, k=1)[0]
    member['jail_until'] = time.time() + (tier['minutes'] * 60)
    member['jail_sentence'] = tier['label']
    member['times_jailed'] = member.get('times_jailed', 0) + 1
    return tier['label']


def get_member_status(m):
    if not m['alive']:
        return "Dead"
    now = time.time()
    if m.get('jail_until') and now < m['jail_until']:
        return f"Locked Up ({m['jail_sentence']})"
    return "Free"


def format_member_list(members):
    if not members:
        return "None left."
    lines = []
    for m in members:
        name = f"`{m['name']}`"
        kills = m.get('kills', 0)
        tags = evaluate_status(m)
        tag_str = "  ".join([f"[{t}]" for t in tags]) if tags else "--"
        status = get_member_status(m)
        lines.append(f"{name}  |  {tag_str}  |  {kills} kills  |  {status}")
    return "\n".join(lines)


def add_revenge_target(gang, killer_name, enemy_gang_info, enemy_rep):
    if 'revenge_targets' not in gang:
        gang['revenge_targets'] = []
    for target in gang['revenge_targets']:
        if target['gang'] == enemy_gang_info['name']:
            target['name'] = killer_name
            target['enemy_rep'] = enemy_rep
            return
    gang['revenge_targets'].append({
        "name": killer_name,
        "gang": enemy_gang_info['name'],
        "gang_info": enemy_gang_info,
        "enemy_rep": enemy_rep,
    })


def get_revenge_targets(gang):
    return gang.get('revenge_targets', [])


def remove_revenge_target(gang, gang_name):
    if 'revenge_targets' not in gang:
        return
    gang['revenge_targets'] = [t for t in gang['revenge_targets'] if t['gang'] != gang_name]


# ─────────────────────────────────────────────
# SLIDE OUTCOME
# ─────────────────────────────────────────────

def calculate_slide_outcome(gang, rolling_members, enemy_rep, is_revenge=False):
    player_rep = gang['rep']
    rep_diff = player_rep - enemy_rep
    win_chance = 50 + int((rep_diff / 500) * 40)
    win_chance = max(10, min(90, win_chance))
    if is_revenge:
        win_chance = min(95, win_chance + 10)

    player_won = random.randint(1, 100) <= win_chance
    outcome_lines = []
    kills_this_fight = {}

    if player_won:
        rep_gain = random.randint(20, int(max(1, enemy_rep * 0.4)))
        if is_revenge:
            rep_gain = int(rep_gain * 1.25)
        gang['rep'] = player_rep + rep_gain
        gang['fights_won'] = gang.get('fights_won', 0) + 1

        win_kill_templates = [
            "{member} was the first one out the car before it even stopped moving. He had eyes on the target the whole ride over and the moment his feet hit the pavement he was already squeezing. Dropped two before they even registered what was happening and had his door back open before the echo cleared.",
            "{member} came in from the alley where nobody was watching. Crept the whole length of the block in the dark, waited until the right moment, then stepped out and handled every single one of them. Walked back through the same alley like a ghost. Nobody saw a face.",
            "{member} pulled up on the opp's shot caller directly — none of the foot soldiers, straight to the top. Words were exchanged for about four seconds before {member} made it clear this wasn't a conversation. Left a message the whole set would understand.",
            "{member} had been sitting on the location for six hours before anyone else arrived. By the time the rest of the crew pulled up, {member} had already mapped every exit, counted heads, and picked the angle. When it went down it was over in under a minute.",
            "{member} rushed straight into the middle of their whole group without hesitating for a single second — didn't wait for backup, didn't look for cover, just moved. The opps scattered in every direction. Three of them didn't get far enough.",
            "{member} caught the opp's lieutenant coming out the back of the trap house alone at the worst possible time. Blocked the exit, made sure they understood who sent the message, and left them there as a reminder of who owns these streets.",
            "{member} moved through the whole block like he had a map of every corner in his head. Hit the first two before they even looked up, kept moving, caught a third one trying to make it to a car. By the time sirens were anywhere in earshot the crew was already gone.",
            "{member} waited until the shift changed and the block was thinnest, then struck with everything the crew had. By the time the opps realized how bad they were outnumbered it was already over. The ones who ran spread the word themselves.",
            "{member} had been watching their patterns for three days straight before making a move. Knew exactly when the corner would be down to two people and hit it at that exact window. Precision over power — the whole thing was surgical.",
            "{member} set up a fake meet through a mutual and used that to hit them where it hurt most. Took the stash, left a message, and walked out with the situation flipped entirely in the set's favor.",
            "{member} went in through the back while the rest of the crew created a distraction at the front. The opps split their attention and that half-second of confusion was all {member} needed. Came out clean while the enemy was still trying to figure out what just happened.",
        ]

        for m in rolling_members:
            old_kills = m.get('kills', 0)
            m['kills'] = old_kills + 1
            m['missions_survived'] = m.get('missions_survived', 0) + 1
            kills_this_fight[m['name']] = kills_this_fight.get(m['name'], 0) + 1
            line = random.choice(win_kill_templates).replace("{member}", f"`{m['name']}`")
            outcome_lines.append(line)

        if len(get_alive_members(gang)) > 1 and random.randint(1, 100) <= 20:
            still_alive = [m for m in rolling_members if m['alive']]
            if still_alive:
                casualty = random.choice(still_alive)
                casualty['alive'] = False
                casualty['deaths'] = casualty.get('deaths', 0) + 1
                friendly_loss_lines = [
                    f"`{casualty['name']}` caught a round in the chest during the exchange. Stayed on his feet long enough to make it back to the car but was gone before they reached the block. Won the fight but the set lost somebody real tonight.",
                    f"`{casualty['name']}` took a shot from someone hiding behind a car on the far end of the block. The crew didn't realize until they were already pulling off. He didn't make it to the hospital.",
                    f"One of the opps who was already down still had enough left to get a shot off. `{casualty['name']}` caught it in the neck. The crew held the block but held a funeral three days later.",
                    f"`{casualty['name']}` took a stray during the chaos — wrong place, wrong angle, bad luck. The streets claimed another one that night. Set won the slide but the victory felt hollow.",
                    f"`{casualty['name']}` pushed too deep into their territory without cover and got cut off. By the time the crew circled back it was too late. Another name on the wall.",
                    f"`{casualty['name']}` was covering the exit when a shooter appeared from a second floor window nobody had eyes on. Took two shots to the back and was gone before the ambulance was even called.",
                    f"The celebration was cut short. `{casualty['name']}` had been hit early in the fight but kept moving on adrenaline and nobody realized how bad it was until the car was three blocks away. He didn't make it to morning.",
                ]
                outcome_lines.append(random.choice(friendly_loss_lines))

        if random.randint(1, 100) <= 15:
            now = time.time()
            still_free = [m for m in rolling_members if m['alive'] and (m.get('jail_until') is None or now >= m['jail_until'])]
            if still_free:
                jailed = random.choice(still_free)
                sentence = send_to_jail(jailed)
                jail_after_win_lines = [
                    f"Task force had been sitting on the block all week waiting for exactly this. `{jailed['name']}` got flagged leaving the scene — plate ran, warrant pulled, lights on before they made it two miles. Facing {sentence} and the DA isn't offering anything.",
                    f"A neighbor two houses down had a camera pointed at the street and handed the footage over the next morning. `{jailed['name']}`'s face was clear as day on four different frames. Got picked up at a family member's house by noon. {sentence} sentence.",
                    f"Somebody in the area talked. Whether it was fear or money nobody knows, but `{jailed['name']}`'s description was in the system before sunrise. Knocked at the gas station the following evening. {sentence} — no bail hearing for thirty days.",
                    f"`{jailed['name']}` went back to the block an hour later to check on things and rolled straight into a plainclothes unit that had been watching since the incident. Didn't even realize it was happening until the cuffs were on. {sentence} and the lawyer isn't optimistic.",
                    f"Phone records and cell tower data put `{jailed['name']}` at the exact location at the exact time. Federal involvement made bail impossible. {sentence} sentence and every appeal got denied.",
                    f"A traffic stop two exits away turned into a full search when the officer ran the plates. `{jailed['name']}` had no way to explain what was found in the car. {sentence} — the public defender said take the deal.",
                ]
                outcome_lines.append(random.choice(jail_after_win_lines))

        return {
            "won": True,
            "rep_gain": rep_gain,
            "old_rep": player_rep,
            "new_rep": gang['rep'],
            "enemy_rep": enemy_rep,
            "outcome_lines": outcome_lines,
            "kills_this_fight": kills_this_fight,
            "total_bodies": get_gang_bodies(gang),
            "total_deaths": get_gang_deaths(gang),
            "members_alive": len(get_alive_members(gang)),
        }

    else:
        gang['fights_lost'] = gang.get('fights_lost', 0) + 1

        for m in rolling_members:
            if len(get_alive_members(gang)) > 1 and random.randint(1, 100) <= 40:
                m['alive'] = False
                m['deaths'] = m.get('deaths', 0) + 1
                death_lines = [
                    f"`{m['name']}` was the one who moved first and caught the first shot because of it. Took two rounds before he hit the ground and never got back up. The crew had to leave him there and couldn't even go back until the next morning.",
                    f"`{m['name']}` got cut off from the rest of the crew when the opps came from a second direction nobody had seen. Cornered between two buildings with no way out. They found the body two hours after the crew made it back.",
                    f"`{m['name']}` took a shot through a car window trying to provide cover for the others. The bullet went through the glass and hit something vital. Was gone before anyone could get to him.",
                    f"The opps had numbers and positioning that the crew didn't account for. `{m['name']}` was the one who took the worst of it — caught in the open with nowhere to go. Died on that block.",
                    f"`{m['name']}` stood his ground even when the crew started falling back. Refused to leave until everyone else was out. That decision cost him his life. He held the line but didn't make it off it.",
                    f"A shooter came from a rooftop that nobody had checked. `{m['name']}` never even saw where the shot came from. Dropped in the middle of the street. The set lost one of their realest that night.",
                    f"`{m['name']}` tried to make it to the car but the opps had the exit cut off. Took three shots trying to push through and collapsed ten feet short of the door. The crew had to pull off without him.",
                    f"`{m['name']}` took a round to the stomach early in the exchange and kept fighting for another two minutes before the blood loss caught up. He went out swinging.",
                ]
                outcome_lines.append(random.choice(death_lines))
            else:
                if random.randint(1, 100) <= 30 and m['alive']:
                    sentence = send_to_jail(m)
                    escape_then_caught_lines = [
                        f"`{m['name']}` made it out of the immediate situation but the block was already surrounded by the time they reached the car. Got hemmed up at the intersection a quarter mile away with everything still on them. {sentence} and they're not getting out on bail.",
                        f"`{m['name']}` ran through yards and back streets for twenty minutes before collapsing from exhaustion two neighborhoods over. A patrol unit found them sitting on a curb. {sentence} sentence — the DA stacked every charge available.",
                        f"`{m['name']}` escaped the gunfire but a helicopter was already in the air. Tracked on foot for six blocks and taken down by a K9 unit. Facing {sentence} and multiple charges that won't help the case.",
                        f"Cameras on the bus route caught `{m['name']}`'s full face and route. Task force knocked on the door the next morning with a warrant already signed. {sentence} — no negotiating with what they have.",
                        f"`{m['name']}` made it back to the hood but somebody on the block had already been talking to detectives. Got scooped up sitting on the porch the next afternoon. {sentence} sentence.",
                        f"The getaway car broke down four blocks away. `{m['name']}` was still sitting in it when the first patrol unit rolled up. {sentence} — caught red handed with nowhere to go.",
                    ]
                    outcome_lines.append(random.choice(escape_then_caught_lines))
                else:
                    m['missions_survived'] = m.get('missions_survived', 0) + 1
                    survived_lines = [
                        f"`{m['name']}` took a round through the shoulder that spun him completely around but somehow kept moving. Made it back to the car bleeding through his shirt, jaw tight, not saying a word the whole drive. Alive but not the same after that night.",
                        f"`{m['name']}` dove behind a parked truck when the shooting started and stayed flat on the ground for four minutes while rounds hit the vehicle above him. Crawled to the alley when it went quiet and made it back on foot. Shaken but breathing.",
                        f"`{m['name']}` caught a graze across the ribs — burned like fire but nothing that would kill him. Wrapped it with a shirt in the backseat and didn't go to the hospital. Walked into the trap house two hours later looking like nothing happened.",
                        f"`{m['name']}` took a hit in the leg during the retreat but refused to go down. Leaned on the car door the whole ride back and bit through the pain without a sound. Still standing. Still in it.",
                        f"`{m['name']}` took a pistol grip to the face when the opps rushed — cut above the eye, nose broken, vision blurred. Made it out but took a beating that the whole set saw.",
                        f"`{m['name']}` ran the wrong direction and ended up cornered in a dead end, had to climb a fence with shots landing around his feet. Made it over. Landed hard. Got back to the block two hours later. Still counts as making it out.",
                        f"`{m['name']}` took a fragment to the forearm from a round that hit the concrete next to him. Deep enough to need stitches but not deep enough to stop him. Got patched up in someone's bathroom and was back on the block by morning.",
                        f"`{m['name']}` got clipped in the ear — half an inch to the left and that would have been it. Walked back to the car with blood running down his neck like it was nothing.",
                    ]
                    outcome_lines.append(random.choice(survived_lines))

        rep_loss = random.randint(20, int(max(1, player_rep * 0.25)))
        gang['rep'] = max(1, player_rep - rep_loss)

        return {
            "won": False,
            "rep_loss": player_rep - gang['rep'],
            "old_rep": player_rep,
            "new_rep": gang['rep'],
            "enemy_rep": enemy_rep,
            "outcome_lines": outcome_lines,
            "kills_this_fight": kills_this_fight,
            "total_bodies": get_gang_bodies(gang),
            "total_deaths": get_gang_deaths(gang),
            "members_alive": len(get_alive_members(gang)),
        }


async def send_slide_result(channel, gang, enemy_gang_info, result, is_revenge=False):
    if result['won']:
        title = "Revenge Collected — Debt Settled" if is_revenge else "Slide Won — Block Secured"
        descriptions = [
            f"**{gang['name']}** came back for blood and got exactly what they came for. **{enemy_gang_info['name']}** paid for what they did and the whole hood knows who collected.",
            f"**{gang['name']}** ran **{enemy_gang_info['name']}** off the block and claimed everything they had. The hood knows who runs it now.",
            f"**{gang['name']}** pulled up on **{enemy_gang_info['name']}** and left no doubt. That block belongs to them now.",
            f"It wasn't even close. **{gang['name']}** dismantled **{enemy_gang_info['name']}** piece by piece.",
        ] if not is_revenge else [
            f"The debt is settled. **{gang['name']}** hunted down **{enemy_gang_info['name']}** and made them feel every bit of the pain they caused.",
            f"**{gang['name']}** didn't forget and didn't forgive. The message was loud enough for the entire city to hear.",
            f"**{enemy_gang_info['name']}** thought it was over. **{gang['name']}** came back with everything and left no doubt.",
        ]
        color = discord.Color.green()
        footer = "They know not to touch yours again." if is_revenge else "Hold that block. Don't let nobody take what's yours."
    else:
        title = "Revenge Failed — Took Another L" if is_revenge else "Slide Lost — Took an L"
        descriptions = [
            f"**{gang['name']}** came for revenge but **{enemy_gang_info['name']}** was ready. Took another L.",
            f"**{gang['name']}** got run off by **{enemy_gang_info['name']}** tonight. Took heavy losses but the set is still breathing.",
            f"**{gang['name']}** underestimated **{enemy_gang_info['name']}** and paid the price.",
            f"It was a bad night for **{gang['name']}**. **{enemy_gang_info['name']}** sent them back with a clear message.",
        ]
        color = discord.Color.orange()
        footer = "Regroup. Get your head right. Come back harder."

    header_embed = discord.Embed(title=title, description=random.choice(descriptions), color=color)
    header_embed.add_field(name="Opp Cred", value=str(result['enemy_rep']), inline=True)
    if result['won']:
        header_embed.add_field(name="Cred Gained", value=f"+{result['rep_gain']}", inline=True)
    else:
        header_embed.add_field(name="Cred Lost", value=f"-{result['rep_loss']}", inline=True)
    header_embed.add_field(name="New Street Cred", value=f"{result['old_rep']} -> {result['new_rep']}", inline=True)
    header_embed.add_field(name="Members Alive", value=str(result['members_alive']), inline=True)
    await channel.send(embed=header_embed)

    if result['outcome_lines']:
        for i, line in enumerate(result['outcome_lines']):
            story_embed = discord.Embed(description=line, color=color)
            story_embed.set_footer(text=f"Play by play — {i + 1} of {len(result['outcome_lines'])}")
            await channel.send(embed=story_embed)
            await asyncio.sleep(1)

    kills_lines = []
    for name, k in result.get('kills_this_fight', {}).items():
        kills_lines.append(f"`{name}` — {k} kill{'s' if k != 1 else ''} this run")
    kills_text = "\n".join(kills_lines) if kills_lines else "No bodies this run."

    summary_embed = discord.Embed(title="Run Summary", color=color)
    summary_embed.add_field(name="Kills This Run", value=kills_text, inline=False)
    summary_embed.set_footer(text=footer)
    await channel.send(embed=summary_embed)


# ─────────────────────────────────────────────
# EVENTS
# ─────────────────────────────────────────────

EVENTS = [
    {"name": "Corner Locked Down", "description": "{member} spent the whole night putting in work on Figueroa, muscling every last corner boy off the strip until nobody dared step foot on it. By morning, **{name}** owned every inch of that block and the whole neighborhood knew it.", "type": "rep_up", "value": (20, 80), "color": discord.Color.green()},
    {"name": "Successful Lick", "description": "{member} moved quiet and precise — scoped the target for two days, waited for the perfect moment, and walked away clean with enough to keep **{name}** comfortable for months. Nobody saw a thing. Nobody said a thing.", "type": "rep_up", "value": (30, 100), "color": discord.Color.green()},
    {"name": "Street Fight Victory", "description": "{member} ran into four of the opps outside the liquor store on Central and didn't hesitate for a second. Squared up solo, dropped two of them, and walked away without a scratch. **{name}**'s name rang out before the night was over.", "type": "rep_up", "value": (20, 60), "color": discord.Color.green()},
    {"name": "Territory Claimed", "description": "**{name}** moved on a new block that the opps had been sitting on for months. {member} led the crew in, posted up in broad daylight, and dared anyone to say something. Nobody did. That block is **{name}**'s now.", "type": "rep_up", "value": (40, 120), "color": discord.Color.green()},
    {"name": "OG Vouched", "description": "One of the most respected OGs in the city pulled {member} aside and told him straight — he had been watching **{name}** and they were doing it right. He made a few calls that same night. Doors opened that nobody even knew existed.", "type": "rep_up", "value": (50, 150), "color": discord.Color.green()},
    {"name": "Retaliation Hit", "description": "The opps disrespected **{name}** at a vigil last week. {member} didn't forget. Waited a full week so nobody would expect it, then showed up at exactly the right time and delivered the message personally. The streets went quiet after that.", "type": "rep_up", "value": (60, 180), "color": discord.Color.green()},
    {"name": "Prison Connects Made", "description": "{member} got word inside through a cousin doing a stretch at Corcoran. Made the right introductions, passed the right messages, and now **{name}** has connects in three different facilities. Business does not stop just because somebody is locked up.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Rival Scattered", "description": "{member} pulled up on the opposition's main corner with the whole crew and gave them one warning. They didn't take it seriously. **{name}** hit back so hard and so fast that within 48 hours the opps had abandoned three blocks without a single shot being fired.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    {"name": "Hood Documentary", "description": "A filmmaker from outside the city came through to document real street life and {member} let them follow for a week. The footage went viral — raw and uncut. Now everyone knows {member}'s face and **{name}**'s name. Respect flowing in from all directions.", "type": "rep_up", "value": (30, 90), "color": discord.Color.green()},
    {"name": "Rapper Shoutout", "description": "A certified street rapper dropped a project and buried {member}'s name in two different tracks — name, hood, and **{name}** repped fully. The comment sections went crazy. People from three cities were asking about the set by the next morning.", "type": "rep_up", "value": (50, 130), "color": discord.Color.green()},
    {"name": "Fed the Block", "description": "{member} pulled out of pocket and threw a full cookout on the block — ribs, cases of water, music, the whole thing. Families came out, elders dapped up the crew, and kids who never talked to **{name}** before were showing love. Community locked in solid.", "type": "rep_up", "value": (25, 70), "color": discord.Color.green()},
    {"name": "Big Score", "description": "{member} linked up with a connect that came through a third party and set up the biggest score **{name}** had seen in years. Everything went smooth — product moved fast, money came back clean, and every member of the crew ate well for the first time in a long time.", "type": "rep_up", "value": (60, 160), "color": discord.Color.green()},
    {"name": "Took the Block Back", "description": "The opps had been sitting on a block that used to belong to **{name}** for six months. {member} organized the whole thing — right time, right numbers, right message. They moved at 2am and by sunrise that block was flying **{name}**'s colors again.", "type": "rep_up", "value": (70, 170), "color": discord.Color.green()},
    {"name": "Put in Work", "description": "There was a name on a list that needed to be handled. {member} didn't ask questions, didn't ask for extra. Just said when and where and got it done quietly, cleanly, with no trail left behind. **{name}** moves different because of soldiers like that.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    {"name": "Weapons Cache Found", "description": "{member} got a tip about a stash that a rival set had buried near the rail yard. Went out there at 3am with two others, dug it up, and brought everything back to the block. **{name}** is better equipped tonight than they were this morning.", "type": "rep_up", "value": (50, 140), "color": discord.Color.green()},
    {"name": "Court Case Dismissed", "description": "{member} had been facing serious charges that had the whole set walking on eggshells for months. The DA's key witness stopped cooperating and without testimony the case fell apart completely. {member} walked out of the courthouse and came straight back to the block. **{name}** is at full strength.", "type": "rep_up", "value": (40, 110), "color": discord.Color.green()},
    {"name": "Neighborhood Loyalty", "description": "Three different families on the block independently told detectives they saw nothing and had nothing to say when investigators came around asking questions about **{name}**. {member} built that loyalty over years of showing up for people when it mattered. Now it's paying off.", "type": "rep_up", "value": (35, 95), "color": discord.Color.green()},
    {"name": "Set the Trap", "description": "{member} spent two weeks feeding false information to someone suspected of talking to the opposition. When the opps showed up exactly where the false tip said to be, **{name}** was waiting. The ambush was clean and the source problem was handled at the same time.", "type": "rep_up", "value": (70, 180), "color": discord.Color.green()},
    {"name": "Made Bail", "description": "One of **{name}**'s most important members had been sitting in county for three months. {member} coordinated the whole effort — called in favors, moved money, found the right bondsman. That soldier walked out yesterday and the set is stronger for it.", "type": "rep_up", "value": (30, 80), "color": discord.Color.green()},
    {"name": "New Connect", "description": "{member} got introduced to a supplier through a mutual from up north who vouched for **{name}** personally. The first order came in clean, the price was right, and the quality was better than anything the set had been working with before. The operation just leveled up.", "type": "rep_up", "value": (60, 150), "color": discord.Color.green()},
    {"name": "Snitch in the Ranks", "description": "The feds had been watching **{name}** for weeks and nobody could figure out how they knew so much. Then a sealed document leaked through a lawyer's office — {member}'s name was on it. Cooperating since the summer. The set is fractured. Trust is gone. Rep is in the dirt.", "type": "rep_down", "value": (30, 100), "color": discord.Color.orange(), "snitch": True},
    {"name": "Botched Mission", "description": "{member} had one job — get in, handle it, get out. Instead they froze at the wrong moment, dropped something they shouldn't have, and had to abort. Three people on the block filmed the whole thing from their porch. **{name}** is a punchline on the streets right now.", "type": "rep_down", "value": (20, 80), "color": discord.Color.orange()},
    {"name": "Homie Got Knocked", "description": "Task force rolled up on {member} while they were sitting outside with product on them and a warrant already signed. Bail was denied at the hearing. **{name}** lost one of their most solid members overnight and the whole operation slowed down.", "type": "rep_down", "value": (40, 120), "color": discord.Color.orange()},
    {"name": "Ran Off the Block", "description": "The opps pulled up three cars deep right at shift change when **{name}** only had two people on the corner. {member} tried to hold it but the math wasn't there. Had to fall back and watch them take over the block. Whole hood saw it happen in real time.", "type": "rep_down", "value": (50, 150), "color": discord.Color.orange()},
    {"name": "Internal Beef", "description": "{member} and another member of **{name}** got into a bad argument over money that turned physical right outside the trap house. Neighbors recorded it. Other sets are sharing the video and laughing. Nothing breaks a crew's reputation faster than airing out internal problems in public.", "type": "rep_down", "value": (25, 75), "color": discord.Color.orange()},
    {"name": "LAPD Raid", "description": "Forty officers hit **{name}**'s main spot at 5am with a no-knock warrant and body cams rolling. {member} and two others barely got out the back before the doors came down. Everything inside got seized — product, cash, phones, weapons. The whole operation is on pause.", "type": "rep_down", "value": (60, 180), "color": discord.Color.orange()},
    {"name": "Caught Lacking", "description": "The opps caught {member} alone at a gas station on the wrong side of town, repping **{name}** loud with nowhere to run. Took everything off them, recorded the whole thing, and posted it online before {member} even made it back to the hood. The comments are brutal.", "type": "rep_down", "value": (30, 90), "color": discord.Color.orange()},
    {"name": "Lost the Package", "description": "{member} was moving a major package cross-town and made a wrong decision that cost everything. Whether it got taken by the opps or seized at a checkpoint, the result was the same — **{name}** lost the product, lost the money, and the connect is threatening to cut them off.", "type": "rep_down", "value": (45, 130), "color": discord.Color.orange()},
    {"name": "Homie Flipped", "description": "{member} had been facing a fifteen-year bid and nobody knew they had been cooperating for months. The DA announced the indictments on a Tuesday morning. **{name}** lost four members to federal charges in one day. The betrayal runs deep.", "type": "rep_down", "value": (50, 160), "color": discord.Color.orange(), "snitch": True},
    {"name": "Jumped by Opps", "description": "Eight of the opposition cornered {member} two blocks from home in the middle of the afternoon with witnesses everywhere. Beat them down for a full minute while people recorded on their phones. **{name}**'s name is attached to that video and the streets are not letting it go.", "type": "rep_down", "value": (35, 110), "color": discord.Color.orange()},
    {"name": "Fronted and Folded", "description": "{member} got on social media and called out a rival set by name — specific threats, specific locations, specific times. The whole city was watching. When the moment came, {member} was nowhere to be found. **{name}** has not heard the end of it.", "type": "rep_down", "value": (40, 100), "color": discord.Color.orange()},
    {"name": "Car Got Pulled Over Dirty", "description": "{member} was riding dirty through the wrong part of town when a routine traffic stop turned into a full search. The officer found everything — product, a pistol, and a scale. **{name}** lost a soldier and a significant amount of supply in one stop that could have been avoided.", "type": "rep_down", "value": (35, 95), "color": discord.Color.orange()},
    {"name": "Stash House Burned", "description": "Somebody gave up the location of **{name}**'s secondary stash house. The opps hit it at noon when it was lightly guarded — {member} barely made it out the back window. Everything inside was gone. Months of work wiped out in under ten minutes.", "type": "rep_down", "value": (55, 150), "color": discord.Color.orange()},
    {"name": "Connect Cut Them Off", "description": "Word got back to **{name}**'s main connect that {member} had been moving product independently on the side. The relationship ended immediately and the supply dried up overnight. The set is scrambling and the streets can tell something is off.", "type": "rep_down", "value": (45, 120), "color": discord.Color.orange()},
    {"name": "Funeral Turned Violent", "description": "The set gathered to bury one of their own and the opps chose that moment to pull up and show out. {member} tried to keep things calm but it escalated fast. Three people got hit, the service had to be abandoned, and the disrespect spread through the whole hood by nightfall.", "type": "rep_down", "value": (60, 160), "color": discord.Color.orange()},
    {"name": "Quiet Night", "description": "{member} held down the corner all night from sundown to sunrise — stayed alert, watched the block, kept things moving. But there was nothing to report. No moves, no incidents, no problems. Sometimes the streets just go still. **{name}** is positioned and ready.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Laying Low", "description": "There has been too much heat in the area lately — patrol cars circling every hour, a couple of unfamiliar faces asking questions, and word that the task force has been running plates. {member} made the call to keep **{name}** off the corners for the night. Smart move.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Watching and Waiting", "description": "{member} spent the night riding through the area, getting eyes on enemy positions, counting heads, and logging patterns. No action taken tonight — this was reconnaissance. **{name}** is building a picture and when the time comes to move, they will move informed.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Regrouping", "description": "After recent events the crew needed a night to regroup. {member} called everyone in, sat them down, and had a real conversation about what went wrong and what needs to change. **{name}** came out of that meeting more focused than they have been in months.", "type": "nothing", "color": discord.Color.greyple()},
]

EVENT_WEIGHTS = [200 for _ in EVENTS]

BLOCK_PARTY_EVENTS = [
    {"name": "Block Party Jumping", "description": "The whole hood came out. Music rattling windows two blocks over, kids on bikes, OGs posted on lawn chairs, young ones dancing in the street. {member} kept the energy right all night — making sure everyone was fed, everyone was good, and **{name}**'s name stayed on every lip in a positive way. By the end of the night the community felt like one unit.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Community Showed Love", "description": "Families from three streets over came through specifically because they heard **{name}** was throwing it down. {member} made sure every single person felt welcome — passed out food personally, checked on the elders, kept the little ones entertained. The neighborhood didn't just attend the party. They claimed it.", "type": "rep_up", "value": (30, 80), "color": discord.Color.green()},
    {"name": "Local Legend Pulled Up", "description": "A respected OG who hadn't been seen publicly in years showed up unannounced and spent two hours at **{name}**'s block party. Sat with {member} for a long time. Told stories. Gave his blessing in front of everyone who mattered. That kind of endorsement doesn't get bought — it gets earned.", "type": "rep_up", "value": (50, 130), "color": discord.Color.green()},
    {"name": "Rival Set Sent a Message", "description": "Word got back before midnight that a rival set had sent someone through earlier to see if the party was real or a setup. When they reported back that it was genuine — food, families, no trap — the rival set sent a message through a mutual: they respected the move. **{name}**'s rep climbed just from doing things right.", "type": "rep_up", "value": (35, 90), "color": discord.Color.green()},
    {"name": "Block Party Goes All Night", "description": "What started at 4pm was still going strong at 2am. {member} kept refilling the food, kept the speakers on, kept the vibe elevated. People who had to work the next morning stayed anyway. By the time it finally wound down the whole block had been fed, watered, and reminded why **{name}** runs this hood.", "type": "rep_up", "value": (45, 110), "color": discord.Color.green()},
    {"name": "News Crew Showed Up", "description": "A local news segment on community events came through to film. {member} handled the camera perfectly — spoke about giving back, spoke about the neighborhood, never said anything that could be used wrong. The segment aired the next morning and **{name}**'s hood got shown in a light people don't usually see.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Young Ones Got Recruited", "description": "Three younger kids from the block spent the whole party watching how **{name}** moved — how {member} carried themselves, how the crew operated, how they were treated by everyone around them. Before the night was over all three had made it clear they wanted in. The set is growing from the roots up.", "type": "rep_up", "value": (25, 65), "color": discord.Color.green()},
    {"name": "Driveby — Party Shot Up", "description": "Everything was going right until a dark car rolled through slow from the north end of the block. {member} saw it coming a half second before it started but there was no time. Shots fired into the crowd before the car accelerated and disappeared. People scattered, the night that was supposed to build community ended in chaos.", "type": "driveby", "color": discord.Color.dark_red()},
    {"name": "Driveby — Second Pass", "description": "The first pass was just to see who flinched. {member} tried to get people moving but the second car came from the opposite direction before anyone could regroup. Two vehicles, two angles, maximum confusion. By the time it was over the block was empty and the party was done.", "type": "driveby", "color": discord.Color.dark_red()},
    {"name": "Opps Crashed the Party", "description": "Six of them walked up on foot from the alley acting like they belonged. {member} clocked them immediately and tried to de-escalate but one of the opps went straight for confrontation. What started as words turned into a full brawl in the middle of the street with kids and elders still on the block. Three people got hurt before it broke up.", "type": "brawl", "color": discord.Color.red()},
    {"name": "Police Rolled Through", "description": "Two patrol cars pulled up slow around 9pm and parked at opposite ends of the block. Officers got out and started walking through the party, hands on belts, asking questions nobody was going to answer. {member} kept the crew calm and told everyone to stay cool. After forty minutes of harassment with nothing to show for it the officers left — but the mood never recovered.", "type": "police_harassment", "color": discord.Color.blue()},
    {"name": "Task Force Showed Up", "description": "Four unmarked cars and a van pulled up simultaneously from different directions — clearly planned. Task force officers in tactical gear moved through the crowd demanding ID, running names, pulling people aside. {member} got detained for two hours before being released without charges. Half the party left the moment the vans showed up.", "type": "police_raid", "color": discord.Color.blue()},
    {"name": "Police Arrested Several", "description": "Officers came through on foot shortly after dark and started running warrants on anyone they could stop. {member} watched helplessly as members of the crew got walked to patrol cars in front of the whole neighborhood — hands behind their backs, the block watching in silence. The party was over the moment the first set of cuffs came out.", "type": "police_arrests", "color": discord.Color.blue()},
    {"name": "Undercover in the Crowd", "description": "Two days after the block party, word came back through a lawyer that there had been undercover officers in the crowd the entire time taking photos and recording conversations. {member} hadn't noticed anything off. Everything said and seen that night was potentially documented. **{name}** went quiet immediately.", "type": "rep_down", "value": (30, 80), "color": discord.Color.orange()},
    {"name": "Fight Broke Out", "description": "An argument over something small escalated faster than anyone expected. {member} tried to step in but by then it had already spread to a full crowd brawl. Tables knocked over, food everywhere, people running. The block party became a crime scene. Took three days for people to start talking to **{name}** normally again.", "type": "rep_down", "value": (20, 60), "color": discord.Color.orange()},
    {"name": "Someone Got Stabbed", "description": "Nobody saw who did it or why but the ambulance showed up to **{name}**'s block party for someone who had been stabbed near the back of the crowd. {member} didn't know the victim or the situation but it didn't matter — the party was on their block, under their name, and the reputation damage was immediate.", "type": "rep_down", "value": (40, 100), "color": discord.Color.orange()},
    {"name": "Rain Killed the Vibe", "description": "It had been sunny all week and the forecast looked fine until it didn't. {member} had everything set up perfectly when the sky opened up an hour in. People scattered. The food got soaked. Equipment got damaged. **{name}** spent the money but the neighborhood barely got to enjoy it.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Turnout Was Low", "description": "The word got out and the setup was solid but people just didn't show up the way they were supposed to. {member} stood at a half-empty block for three hours wondering what went wrong. Maybe the timing was off. **{name}** put in the effort but the result was a quiet night instead of the statement they wanted to make.", "type": "nothing", "color": discord.Color.greyple()},
]

SOLO_WIN_LINES = [
    "{member} moved through the dark like he had been planning this for weeks. Found the opp alone outside a convenience store two blocks into enemy territory, waited until the moment was right, and handled it so clean that nobody in earshot flinched. Walked back to the block without a scratch and didn't say a word about it for three days.",
    "{member} tracked the target's routine for four days before making a move. Caught him at the worst possible moment — alone, no backup, no exit. The whole thing was over in under thirty seconds. The opp's set didn't even know what happened until the next morning.",
    "{member} went out solo against everyone's advice and came back with a body count that silenced every doubt. Crept in from the east side of the block where the cameras don't reach, handled the business that needed to be handled, and was back home before midnight like nothing happened.",
    "{member} didn't ask for permission and didn't wait for backup. Spotted an opportunity, took it, and executed it perfectly. One opp down, message sent, rep earned. The kind of move that gets talked about for years.",
    "There was a name that needed to be crossed off a list and {member} volunteered without hesitation. Moved alone through three enemy blocks, found the target, and made sure the message was unmistakable. The set's reputation grew three times that night from a single person's work.",
    "{member} set up the whole thing personally — scouted the location, timed the approach, picked the angle. When the moment came there was no hesitation, no second-guessing. The target never saw it coming. Solo. Clean. Permanent.",
]

SOLO_SURVIVED_LINES = [
    "{member} made it back but barely. Took a round to the arm on the way out that burned through muscle and bone. Wrapped it with a belt in the alley, bit down on nothing, and walked six blocks back to the hood in the dark. Alive but marked.",
    "{member} got made before the approach was complete. Had to run three blocks with shots landing behind him — one clipped the heel of his shoe, another grazed his collar. Made it over a fence and disappeared into a backyard. Sat in the dark for two hours before it was safe to move. Still breathing. Still standing.",
    "{member} took a hit to the ribs during the exchange that cracked something. Couldn't breathe right the whole way back. Refused to go to the hospital and sat in the trap house until the worst of it passed. The mission didn't go the way it was supposed to but {member} came home.",
    "The opp had backup that nobody knew about. {member} fought through two of them and made it out the side but caught a graze across the back of the neck in the process. An inch deeper and it would have been over. Crawled through a drainage ditch to lose them and emerged on the other side still moving.",
    "{member} walked into something bigger than expected. Outnumbered three to one with no exits, had to fight through it with nothing but instinct. Made it out with a broken hand, a split face, and a story that nobody who wasn't there would believe. Came back breathing. That counts.",
    "{member} got caught in the open and took a shot to the thigh. Went down, got back up, went down again, got back up again. Made it to an alley and tourniquet'd it with a shoelace. Two hours later was sitting on the block acting like it was a normal night. The set knew. Nobody asked questions.",
]

SOLO_JAILED_LINES = [
    "{member} handled the business clean but made one mistake on the way out — ran a red light four blocks from the scene with blood on the jacket. Officer pulled them over before they could think. Everything unraveled from that single traffic stop. Facing {sentence} and the lawyer isn't saying much that's encouraging.",
    "{member} didn't realize the area had been under surveillance for two weeks. The whole approach was on camera. Detectives had a name and a face before the sun came up the next morning. Got knocked at the crib at 6am with a warrant already signed. {sentence} — no bail set.",
    "A witness on the block got a clear look and called it in immediately. {member} was less than a mile away when the description went out over the radio. Three patrol units converged. {sentence} sentence and the DA is treating it as a priority case.",
    "{member} got back to the block and thought it was over. Two days later a task force unit knocked on the door with a folder full of evidence — photos, phone records, cell tower data. The case was already built. {sentence} and every motion the lawyer filed got denied.",
    "The opp's people knew who was responsible within an hour and passed the name directly to detectives. {member} was picked up at a family gathering the next afternoon in front of everyone. {sentence} — the set went silent the moment they heard.",
]

SOLO_KILLED_LINES = [
    "{member} went out alone and didn't come back. The details came through in pieces over the next few hours — went deep into enemy territory, got cut off, and took three shots before going down. The block held a vigil two nights later. Another name on the wall. Another empty spot in the set.",
    "{member} moved solo and ran into more than expected. Fought until there was nothing left to fight with. The body was found before morning. The set lost one of their own to a mission that wasn't supposed to go that way. The grief hit the whole crew at once.",
    "The opp's neighborhood was more locked down than anyone realized. {member} got spotted the moment they crossed the boundary and never made it to the target. Surrounded with no exit and no backup. The set found out through the streets. Took three days before anyone could talk about it without going quiet.",
    "{member} almost made it out. Was within two blocks of safety when they got cut off from behind. The shots came fast. By the time anyone could get there it was already over. The set buried one of their most fearless soldiers and the block hasn't been the same since.",
    "Going solo was the choice {member} made and the streets don't negotiate with that kind of courage. Made it to the target, handled the business, and caught three on the way out. Didn't make it back. The set carries that weight now. The name won't be forgotten.",
]

# ─────────────────────────────────────────────
# COMMAND HANDLERS
# ─────────────────────────────────────────────

async def handle_solo(message, args):
    if len(args) < 2:
        await message.channel.send("Usage: `solo <code> <member name>`\nExample: `solo XKRV Joker`")
        return

    code = args[0].upper()
    member_name = " ".join(args[1:])

    if code not in gangs:
        await message.channel.send(f"No crew found with code `{code}`.")
        return

    gang = gangs[code]
    if gang['owner_id'] != message.author.id:
        await message.channel.send("That ain't your crew.")
        return
    if not gang['alive']:
        await message.channel.send(f"**{gang['name']}** has been disbanded.")
        return

    target_member = None
    for m in gang['members']:
        if m['name'].lower() == member_name.lower():
            target_member = m
            break

    if target_member is None:
        roster = ", ".join([f"`{m['name']}`" for m in gang['members']])
        await message.channel.send(f"No member named `{member_name}` found in **{gang['name']}**.\nRoster: {roster}")
        return

    if not target_member['alive']:
        await message.channel.send(f"`{target_member['name']}` is dead. Can't send a dead man on a mission.")
        return

    now = time.time()
    if target_member.get('jail_until') and now < target_member['jail_until']:
        await message.channel.send(f"`{target_member['name']}` is locked up right now. They can't roll out until their sentence is done.")
        return

    enemy_gang_info = random.choice(LA_GANGS)
    enemy_rep = random.randint(10, 500)
    player_rep = gang['rep']

    rep_diff = player_rep - enemy_rep
    win_chance = 40 + int((rep_diff / 500) * 30)
    win_chance = max(10, min(75, win_chance))
    roll = random.randint(1, 100)

    send_off_lines = [
        f"`{target_member['name']}` told nobody where they were going. Grabbed what they needed, checked the clip, and walked out alone into the night. **{gang['name']}** wouldn't know the outcome until they came back — or didn't.",
        f"No crew. No backup. No plan B. `{target_member['name']}` moved out solo into **{enemy_gang_info['name']}** territory with one objective and nothing to lose.",
        f"`{target_member['name']}` had been sitting on this for days. Didn't say a word to anyone in **{gang['name']}**. Just made the decision, picked up, and went. Alone.",
        f"The rest of the set didn't even know `{target_member['name']}` had left until the door was already closed. Moving solo into **{enemy_gang_info['name']}** territory. No radio. No backup. Just the mission.",
    ]

    tags = evaluate_status(target_member)
    tag_str = "  ".join([f"[{t}]" for t in tags]) if tags else "--"

    intro_embed = discord.Embed(title="Solo Mission", description=random.choice(send_off_lines), color=discord.Color.dark_red())
    intro_embed.add_field(name="Soldier", value=f"`{target_member['name']}`", inline=True)
    intro_embed.add_field(name="Tags", value=tag_str, inline=True)
    intro_embed.add_field(name="Kills", value=str(target_member.get('kills', 0)), inline=True)
    intro_embed.add_field(name="Target Territory", value=f"{enemy_gang_info['name']} — {enemy_gang_info['hood']}", inline=False)
    intro_embed.set_footer(text="One man. No backup. Whatever happens next happens alone.")
    await message.channel.send(embed=intro_embed)
    await asyncio.sleep(3)

    old_kills = target_member.get('kills', 0)

    if roll <= win_chance:
        target_member['kills'] = old_kills + 1
        target_member['missions_survived'] = target_member.get('missions_survived', 0) + 1
        rep_gain = random.randint(15, 60)
        gang['rep'] = player_rep + rep_gain
        story = random.choice(SOLO_WIN_LINES).replace("{member}", f"`{target_member['name']}`")
        new_tags = evaluate_status(target_member)
        new_tag_str = "  ".join([f"[{t}]" for t in new_tags]) if new_tags else "--"

        result_embed = discord.Embed(title="Solo Mission — Target Down", description=story, color=discord.Color.green())
        result_embed.add_field(name="Soldier", value=f"`{target_member['name']}`", inline=True)
        result_embed.add_field(name="Tags", value=new_tag_str, inline=True)
        result_embed.add_field(name="Kills", value=str(target_member['kills']), inline=True)
        result_embed.add_field(name="Cred Gained", value=f"+{rep_gain}", inline=True)
        result_embed.add_field(name="New Street Cred", value=f"{player_rep} -> {gang['rep']}", inline=True)
        result_embed.set_footer(text="Solo work. The set eats off one man's courage tonight.")
        await message.channel.send(embed=result_embed)

    elif roll <= win_chance + 30:
        target_member['missions_survived'] = target_member.get('missions_survived', 0) + 1
        story = random.choice(SOLO_SURVIVED_LINES).replace("{member}", f"`{target_member['name']}`")
        rep_loss = random.randint(5, 25)
        gang['rep'] = max(1, player_rep - rep_loss)

        result_embed = discord.Embed(title="Solo Mission — Made It Back", description=story, color=discord.Color.orange())
        result_embed.add_field(name="Soldier", value=f"`{target_member['name']}`", inline=True)
        result_embed.add_field(name="Tags", value=tag_str, inline=True)
        result_embed.add_field(name="Kills", value=str(target_member.get('kills', 0)), inline=True)
        result_embed.add_field(name="Cred Lost", value=f"-{rep_loss}", inline=True)
        result_embed.add_field(name="New Street Cred", value=f"{player_rep} -> {gang['rep']}", inline=True)
        result_embed.set_footer(text="Came back alive. That has to count for something.")
        await message.channel.send(embed=result_embed)

    elif roll <= win_chance + 50:
        sentence = send_to_jail(target_member)
        story = random.choice(SOLO_JAILED_LINES).replace("{member}", f"`{target_member['name']}`").replace("{sentence}", sentence)
        rep_loss = random.randint(10, 35)
        gang['rep'] = max(1, player_rep - rep_loss)

        result_embed = discord.Embed(title="Solo Mission — Knocked", description=story, color=discord.Color.blue())
        result_embed.add_field(name="Soldier", value=f"`{target_member['name']}`", inline=True)
        result_embed.add_field(name="Tags", value=tag_str, inline=True)
        result_embed.add_field(name="Sentence", value=sentence, inline=True)
        result_embed.add_field(name="Cred Lost", value=f"-{rep_loss}", inline=True)
        result_embed.add_field(name="New Street Cred", value=f"{player_rep} -> {gang['rep']}", inline=True)
        result_embed.set_footer(text="One man down. The set carries on.")
        await message.channel.send(embed=result_embed)

    else:
        if len(get_alive_members(gang)) > 1:
            target_member['alive'] = False
            target_member['deaths'] = target_member.get('deaths', 0) + 1
            story = random.choice(SOLO_KILLED_LINES).replace("{member}", f"`{target_member['name']}`")
            rep_loss = random.randint(20, 60)
            gang['rep'] = max(1, player_rep - rep_loss)
            check_and_mark_dead(code)

            result_embed = discord.Embed(title="Solo Mission — Fallen", description=story, color=discord.Color.dark_grey())
            result_embed.add_field(name="Soldier", value=f"`{target_member['name']}`", inline=True)
            result_embed.add_field(name="Final Tags", value=tag_str, inline=True)
            result_embed.add_field(name="Kills", value=str(target_member.get('kills', 0)), inline=True)
            result_embed.add_field(name="Cred Lost", value=f"-{rep_loss}", inline=True)
            result_embed.add_field(name="New Street Cred", value=f"{player_rep} -> {gang['rep']}", inline=True)
            result_embed.add_field(name="Members Alive", value=str(len(get_alive_members(gang))), inline=True)
            result_embed.set_footer(text="The set lost a soldier tonight. That name stays on the wall.")
            await message.channel.send(embed=result_embed)
        else:
            sentence = send_to_jail(target_member)
            story = random.choice(SOLO_JAILED_LINES).replace("{member}", f"`{target_member['name']}`").replace("{sentence}", sentence)
            rep_loss = random.randint(10, 35)
            gang['rep'] = max(1, player_rep - rep_loss)

            result_embed = discord.Embed(title="Solo Mission — Knocked", description=story, color=discord.Color.blue())
            result_embed.add_field(name="Soldier", value=f"`{target_member['name']}`", inline=True)
            result_embed.add_field(name="Tags", value=tag_str, inline=True)
            result_embed.add_field(name="Sentence", value=sentence, inline=True)
            result_embed.add_field(name="Cred Lost", value=f"-{rep_loss}", inline=True)
            result_embed.add_field(name="New Street Cred", value=f"{player_rep} -> {gang['rep']}", inline=True)
            result_embed.set_footer(text="Last man standing is locked up. Hold it down until they're out.")
            await message.channel.send(embed=result_embed)


async def handle_block(message, args):
    if not args:
        await message.channel.send("Usage: `block <code>`\nExample: `block XKRV`")
        return

    code = args[0].upper()
    if code not in gangs:
        await message.channel.send(f"No crew found with code `{code}`.")
        return

    gang = gangs[code]
    if gang['owner_id'] != message.author.id:
        await message.channel.send("That ain't your crew.")
        return
    if not gang['alive']:
        await message.channel.send(f"**{gang['name']}** has been disbanded.")
        return

    free_members = get_free_members(gang)
    if not free_members:
        await message.channel.send(f"**{gang['name']}** has no free members to run the block party.")
        return

    host_member = random.choice(free_members)
    old_rep = gang['rep']

    setup_descriptions = [
        f"**{gang['name']}** is setting up on {gang['hood']}. `{host_member['name']}` is running point — speakers getting dragged out, tables going up, word spreading through the block that tonight is the night.",
        f"`{host_member['name']}` has been planning this for a week. Tables, food, music — everything is going up on the block right now. **{gang['name']}** is about to show the hood what they're really about.",
        f"The whole crew is outside setting up for the **{gang['name']}** block party. `{host_member['name']}` is directing everything — where the speakers go, where the food tables go, who is on what corner keeping watch.",
        f"**{gang['name']}** shut down the block for the night. `{host_member['name']}` called it three days ago and made it happen — food ordered, music lined up, the whole hood invited. People are already starting to gather.",
    ]

    setup_embed = discord.Embed(title="Block Party", description=random.choice(setup_descriptions), color=discord.Color.dark_gold())
    setup_embed.add_field(name="Hood", value=gang['hood'], inline=True)
    setup_embed.add_field(name="Host", value=f"`{host_member['name']}`", inline=True)
    setup_embed.add_field(name="Street Cred", value=str(old_rep), inline=True)
    setup_embed.set_footer(text="The block is live...")
    await message.channel.send(embed=setup_embed)
    await asyncio.sleep(2)

    num_events = random.randint(2, 4)
    rep_change = 0
    members_jailed = []
    members_killed = []

    for i in range(num_events):
        await asyncio.sleep(2)
        current_free = get_free_members(gang)
        featured = random.choice(current_free) if current_free else host_member
        event = random.choice(BLOCK_PARTY_EVENTS)
        desc = event['description'].replace("{member}", f"`{featured['name']}`").replace("{name}", gang['name'])

        event_embed = discord.Embed(title=event['name'], description=desc, color=event['color'])
        extra_lines = []

        if event['type'] == 'rep_up':
            gain = random.randint(*event['value'])
            rep_change += gain
            featured['missions_survived'] = featured.get('missions_survived', 0) + 1
            event_embed.add_field(name="Cred", value=f"+{gain}", inline=True)

        elif event['type'] == 'rep_down':
            loss = random.randint(*event['value'])
            rep_change -= loss
            if event.get('snitch'):
                featured['times_snitched'] = featured.get('times_snitched', 0) + 1
            event_embed.add_field(name="Cred", value=f"-{loss}", inline=True)

        elif event['type'] == 'driveby':
            rival = random.choice(LA_GANGS)
            rival_rep = random.randint(50, 400)
            killer_name = random.choice(STREET_NAMES)
            loss = random.randint(40, 120)
            rep_change -= loss
            alive_now = get_alive_members(gang)
            if len(alive_now) > 1:
                num_victims = min(random.randint(1, 2), len(alive_now) - 1)
                victims = random.sample(alive_now, k=num_victims)
                for v in victims:
                    v['alive'] = False
                    v['deaths'] = v.get('deaths', 0) + 1
                    members_killed.append(v['name'])
                    extra_lines.append(f"`{v['name']}` was hit and didn't make it.")
            add_revenge_target(gang, killer_name, rival, rival_rep)
            event_embed.add_field(name="Cred", value=f"-{loss}", inline=True)
            event_embed.add_field(name="Responsible", value=f"**{rival['name']}** — `{killer_name}` pulled the trigger", inline=False)
            if extra_lines:
                event_embed.add_field(name="Fallen", value="\n".join(extra_lines), inline=False)
            event_embed.set_footer(text=f"Blood owed. Type `revenge {code}` to see your targets.")

        elif event['type'] == 'brawl':
            rival = random.choice(LA_GANGS)
            rival_rep = random.randint(30, 300)
            crasher_name = random.choice(STREET_NAMES)
            loss = random.randint(20, 70)
            rep_change -= loss
            current_free2 = get_free_members(gang)
            if current_free2 and random.randint(1, 100) <= 40:
                victim = random.choice(current_free2)
                sentence = send_to_jail(victim)
                members_jailed.append((victim['name'], sentence))
                extra_lines.append(f"`{victim['name']}` got knocked during the brawl — {sentence}.")
            add_revenge_target(gang, crasher_name, rival, rival_rep)
            event_embed.add_field(name="Cred", value=f"-{loss}", inline=True)
            event_embed.add_field(name="Who Crashed It", value=f"**{rival['name']}** — `{crasher_name}` led the charge", inline=False)
            if extra_lines:
                event_embed.add_field(name="Locked Up", value="\n".join(extra_lines), inline=False)
            event_embed.set_footer(text=f"They came to your party and disrespected. Type `revenge {code}` to handle it.")

        elif event['type'] == 'police_harassment':
            loss = random.randint(10, 40)
            rep_change -= loss
            event_embed.add_field(name="Cred", value=f"-{loss}", inline=True)

        elif event['type'] == 'police_raid':
            loss = random.randint(30, 80)
            rep_change -= loss
            current_free3 = get_free_members(gang)
            if current_free3:
                num_arrested = min(random.randint(1, 2), len(current_free3))
                arrested = random.sample(current_free3, k=num_arrested)
                for a in arrested:
                    sentence = send_to_jail(a)
                    members_jailed.append((a['name'], sentence))
                    extra_lines.append(f"`{a['name']}` got taken in — {sentence}.")
            event_embed.add_field(name="Cred", value=f"-{loss}", inline=True)
            if extra_lines:
                event_embed.add_field(name="Locked Up", value="\n".join(extra_lines), inline=False)

        elif event['type'] == 'police_arrests':
            loss = random.randint(20, 60)
            rep_change -= loss
            current_free4 = get_free_members(gang)
            if current_free4:
                num_arrested = min(random.randint(1, 3), len(current_free4))
                arrested = random.sample(current_free4, k=num_arrested)
                for a in arrested:
                    sentence = send_to_jail(a)
                    members_jailed.append((a['name'], sentence))
                    extra_lines.append(f"`{a['name']}` walked to the car in cuffs — {sentence}.")
            event_embed.add_field(name="Cred", value=f"-{loss}", inline=True)
            if extra_lines:
                event_embed.add_field(name="Locked Up", value="\n".join(extra_lines), inline=False)

        elif event['type'] == 'nothing':
            event_embed.add_field(name="Cred", value="No change", inline=True)

        if not event_embed.footer.text or event_embed.footer.text == discord.Embed.Empty:
            event_embed.set_footer(text=f"Event {i + 1} of {num_events}")
        await message.channel.send(embed=event_embed)

    gang['rep'] = max(1, gang['rep'] + rep_change)
    new_rep = gang['rep']
    check_and_mark_dead(code)
    await asyncio.sleep(2)

    summary_color = discord.Color.green() if rep_change >= 0 else discord.Color.orange()
    footer = ("The hood is talking. That party put the set on a different level." if rep_change >= 80 else "Night is over. The block is quiet now.") if rep_change >= 0 else "The party is over. Not the way anyone wanted it to end."
    rep_display = f"{old_rep} -> {new_rep} (+{rep_change})" if rep_change >= 0 else f"{old_rep} -> {new_rep} ({rep_change})"

    summary_embed = discord.Embed(title="Block Party — Night Done", description=f"The **{gang['name']}** block party on {gang['hood']} is wrapped up. Here is the final count.", color=summary_color)
    summary_embed.add_field(name="Street Cred", value=rep_display, inline=False)
    summary_embed.add_field(name="Members Alive", value=str(len(get_alive_members(gang))), inline=True)
    summary_embed.add_field(name="Members Free", value=str(len(get_free_members(gang))), inline=True)
    if members_killed:
        summary_embed.add_field(name="Fallen Tonight", value="\n".join([f"`{n}`" for n in members_killed]), inline=False)
    if members_jailed:
        summary_embed.add_field(name="Locked Up Tonight", value="\n".join([f"`{name}` — {sentence}" for name, sentence in members_jailed]), inline=False)

    all_targets = get_revenge_targets(gang)
    if all_targets:
        summary_embed.add_field(name="Blood Owed", value="\n".join([f"**{t['gang']}** — `{t['name']}`" for t in all_targets]), inline=False)
        summary_embed.add_field(name="\u200b", value=f"Type `revenge {code}` to choose who to go after.", inline=False)

    summary_embed.set_footer(text=footer)
    await message.channel.send(embed=summary_embed)


async def handle_gang(message, args):
    user_id = message.author.id
    if not is_admin(message):
        if user_has_active_gang(user_id):
            await message.channel.send("You already got a crew running. Type `show` to see them.")
            return

    la_gang = random.choice(LA_GANGS)
    code = generate_code()
    rep = random.randint(10, 100)
    members = generate_ai_members(random.randint(4, 7))

    gangs[code] = {
        "name": la_gang["name"],
        "hood": la_gang["hood"],
        "leader": members[0]['name'],
        "rep": rep,
        "owner_id": user_id,
        "owner_name": message.author.name,
        "code": code,
        "alive": True,
        "fights_won": 0,
        "fights_lost": 0,
        "members": members,
        "revenge_targets": [],
    }

    if not is_admin(message):
        active_gang_owners.add(user_id)

    member_lines = "\n".join([f"`{m['name']}`" for m in members])
    embed = discord.Embed(title="You're In", description=f"You just got put on with **{la_gang['name']}**.", color=discord.Color.dark_grey())
    embed.add_field(name="Hood", value=la_gang["hood"], inline=True)
    embed.add_field(name="Shot Caller", value=f"`{members[0]['name']}`", inline=True)
    embed.add_field(name="Street Cred", value=str(rep), inline=True)
    embed.add_field(name="Members", value=str(len(members)), inline=True)
    embed.add_field(name="Code", value=f"`{code}`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Crew", value=member_lines, inline=False)
    embed.set_footer(text="Type: mission <code> | slide <code> <number> | recruit <code> | revenge <code> | block <code> | solo <code> <name> | show")
    await message.channel.send(embed=embed)


async def handle_show(message, args):
    user_id = message.author.id
    user_gangs = [g for g in gangs.values() if g['owner_id'] == user_id]

    if not user_gangs:
        await message.channel.send("You got no crew. Type `gang` to start one.")
        return

    alive = [g for g in user_gangs if g['alive']]
    dead_count = len(user_gangs) - len(alive)

    embed = discord.Embed(
        title=f"{message.author.name}'s Crew",
        description=f"Active: {len(alive)}   |   Disbanded: {dead_count}",
        color=discord.Color.dark_grey()
    )

    if alive:
        for g in alive:
            fights_won = g.get('fights_won', 0)
            fights_lost = g.get('fights_lost', 0)
            total = fights_won + fights_lost
            win_rate = f"{int((fights_won / total) * 100)}%" if total > 0 else "N/A"
            targets = get_revenge_targets(g)

            stats_lines = [
                f"Hood: {g.get('hood', 'Unknown')}",
                f"Code: `{g['code']}`",
                f"Shot Caller: `{g.get('leader', 'Unknown')}`",
                f"Street Cred: {g['rep']}",
                f"Record: {fights_won}W — {fights_lost}L   |   Win Rate: {win_rate}",
                f"Kills: {get_gang_bodies(g)}   |   Deaths: {get_gang_deaths(g)}",
                f"Alive: {len(get_alive_members(g))}   |   Free: {len(get_free_members(g))}",
            ]
            if targets:
                for t in targets:
                    stats_lines.append(f"Blood Owed: `{t['name']}` — {t['gang']}")

            embed.add_field(name=g['name'], value="\n".join(stats_lines), inline=False)
            embed.add_field(name="Roster", value=format_member_list(g['members']), inline=False)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
    else:
        embed.add_field(name="No Active Crew", value="Your crew got disbanded. Type `gang` to start fresh.", inline=False)

    embed.set_footer(text="Type: mission <code> | slide <code> <number> | recruit <code> | revenge <code> | block <code> | solo <code> <name> | show")
    await message.channel.send(embed=embed)


async def handle_mission(message, args):
    if not args:
        await message.channel.send("Usage: `mission <code>`\nExample: `mission XKRV`")
        return

    code = args[0].upper()
    if code not in gangs:
        await message.channel.send(f"No crew found with code `{code}`.")
        return

    gang = gangs[code]
    if gang['owner_id'] != message.author.id:
        await message.channel.send("That ain't your crew.")
        return
    if not gang['alive']:
        await message.channel.send(f"**{gang['name']}** has been disbanded.")
        return

    free_members = get_free_members(gang)
    if not free_members:
        await message.channel.send(f"**{gang['name']}** has no free members right now. Everyone is locked up or dead.")
        return

    featured_member = random.choice(free_members)
    event = random.choices(EVENTS, weights=EVENT_WEIGHTS, k=1)[0]
    rep = gang['rep']
    old_kills = featured_member.get('kills', 0)
    tags = evaluate_status(featured_member)
    tag_str = "  ".join([f"[{t}]" for t in tags]) if tags else "--"

    embed = discord.Embed(
        title=event['name'],
        description=event['description'].format(name=gang['name'], member=f"`{featured_member['name']}`"),
        color=event['color']
    )
    embed.add_field(name="Crew", value=gang['name'], inline=True)
    embed.add_field(name="Member", value=f"`{featured_member['name']}`", inline=True)
    embed.add_field(name="Tags", value=tag_str, inline=True)

    if event['type'] == 'rep_up':
        gain = random.randint(*event['value'])
        gang['rep'] = rep + gain
        featured_member['missions_survived'] = featured_member.get('missions_survived', 0) + 1
        if random.randint(1, 100) <= 20:
            featured_member['kills'] = old_kills + 1
            embed.add_field(name="Kill", value=f"`{featured_member['name']}` +1", inline=True)
        embed.add_field(name="Street Cred", value=f"{rep} -> {gang['rep']} (+{gain})", inline=True)
        updated_tags = evaluate_status(featured_member)
        embed.add_field(name="Updated Tags", value="  ".join([f"[{t}]" for t in updated_tags]) if updated_tags else "--", inline=True)
        embed.set_footer(text="Rep rising on the streets...")

    elif event['type'] == 'rep_down':
        loss = random.randint(*event['value'])
        new_rep = max(1, rep - loss)
        actual_loss = rep - new_rep
        gang['rep'] = new_rep
        if event.get('snitch'):
            featured_member['times_snitched'] = featured_member.get('times_snitched', 0) + 1
        extra_info = []
        if random.randint(1, 100) <= 15 and len(get_alive_members(gang)) > 1:
            featured_member['alive'] = False
            featured_member['deaths'] = featured_member.get('deaths', 0) + 1
            extra_info.append(f"`{featured_member['name']}` didn't make it out — body found two blocks away")
        elif random.randint(1, 100) <= 25:
            sentence = send_to_jail(featured_member)
            extra_info.append(f"`{featured_member['name']}` got knocked and is facing {sentence}")
        if extra_info:
            embed.add_field(name="What Happened", value="\n".join(extra_info), inline=False)
        embed.add_field(name="Street Cred", value=f"{rep} -> {gang['rep']} (-{actual_loss})", inline=True)
        updated_tags = evaluate_status(featured_member)
        embed.add_field(name="Updated Tags", value="  ".join([f"[{t}]" for t in updated_tags]) if updated_tags else "--", inline=True)
        embed.set_footer(text="Taking an L on the streets...")

    elif event['type'] == 'nothing':
        embed.add_field(name="Street Cred", value=str(rep), inline=True)
        embed.set_footer(text="Nothing popped off tonight.")

    await message.channel.send(embed=embed)


async def handle_recruit(message, args):
    if not args:
        await message.channel.send("Usage: `recruit <code>`\nExample: `recruit XKRV`")
        return

    code = args[0].upper()
    if code not in gangs:
        await message.channel.send(f"No crew found with code `{code}`.")
        return

    gang = gangs[code]
    if gang['owner_id'] != message.author.id:
        await message.channel.send("That ain't your crew.")
        return
    if not gang['alive']:
        await message.channel.send(f"**{gang['name']}** has been disbanded.")
        return

    existing_names = {m['name'] for m in gang['members']}
    available = [n for n in STREET_NAMES if n not in existing_names]

    if not available:
        await message.channel.send(f"**{gang['name']}** roster is already full.")
        return

    if random.randint(1, 2) == 1:
        new_name = random.choice(available)
        new_member = {
            "name": new_name,
            "rep": random.randint(10, 150),
            "alive": True,
            "kills": 0,
            "deaths": 0,
            "times_jailed": 0,
            "times_snitched": 0,
            "missions_survived": 0,
            "came_back_from_zero": False,
            "jail_until": None,
            "jail_sentence": None,
        }
        gang['members'].append(new_member)
        descriptions = [
            f"**`{new_name}`** had been hanging around the block for weeks watching how **{gang['name']}** moved. Finally pulled them aside, looked them in the eye, and put them on. They didn't hesitate.",
            f"Word got to **`{new_name}`** through a mutual that **{gang['name']}** was looking. They showed up the next day ready to work. No questions, no hesitation — just loyalty.",
            f"**`{new_name}`** proved themselves during a situation last month that nobody forgot. After that, the decision to put them on with **{gang['name']}** was unanimous.",
            f"**`{new_name}`** grew up two blocks over and always had love for **{gang['name']}**. When the invitation finally came, they were ready — had been ready for a long time.",
        ]
        embed = discord.Embed(title="New Member", description=random.choice(descriptions), color=discord.Color.teal())
        embed.add_field(name="Gang", value=gang['name'], inline=True)
        embed.add_field(name="New Member", value=f"`{new_name}`", inline=True)
        embed.add_field(name="Total Members", value=str(len(get_alive_members(gang))), inline=True)
        embed.set_footer(text="Keep building the set.")
    else:
        descriptions = [
            f"**{gang['name']}** put the word out through three different people but nobody came through. Either the timing is wrong or the streets aren't feeling it right now. Try again.",
            f"There was a candidate — seemed solid, seemed interested. Then they just stopped answering. **{gang['name']}** can't afford dead weight anyway. Try again.",
            f"The recruitment process hit a wall. People are either already committed elsewhere or they're too scared to make the move. The set needs to keep pushing.",
            f"Word didn't travel the way it needed to. **{gang['name']}** is out there but not everyone is ready to step up. The right one is out there somewhere.",
        ]
        embed = discord.Embed(title="Nobody Came Through", description=random.choice(descriptions), color=discord.Color.dark_grey())
        embed.add_field(name="Gang", value=gang['name'], inline=True)
        embed.add_field(name="Members", value=str(len(get_alive_members(gang))), inline=True)
        embed.set_footer(text="50/50. Try again.")

    await message.channel.send(embed=embed)


async def handle_slide(message, args):
    # Usage: slide <code> <number>
    # number = how many members roll out (1 to however many are free, capped at 10)
    if len(args) < 2:
        await message.channel.send(
            "Usage: `slide <code> <number>`\n"
            "Number is how many members roll out.\n"
            "Example: `slide XKRV 3`"
        )
        return

    code = args[0].upper()
    if code not in gangs:
        await message.channel.send(f"No crew found with code `{code}`.")
        return

    gang = gangs[code]
    if gang['owner_id'] != message.author.id:
        await message.channel.send("That ain't your crew.")
        return
    if not gang['alive']:
        await message.channel.send(f"**{gang['name']}** has been disbanded.")
        return

    try:
        requested_count = int(args[1])
    except ValueError:
        await message.channel.send("The number needs to be a whole number. Example: `slide XKRV 3`")
        return

    if requested_count < 1:
        await message.channel.send("You need to send at least 1 person.")
        return

    free_members = get_free_members(gang)
    if not free_members:
        await message.channel.send(f"**{gang['name']}** has nobody free to roll out right now.")
        return

    # Cap at however many are actually free, max 10
    actual_count = min(requested_count, len(free_members), 10)
    if actual_count < requested_count:
        await message.channel.send(
            f"Only {len(free_members)} members are free right now. Rolling with {actual_count}."
        )

    rolling_members = random.sample(free_members, actual_count)

    enemy_gang_info = random.choice(LA_GANGS)
    enemy_members = generate_ai_members(random.randint(1, max(1, actual_count)))
    enemy_rep = random.randint(10, 500)
    player_rep = gang['rep']

    slide_intros = [
        f"**{gang['name']}** got word that **{enemy_gang_info['name']}** has been running their mouth. Time to pull up and make it clear.",
        f"**{enemy_gang_info['name']}** crossed a line they can't uncross. **{gang['name']}** is loading up and heading out.",
        f"The disrespect from **{enemy_gang_info['name']}** has been building for weeks. Tonight **{gang['name']}** settles it.",
        f"**{gang['name']}** got intel on where **{enemy_gang_info['name']}** is posted. The crew is rolling out right now.",
    ]

    rolling_display = "\n".join([f"`{m['name']}`" for m in rolling_members])
    enemy_display = "\n".join([f"`{m['name']}`" for m in enemy_members])

    intro_embed = discord.Embed(title="Slide", description=random.choice(slide_intros), color=discord.Color.dark_red())
    intro_embed.add_field(name=gang['name'], value=f"Cred: {player_rep}\nRolling {actual_count} deep\n\n{rolling_display}", inline=True)
    intro_embed.add_field(name="VS", value="\u200b", inline=True)
    intro_embed.add_field(name=enemy_gang_info['name'], value=f"Cred: {enemy_rep}\n\n{enemy_display}", inline=True)
    intro_embed.set_footer(text="It's on...")
    await message.channel.send(embed=intro_embed)

    alive_before = set(m['name'] for m in get_alive_members(gang))
    result = calculate_slide_outcome(gang, rolling_members, enemy_rep)
    alive_after = set(m['name'] for m in get_alive_members(gang))

    if alive_before - alive_after:
        add_revenge_target(gang, random.choice([m['name'] for m in enemy_members]), enemy_gang_info, enemy_rep)

    check_and_mark_dead(code)
    await asyncio.sleep(3)
    await send_slide_result(message.channel, gang, enemy_gang_info, result)


async def handle_revenge(message, args):
    if not args:
        await message.channel.send("Usage: `revenge <code>`\nExample: `revenge XKRV`")
        return

    code = args[0].upper()
    if code not in gangs:
        await message.channel.send(f"No crew found with code `{code}`.")
        return

    gang = gangs[code]
    if gang['owner_id'] != message.author.id:
        await message.channel.send("That ain't your crew.")
        return
    if not gang['alive']:
        await message.channel.send(f"**{gang['name']}** has been disbanded.")
        return

    targets = get_revenge_targets(gang)
    if not targets:
        await message.channel.send(f"**{gang['name']}** has no blood owed right now. Nobody has taken one of yours.")
        return

    free_members = get_free_members(gang)
    if not free_members:
        await message.channel.send(f"**{gang['name']}** has nobody free to roll out for revenge right now.")
        return

    last_killer = random.choice(targets)
    enemy_gang_info = last_killer['gang_info']
    enemy_rep = last_killer.get('enemy_rep', random.randint(10, 500))
    enemy_members = generate_ai_members(random.randint(2, 4))
    player_rep = gang['rep']

    max_rollers = min(3, len(free_members))
    rolling_members = random.sample(free_members, random.randint(1, max_rollers))

    rolling_display = "\n".join([f"`{m['name']}`" for m in rolling_members])
    enemy_display = "\n".join([f"`{m['name']}`" for m in enemy_members])

    revenge_intros = [
        f"**{gang['name']}** hasn't slept right since they lost one of their own. Tonight they found out where **{enemy_gang_info['name']}** is posted and the crew is moving with one thing in mind.",
        f"The grief turned to fire. **{gang['name']}** has been watching, waiting, and planning. They know exactly where **{enemy_gang_info['name']}** will be tonight and they're not going empty handed.",
        f"There is only one thing on **{gang['name']}**'s mind right now. The fallen deserve to be honored. **{enemy_gang_info['name']}** is about to feel exactly what they caused.",
        f"**{gang['name']}** went quiet for a week — no moves, no noise, just planning. Tonight that silence ends. They're pulling up on **{enemy_gang_info['name']}** and they're not leaving until the debt is paid.",
    ]

    intro_embed = discord.Embed(title="Revenge", description=random.choice(revenge_intros), color=discord.Color.dark_red())
    intro_embed.add_field(name=gang['name'], value=f"Cred: {player_rep}\nRolling {len(rolling_members)} deep\n\n{rolling_display}", inline=True)
    intro_embed.add_field(name="VS", value="\u200b", inline=True)
    intro_embed.add_field(name=enemy_gang_info['name'], value=f"Cred: {enemy_rep}\n\n{enemy_display}", inline=True)
    intro_embed.add_field(name="Target Tonight", value=f"`{last_killer['name']}` of **{enemy_gang_info['name']}**", inline=False)

    remaining_before = [t for t in targets if t['gang'] != enemy_gang_info['name']]
    if remaining_before:
        intro_embed.add_field(name="Still Owed After This", value="\n".join([f"**{t['gang']}** — `{t['name']}`" for t in remaining_before]), inline=False)

    intro_embed.set_footer(text="This one is personal...")
    await message.channel.send(embed=intro_embed)

    alive_before = set(m['name'] for m in get_alive_members(gang))
    result = calculate_slide_outcome(gang, rolling_members, enemy_rep, is_revenge=True)
    alive_after = set(m['name'] for m in get_alive_members(gang))

    if result['won']:
        remove_revenge_target(gang, enemy_gang_info['name'])
    elif alive_before - alive_after:
        add_revenge_target(gang, random.choice([m['name'] for m in enemy_members]), enemy_gang_info, enemy_rep)

    check_and_mark_dead(code)
    await asyncio.sleep(3)
    await send_slide_result(message.channel, gang, enemy_gang_info, result, is_revenge=True)

    remaining_targets = get_revenge_targets(gang)
    if remaining_targets:
        followup = discord.Embed(title="Blood Still Owed", description=f"**{gang['name']}** still has debts to collect.", color=discord.Color.dark_red())
        for t in remaining_targets:
            followup.add_field(name=t['gang'], value=f"`{t['name']}`", inline=True)
        followup.set_footer(text=f"Type `revenge {code}` again to go after another one.")
        await message.channel.send(embed=followup)


# ─────────────────────────────────────────────
# BOT EVENTS
# ─────────────────────────────────────────────

COMMANDS = {
    "gang": handle_gang,
    "show": handle_show,
    "mission": handle_mission,
    "slide": handle_slide,
    "recruit": handle_recruit,
    "revenge": handle_revenge,
    "block": handle_block,
    "solo": handle_solo,
}


@bot.event
async def on_ready():
    print(f'{bot.user} is online')


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.guild is None:
        await message.channel.send("Commands can only be used in servers, not DMs.")
        return

    content = message.content.strip()
    parts = content.split()
    if not parts:
        return

    cmd = parts[0].lower()
    args = parts[1:]

    if cmd in COMMANDS:
        await COMMANDS[cmd](message, args)


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env")
    else:
        keep_alive()
        bot.run(TOKEN)
