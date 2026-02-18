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

gangs = {}
active_gang_owners = set()

STREET_NAMES = [
    "Joker", "Puppet", "Casper", "Looney", "Sleepy", "Smiley", "Boxer",
    "Psycho", "Creeper", "Scrappy", "Stomper", "Trigger", "Cartoon",
    "Termite", "Drowsy", "Spanky", "Grumpy", "Mugsy", "Sniper", "Crazy",
    "Silent", "Savage", "Naughty", "Pnut", "Sinner", "Danger", "Vicious",
    "Bandit", "Sinister", "Diablo", "Capone", "Scarface", "Hitman",
    "Shadow", "Travieso", "Coyote", "Terminator", "Speedy", "Ghost",
    "Mosco", "Huero", "Wino", "Payaso", "Pelon", "Chato", "Chico",
    "Chino", "Chuco", "Chuey", "Loco", "Paco", "Cuco", "Kiko", "Neto",
    "Memo", "Tavo", "Pollo", "Gallo", "Guero", "Wero", "Moco", "Mondo",
    "Indio", "Primo", "Cisco", "Dolo", "Kilo", "Trey", "Ocho", "Flaco",
    "Gordo", "Lobo", "Puma", "Tigre", "Cobra", "Halcon", "Aguila",
    "Vibora", "Cuervo", "Pantera", "Leon", "Tiburon", "Falcon", "Mamba",
    "Viper", "Rattler", "Jaguar", "Oso", "Gato", "Toro", "Zorro",
    "Menace", "Havoc", "Chaos", "Reckless", "Outlaw", "Rebel", "Bruiser",
    "Crusher", "Razor", "Blade", "Hammer", "Spike", "Brawler", "Slugger",
    "Mauler", "Grimey", "Murk", "Smoky", "Bones", "Skull", "Blaze",
    "Ember", "Scorch", "Flare", "Toxic", "Plague", "Blackout", "Ambush",
    "Warden", "Feral", "Rabid", "Predator", "Apex", "Titan", "Sledge",
    "Purge", "Scar", "Bounty", "Felony", "Breach", "Choke", "Silence",
    "Whisper", "Wraith", "Phantom", "Venom", "Vulture", "Rogue", "Ronin",
    "Specter", "Enforcer", "Kingpin", "Dagger", "Stiletto", "Shiv",
    "Grimm", "Ranger", "Warlock", "Warlord", "Nero", "Brutus", "Maximus",
    "Atlas", "Onyx", "Flint", "Cinder", "Colt", "Draco", "Mako", "Rook",
    "Demon", "Blanco", "Bruno", "Damian", "Dario", "Diego", "Domingo",
    "Fabian", "Felix", "Fidel", "Frankie", "Freddy", "Gabriel", "Gerardo",
    "Giovani", "Gus", "Hugo", "Ivan", "Javier", "Joey", "Johnny",
    "Junior", "Lazaro", "Louie", "Lucas", "Luciano", "Manny", "Marco",
    "Mauricio", "Mijo", "Mundo", "Nacho", "Nando", "Noel", "Octavio",
    "Omar", "Orlando", "Osvaldo", "Pedro", "Pepe", "Quico", "Rafael",
    "Ramon", "Raul", "Rico", "Rolo", "Roman", "Romeo", "Ruben", "Rudy",
    "Sammy", "Santos", "Saul", "Sergio", "Tito", "Tony", "Torres",
    "Ulises", "Valdez", "Valentino", "Vicente", "Xolo", "Yogi",
    "Navarro", "Montoya", "Fuentes", "Delgado", "Salazar", "Mendez",
    "Ibarra", "Pacheco", "Cisneros", "Trujillo", "Becerra", "Bernal",
    "Ybarra", "Contreras", "Tapia", "Ornelas", "Renteria", "Chairez",
    "Quinones", "Escobar", "Camilo", "Clemente", "Bernardo", "Baltazar",
    "Armando", "Alfredo", "Alejandro", "Andres", "Antonio", "Arturo",
    "Emilio", "Enrique", "Ernesto", "Esteban", "Eduardo", "Efren",
    "Fernando", "Felipe", "Hector", "Ignacio", "Jesus", "Jorge", "Jose",
    "Juan", "Julio", "Leonardo", "Lorenzo", "Luis", "Mario", "Miguel",
    "Oscar", "Pablo", "Ricardo", "Roberto", "Rodrigo", "Salvador",
    "Santiago", "Victor", "Xavier",
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
    {"name": "Diamond Street Locos", "hood": "Silver Lake, LA"},
    {"name": "Mara Salvatrucha Westside", "hood": "Westside, LA"},
    {"name": "Rockwood Street Locos", "hood": "Echo Park, LA"},
    {"name": "Glendale Locos 13", "hood": "Glendale, LA"},
    {"name": "Azusa 13", "hood": "Azusa, LA"},
    {"name": "Norwalk Locos 13", "hood": "Norwalk, LA"},
    {"name": "Whittier Varrio Locos", "hood": "Whittier, LA"},
    {"name": "South Gate Locos", "hood": "South Gate, LA"},
    {"name": "Lynwood Bloods", "hood": "Lynwood, LA"},
    {"name": "Paramount Locos 13", "hood": "Paramount, LA"},
    {"name": "Carson Crips", "hood": "Carson, LA"},
    {"name": "Varrio Carson 13", "hood": "Carson, LA"},
    {"name": "Varrio Wilmington 13", "hood": "Wilmington, LA"},
    {"name": "Eastside Longos", "hood": "Long Beach, LA"},
    {"name": "West Side Longos", "hood": "Long Beach, LA"},
    {"name": "Insane Long Beach Crips", "hood": "Long Beach, LA"},
    {"name": "Sons of Samoa", "hood": "Carson, LA"},
    {"name": "Hawthorne Piru", "hood": "Hawthorne, LA"},
    {"name": "Lawndale Bloods", "hood": "Lawndale, LA"},
    {"name": "Gardena Shotgun Crips", "hood": "Gardena, LA"},
    {"name": "Inglewood Crips", "hood": "Inglewood, LA"},
    {"name": "Queen Street Bloods", "hood": "Inglewood, LA"},
    {"name": "Black P Stone Jungles", "hood": "Hyde Park, LA"},
    {"name": "Jungle Boys", "hood": "Baldwin Hills, LA"},
    {"name": "Westside Piru", "hood": "Compton, LA"},
    {"name": "Eastside Pomona Crips", "hood": "Pomona, LA"},
    {"name": "Pomona Varrio 12", "hood": "Pomona, LA"},
    {"name": "Montebello Park Gang", "hood": "Montebello, LA"},
    {"name": "Barrio El Sereno", "hood": "El Sereno, LA"},
    {"name": "Pico Viejo Locos", "hood": "Pico-Union, LA"},
    {"name": "Mid City Stoners 13", "hood": "Mid-City, LA"},
    {"name": "Malditos 13", "hood": "Lincoln Heights, LA"},
    {"name": "Lincoln Heights Locos", "hood": "Lincoln Heights, LA"},
    {"name": "Eastside Clover", "hood": "Glassel Park, LA"},
    {"name": "Cypress Park Locos", "hood": "Cypress Park, LA"},
    {"name": "Highland Park Gang", "hood": "Highland Park, LA"},
    {"name": "San Fer 13", "hood": "San Fernando, LA"},
    {"name": "Sylmar Locotes", "hood": "Sylmar, LA"},
    {"name": "North Hollywood Locos", "hood": "North Hollywood, LA"},
    {"name": "Barrio Van Nuys Locos", "hood": "Van Nuys, LA"},
]

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

MSG_DELAY = 2.1

# Helpers

def is_admin(message):
    return isinstance(message.author, discord.Member) and message.author.guild_permissions.administrator

def user_has_active_gang(user_id):
    return any(g['owner_id'] == user_id and g['alive'] for g in gangs.values())

def generate_code():
    while True:
        code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
        if code not in gangs:
            return code

def make_member(name):
    return {
        "name": name, "alive": True, "kills": 0, "deaths": 0,
        "times_jailed": 0, "times_snitched": 0, "missions_survived": 0,
        "jail_until": None, "jail_sentence": None,
    }

def generate_ai_members(count=5):
    names = random.sample(STREET_NAMES, min(count, len(STREET_NAMES)))
    return [make_member(n) for n in names]

def get_alive_members(gang):
    return [m for m in gang['members'] if m['alive']]

def get_dead_members(gang):
    return [m for m in gang['members'] if not m['alive']]

def is_jailed(member):
    if not member.get('jail_until'):
        return False
    try:
        return float(member['jail_until']) > time.time()
    except (TypeError, ValueError):
        return False

def get_free_members(gang):
    return [m for m in gang['members'] if m['alive'] and not is_jailed(m)]

def get_jailed_members(gang):
    return [m for m in gang['members'] if m['alive'] and is_jailed(m)]

def get_gang_bodies(gang):
    return sum(m['kills'] for m in gang['members'])

def get_gang_deaths(gang):
    return sum(m['deaths'] for m in gang['members'])

def check_and_mark_dead(code):
    gang = gangs[code]
    if not get_alive_members(gang):
        gang['alive'] = False
        if not user_has_active_gang(gang['owner_id']):
            active_gang_owners.discard(gang['owner_id'])

def send_to_jail(member):
    tier = random.choices(SENTENCE_TIERS, weights=SENTENCE_WEIGHTS, k=1)[0]
    member['jail_until'] = time.time() + tier['minutes'] * 60
    member['jail_sentence'] = tier['label']
    member['times_jailed'] += 1
    return tier['label']

def get_member_status(m):
    if not m['alive']:
        return "Dead"
    if is_jailed(m):
        return f"Locked Up ({m['jail_sentence']})"
    return "Free"

def add_revenge_target(gang, killer_name, enemy_info, enemy_rep):
    targets = gang.setdefault('revenge_targets', [])
    for t in targets:
        if t['gang'] == enemy_info['name']:
            t['name'] = killer_name
            t['enemy_rep'] = enemy_rep
            return
    targets.append({"name": killer_name, "gang": enemy_info['name'], "gang_info": enemy_info, "enemy_rep": enemy_rep})

def get_revenge_targets(gang):
    return gang.get('revenge_targets', [])

def remove_revenge_target(gang, gang_name):
    gang['revenge_targets'] = [t for t in gang.get('revenge_targets', []) if t['gang'] != gang_name]

async def safe_send(channel, embed=None, content=None):
    try:
        if embed:
            await channel.send(embed=embed)
        elif content:
            await channel.send(content)
    except discord.HTTPException as e:
        print(f"safe_send error: {e}")

# Short outcome phrases

def member_result_line(name, outcome, sentence=None):
    if outcome == "kill":
        return random.choice([
            f"`{name}` -- handled business, got a body.",
            f"`{name}` -- put in work, target down.",
            f"`{name}` -- moved clean, mission done.",
        ])
    elif outcome == "friendly_kill":
        return random.choice([
            f"`{name}` -- caught a stray. Didn't make it back.",
            f"`{name}` -- took a shot leaving the scene. Gone.",
            f"`{name}` -- won the fight, lost the night. RIP.",
        ])
    elif outcome == "death":
        return random.choice([
            f"`{name}` -- got caught out. Didn't make it.",
            f"`{name}` -- outnumbered with no exit. Left on that block.",
            f"`{name}` -- took too many. Gone.",
        ])
    elif outcome == "jail":
        return random.choice([
            f"`{name}` -- knocked. Facing {sentence}.",
            f"`{name}` -- hemmed up leaving the scene. {sentence}.",
            f"`{name}` -- task force was waiting. {sentence}.",
        ])
    elif outcome == "survived":
        return random.choice([
            f"`{name}` -- took a hit but made it back.",
            f"`{name}` -- caught a graze. Still standing.",
            f"`{name}` -- got out clean.",
        ])
    return f"`{name}` -- status unknown."

# Slide Logic

def calculate_slide_outcome(gang, rolling_members, enemy_rep, is_revenge=False):
    player_rep = gang['rep']
    rep_diff = player_rep - enemy_rep
    win_chance = max(10, min(90, 50 + int((rep_diff / 500) * 40)))
    if is_revenge:
        win_chance = min(95, win_chance + 10)

    player_won = random.randint(1, 100) <= win_chance
    member_lines = []
    kills_this_fight = {}
    fallen = []
    jailed = []

    if player_won:
        rep_gain = random.randint(20, max(1, int(enemy_rep * 0.4)))
        if is_revenge:
            rep_gain = int(rep_gain * 1.25)
        gang['rep'] = player_rep + rep_gain
        gang['fights_won'] = gang.get('fights_won', 0) + 1

        for m in rolling_members:
            if is_jailed(m):
                continue
            m['kills'] += 1
            m['missions_survived'] += 1
            kills_this_fight[m['name']] = kills_this_fight.get(m['name'], 0) + 1
            member_lines.append(member_result_line(m['name'], "kill"))

        free_rolling = [m for m in rolling_members if not is_jailed(m)]
        if len(get_alive_members(gang)) > 1 and random.randint(1, 100) <= 20 and free_rolling:
            c = random.choice(free_rolling)
            c['alive'] = False
            c['deaths'] += 1
            fallen.append(c['name'])
            member_lines.append(member_result_line(c['name'], "friendly_kill"))

        if random.randint(1, 100) <= 15:
            free_rolling2 = [m for m in rolling_members if m['alive'] and not is_jailed(m)]
            if free_rolling2:
                j = random.choice(free_rolling2)
                s = send_to_jail(j)
                jailed.append((j['name'], s))
                member_lines.append(member_result_line(j['name'], "jail", s))

        return {
            "won": True, "rep_gain": rep_gain, "old_rep": player_rep, "new_rep": gang['rep'],
            "enemy_rep": enemy_rep, "member_lines": member_lines, "kills_this_fight": kills_this_fight,
            "members_alive": len(get_alive_members(gang)), "fallen": fallen, "jailed": jailed,
        }
    else:
        gang['fights_lost'] = gang.get('fights_lost', 0) + 1

        for m in rolling_members:
            if is_jailed(m):
                continue
            if len(get_alive_members(gang)) > 1 and random.randint(1, 100) <= 40:
                m['alive'] = False
                m['deaths'] += 1
                fallen.append(m['name'])
                member_lines.append(member_result_line(m['name'], "death"))
            elif random.randint(1, 100) <= 30:
                s = send_to_jail(m)
                jailed.append((m['name'], s))
                member_lines.append(member_result_line(m['name'], "jail", s))
            else:
                m['missions_survived'] += 1
                member_lines.append(member_result_line(m['name'], "survived"))

        rep_loss = random.randint(20, max(1, int(player_rep * 0.25)))
        gang['rep'] = max(1, player_rep - rep_loss)

        return {
            "won": False, "rep_loss": player_rep - gang['rep'], "old_rep": player_rep, "new_rep": gang['rep'],
            "enemy_rep": enemy_rep, "member_lines": member_lines, "kills_this_fight": kills_this_fight,
            "members_alive": len(get_alive_members(gang)), "fallen": fallen, "jailed": jailed,
        }


async def send_slide_result(channel, gang, enemy_info, result, rolling, is_revenge=False):
    overall_color = discord.Color.green() if result['won'] else discord.Color.orange()
    title = ("Revenge Collected" if is_revenge else "Slide Won") if result['won'] else ("Revenge Failed" if is_revenge else "Slide Lost")
    cred_line = f"{result['old_rep']} -> {result['new_rep']} (+{result['rep_gain']})" if result['won'] else f"{result['old_rep']} -> {result['new_rep']} (-{result['rep_loss']})"

    rolling_names = ", ".join(f"`{m['name']}`" for m in rolling if not is_jailed(m))
    intro = discord.Embed(title="Slide", color=discord.Color.dark_red())
    intro.description = (
        f"**{gang['name']}** vs **{enemy_info['name']}**\n"
        f"Your Cred: {result['old_rep']}  |  Opp Cred: {result['enemy_rep']}\n\n"
        f"Rolling: {rolling_names}"
    )
    await safe_send(channel, embed=intro)
    await asyncio.sleep(MSG_DELAY)

    crew_lines = "\n".join(result['member_lines']) if result['member_lines'] else "Nothing to report."
    kills_lines = "\n".join(f"`{n}` -- {k} kill{'s' if k != 1 else ''}" for n, k in result['kills_this_fight'].items()) if result['kills_this_fight'] else "No bodies."

    desc = (
        f"**Cred:** {cred_line}\n"
        f"**Still Standing:** {result['members_alive']}\n\n"
        f"**Crew**\n{crew_lines}\n\n"
        f"**Kills**\n{kills_lines}"
    )
    if result['fallen']:
        desc += "\n\n**Fallen:** " + ", ".join(f"`{n}`" for n in result['fallen'])
    if result['jailed']:
        desc += "\n**Locked Up:** " + ", ".join(f"`{n}` ({s})" for n, s in result['jailed'])

    result_embed = discord.Embed(title=title, description=desc, color=overall_color)
    result_embed.set_footer(text="They won't touch yours again." if result['won'] else "Regroup. Come back harder.")
    await safe_send(channel, embed=result_embed)


# Mission handler

async def handle_mission(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `mission <code>`")
        return

    code = args[0].upper()
    gang = gangs.get(code)
    if not gang:
        await safe_send(message.channel, content=f"No crew found with code `{code}`.")
        return
    if gang['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That ain't your crew.")
        return
    if not gang['alive']:
        await safe_send(message.channel, content=f"**{gang['name']}** has been disbanded.")
        return

    free = get_free_members(gang)
    if not free:
        await safe_send(message.channel, content=f"**{gang['name']}** has no free members right now. Everyone is locked up or dead.")
        return

    member = random.choice(free)

    if random.randint(1, 100) <= 40:
        await run_drug_mission(message.channel, gang, member, code)
    else:
        rep = gang['rep']
        event = random.choice(EVENTS)
        embed = discord.Embed(
            title=event['name'],
            description=event['description'].format(name=gang['name'], member=f"`{member['name']}`"),
            color=event['color']
        )

        if event['type'] == 'rep_up':
            gain = random.randint(*event['value'])
            gang['rep'] = rep + gain
            member['missions_survived'] += 1
            if random.randint(1, 100) <= 20:
                member['kills'] += 1
            embed.description += f"\n\nStreet Cred: {rep} -> {gang['rep']} (+{gain})"
            embed.set_footer(text="Rep rising.")

        elif event['type'] == 'rep_down':
            loss = random.randint(*event['value'])
            new_rep = max(1, rep - loss)
            actual_loss = rep - new_rep
            gang['rep'] = new_rep
            if event.get('snitch'):
                member['times_snitched'] += 1
            extra = []
            free_now = get_free_members(gang)
            if random.randint(1, 100) <= 15 and len(get_alive_members(gang)) > 1 and not is_jailed(member):
                member['alive'] = False
                member['deaths'] += 1
                extra.append(f"`{member['name']}` didn't make it out.")
            elif random.randint(1, 100) <= 25 and not is_jailed(member):
                s = send_to_jail(member)
                extra.append(f"`{member['name']}` got knocked -- {s}.")
            if extra:
                embed.description += "\n\n" + "\n".join(extra)
            embed.description += f"\n\nStreet Cred: {rep} -> {gang['rep']} (-{actual_loss})"
            embed.set_footer(text="Taking an L.")

        elif event['type'] == 'nothing':
            embed.description += f"\n\nStreet Cred: {rep} (no change)"
            embed.set_footer(text="Nothing popped off.")

        await safe_send(message.channel, embed=embed)


async def run_drug_mission(channel, gang, member, code):
    if is_jailed(member):
        await safe_send(channel, content=f"`{member['name']}` is locked up and can't run a mission.")
        return

    rep = gang['rep']
    event = random.choice(DRUG_EVENTS)
    embed = discord.Embed(
        title=event['name'],
        description=event['description'].format(name=gang['name'], member=f"`{member['name']}`"),
        color=event['color']
    )

    if event['type'] == 'drug_win':
        gain = random.randint(*event['value'])
        gang['rep'] = rep + gain
        member['missions_survived'] += 1
        embed.description += f"\n\nStreet Cred: {rep} -> {gang['rep']} (+{gain})"
        embed.set_footer(text="Trap is open. Money coming in.")

    elif event['type'] == 'drug_jail':
        loss = random.randint(*event.get('value', (20, 60)))
        gang['rep'] = max(1, rep - loss)
        s = send_to_jail(member)
        embed.description += f"\n\n`{member['name']}` got knocked -- {s}.\nStreet Cred: {rep} -> {gang['rep']} (-{loss})"
        embed.set_footer(text="One man down. The trap goes quiet.")

    elif event['type'] == 'drug_killed':
        loss = random.randint(*event.get('value', (30, 80)))
        gang['rep'] = max(1, rep - loss)
        if len(get_alive_members(gang)) > 1:
            member['alive'] = False
            member['deaths'] += 1
            check_and_mark_dead(code)
            embed.description += f"\n\n`{member['name']}` didn't make it back.\nStreet Cred: {rep} -> {gang['rep']} (-{loss})\nMembers Alive: {len(get_alive_members(gang))}"
        else:
            s = send_to_jail(member)
            embed.description += f"\n\n`{member['name']}` got knocked -- {s}.\nStreet Cred: {rep} -> {gang['rep']} (-{loss})"
        embed.set_footer(text="The streets took another one.")

    elif event['type'] == 'drug_nothing':
        embed.description += f"\n\nStreet Cred: {rep} (no change)"
        embed.set_footer(text="Slow night on the trap.")

    await safe_send(channel, embed=embed)


# DP Command -- Disciplinary Punishment

async def handle_dp(message, args):
    if len(args) < 2:
        await safe_send(message.channel, content="Usage: `dp <code> <name>`")
        return

    code = args[0].upper()
    member_name = " ".join(args[1:])
    gang = gangs.get(code)

    if not gang:
        await safe_send(message.channel, content=f"No crew found with code `{code}`.")
        return
    if gang['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That ain't your crew.")
        return
    if not gang['alive']:
        await safe_send(message.channel, content=f"**{gang['name']}** has been disbanded.")
        return

    target = next((m for m in gang['members'] if m['name'].lower() == member_name.lower()), None)
    if not target:
        roster = ", ".join(f"`{m['name']}`" for m in gang['members'])
        await safe_send(message.channel, content=f"No member named `{member_name}`.\nRoster: {roster}")
        return
    if not target['alive']:
        await safe_send(message.channel, content=f"`{target['name']}` is already dead.")
        return

    free = get_free_members(gang)
    beaters = [m for m in free if m['name'] != target['name']]

    if not beaters:
        await safe_send(message.channel, content="Nobody free to handle the DP right now.")
        return

    intro = discord.Embed(title="Disciplinary Punishment", color=discord.Color.dark_red())
    intro.description = (
        f"**{gang['name']}** is handling business internally.\n\n"
        f"`{target['name']}` stepped out of line. The set is about to address it."
    )
    intro.set_footer(text="Nobody talks. Nobody walks. This stays in house.")
    await safe_send(message.channel, embed=intro)
    await asyncio.sleep(MSG_DELAY)

    beat_lines = []
    num_involved = min(len(beaters), random.randint(2, 5))
    involved = random.sample(beaters, num_involved)

    beating_phrases = [
        f"`{m['name']}` stepped up first and caught `{target['name']}` with a clean one.",
        f"`{m['name']}` didn't say a word -- just went straight to work.",
        f"`{m['name']}` made sure `{target['name']}` felt every second of it.",
        f"`{m['name']}` held `{target['name']}` up so the rest could get their licks in.",
        f"`{m['name']}` came in last but hit the hardest.",
        f"`{m['name']}` didn't hold back. No mercy, no words.",
        f"`{m['name']}` went in swinging and didn't stop till someone pulled him off.",
        f"`{m['name']}` caught `{target['name']}` with a right hand that dropped him to the ground.",
    ]

    for m in involved:
        beat_lines.append(random.choice(beating_phrases).replace(f"`{m['name']}`", f"`{m['name']}`"))

    await asyncio.sleep(MSG_DELAY)

    beat_embed = discord.Embed(title="The DP", color=discord.Color.dark_gold())
    beat_embed.description = "\n".join(beat_lines)
    await safe_send(message.channel, embed=beat_embed)
    await asyncio.sleep(MSG_DELAY)

    roll = random.randint(1, 100)

    if roll <= 15:
        # Killed during DP
        if len(get_alive_members(gang)) > 1:
            target['alive'] = False
            target['deaths'] += 1
            check_and_mark_dead(code)
            result_embed = discord.Embed(title="DP -- Didn't Make It", color=discord.Color.dark_grey())
            result_embed.description = (
                f"`{target['name']}` took too much. They didn't walk away from this one.\n\n"
                f"The set made a decision and that decision is final.\n"
                f"Members Alive: {len(get_alive_members(gang))}"
            )
            result_embed.set_footer(text="That name stays off the wall. They chose this.")
        else:
            result_embed = discord.Embed(title="DP -- Last Man Standing", color=discord.Color.orange())
            result_embed.description = (
                f"`{target['name']}` is the last one breathing. Can't finish what got started.\n"
                f"They live -- for now."
            )
            result_embed.set_footer(text="Unfinished business.")

    elif roll <= 45:
        # Kicked out
        gang['members'].remove(target)
        result_embed = discord.Embed(title="DP -- Kicked Out", color=discord.Color.red())
        result_embed.description = (
            f"`{target['name']}` got beat out of the set.\n\n"
            f"They took their licks and when it was over they were told to walk.\n"
            f"They are no longer part of **{gang['name']}**.\n"
            f"Members Alive: {len(get_alive_members(gang))}"
        )
        result_embed.set_footer(text="Don't come back around.")

    else:
        # Beaten but stays in
        result_embed = discord.Embed(title="DP -- Beat Down, Still In", color=discord.Color.orange())
        result_embed.description = (
            f"`{target['name']}` took the DP and is still standing -- barely.\n\n"
            f"They took every hit without running. The set decided that counts for something.\n"
            f"`{target['name']}` is still part of **{gang['name']}** but they know what time it is now."
        )
        result_embed.set_footer(text="One more slip and it won't end the same way.")

    await safe_send(message.channel, embed=result_embed)


# Commands

async def handle_gang(message, args):
    user_id = message.author.id
    if not is_admin(message) and user_has_active_gang(user_id):
        await safe_send(message.channel, content="You already got a crew running. Type `show` to see them.")
        return

    la_gang = random.choice(LA_GANGS)
    code = generate_code()
    members = generate_ai_members(random.randint(4, 7))
    rep = random.randint(10, 100)

    gangs[code] = {
        "name": la_gang["name"], "hood": la_gang["hood"],
        "leader": members[0]['name'], "rep": rep,
        "owner_id": user_id, "owner_name": message.author.name,
        "code": code, "alive": True,
        "fights_won": 0, "fights_lost": 0,
        "members": members, "revenge_targets": [],
    }

    if not is_admin(message):
        active_gang_owners.add(user_id)

    member_lines = "\n".join(f"`{m['name']}`" for m in members)
    embed = discord.Embed(
        title="You're In",
        description=(
            f"You just got put on with **{la_gang['name']}**.\n\n"
            f"Hood: {la_gang['hood']}\n"
            f"Shot Caller: `{members[0]['name']}`\n"
            f"Street Cred: {rep}\n"
            f"Members: {len(members)}\n"
            f"Code: `{code}`\n\n"
            f"{member_lines}"
        ),
        color=discord.Color.dark_grey()
    )
    embed.set_footer(text="mission | slide | recruit | revenge | block | solo | dp | show | delete")
    await safe_send(message.channel, embed=embed)


async def handle_show(message, args):
    user_id = message.author.id
    user_gangs = [g for g in gangs.values() if g['owner_id'] == user_id]

    if not user_gangs:
        await safe_send(message.channel, content="You got no crew. Type `gang` to start one.")
        return

    alive_gangs = [g for g in user_gangs if g['alive']]
    dead_count = len(user_gangs) - len(alive_gangs)

    desc = f"Active: {len(alive_gangs)}   |   Disbanded: {dead_count}"

    if alive_gangs:
        for g in alive_gangs:
            fw = g.get('fights_won', 0)
            fl = g.get('fights_lost', 0)
            total = fw + fl
            win_rate = f"{int((fw / total) * 100)}%" if total > 0 else "N/A"
            targets = get_revenge_targets(g)
            blood_lines = ""
            if targets:
                blood_lines = "\n" + "\n".join(f"Blood Owed: `{t['name']}` | {t['gang']}" for t in targets)
            desc += (
                f"\n\n**{g['name']}**\n"
                f"Hood: {g.get('hood', 'Unknown')}\n"
                f"Code: `{g['code']}`\n"
                f"Shot Caller: `{g.get('leader', 'Unknown')}`\n"
                f"Street Cred: {g['rep']}\n"
                f"Record: {fw}W -- {fl}L   Win Rate: {win_rate}\n"
                f"Kills: {get_gang_bodies(g)}   Deaths: {get_gang_deaths(g)}\n"
                f"Alive: {len(get_alive_members(g))}   Free: {len(get_free_members(g))}"
                + blood_lines
            )
    else:
        desc += "\n\nNo active crew. Type `gang` to start fresh."

    embed = discord.Embed(title=f"{message.author.name}'s Crew", description=desc, color=discord.Color.dark_grey())

    if alive_gangs:
        for g in alive_gangs:
            alive = get_alive_members(g)
            if alive:
                roster_lines = "\n".join(
                    f"`{m['name']}` | {m['kills']} kills | {get_member_status(m)}" for m in alive
                )
                embed.add_field(name=f"{g['name']} -- Active Roster", value=roster_lines, inline=False)

    embed.set_footer(text="mission | slide | recruit | revenge | block | solo | dp | show | delete")
    await safe_send(message.channel, embed=embed)

    has_dead = any(get_dead_members(g) for g in alive_gangs)
    if has_dead:
        rip_embed = discord.Embed(
            title="Rest In Power",
            description="Homies who fell in the streets. Their names stay on the wall.",
            color=discord.Color.dark_grey()
        )
        for g in alive_gangs:
            dead = get_dead_members(g)
            if dead:
                dead_lines = "\n".join(f"`{m['name']}` | {m['kills']} kills | Dead" for m in dead)
                rip_embed.add_field(name=f"{g['name']} -- Fallen", value=dead_lines, inline=False)
        rip_embed.set_footer(text="Gone but not forgotten.")
        await safe_send(message.channel, embed=rip_embed)


async def handle_recruit(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `recruit <code> <number>` -- Example: `recruit XKRV 3`")
        return

    code = args[0].upper()
    gang = gangs.get(code)
    if not gang:
        await safe_send(message.channel, content=f"No crew found with code `{code}`.")
        return
    if gang['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That ain't your crew.")
        return
    if not gang['alive']:
        await safe_send(message.channel, content=f"**{gang['name']}** has been disbanded.")
        return

    requested = 1
    if len(args) >= 2:
        try:
            requested = int(args[1])
        except ValueError:
            await safe_send(message.channel, content="The number needs to be a whole number. Example: `recruit XKRV 3`")
            return
        if requested < 1:
            await safe_send(message.channel, content="Recruit at least 1.")
            return
        if requested > 10:
            await safe_send(message.channel, content="Max 10 at once.")
            return

    existing = {m['name'] for m in gang['members']}
    available = [n for n in STREET_NAMES if n not in existing]
    if not available:
        await safe_send(message.channel, content=f"**{gang['name']}** roster is maxed out.")
        return

    actual = min(requested, len(available))
    joined = []
    failed = 0

    for _ in range(actual):
        if not available:
            break
        if random.randint(1, 100) <= 60:
            new_name = random.choice(available)
            available.remove(new_name)
            existing.add(new_name)
            gang['members'].append(make_member(new_name))
            joined.append(new_name)
        else:
            failed += 1

    embed = discord.Embed(color=discord.Color.teal() if joined else discord.Color.dark_grey())

    if joined and failed == 0:
        embed.title = f"{len(joined)} Joined the Set"
        lines = "\n".join(f"`{n}`" for n in joined)
        embed.description = f"{lines}\n\nAll {len(joined)} came through. Total Alive: {len(get_alive_members(gang))}"
    elif joined and failed > 0:
        embed.title = f"{len(joined)} Joined -- {failed} Fell Through"
        lines = "\n".join(f"`{n}`" for n in joined)
        embed.description = f"Joined:\n{lines}\n\n{failed} didn't show. Total Alive: {len(get_alive_members(gang))}"
        embed.color = discord.Color.gold()
    else:
        embed.title = "Nobody Came Through"
        embed.description = f"Put the word out for {requested} but nobody stepped up.\nMembers: {len(get_alive_members(gang))}"

    embed.set_footer(text=f"recruit {code} <number> to try again.")
    await safe_send(message.channel, embed=embed)


async def handle_slide(message, args):
    if len(args) < 2:
        await safe_send(message.channel, content="Usage: `slide <code> <number>`")
        return

    code = args[0].upper()
    gang = gangs.get(code)
    if not gang:
        await safe_send(message.channel, content=f"No crew found with code `{code}`.")
        return
    if gang['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That ain't your crew.")
        return
    if not gang['alive']:
        await safe_send(message.channel, content=f"**{gang['name']}** has been disbanded.")
        return

    try:
        requested = int(args[1])
    except ValueError:
        await safe_send(message.channel, content="Needs to be a number.")
        return

    if requested < 1:
        await safe_send(message.channel, content="Send at least 1.")
        return

    free = get_free_members(gang)
    if not free:
        await safe_send(message.channel, content="Nobody free to roll out. Everyone is locked up or dead.")
        return

    actual = min(requested, len(free), 10)
    rolling = random.sample(free, actual)
    enemy_info = random.choice(LA_GANGS)
    enemy_rep = random.randint(10, 500)

    alive_before = {m['name'] for m in get_alive_members(gang)}
    result = calculate_slide_outcome(gang, rolling, enemy_rep)
    alive_after = {m['name'] for m in get_alive_members(gang)}

    if alive_before - alive_after:
        killer_name = random.choice(STREET_NAMES)
        add_revenge_target(gang, killer_name, enemy_info, enemy_rep)

    check_and_mark_dead(code)
    await send_slide_result(message.channel, gang, enemy_info, result, rolling)


async def handle_revenge(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `revenge <code>`")
        return

    code = args[0].upper()
    gang = gangs.get(code)
    if not gang:
        await safe_send(message.channel, content=f"No crew found with code `{code}`.")
        return
    if gang['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That ain't your crew.")
        return
    if not gang['alive']:
        await safe_send(message.channel, content=f"**{gang['name']}** has been disbanded.")
        return

    targets = get_revenge_targets(gang)
    if not targets:
        await safe_send(message.channel, content="No blood owed right now.")
        return

    free = get_free_members(gang)
    if not free:
        await safe_send(message.channel, content="Nobody free to roll out. Everyone is locked up or dead.")
        return

    target = random.choice(targets)
    enemy_info = target['gang_info']
    enemy_rep = target.get('enemy_rep', random.randint(10, 500))
    rolling = random.sample(free, random.randint(1, min(3, len(free))))

    alive_before = {m['name'] for m in get_alive_members(gang)}
    result = calculate_slide_outcome(gang, rolling, enemy_rep, is_revenge=True)
    alive_after = {m['name'] for m in get_alive_members(gang)}

    if result['won']:
        remove_revenge_target(gang, enemy_info['name'])
    elif alive_before - alive_after:
        add_revenge_target(gang, target['name'], enemy_info, enemy_rep)

    check_and_mark_dead(code)
    await send_slide_result(message.channel, gang, enemy_info, result, rolling, is_revenge=True)

    remaining_after = get_revenge_targets(gang)
    if remaining_after:
        followup = discord.Embed(
            title="Blood Still Owed",
            description="\n".join(f"**{t['gang']}** | `{t['name']}`" for t in remaining_after) + f"\n\nType `revenge {code}` again.",
            color=discord.Color.dark_red()
        )
        await safe_send(message.channel, embed=followup)


async def handle_solo(message, args):
    if len(args) < 2:
        await safe_send(message.channel, content="Usage: `solo <code> <name>`")
        return

    code = args[0].upper()
    member_name = " ".join(args[1:])
    gang = gangs.get(code)

    if not gang:
        await safe_send(message.channel, content=f"No crew found with code `{code}`.")
        return
    if gang['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That ain't your crew.")
        return
    if not gang['alive']:
        await safe_send(message.channel, content=f"**{gang['name']}** has been disbanded.")
        return

    target = next((m for m in gang['members'] if m['name'].lower() == member_name.lower()), None)
    if not target:
        roster = ", ".join(f"`{m['name']}`" for m in gang['members'])
        await safe_send(message.channel, content=f"No member named `{member_name}`.\nRoster: {roster}")
        return
    if not target['alive']:
        await safe_send(message.channel, content=f"`{target['name']}` is dead.")
        return
    if is_jailed(target):
        await safe_send(message.channel, content=f"`{target['name']}` is locked up and can't run solo.")
        return

    enemy_info = random.choice(LA_GANGS)
    enemy_rep = random.randint(10, 500)
    player_rep = gang['rep']
    win_chance = max(10, min(75, 40 + int(((player_rep - enemy_rep) / 500) * 30)))
    roll = random.randint(1, 100)

    intro = discord.Embed(title="Solo Mission", color=discord.Color.dark_red())
    intro.description = (
        f"`{target['name']}` rolled out alone into **{enemy_info['name']}** territory.\n\n"
        f"Kills so far: {target['kills']}  |  Hood: {enemy_info['hood']}"
    )
    intro.set_footer(text="One man. No backup.")
    await safe_send(message.channel, embed=intro)
    await asyncio.sleep(MSG_DELAY)

    if roll <= win_chance:
        target['kills'] += 1
        target['missions_survived'] += 1
        rep_gain = random.randint(15, 60)
        gang['rep'] = player_rep + rep_gain
        embed = discord.Embed(title="Solo -- Target Down", color=discord.Color.green())
        embed.description = (
            f"`{target['name']}` moved clean. Target handled.\n\n"
            f"Kills: {target['kills']}  |  Cred: {player_rep} -> {gang['rep']} (+{rep_gain})"
        )
        embed.set_footer(text="Solo work. The set eats tonight.")
    elif roll <= win_chance + 30:
        target['missions_survived'] += 1
        rep_loss = random.randint(5, 25)
        gang['rep'] = max(1, player_rep - rep_loss)
        embed = discord.Embed(title="Solo -- Made It Back", color=discord.Color.orange())
        embed.description = (
            f"`{target['name']}` took a hit but got back.\n\n"
            f"Kills: {target['kills']}  |  Cred: {player_rep} -> {gang['rep']} (-{rep_loss})"
        )
        embed.set_footer(text="Alive. That counts.")
    elif roll <= win_chance + 50:
        s = send_to_jail(target)
        rep_loss = random.randint(10, 35)
        gang['rep'] = max(1, player_rep - rep_loss)
        embed = discord.Embed(title="Solo -- Knocked", color=discord.Color.blue())
        embed.description = (
            f"`{target['name']}` got caught leaving the scene. Facing {s}.\n\n"
            f"Cred: {player_rep} -> {gang['rep']} (-{rep_loss})"
        )
        embed.set_footer(text="One man down.")
    else:
        rep_loss = random.randint(20, 60)
        gang['rep'] = max(1, player_rep - rep_loss)
        if len(get_alive_members(gang)) > 1:
            target['alive'] = False
            target['deaths'] += 1
            check_and_mark_dead(code)
            embed = discord.Embed(title="Solo -- Fallen", color=discord.Color.dark_grey())
            embed.description = (
                f"`{target['name']}` didn't come back. Another name on the wall.\n\n"
                f"Kills: {target['kills']}  |  Cred: {player_rep} -> {gang['rep']} (-{rep_loss})\n"
                f"Members Alive: {len(get_alive_members(gang))}"
            )
            embed.set_footer(text="Gone but not forgotten.")
        else:
            s = send_to_jail(target)
            embed = discord.Embed(title="Solo -- Knocked", color=discord.Color.blue())
            embed.description = (
                f"`{target['name']}` got caught. Facing {s}.\n\n"
                f"Cred: {player_rep} -> {gang['rep']} (-{rep_loss})"
            )
            embed.set_footer(text="Last man standing is locked up.")

    await safe_send(message.channel, embed=embed)


async def handle_block(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `block <code>`")
        return

    code = args[0].upper()
    gang = gangs.get(code)
    if not gang:
        await safe_send(message.channel, content=f"No crew found with code `{code}`.")
        return
    if gang['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That ain't your crew.")
        return
    if not gang['alive']:
        await safe_send(message.channel, content=f"**{gang['name']}** has been disbanded.")
        return

    free = get_free_members(gang)
    if not free:
        await safe_send(message.channel, content="No free members to run the block party. Everyone is locked up or dead.")
        return

    host = random.choice(free)
    old_rep = gang['rep']

    setup_embed = discord.Embed(title="Block Party", color=discord.Color.dark_gold())
    setup_embed.description = (
        f"**{gang['name']}** is throwing down on {gang['hood']}.\n"
        f"Host: `{host['name']}`  |  Street Cred: {old_rep}"
    )
    setup_embed.set_footer(text="The block is live...")
    await safe_send(message.channel, embed=setup_embed)
    await asyncio.sleep(MSG_DELAY)

    num_events = random.randint(2, 4)
    rep_change = 0
    members_jailed = []
    members_killed = []

    for i in range(num_events):
        await asyncio.sleep(MSG_DELAY)
        current_free = get_free_members(gang)
        if not current_free:
            break
        featured = random.choice(current_free)
        event = random.choice(BLOCK_PARTY_EVENTS)
        desc = event['description'].replace("{member}", f"`{featured['name']}`").replace("{name}", gang['name'])

        ev_embed = discord.Embed(title=event['name'], description=desc, color=event['color'])
        extra = []

        if event['type'] == 'rep_up':
            gain = random.randint(*event['value'])
            rep_change += gain
            featured['missions_survived'] += 1
            ev_embed.description += f"\n\nCred: +{gain}"

        elif event['type'] == 'rep_down':
            loss = random.randint(*event['value'])
            rep_change -= loss
            if event.get('snitch'):
                featured['times_snitched'] += 1
            ev_embed.description += f"\n\nCred: -{loss}"

        elif event['type'] == 'driveby':
            rival = random.choice(LA_GANGS)
            rival_rep = random.randint(50, 400)
            killer_name = random.choice(STREET_NAMES)
            loss = random.randint(40, 120)
            rep_change -= loss
            alive_now = get_alive_members(gang)
            if len(alive_now) > 1:
                victims = random.sample(alive_now, min(random.randint(1, 2), len(alive_now) - 1))
                for v in victims:
                    if is_jailed(v):
                        continue
                    v['alive'] = False
                    v['deaths'] += 1
                    members_killed.append(v['name'])
                    extra.append(f"`{v['name']}` didn't make it.")
            add_revenge_target(gang, killer_name, rival, rival_rep)
            ev_embed.description += f"\n\n**{rival['name']}** -- `{killer_name}` pulled the trigger. Cred: -{loss}"
            if extra:
                ev_embed.description += "\nFallen: " + ", ".join(extra)
            ev_embed.set_footer(text=f"Type `revenge {code}` to collect.")

        elif event['type'] == 'brawl':
            rival = random.choice(LA_GANGS)
            rival_rep = random.randint(30, 300)
            crasher = random.choice(STREET_NAMES)
            loss = random.randint(20, 70)
            rep_change -= loss
            cf = get_free_members(gang)
            if cf and random.randint(1, 100) <= 40:
                victim = random.choice(cf)
                if not is_jailed(victim):
                    s = send_to_jail(victim)
                    members_jailed.append((victim['name'], s))
                    extra.append(f"`{victim['name']}` knocked -- {s}.")
            add_revenge_target(gang, crasher, rival, rival_rep)
            ev_embed.description += f"\n\n**{rival['name']}** crashed it. Cred: -{loss}"
            if extra:
                ev_embed.description += "\n" + ", ".join(extra)
            ev_embed.set_footer(text=f"Type `revenge {code}` to handle it.")

        elif event['type'] in ('police_harassment', 'police_raid', 'police_arrests'):
            loss = random.randint(10, 80)
            rep_change -= loss
            cf = get_free_members(gang)
            if event['type'] != 'police_harassment' and cf:
                count = 1 if event['type'] == 'police_raid' else random.randint(1, 2)
                arrested = random.sample(cf, min(count, len(cf)))
                for a in arrested:
                    if not is_jailed(a):
                        s = send_to_jail(a)
                        members_jailed.append((a['name'], s))
                        extra.append(f"`{a['name']}` -- {s}.")
            ev_embed.description += f"\n\nCred: -{loss}"
            if extra:
                ev_embed.description += "\nLocked Up: " + ", ".join(extra)

        elif event['type'] == 'nothing':
            ev_embed.description += "\n\nCred: No change"

        if not ev_embed.footer.text:
            ev_embed.set_footer(text=f"Event {i + 1} of {num_events}")
        await safe_send(message.channel, embed=ev_embed)

    gang['rep'] = max(1, gang['rep'] + rep_change)
    check_and_mark_dead(code)
    await asyncio.sleep(MSG_DELAY)

    color = discord.Color.green() if rep_change >= 0 else discord.Color.orange()
    rep_display = f"{old_rep} -> {gang['rep']} (+{rep_change})" if rep_change >= 0 else f"{old_rep} -> {gang['rep']} ({rep_change})"

    summary = discord.Embed(title="Block Party -- Done", color=color)
    summary.description = (
        f"**{gang['name']}** on {gang['hood']} -- night wrapped.\n\n"
        f"Cred: {rep_display}\n"
        f"Alive: {len(get_alive_members(gang))}  |  Free: {len(get_free_members(gang))}"
    )
    if members_killed:
        summary.description += "\nFallen: " + ", ".join(f"`{n}`" for n in members_killed)
    if members_jailed:
        summary.description += "\nLocked Up: " + ", ".join(f"`{n}` ({s})" for n, s in members_jailed)
    all_targets = get_revenge_targets(gang)
    if all_targets:
        summary.description += "\n\nBlood Owed:\n" + "\n".join(f"**{t['gang']}** | `{t['name']}`" for t in all_targets)
        summary.description += f"\n\nType `revenge {code}` to go after them."
    summary.set_footer(text="Night is over." if rep_change >= 0 else "Not the way anyone wanted it to end.")
    await safe_send(message.channel, embed=summary)


async def handle_delete(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `delete <code>`")
        return

    code = args[0].upper()
    gang = gangs.get(code)

    if not gang:
        await safe_send(message.channel, content=f"No crew found with code `{code}`.")
        return
    if gang['owner_id'] != message.author.id and not is_admin(message):
        await safe_send(message.channel, content="That ain't your crew.")
        return

    gang_name = gang['name']
    owner_id = gang['owner_id']
    del gangs[code]
    if not user_has_active_gang(owner_id):
        active_gang_owners.discard(owner_id)

    embed = discord.Embed(
        title="Crew Deleted",
        description=f"**{gang_name}** (`{code}`) wiped. Type `gang` to start fresh.",
        color=discord.Color.dark_red()
    )
    await safe_send(message.channel, embed=embed)


# Drug Mission Events

DRUG_EVENTS = [
    {"name": "Trap Popping", "description": "{member} had the trap running smooth all night. Fiends lining up, money counted twice. **{name}** ate good tonight.", "type": "drug_win", "value": (40, 120), "color": discord.Color.green()},
    {"name": "Bulk Move", "description": "{member} connected with a buyer moving weight -- whole brick gone in one transaction. **{name}** just made more in an hour than most make in a week.", "type": "drug_win", "value": (80, 200), "color": discord.Color.green()},
    {"name": "New Corner Opened", "description": "{member} posted up on a fresh corner nobody had claimed yet. By midnight it was running full. **{name}** just expanded the operation.", "type": "drug_win", "value": (50, 130), "color": discord.Color.green()},
    {"name": "Product Came In Clean", "description": "The new batch arrived and it was stronger than anything **{name}** had moved before. {member} tested it, priced it right, and word spread fast.", "type": "drug_win", "value": (60, 150), "color": discord.Color.green()},
    {"name": "Middle Man Cut Out", "description": "{member} went direct to the supplier and cut out the middleman. Same product, better price. **{name}**'s margins just doubled.", "type": "drug_win", "value": (70, 160), "color": discord.Color.green()},
    {"name": "Loyal Customer Base", "description": "The regulars came through all night without being chased. {member} held it down and the money kept coming. **{name}** has this corner on lock.", "type": "drug_win", "value": (30, 90), "color": discord.Color.green()},
    {"name": "Out of Town Plug", "description": "{member} linked up with someone passing through who needed to move product fast and cheap. **{name}** bought low and flipped it for triple.", "type": "drug_win", "value": (90, 220), "color": discord.Color.green()},
    {"name": "Phone Trap Running", "description": "{member} set up a delivery line -- no corner exposure, just calls coming in all night. **{name}** got paid without stepping outside.", "type": "drug_win", "value": (45, 110), "color": discord.Color.green()},
    {"name": "Dirty Money Cleaned", "description": "A contact of {member}'s ran **{name}**'s cash through a legitimate front. Everything came back clean and accounted for.", "type": "drug_win", "value": (55, 140), "color": discord.Color.green()},
    {"name": "First Time Buyers Hooked", "description": "{member} gave out samples to people who had never bought before. By the end of the night three of them were back spending real money. **{name}**'s customer list just grew.", "type": "drug_win", "value": (35, 85), "color": discord.Color.green()},
    {"name": "High-End Client", "description": "{member} got introduced to someone with real money who wanted quality product delivered quietly. **{name}** just opened a new revenue stream nobody expected.", "type": "drug_win", "value": (100, 250), "color": discord.Color.green()},
    {"name": "Quick Flip", "description": "{member} bought a small batch, cut it smart, and moved it all before sunrise. Fast money. No drama. **{name}** keeps it efficient.", "type": "drug_win", "value": (25, 70), "color": discord.Color.green()},
    {"name": "Corner Tax Collected", "description": "A smaller operation was running on **{name}**'s turf without permission. {member} paid them a visit and now they pay rent every week.", "type": "drug_win", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Stepped on Right", "description": "{member} stretched the product without killing the quality. Same profit margin, twice the volume. **{name}**'s operation just scaled up.", "type": "drug_win", "value": (50, 120), "color": discord.Color.green()},
    {"name": "Opp Trap Taken Over", "description": "The opps had a corner running. {member} moved in when they were understaffed and took it over clean. **{name}** is now running their spot.", "type": "drug_win", "value": (80, 180), "color": discord.Color.green()},
    {"name": "Undercover Buyer", "description": "{member} was moving product when a buyer didn't feel right. Too late -- badge came out before the deal was even done. Knocked at the scene.", "type": "drug_jail", "value": (30, 80), "color": discord.Color.blue()},
    {"name": "Traffic Stop Gone Wrong", "description": "{member} was running a delivery when a routine stop turned into a full search. Product found in the center console. Everything fell apart from there.", "type": "drug_jail", "value": (25, 70), "color": discord.Color.blue()},
    {"name": "Controlled Buy", "description": "Detectives had been running controlled buys on the corner for two weeks. {member} didn't know. The arrest was already planned before they even stepped outside.", "type": "drug_jail", "value": (35, 90), "color": discord.Color.blue()},
    {"name": "Stash Spot Raided", "description": "Someone gave up the location of **{name}**'s stash. Officers hit it with a warrant at 4am. {member} was inside and had nowhere to go.", "type": "drug_jail", "value": (40, 100), "color": discord.Color.blue()},
    {"name": "Informant in the Circle", "description": "A regular customer had been working with detectives for months. Every transaction {member} made was recorded. The indictment came down on a Wednesday.", "type": "drug_jail", "value": (50, 120), "color": discord.Color.blue()},
    {"name": "Federal Wiretap", "description": "The feds had been listening for six months. {member} didn't know the phone was burned. Every conversation, every deal, every location -- all on tape. No bail.", "type": "drug_jail", "value": (60, 150), "color": discord.Color.blue()},
    {"name": "Caught Holding", "description": "{member} got stopped with product on them and no story that made sense. Simple possession charge turned into intent to distribute once they counted the weight.", "type": "drug_jail", "value": (20, 60), "color": discord.Color.blue()},
    {"name": "Trap Phone Seized", "description": "Officers pulled {member} over and found the trap phone. Two thousand contacts and a full call log. Built the whole case from that one device.", "type": "drug_jail", "value": (35, 85), "color": discord.Color.blue()},
    {"name": "Corner Sweep", "description": "LAPD ran a sweep on the block and grabbed everyone standing outside. {member} was holding and got charged. Wrong place, wrong time, wrong pockets.", "type": "drug_jail", "value": (25, 65), "color": discord.Color.blue()},
    {"name": "Drug Task Force", "description": "A specialized narcotics unit had **{name}**'s operation mapped out for months. Hit four locations simultaneously at 6am. {member} was at one of them.", "type": "drug_jail", "value": (55, 140), "color": discord.Color.blue()},
    {"name": "Robbery Gone Wrong", "description": "Someone came for the stash and wasn't planning to leave witnesses. {member} was at the trap when they kicked the door. Didn't make it out.", "type": "drug_killed", "value": (40, 100), "color": discord.Color.dark_red()},
    {"name": "Opps Hit the Trap", "description": "The opps knew exactly where **{name}** was running the operation. They came in force and {member} was caught inside with no backup and no exit.", "type": "drug_killed", "value": (50, 120), "color": discord.Color.dark_red()},
    {"name": "Bad Deal Turned Deadly", "description": "A deal with an unknown buyer went sideways fast. {member} realized too late they weren't buyers -- they were robbers with guns already out.", "type": "drug_killed", "value": (45, 110), "color": discord.Color.dark_red()},
    {"name": "Retaliation Hit at the Trap", "description": "The opps came back over something that happened three weeks ago and {member} was the one they found. Caught slipping at the spot with no crew around.", "type": "drug_killed", "value": (55, 130), "color": discord.Color.dark_red()},
    {"name": "Set Up by a Plug", "description": "The connect {member} had been using set them up. Sent them to a location with product and the opps were already there waiting. No way out.", "type": "drug_killed", "value": (60, 150), "color": discord.Color.dark_red()},
    {"name": "Slow Night", "description": "{member} held the corner for six hours and barely moved anything. Nobody came through. **{name}**'s trap had a quiet one tonight.", "type": "drug_nothing", "color": discord.Color.greyple()},
    {"name": "Too Much Heat", "description": "Patrol cars were circling every twenty minutes. {member} kept the product put away all night rather than risk it. Smart call but no money made.", "type": "drug_nothing", "color": discord.Color.greyple()},
    {"name": "Bad Batch", "description": "The product that came in wasn't what was promised. {member} tested it and shut the trap down rather than move garbage. **{name}** has a reputation to protect.", "type": "drug_nothing", "color": discord.Color.greyple()},
    {"name": "No-Show Plug", "description": "{member} waited three hours for the connect to show up with re-up. They never came. No product, no sales, nothing. Night wasted.", "type": "drug_nothing", "color": discord.Color.greyple()},
    {"name": "Competition on the Block", "description": "Another crew set up shop two blocks over and pulled all the traffic away. {member} held the corner but nobody came. **{name}** needs to deal with that competition.", "type": "drug_nothing", "color": discord.Color.greyple()},
]

# Regular Mission Events

EVENTS = [
    {"name": "Corner Locked Down", "description": "{member} muscled every corner boy off Figueroa. By morning **{name}** owned every inch of that block.", "type": "rep_up", "value": (20, 80), "color": discord.Color.green()},
    {"name": "Successful Lick", "description": "{member} scoped the target for two days and walked away clean. **{name}** is comfortable for months.", "type": "rep_up", "value": (30, 100), "color": discord.Color.green()},
    {"name": "Street Fight Victory", "description": "{member} ran into four opps outside the liquor store, squared up solo, dropped two, walked away clean. **{name}**'s name rang out.", "type": "rep_up", "value": (20, 60), "color": discord.Color.green()},
    {"name": "Territory Claimed", "description": "{member} led **{name}** onto a block the opps had held for months. Posted up in broad daylight. Nobody said a word.", "type": "rep_up", "value": (40, 120), "color": discord.Color.green()},
    {"name": "OG Vouched", "description": "A respected OG pulled {member} aside and made a few calls. Doors opened for **{name}** that nobody knew existed.", "type": "rep_up", "value": (50, 150), "color": discord.Color.green()},
    {"name": "Retaliation Hit", "description": "{member} waited a full week then delivered the message personally. The streets went quiet. **{name}** doesn't forget.", "type": "rep_up", "value": (60, 180), "color": discord.Color.green()},
    {"name": "Prison Connects Made", "description": "{member} made the right introductions inside. **{name}** now has connects in three facilities.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Rival Scattered", "description": "{member} pulled up on the opp's main corner with the whole crew. One warning. 48 hours later **{name}** had three new blocks.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    {"name": "Rapper Shoutout", "description": "A rapper buried {member}'s name in two tracks -- **{name}** repped fully. Three cities were asking about the set by morning.", "type": "rep_up", "value": (50, 130), "color": discord.Color.green()},
    {"name": "Fed the Block", "description": "{member} threw a cookout. Families came out, OGs showed love. **{name}** has the community locked in.", "type": "rep_up", "value": (25, 70), "color": discord.Color.green()},
    {"name": "Big Score", "description": "{member} set up the biggest score **{name}** had seen in years. Product moved fast, money came back clean. Everyone ate.", "type": "rep_up", "value": (60, 160), "color": discord.Color.green()},
    {"name": "Took the Block Back", "description": "The opps had **{name}**'s old block for six months. {member} moved at 2am. By sunrise **{name}**'s colors were back up.", "type": "rep_up", "value": (70, 170), "color": discord.Color.green()},
    {"name": "Put in Work", "description": "There was a name on a list. {member} got it done quietly with no trail. **{name}** moves different because of soldiers like that.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    {"name": "Court Case Dismissed", "description": "The DA's key witness stopped cooperating. {member} walked out of the courthouse and came straight back to the block.", "type": "rep_up", "value": (40, 110), "color": discord.Color.green()},
    {"name": "Neighborhood Loyalty", "description": "Three families told detectives they saw nothing. {member} built that loyalty over years. **{name}** is protected.", "type": "rep_up", "value": (35, 95), "color": discord.Color.green()},
    {"name": "New Connect", "description": "{member} got introduced to a new supplier. First order came in clean. **{name}**'s operation just leveled up.", "type": "rep_up", "value": (60, 150), "color": discord.Color.green()},
    {"name": "Car Jacking Score", "description": "{member} spotted a luxury car sitting alone and moved on it clean. Stripped and gone before anyone called it in. **{name}** got paid tonight.", "type": "rep_up", "value": (35, 90), "color": discord.Color.green()},
    {"name": "Weapons Stash Found", "description": "{member} came across an unguarded weapons cache the opps had buried. Brought everything back. **{name}** is now better armed than ever.", "type": "rep_up", "value": (55, 140), "color": discord.Color.green()},
    {"name": "Bail Money Raised", "description": "{member} organized the whole hood to pool money and get three members out on bail overnight. **{name}** takes care of their own.", "type": "rep_up", "value": (30, 80), "color": discord.Color.green()},
    {"name": "Extortion Paid", "description": "A business on the block that had been refusing to pay finally sent {member} an envelope. Word travels. **{name}** is now collecting from four spots on that strip.", "type": "rep_up", "value": (45, 115), "color": discord.Color.green()},
    {"name": "Jumped In New Soldier", "description": "{member} oversaw the jump-in of a young kid who had been putting in work for months. The whole set watched. **{name}** is growing the right way.", "type": "rep_up", "value": (20, 55), "color": discord.Color.green()},
    {"name": "Hood Tax Enforced", "description": "Two operations in the area had been ignoring **{name}**'s tax. {member} paid both of them a personal visit. Both paid by end of day.", "type": "rep_up", "value": (50, 125), "color": discord.Color.green()},
    {"name": "Witness Scared Off", "description": "There was a trial coming up with a key witness. {member} made sure that witness understood what was at stake. Case collapsed the next morning.", "type": "rep_up", "value": (65, 160), "color": discord.Color.green()},
    {"name": "Armed Robbery Clean", "description": "{member} hit a spot that had been cased for two weeks. In and out in four minutes. No plates, no faces, no trail. **{name}** got paid clean.", "type": "rep_up", "value": (55, 135), "color": discord.Color.green()},
    {"name": "Opp Leader Handled", "description": "The opp set's leader had been the problem for months. {member} found him alone and made sure he won't be running anything for a long time.", "type": "rep_up", "value": (90, 220), "color": discord.Color.green()},
    {"name": "Protected the Hood", "description": "A crew from out of town tried to set up on **{name}**'s turf. {member} gathered the set and pushed them out before they got comfortable. They haven't come back.", "type": "rep_up", "value": (45, 110), "color": discord.Color.green()},
    {"name": "Funeral Respect Shown", "description": "{member} organized **{name}**'s presence at a fallen OG's funeral -- clean, organized, respectful. The older generation noticed. Doors opened.", "type": "rep_up", "value": (30, 75), "color": discord.Color.green()},
    {"name": "Rival Beef Squashed", "description": "A longstanding beef with a nearby set was costing both sides money. {member} brokered a sit-down and a truce. **{name}** now has a working relationship where there was only war.", "type": "rep_up", "value": (60, 145), "color": discord.Color.green()},
    {"name": "Church Donation", "description": "{member} dropped a significant envelope at the neighborhood church -- no names, no cameras. But the pastor knows who it came from. Community goodwill can't be bought but **{name}** found a way.", "type": "rep_up", "value": (25, 65), "color": discord.Color.green()},
    {"name": "Opp Stash Robbed", "description": "{member} had been watching the opp's stash location for three weeks. Hit it at the perfect moment -- took everything and left nothing. **{name}** is eating off the competition's work.", "type": "rep_up", "value": (75, 185), "color": discord.Color.green()},
    {"name": "Snitch in the Ranks", "description": "A sealed document leaked -- {member}'s name was on it. Cooperating since summer. **{name}** is fractured. Trust is gone.", "type": "rep_down", "value": (30, 100), "color": discord.Color.orange(), "snitch": True},
    {"name": "Botched Mission", "description": "{member} froze at the wrong moment. Three people on the porch filmed the whole thing. **{name}** is a punchline right now.", "type": "rep_down", "value": (20, 80), "color": discord.Color.orange()},
    {"name": "Homie Got Knocked", "description": "Task force rolled up on {member} with a warrant already signed. Bail denied. **{name}** lost one of their most solid members overnight.", "type": "rep_down", "value": (40, 120), "color": discord.Color.orange()},
    {"name": "Ran Off the Block", "description": "The opps pulled up three cars deep. {member} tried to hold it but the math wasn't there. Whole hood saw it.", "type": "rep_down", "value": (50, 150), "color": discord.Color.orange()},
    {"name": "Internal Beef", "description": "{member} and another member got into it over money right outside the trap. Neighbors recorded it. Other sets are laughing.", "type": "rep_down", "value": (25, 75), "color": discord.Color.orange()},
    {"name": "LAPD Raid", "description": "Forty officers hit **{name}**'s spot at 5am. {member} barely got out the back. Everything seized. The operation is on pause.", "type": "rep_down", "value": (60, 180), "color": discord.Color.orange()},
    {"name": "Caught Lacking", "description": "The opps caught {member} alone at a gas station. Took everything, recorded it, posted it. **{name}**'s name is on that video.", "type": "rep_down", "value": (30, 90), "color": discord.Color.orange()},
    {"name": "Lost the Package", "description": "{member} lost the package cross-town. **{name}** lost the product, the money, and the connect is threatening to cut them off.", "type": "rep_down", "value": (45, 130), "color": discord.Color.orange()},
    {"name": "Homie Flipped", "description": "{member} had been cooperating for months. DA announced indictments on a Tuesday. **{name}** lost four members to federal charges in one day.", "type": "rep_down", "value": (50, 160), "color": discord.Color.orange(), "snitch": True},
    {"name": "Jumped by Opps", "description": "Eight opps cornered {member} in broad daylight with witnesses everywhere. People recorded it. **{name}**'s name is attached to that video.", "type": "rep_down", "value": (35, 110), "color": discord.Color.orange()},
    {"name": "Stash House Burned", "description": "Somebody gave up the location. Opps hit it at noon. {member} barely got out the back window. Months of work gone in ten minutes.", "type": "rep_down", "value": (55, 150), "color": discord.Color.orange()},
    {"name": "Shot and Missed", "description": "{member} took a shot at an opp in broad daylight and missed. Three witnesses, two cameras, and the target got away. **{name}** looks bad and the heat just tripled.", "type": "rep_down", "value": (30, 85), "color": discord.Color.orange()},
    {"name": "Robbery Gone Wrong", "description": "{member} hit the wrong spot -- it was empty. Came back with nothing and the whole hood heard about it by morning. **{name}** is catching jokes.", "type": "rep_down", "value": (20, 65), "color": discord.Color.orange()},
    {"name": "Parole Violated", "description": "{member} got pulled over with something small and the parole officer wasn't playing. Revoked on the spot. **{name}** lost a solid member over nothing.", "type": "rep_down", "value": (30, 80), "color": discord.Color.orange()},
    {"name": "Money Stolen Internally", "description": "Cash went missing from the stash and all roads led back to {member}. Whether it was them or not nobody will ever know but the trust is broken. **{name}** is eating itself.", "type": "rep_down", "value": (40, 100), "color": discord.Color.orange()},
    {"name": "Marked by Feds", "description": "A federal agent showed up at {member}'s front door asking questions. Didn't arrest them -- just let them know they were being watched. **{name}** has to move different now.", "type": "rep_down", "value": (35, 90), "color": discord.Color.orange()},
    {"name": "Disrespected at the Vigil", "description": "The opps showed up to **{name}**'s fallen member's vigil and acted up. {member} couldn't respond in front of the family. The disrespect is on every social media page.", "type": "rep_down", "value": (45, 110), "color": discord.Color.orange()},
    {"name": "Gang Injunction Filed", "description": "The city filed a gang injunction targeting **{name}**'s territory. {member} can't be outside after dark, can't associate, can't even stand on their own block legally.", "type": "rep_down", "value": (50, 130), "color": discord.Color.orange()},
    {"name": "Social Media Beef", "description": "{member} got into it online with a rival set and said too much. Posted their location, their crew, their plans. The opps screenshotted everything. **{name}** is compromised.", "type": "rep_down", "value": (25, 70), "color": discord.Color.orange()},
    {"name": "Quiet Night", "description": "{member} held down the corner all night. Nothing to report. **{name}** is positioned and ready.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Laying Low", "description": "Too much heat. Patrol cars every hour. {member} kept **{name}** off the corners tonight. Smart move.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Watching and Waiting", "description": "{member} spent the night getting eyes on enemy positions. No action tonight -- reconnaissance. **{name}** is building a picture.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Regrouping", "description": "{member} called everyone in after recent events. Real conversation about what went wrong. **{name}** came out more focused.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Nothing Moving", "description": "Dead night. {member} sat outside for four hours and not a soul came through. **{name}** is patient.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Lying in Wait", "description": "{member} set up an ambush that never got triggered. The target didn't show. **{name}** stays ready.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Equipment Check", "description": "{member} ran an inventory of **{name}**'s weapons and resources tonight. Everything accounted for. Ready when needed.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Stayed Home", "description": "The word on the street was that something was about to pop off and it wasn't clear from which direction. {member} made the call to keep **{name}** inside. Nothing happened.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Fog of War", "description": "Conflicting intel had **{name}** moving in three different directions tonight. {member} called it off before anyone committed to the wrong play. Smart.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Rain Night", "description": "Nobody moves in the rain. {member} kept **{name}** off the streets and waited it out. The block is still there tomorrow.", "type": "nothing", "color": discord.Color.greyple()},
]

# Block Party Events

BLOCK_PARTY_EVENTS = [
    {"name": "Block Party Jumping", "description": "Music rattling windows two blocks over. {member} kept the energy right all night. **{name}**'s name on every lip.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Community Showed Love", "description": "Families from three streets came through. {member} passed out food personally and checked on the elders.", "type": "rep_up", "value": (30, 80), "color": discord.Color.green()},
    {"name": "Local Legend Pulled Up", "description": "An OG nobody had seen publicly in years showed up. Sat with {member} for two hours and gave his blessing in front of everyone.", "type": "rep_up", "value": (50, 130), "color": discord.Color.green()},
    {"name": "Rival Set Sent Respect", "description": "A rival set sent someone through to check. They reported back -- food, families, no trap. Respect came through a mutual.", "type": "rep_up", "value": (35, 90), "color": discord.Color.green()},
    {"name": "Block Party Goes All Night", "description": "Started at 4pm, still going at 2am. {member} kept refilling the food. People who had work the next morning stayed.", "type": "rep_up", "value": (45, 110), "color": discord.Color.green()},
    {"name": "News Crew Showed Up", "description": "Local news came through. {member} handled the camera -- spoke about giving back, never said anything wrong. Segment aired next morning.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Young Ones Got Recruited", "description": "Three younger kids watched **{name}** all night. Before it was over all three made it clear they wanted in.", "type": "rep_up", "value": (25, 65), "color": discord.Color.green()},
    {"name": "City Council Member Showed Up", "description": "A local politician came through looking for photo ops. {member} stayed calm and let them take pictures. **{name}** just got political cover.", "type": "rep_up", "value": (35, 85), "color": discord.Color.green()},
    {"name": "Free Clothes Giveaway", "description": "{member} organized a full clothing drive at the party. Families lined up for blocks. **{name}**'s name is synonymous with taking care of the community now.", "type": "rep_up", "value": (30, 75), "color": discord.Color.green()},
    {"name": "Local Artist Performed", "description": "A respected local rapper did a surprise set. {member} made it happen. The crowd was three times what was expected. **{name}** put on for the whole hood tonight.", "type": "rep_up", "value": (45, 115), "color": discord.Color.green()},
    {"name": "Kids Tournament", "description": "{member} set up a basketball tournament for the neighborhood kids. Parents watched, grandparents sat in lawn chairs. **{name}** looked like pillars of the community.", "type": "rep_up", "value": (30, 80), "color": discord.Color.green()},
    {"name": "Street Preacher Blessed It", "description": "A well-known street preacher came through and blessed the event publicly. Said **{name}** was doing what the church couldn't. That carries weight in this hood.", "type": "rep_up", "value": (25, 65), "color": discord.Color.green()},
    {"name": "Food Trucks Came Through", "description": "{member} linked up with three food trucks who came for free in exchange for exposure. The block ate better tonight than most people eat all week. **{name}** delivered.", "type": "rep_up", "value": (40, 95), "color": discord.Color.green()},
    {"name": "Block Rep Solidified", "description": "By the end of the night every family on this block knew **{name}**'s name. {member} made sure of it -- handshakes, conversations, real connection. This block is locked.", "type": "rep_up", "value": (35, 90), "color": discord.Color.green()},
    {"name": "Driveby -- Party Shot Up", "description": "A dark car rolled through slow. {member} saw it half a second before it started. No time. Shots into the crowd then gone.", "type": "driveby", "color": discord.Color.dark_red()},
    {"name": "Driveby -- Second Pass", "description": "First pass was to see who flinched. Second car came from the opposite direction. By the time it was over the block was empty.", "type": "driveby", "color": discord.Color.dark_red()},
    {"name": "Motorcycles Did a Driveby", "description": "Two motorcycles came through at full speed from opposite ends of the block. {member} dove for cover. Shots everywhere. Three people hit the ground.", "type": "driveby", "color": discord.Color.dark_red()},
    {"name": "Opps Crashed the Party", "description": "Six of them walked up from the alley. {member} tried to de-escalate but one went straight for confrontation. Full brawl in the street.", "type": "brawl", "color": discord.Color.red()},
    {"name": "Rival Hood Walked Through", "description": "A group from a rival neighborhood showed up uninvited and started mugging for the cameras. {member} stepped up and it turned physical fast.", "type": "brawl", "color": discord.Color.red()},
    {"name": "Dice Game Fight", "description": "A dice game on the side street turned into a stabbing situation. {member} tried to pull people apart. By the time it was over two people were bleeding and the party was done.", "type": "brawl", "color": discord.Color.red()},
    {"name": "Police Rolled Through", "description": "Two patrol cars parked at opposite ends. Officers asked questions nobody answered. {member} kept the crew calm. They left after forty minutes.", "type": "police_harassment", "color": discord.Color.blue()},
    {"name": "Helicopter Circled for an Hour", "description": "A police helicopter circled the block with a spotlight for over an hour. {member} kept people from scattering but the vibe was killed completely.", "type": "police_harassment", "color": discord.Color.blue()},
    {"name": "Noise Complaint Cops", "description": "Officers came through on a noise complaint and started looking for reasons to escalate. {member} turned the music down and kept everyone calm. They eventually left.", "type": "police_harassment", "color": discord.Color.blue()},
    {"name": "Task Force Showed Up", "description": "Four unmarked cars hit simultaneously. Task force moved through demanding ID. {member} got detained two hours then released.", "type": "police_raid", "color": discord.Color.blue()},
    {"name": "Police Arrested Several", "description": "Officers started running warrants after dark. {member} watched crew members get walked to patrol cars in front of the whole neighborhood.", "type": "police_arrests", "color": discord.Color.blue()},
    {"name": "Undercover in the Crowd", "description": "Word came back through a lawyer two days later -- undercovers had been in the crowd the whole time. **{name}** went quiet immediately.", "type": "rep_down", "value": (30, 80), "color": discord.Color.orange()},
    {"name": "Fight Broke Out", "description": "Something small escalated fast. {member} tried to step in but it spread. Tables down, food everywhere. The party became a crime scene.", "type": "rep_down", "value": (20, 60), "color": discord.Color.orange()},
    {"name": "Someone Got Stabbed", "description": "The ambulance showed up to **{name}**'s party. Nobody saw who or why. It was on their block, under their name.", "type": "rep_down", "value": (40, 100), "color": discord.Color.orange()},
    {"name": "Generator Blew", "description": "The generator powering the sound system blew two hours in. Music gone, lights gone. Half the crowd left in twenty minutes. {member} couldn't recover the energy.", "type": "rep_down", "value": (15, 45), "color": discord.Color.orange()},
    {"name": "Food Ran Out Early", "description": "{member} underestimated the turnout. Food was gone by 7pm. People who came hungry left angry. **{name}** will hear about this.", "type": "rep_down", "value": (15, 40), "color": discord.Color.orange()},
    {"name": "Drunk Uncle Caused a Scene", "description": "A family member of someone in **{name}** got drunk and started yelling things that should never be said publicly. {member} had to physically remove them. It was recorded.", "type": "rep_down", "value": (20, 55), "color": discord.Color.orange()},
    {"name": "Rain Killed the Vibe", "description": "Sky opened up an hour in. People scattered, food soaked, equipment damaged. **{name}** spent the money for nothing.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Turnout Was Low", "description": "Setup was solid but people didn't show. {member} stood at a half-empty block for three hours. Just a quiet night.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Wrong Weekend", "description": "Two other events were happening in the hood the same night. {member} didn't know until it was too late. The crowd split three ways. **{name}** will plan better next time.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Sound System Never Arrived", "description": "The DJ backed out last minute and the backup speaker blew in the first hour. {member} tried to keep it going on phone speakers. Nobody stayed.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Permit Issue", "description": "The city showed up with a cease and desist before the party even got started. {member} kept it peaceful but the block party was over before it began.", "type": "nothing", "color": discord.Color.greyple()},
]

# Bot Events

COMMANDS = {
    "gang": handle_gang,
    "show": handle_show,
    "mission": handle_mission,
    "slide": handle_slide,
    "recruit": handle_recruit,
    "revenge": handle_revenge,
    "block": handle_block,
    "solo": handle_solo,
    "dp": handle_dp,
    "delete": handle_delete,
}

@bot.event
async def on_ready():
    print(f'{bot.user} is online')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.guild is None:
        await message.channel.send("Commands only work in servers, not DMs.")
        return

    parts = message.content.strip().split()
    if not parts:
        return

    cmd = parts[0].lower()
    args = parts[1:]

    if cmd in COMMANDS:
        try:
            await COMMANDS[cmd](message, args)
        except discord.HTTPException as e:
            print(f"HTTP error in {cmd}: {e}")
        except Exception as e:
            print(f"Error in {cmd}: {e}")

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env")
    else:
        keep_alive()
        bot.run(TOKEN)
