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

MSG_DELAY = 4.5

# ─── Helpers ───────────────────────────────────────────────────────────────────

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
    return bool(member['jail_until'] and time.time() < member['jail_until'])

def get_free_members(gang):
    return [m for m in gang['members'] if m['alive'] and not is_jailed(m)]

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
    except discord.HTTPException:
        pass

# ─── Story Lines ───────────────────────────────────────────────────────────────

WIN_LINES = [
    "{m} was the first one out the car before it even stopped moving. Had eyes on the target the whole ride and the moment his feet hit the pavement he was already squeezing. Dropped two before they registered what was happening.",
    "{m} came in from the alley where nobody was watching. Crept the full length of the block in the dark, waited for the right moment, stepped out and handled every one of them. Walked back like a ghost. Nobody saw a face.",
    "{m} pulled up on the opp's shot caller directly — none of the foot soldiers, straight to the top. Four seconds of words before {m} made it clear this wasn't a conversation. Left a message the whole set would understand.",
    "{m} had been sitting on the location for six hours before the crew pulled up. Already mapped every exit, counted heads, picked the angle. When it went down it was over in under a minute.",
    "{m} rushed straight into the middle of their whole group without hesitating — no backup, no cover, just moved. Opps scattered. Three didn't get far enough.",
    "{m} caught the opp's lieutenant alone coming out the back of the trap house at the worst possible time. Blocked the exit, left a reminder of who owns these streets.",
    "{m} moved through the block like he had a map memorized. Hit the first two before they looked up, kept moving, caught a third trying to reach a car. Sirens were still miles out when the crew was already gone.",
    "{m} waited until the shift changed and the block was thinnest, then struck with everything. By the time the opps realized how bad they were outnumbered it was already over.",
    "{m} had been watching their patterns for three days. Knew exactly when the corner would be down to two people and hit that window. Precision over power — surgical.",
    "{m} set up a fake meet through a mutual and used it to hit them where it hurt most. Took the stash, left a message, walked out with the situation flipped entirely.",
    "{m} went in through the back while the crew created a distraction at the front. Opps split their attention and that half-second of confusion was all {m} needed. Came out clean.",
]

FRIENDLY_LOSS_LINES = [
    "`{c}` caught a round in the chest during the exchange. Stayed on his feet long enough to make it back to the car but was gone before they reached the block. Won the fight but lost somebody real tonight.",
    "`{c}` took a shot from behind a car on the far end of the block. The crew didn't realize until they were pulling off. He didn't make it to the hospital.",
    "One of the opps who was already down got a last shot off. `{c}` caught it in the neck. Set held the block but held a funeral three days later.",
    "`{c}` took a stray — wrong place, wrong angle, bad luck. The streets claimed another one. Set won the slide but the victory felt hollow.",
    "`{c}` pushed too deep without cover and got cut off. By the time the crew circled back it was too late. Another name on the wall.",
    "`{c}` was covering the exit when a shooter appeared from a second floor window nobody had eyes on. Two shots to the back. Gone before the ambulance was called.",
]

JAIL_WIN_LINES = [
    "Task force had been sitting on the block all week. `{j}` got flagged leaving the scene — plate ran, warrant pulled. Facing {s} and the DA isn't offering anything.",
    "A neighbor two houses down had a camera and handed the footage over the next morning. `{j}`'s face was clear on four frames. Picked up at a family member's house by noon. {s} sentence.",
    "Somebody talked. `{j}`'s description was in the system before sunrise. Knocked at the gas station the following evening. {s} — no bail hearing for thirty days.",
    "`{j}` went back to check on things and rolled straight into a plainclothes unit. Didn't realize until the cuffs were on. {s} and the lawyer isn't optimistic.",
    "Phone records put `{j}` at the exact location. Federal involvement made bail impossible. {s} and every appeal got denied.",
]

DEATH_LINES = [
    "`{m}` moved first and caught the first shot because of it. Took two rounds before he hit the ground and never got back up. The crew had to leave him there.",
    "`{m}` got cut off when the opps came from a second direction nobody had seen. Cornered between two buildings. They found the body two hours after the crew made it back.",
    "`{m}` took a shot through a car window trying to cover the others. The bullet hit something vital. Gone before anyone could get to him.",
    "The opps had numbers and positioning the crew didn't account for. `{m}` caught the worst of it — in the open with nowhere to go. Died on that block.",
    "`{m}` stood his ground even when the crew fell back. Refused to leave until everyone was out. That decision cost him his life.",
    "A shooter came from a rooftop nobody had checked. `{m}` never saw where it came from. Dropped in the middle of the street.",
    "`{m}` tried to make it to the car but the opps had the exit cut off. Took three shots trying to push through. Collapsed ten feet short of the door.",
    "`{m}` took a round to the stomach early and kept fighting for two more minutes before the blood loss caught up. He went out swinging.",
]

CAUGHT_LINES = [
    "`{m}` made it out but the block was already surrounded by the time they reached the car. Hemmed up at the intersection a quarter mile away. {s} and not getting out on bail.",
    "`{m}` ran through back streets for twenty minutes before collapsing two neighborhoods over. Patrol unit found them on a curb. {s} — DA stacked every charge.",
    "`{m}` escaped the gunfire but a helicopter was already in the air. Tracked six blocks and taken down by a K9 unit. Facing {s}.",
    "Cameras on the bus route caught `{m}`'s full face. Task force knocked the next morning with a warrant already signed. {s} — no negotiating.",
    "`{m}` made it back to the hood but somebody on the block was already talking to detectives. Scooped up on the porch the next afternoon. {s} sentence.",
    "The getaway car broke down four blocks away. `{m}` was still in it when the first patrol unit rolled up. {s} — caught red handed.",
]

SURVIVED_LINES = [
    "`{m}` took a round through the shoulder that spun him around but kept moving. Made it back bleeding through his shirt, jaw tight, not a word the whole drive. Alive.",
    "`{m}` dove behind a parked truck and stayed flat for four minutes while rounds hit the vehicle above him. Crawled to the alley when it went quiet and made it back on foot.",
    "`{m}` caught a graze across the ribs — burned like fire but not fatal. Wrapped it with a shirt in the backseat. Walked into the trap house two hours later like nothing happened.",
    "`{m}` took a hit in the leg but refused to go down. Leaned on the car door the whole ride back and bit through the pain without a sound. Still in it.",
    "`{m}` took a pistol grip to the face — cut above the eye, nose broken, vision blurred. Made it out but took a beating the whole set saw.",
    "`{m}` ran the wrong direction and got cornered in a dead end. Had to climb a fence with shots landing around his feet. Landed hard. Got back to the block two hours later.",
]

SOLO_WIN_LINES = [
    "{m} moved through the dark like he'd been planning this for weeks. Found the opp alone outside a store two blocks into enemy territory, waited for the right moment, and handled it clean. Walked back without a scratch.",
    "{m} tracked the target's routine for four days. Caught him at the worst possible moment — alone, no backup, no exit. Over in under thirty seconds.",
    "{m} went out solo against everyone's advice and came back with a body count that silenced every doubt. Back home before midnight like nothing happened.",
    "{m} didn't ask for permission and didn't wait for backup. Spotted an opportunity, took it, executed it perfectly. One opp down, message sent.",
    "There was a name that needed to be handled and {m} volunteered without hesitation. Moved alone through three enemy blocks and made sure the message was unmistakable.",
    "{m} set up the whole thing personally — scouted the location, timed the approach, picked the angle. The target never saw it coming. Solo. Clean. Permanent.",
]

SOLO_SURVIVED_LINES = [
    "{m} made it back but barely. Took a round to the arm on the way out. Wrapped it with a belt in the alley and walked six blocks back in the dark. Alive but marked.",
    "{m} got made before the approach was complete. Had to run three blocks with shots landing behind him. Made it over a fence and sat in the dark for two hours before it was safe to move.",
    "{m} took a hit to the ribs that cracked something. Couldn't breathe right the whole way back. Refused the hospital. The mission didn't go right but {m} came home.",
    "The opp had backup nobody knew about. {m} fought through two of them and made it out the side but caught a graze across the neck in the process. An inch deeper and it would've been over.",
    "{m} walked into something bigger than expected. Outnumbered three to one. Made it out with a broken hand and a split face. Came back breathing. That counts.",
]

SOLO_JAILED_LINES = [
    "{m} handled the business clean but ran a red light four blocks from the scene with blood on the jacket. Everything unraveled from that traffic stop. Facing {s} and the lawyer isn't saying much.",
    "{m} didn't realize the area had been under surveillance for two weeks. Detectives had a name and face before sunrise. Got knocked at 6am with a warrant already signed. {s} — no bail.",
    "A witness got a clear look and called it in immediately. {m} was less than a mile away when the description went out. Three patrol units converged. {s} sentence.",
    "{m} got back to the block and thought it was over. Two days later task force knocked with photos, phone records, cell tower data. The case was already built. {s}.",
    "The opp's people knew who was responsible within an hour and passed the name directly to detectives. {m} was picked up at a family gathering the next afternoon. {s}.",
]

SOLO_KILLED_LINES = [
    "{m} went out alone and didn't come back. Went deep into enemy territory, got cut off, took three shots before going down. The block held a vigil two nights later. Another name on the wall.",
    "{m} moved solo and ran into more than expected. Fought until there was nothing left to fight with. The body was found before morning. The grief hit the whole crew at once.",
    "The opp's neighborhood was more locked down than anyone realized. {m} got spotted the moment they crossed the boundary and never made it to the target. Surrounded. No exit.",
    "{m} almost made it out. Was within two blocks of safety when they got cut off from behind. The shots came fast. By the time anyone could get there it was already over.",
    "Going solo was the choice {m} made and the streets don't negotiate with that kind of courage. Made it to the target, handled the business, and caught three on the way out. Didn't make it back.",
]

EVENTS = [
    {"name": "Corner Locked Down", "description": "{member} spent the whole night on Figueroa muscling every corner boy off the strip until nobody dared step foot on it. By morning **{name}** owned every inch of that block.", "type": "rep_up", "value": (20, 80), "color": discord.Color.green()},
    {"name": "Successful Lick", "description": "{member} moved quiet and precise — scoped the target for two days, waited for the perfect moment, and walked away clean with enough to keep **{name}** comfortable for months.", "type": "rep_up", "value": (30, 100), "color": discord.Color.green()},
    {"name": "Street Fight Victory", "description": "{member} ran into four of the opps outside the liquor store on Central and didn't hesitate. Squared up solo, dropped two of them, and walked away without a scratch. **{name}**'s name rang out before the night was over.", "type": "rep_up", "value": (20, 60), "color": discord.Color.green()},
    {"name": "Territory Claimed", "description": "**{name}** moved on a new block the opps had been sitting on for months. {member} led the crew in, posted up in broad daylight, and dared anyone to say something. Nobody did.", "type": "rep_up", "value": (40, 120), "color": discord.Color.green()},
    {"name": "OG Vouched", "description": "One of the most respected OGs in the city pulled {member} aside — he had been watching **{name}** and they were doing it right. He made a few calls that night. Doors opened that nobody knew existed.", "type": "rep_up", "value": (50, 150), "color": discord.Color.green()},
    {"name": "Retaliation Hit", "description": "The opps disrespected **{name}** at a vigil last week. {member} didn't forget. Waited a full week, showed up at exactly the right time and delivered the message personally. The streets went quiet after that.", "type": "rep_up", "value": (60, 180), "color": discord.Color.green()},
    {"name": "Prison Connects Made", "description": "{member} got word inside through a cousin doing a stretch at Corcoran. Made the right introductions and now **{name}** has connects in three different facilities. Business doesn't stop because somebody is locked up.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Rival Scattered", "description": "{member} pulled up on the opposition's main corner with the whole crew and gave them one warning. **{name}** hit back so hard that within 48 hours the opps had abandoned three blocks without a shot fired.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    {"name": "Rapper Shoutout", "description": "A certified street rapper dropped a project and buried {member}'s name in two tracks — hood and **{name}** repped fully. People from three cities were asking about the set by the next morning.", "type": "rep_up", "value": (50, 130), "color": discord.Color.green()},
    {"name": "Fed the Block", "description": "{member} threw a full cookout — ribs, water, music. Families came out, elders dapped up the crew, kids who never talked to **{name}** were showing love. Community locked in solid.", "type": "rep_up", "value": (25, 70), "color": discord.Color.green()},
    {"name": "Big Score", "description": "{member} linked up with a connect through a third party and set up the biggest score **{name}** had seen in years. Product moved fast, money came back clean, every member of the crew ate.", "type": "rep_up", "value": (60, 160), "color": discord.Color.green()},
    {"name": "Took the Block Back", "description": "The opps had been sitting on a block that used to belong to **{name}** for six months. {member} organized it — right time, right numbers. Moved at 2am and by sunrise that block was flying **{name}**'s colors again.", "type": "rep_up", "value": (70, 170), "color": discord.Color.green()},
    {"name": "Put in Work", "description": "There was a name on a list. {member} didn't ask questions, didn't ask for extra. Said when and where and got it done quietly with no trail. **{name}** moves different because of soldiers like that.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    {"name": "Court Case Dismissed", "description": "{member} had been facing serious charges for months. The DA's key witness stopped cooperating and the case fell apart. {member} walked out of the courthouse and came straight back to the block. **{name}** is at full strength.", "type": "rep_up", "value": (40, 110), "color": discord.Color.green()},
    {"name": "Neighborhood Loyalty", "description": "Three different families on the block independently told detectives they saw nothing when investigators came around asking about **{name}**. {member} built that loyalty over years. Now it's paying off.", "type": "rep_up", "value": (35, 95), "color": discord.Color.green()},
    {"name": "New Connect", "description": "{member} got introduced to a supplier through a mutual who vouched for **{name}** personally. First order came in clean, the price was right, quality was better than anything the set had worked with before. The operation just leveled up.", "type": "rep_up", "value": (60, 150), "color": discord.Color.green()},
    {"name": "Snitch in the Ranks", "description": "The feds had been watching **{name}** for weeks and nobody could figure out how they knew so much. Then a sealed document leaked — {member}'s name was on it. Cooperating since the summer. The set is fractured. Trust is gone.", "type": "rep_down", "value": (30, 100), "color": discord.Color.orange(), "snitch": True},
    {"name": "Botched Mission", "description": "{member} had one job — get in, handle it, get out. Instead froze at the wrong moment, had to abort. Three people on the block filmed the whole thing from their porch. **{name}** is a punchline on the streets right now.", "type": "rep_down", "value": (20, 80), "color": discord.Color.orange()},
    {"name": "Homie Got Knocked", "description": "Task force rolled up on {member} sitting outside with product on them and a warrant already signed. Bail was denied. **{name}** lost one of their most solid members overnight.", "type": "rep_down", "value": (40, 120), "color": discord.Color.orange()},
    {"name": "Ran Off the Block", "description": "The opps pulled up three cars deep at shift change when **{name}** only had two people on the corner. {member} tried to hold it but the math wasn't there. Whole hood saw it happen in real time.", "type": "rep_down", "value": (50, 150), "color": discord.Color.orange()},
    {"name": "Internal Beef", "description": "{member} and another member of **{name}** got into a bad argument over money that turned physical right outside the trap house. Neighbors recorded it. Other sets are sharing the video and laughing.", "type": "rep_down", "value": (25, 75), "color": discord.Color.orange()},
    {"name": "LAPD Raid", "description": "Forty officers hit **{name}**'s main spot at 5am with a no-knock warrant. {member} barely got out the back before the doors came down. Everything got seized — product, cash, phones, weapons. The whole operation is on pause.", "type": "rep_down", "value": (60, 180), "color": discord.Color.orange()},
    {"name": "Caught Lacking", "description": "The opps caught {member} alone at a gas station on the wrong side of town repping **{name}** with nowhere to run. Took everything off them, recorded it, and posted it online before {member} even made it back to the hood.", "type": "rep_down", "value": (30, 90), "color": discord.Color.orange()},
    {"name": "Lost the Package", "description": "{member} was moving a major package cross-town and made a wrong decision. Whether it got taken by the opps or seized at a checkpoint — **{name}** lost the product, lost the money, and the connect is threatening to cut them off.", "type": "rep_down", "value": (45, 130), "color": discord.Color.orange()},
    {"name": "Homie Flipped", "description": "{member} had been facing a fifteen-year bid and nobody knew they were cooperating for months. The DA announced indictments on a Tuesday morning. **{name}** lost four members to federal charges in one day.", "type": "rep_down", "value": (50, 160), "color": discord.Color.orange(), "snitch": True},
    {"name": "Jumped by Opps", "description": "Eight of the opposition cornered {member} two blocks from home in the afternoon with witnesses everywhere. Beat them down for a full minute while people recorded. **{name}**'s name is attached to that video and the streets are not letting it go.", "type": "rep_down", "value": (35, 110), "color": discord.Color.orange()},
    {"name": "Stash House Burned", "description": "Somebody gave up the location of **{name}**'s secondary stash house. The opps hit it at noon when it was lightly guarded — {member} barely made it out the back window. Months of work wiped out in under ten minutes.", "type": "rep_down", "value": (55, 150), "color": discord.Color.orange()},
    {"name": "Quiet Night", "description": "{member} held down the corner all night — stayed alert, watched the block, kept things moving. Nothing to report. Sometimes the streets just go still. **{name}** is positioned and ready.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Laying Low", "description": "Too much heat in the area — patrol cars circling every hour, unfamiliar faces asking questions, word that the task force has been running plates. {member} made the call to keep **{name}** off the corners tonight. Smart move.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Watching and Waiting", "description": "{member} spent the night riding through the area, getting eyes on enemy positions, counting heads, logging patterns. No action tonight — reconnaissance. **{name}** is building a picture.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Regrouping", "description": "After recent events the crew needed a night to regroup. {member} called everyone in, sat them down, had a real conversation about what went wrong and what needs to change. **{name}** came out of that meeting more focused.", "type": "nothing", "color": discord.Color.greyple()},
]

BLOCK_PARTY_EVENTS = [
    {"name": "Block Party Jumping", "description": "The whole hood came out. Music rattling windows two blocks over, kids on bikes, OGs on lawn chairs. {member} kept the energy right all night — making sure everyone was fed and **{name}**'s name stayed on every lip.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Community Showed Love", "description": "Families from three streets over came through specifically because they heard **{name}** was throwing it down. {member} made sure every person felt welcome — passed out food personally, checked on the elders.", "type": "rep_up", "value": (30, 80), "color": discord.Color.green()},
    {"name": "Local Legend Pulled Up", "description": "A respected OG who hadn't been seen publicly in years showed up unannounced and spent two hours at **{name}**'s block party. Sat with {member} for a long time. Gave his blessing in front of everyone who mattered.", "type": "rep_up", "value": (50, 130), "color": discord.Color.green()},
    {"name": "Rival Set Sent a Message", "description": "Word got back before midnight that a rival set had sent someone through to check if it was real. When they reported back — food, families, no trap — the rival set sent a message through a mutual: they respected the move.", "type": "rep_up", "value": (35, 90), "color": discord.Color.green()},
    {"name": "Block Party Goes All Night", "description": "What started at 4pm was still going strong at 2am. {member} kept refilling the food, kept the speakers on. People who had to work the next morning stayed anyway. The whole block was fed and reminded why **{name}** runs this hood.", "type": "rep_up", "value": (45, 110), "color": discord.Color.green()},
    {"name": "News Crew Showed Up", "description": "A local news segment came through to film. {member} handled the camera perfectly — spoke about giving back, never said anything that could be used wrong. The segment aired the next morning.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Young Ones Got Recruited", "description": "Three younger kids from the block spent the whole party watching how **{name}** moved. Before the night was over all three had made it clear they wanted in. The set is growing from the roots up.", "type": "rep_up", "value": (25, 65), "color": discord.Color.green()},
    {"name": "Driveby — Party Shot Up", "description": "Everything was going right until a dark car rolled through slow from the north end of the block. {member} saw it coming a half second before it started but there was no time. Shots fired into the crowd before the car accelerated and disappeared.", "type": "driveby", "color": discord.Color.dark_red()},
    {"name": "Driveby — Second Pass", "description": "The first pass was just to see who flinched. {member} tried to get people moving but the second car came from the opposite direction before anyone could regroup. Two vehicles, two angles. By the time it was over the block was empty.", "type": "driveby", "color": discord.Color.dark_red()},
    {"name": "Opps Crashed the Party", "description": "Six of them walked up from the alley acting like they belonged. {member} clocked them immediately and tried to de-escalate but one of the opps went straight for confrontation. Full brawl in the middle of the street. Three people got hurt before it broke up.", "type": "brawl", "color": discord.Color.red()},
    {"name": "Police Rolled Through", "description": "Two patrol cars pulled up slow around 9pm and parked at opposite ends of the block. Officers walked through asking questions nobody was going to answer. {member} kept the crew calm. After forty minutes with nothing to show for it the officers left.", "type": "police_harassment", "color": discord.Color.blue()},
    {"name": "Task Force Showed Up", "description": "Four unmarked cars and a van pulled up simultaneously from different directions. Task force in tactical gear moved through the crowd demanding ID, running names. {member} got detained for two hours before being released without charges.", "type": "police_raid", "color": discord.Color.blue()},
    {"name": "Police Arrested Several", "description": "Officers came through on foot shortly after dark and started running warrants. {member} watched helplessly as crew members got walked to patrol cars in front of the whole neighborhood. The party was over the moment the first cuffs came out.", "type": "police_arrests", "color": discord.Color.blue()},
    {"name": "Undercover in the Crowd", "description": "Two days after the party, word came back through a lawyer that undercover officers had been in the crowd the entire time taking photos and recording conversations. {member} hadn't noticed anything off. **{name}** went quiet immediately.", "type": "rep_down", "value": (30, 80), "color": discord.Color.orange()},
    {"name": "Fight Broke Out", "description": "An argument over something small escalated faster than anyone expected. {member} tried to step in but by then it had spread to a full brawl. Tables knocked over, food everywhere, people running. The block party became a crime scene.", "type": "rep_down", "value": (20, 60), "color": discord.Color.orange()},
    {"name": "Someone Got Stabbed", "description": "Nobody saw who did it or why but the ambulance showed up to **{name}**'s block party for someone who had been stabbed. {member} didn't know the victim but it didn't matter — it was on their block, under their name.", "type": "rep_down", "value": (40, 100), "color": discord.Color.orange()},
    {"name": "Rain Killed the Vibe", "description": "It had been sunny all week until it wasn't. {member} had everything set up perfectly when the sky opened up an hour in. People scattered, food got soaked, equipment got damaged. **{name}** spent the money but the neighborhood barely got to enjoy it.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Turnout Was Low", "description": "The word got out and the setup was solid but people just didn't show up the way they were supposed to. {member} stood at a half-empty block for three hours wondering what went wrong. **{name}** put in the effort but it was a quiet night.", "type": "nothing", "color": discord.Color.greyple()},
]

# ─── Slide Logic ───────────────────────────────────────────────────────────────

def calculate_slide_outcome(gang, rolling_members, enemy_rep, is_revenge=False):
    player_rep = gang['rep']
    rep_diff = player_rep - enemy_rep
    win_chance = max(10, min(90, 50 + int((rep_diff / 500) * 40)))
    if is_revenge:
        win_chance = min(95, win_chance + 10)

    player_won = random.randint(1, 100) <= win_chance
    outcome_lines = []
    kills_this_fight = {}

    if player_won:
        rep_gain = random.randint(20, max(1, int(enemy_rep * 0.4)))
        if is_revenge:
            rep_gain = int(rep_gain * 1.25)
        gang['rep'] = player_rep + rep_gain
        gang['fights_won'] = gang.get('fights_won', 0) + 1

        for m in rolling_members:
            m['kills'] += 1
            m['missions_survived'] += 1
            kills_this_fight[m['name']] = kills_this_fight.get(m['name'], 0) + 1
            outcome_lines.append(("win", random.choice(WIN_LINES).replace("{m}", f"`{m['name']}`")))

        # Friendly casualty chance
        free_rolling = [m for m in rolling_members if not is_jailed(m)]
        if len(get_alive_members(gang)) > 1 and random.randint(1, 100) <= 20 and free_rolling:
            c = random.choice(free_rolling)
            c['alive'] = False
            c['deaths'] += 1
            outcome_lines.append(("loss", random.choice(FRIENDLY_LOSS_LINES).replace("{c}", c['name'])))

        # Jailed after win
        if random.randint(1, 100) <= 15:
            free_rolling2 = [m for m in rolling_members if m['alive'] and not is_jailed(m)]
            if free_rolling2:
                j = random.choice(free_rolling2)
                s = send_to_jail(j)
                outcome_lines.append(("jail", random.choice(JAIL_WIN_LINES).replace("{j}", f"`{j['name']}`").replace("{s}", s)))

        return {"won": True, "rep_gain": rep_gain, "old_rep": player_rep, "new_rep": gang['rep'],
                "enemy_rep": enemy_rep, "outcome_lines": outcome_lines, "kills_this_fight": kills_this_fight,
                "members_alive": len(get_alive_members(gang))}
    else:
        gang['fights_lost'] = gang.get('fights_lost', 0) + 1

        for m in rolling_members:
            if is_jailed(m):
                continue
            if len(get_alive_members(gang)) > 1 and random.randint(1, 100) <= 40:
                m['alive'] = False
                m['deaths'] += 1
                outcome_lines.append(("death", random.choice(DEATH_LINES).replace("{m}", f"`{m['name']}`")))
            elif random.randint(1, 100) <= 30:
                s = send_to_jail(m)
                outcome_lines.append(("jail", random.choice(CAUGHT_LINES).replace("{m}", f"`{m['name']}`").replace("{s}", s)))
            else:
                m['missions_survived'] += 1
                outcome_lines.append(("survived", random.choice(SURVIVED_LINES).replace("{m}", f"`{m['name']}`")))

        rep_loss = random.randint(20, max(1, int(player_rep * 0.25)))
        gang['rep'] = max(1, player_rep - rep_loss)

        return {"won": False, "rep_loss": player_rep - gang['rep'], "old_rep": player_rep, "new_rep": gang['rep'],
                "enemy_rep": enemy_rep, "outcome_lines": outcome_lines, "kills_this_fight": kills_this_fight,
                "members_alive": len(get_alive_members(gang))}


async def send_slide_result(channel, gang, enemy_info, result, is_revenge=False):
    # Color map per outcome type
    type_colors = {
        "win": discord.Color.green(),
        "loss": discord.Color.dark_red(),
        "death": discord.Color.dark_grey(),
        "jail": discord.Color.blue(),
        "survived": discord.Color.orange(),
    }

    overall_color = discord.Color.green() if result['won'] else discord.Color.orange()

    if result['won']:
        title = "Revenge Collected" if is_revenge else "Slide Won"
        cred_line = f"Cred: {result['old_rep']} → {result['new_rep']} (+{result['rep_gain']})"
        footer = "They know not to touch yours again." if is_revenge else "Hold that block."
    else:
        title = "Revenge Failed" if is_revenge else "Slide Lost"
        cred_line = f"Cred: {result['old_rep']} → {result['new_rep']} (-{result['rep_loss']})"
        footer = "Regroup. Come back harder."

    # Header embed — clean, no inline fields
    header = discord.Embed(title=title, color=overall_color)
    header.description = (
        f"**{gang['name']}** vs **{enemy_info['name']}**\n"
        f"Opp Cred: {result['enemy_rep']}\n"
        f"{cred_line}\n"
        f"Members Still Alive: {result['members_alive']}"
    )
    await safe_send(channel, embed=header)
    await asyncio.sleep(MSG_DELAY)

    # One embed per outcome line
    for i, (line_type, line_text) in enumerate(result['outcome_lines']):
        color = type_colors.get(line_type, overall_color)
        embed = discord.Embed(description=line_text, color=color)
        embed.set_footer(text=f"{i + 1} of {len(result['outcome_lines'])}")
        await safe_send(channel, embed=embed)
        await asyncio.sleep(MSG_DELAY)

    # Summary embed
    if result['kills_this_fight']:
        kills_text = "\n".join(
            f"`{n}` — {k} kill{'s' if k != 1 else ''}" for n, k in result['kills_this_fight'].items()
        )
    else:
        kills_text = "No bodies this run."

    summary = discord.Embed(title="Run Summary", description=kills_text, color=overall_color)
    summary.set_footer(text=footer)
    await safe_send(channel, embed=summary)


# ─── Commands ─────────────────────────────────────────────────────────────────

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
        description=f"You just got put on with **{la_gang['name']}**.",
        color=discord.Color.dark_grey()
    )
    embed.description += (
        f"\n\nHood: {la_gang['hood']}"
        f"\nShot Caller: `{members[0]['name']}`"
        f"\nStreet Cred: {rep}"
        f"\nMembers: {len(members)}"
        f"\nCode: `{code}`"
        f"\n\n{member_lines}"
    )
    embed.set_footer(text="mission | slide | recruit | revenge | block | solo | show | delete")
    await safe_send(message.channel, embed=embed)


async def handle_show(message, args):
    user_id = message.author.id
    user_gangs = [g for g in gangs.values() if g['owner_id'] == user_id]

    if not user_gangs:
        await safe_send(message.channel, content="You got no crew. Type `gang` to start one.")
        return

    alive_gangs = [g for g in user_gangs if g['alive']]
    dead_count = len(user_gangs) - len(alive_gangs)

    # ── Embed 1: Active crew stats + living roster ──
    embed = discord.Embed(
        title=f"{message.author.name}'s Crew",
        description=f"Active: {len(alive_gangs)}   |   Disbanded: {dead_count}",
        color=discord.Color.dark_grey()
    )

    if alive_gangs:
        for g in alive_gangs:
            fw = g.get('fights_won', 0)
            fl = g.get('fights_lost', 0)
            total = fw + fl
            win_rate = f"{int((fw / total) * 100)}%" if total > 0 else "N/A"
            targets = get_revenge_targets(g)

            blood_owed = ""
            if targets:
                blood_owed = "\n" + "\n".join(f"Blood Owed: `{t['name']}` | {t['gang']}" for t in targets)

            embed.description += (
                f"\n\n**{g['name']}**"
                f"\nHood: {g.get('hood', 'Unknown')}"
                f"\nCode: `{g['code']}`"
                f"\nShot Caller: `{g.get('leader', 'Unknown')}`"
                f"\nStreet Cred: {g['rep']}"
                f"\nRecord: {fw}W — {fl}L   Win Rate: {win_rate}"
                f"\nKills: {get_gang_bodies(g)}   Deaths: {get_gang_deaths(g)}"
                f"\nAlive: {len(get_alive_members(g))}   Free: {len(get_free_members(g))}"
                + blood_owed
            )

            # Living roster
            alive = get_alive_members(g)
            if alive:
                roster_lines = "\n".join(
                    f"`{m['name']}` | {m['kills']}K | {get_member_status(m)}" for m in alive
                )
                embed.add_field(name=f"{g['name']} — Active Roster", value=roster_lines, inline=False)
    else:
        embed.description += "\n\nNo active crew. Type `gang` to start fresh."

    embed.set_footer(text="mission | slide | recruit | revenge | block | solo | show | delete")
    await safe_send(message.channel, embed=embed)

    # ── Embed 2: Dead homies (only if there are any) ──
    has_dead = any(get_dead_members(g) for g in alive_gangs)
    if has_dead:
        rip_embed = discord.Embed(
            title="🕯️ Rest In Power",
            description="Homies who fell in the streets. Their names stay on the wall.",
            color=discord.Color.dark_grey()
        )
        for g in alive_gangs:
            dead = get_dead_members(g)
            if dead:
                dead_lines = "\n".join(
                    f"`{m['name']}` | {m['kills']} kills | {m['deaths']} death{'s' if m['deaths'] != 1 else ''}"
                    for m in dead
                )
                rip_embed.add_field(name=f"{g['name']} — Fallen", value=dead_lines, inline=False)
        rip_embed.set_footer(text="Gone but not forgotten.")
        await safe_send(message.channel, embed=rip_embed)


async def handle_mission(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `mission <code>` — Example: `mission XKRV`")
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
        await safe_send(message.channel, content=f"**{gang['name']}** has no free members right now.")
        return

    member = random.choice(free)
    event = random.choice(EVENTS)
    rep = gang['rep']

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
        embed.description += f"\n\nStreet Cred: {rep} → {gang['rep']} (+{gain})"
        embed.set_footer(text="Rep rising on the streets...")

    elif event['type'] == 'rep_down':
        loss = random.randint(*event['value'])
        new_rep = max(1, rep - loss)
        actual_loss = rep - new_rep
        gang['rep'] = new_rep
        if event.get('snitch'):
            member['times_snitched'] += 1
        extra = []
        if random.randint(1, 100) <= 15 and len(get_alive_members(gang)) > 1:
            member['alive'] = False
            member['deaths'] += 1
            extra.append(f"`{member['name']}` didn't make it out.")
        elif random.randint(1, 100) <= 25:
            s = send_to_jail(member)
            extra.append(f"`{member['name']}` got knocked — {s}.")
        if extra:
            embed.description += "\n\n" + "\n".join(extra)
        embed.description += f"\n\nStreet Cred: {rep} → {gang['rep']} (-{actual_loss})"
        embed.set_footer(text="Taking an L on the streets...")

    elif event['type'] == 'nothing':
        embed.description += f"\n\nStreet Cred: {rep} (no change)"
        embed.set_footer(text="Nothing popped off tonight.")

    await safe_send(message.channel, embed=embed)


async def handle_recruit(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `recruit <code>` — Example: `recruit XKRV`")
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

    existing = {m['name'] for m in gang['members']}
    available = [n for n in STREET_NAMES if n not in existing]
    if not available:
        await safe_send(message.channel, content=f"**{gang['name']}** roster is already maxed out.")
        return

    if random.randint(1, 2) == 1:
        new_name = random.choice(available)
        gang['members'].append(make_member(new_name))
        desc = random.choice([
            f"`{new_name}` had been hanging around the block for weeks watching how **{gang['name']}** moved. Finally pulled them aside and put them on.",
            f"Word got to `{new_name}` through a mutual that **{gang['name']}** was looking. Showed up the next day ready to work.",
            f"`{new_name}` proved themselves during a situation last month nobody forgot. The decision to put them on was unanimous.",
            f"`{new_name}` grew up two blocks over and always had love for **{gang['name']}**. When the invitation came, they were ready.",
        ])
        embed = discord.Embed(title="New Member", description=desc, color=discord.Color.teal())
        embed.description += f"\n\nNew Member: `{new_name}`\nTotal Alive: {len(get_alive_members(gang))}"
        embed.set_footer(text="Keep building the set.")
    else:
        desc = random.choice([
            f"**{gang['name']}** put the word out through three different people but nobody came through.",
            f"There was a candidate — seemed solid, seemed interested. Then they just stopped answering.",
            f"The recruitment process hit a wall. People are either committed elsewhere or too scared.",
            f"Word didn't travel the way it needed to. **{gang['name']}** is out there but not everyone is ready.",
        ])
        embed = discord.Embed(title="Nobody Came Through", description=desc, color=discord.Color.dark_grey())
        embed.description += f"\n\nMembers: {len(get_alive_members(gang))}"
        embed.set_footer(text="50/50. Try again.")

    await safe_send(message.channel, embed=embed)


async def handle_slide(message, args):
    if len(args) < 2:
        await safe_send(message.channel, content="Usage: `slide <code> <number>` — Example: `slide XKRV 3`")
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
        await safe_send(message.channel, content="That needs to be a number. Example: `slide XKRV 3`")
        return

    if requested < 1:
        await safe_send(message.channel, content="You need to send at least 1 person.")
        return

    free = get_free_members(gang)
    if not free:
        await safe_send(message.channel, content=f"**{gang['name']}** has nobody free to roll out right now.")
        return

    actual = min(requested, len(free), 10)
    if actual < requested:
        await safe_send(message.channel, content=f"Only {len(free)} free. Rolling with {actual}.")

    rolling = random.sample(free, actual)
    enemy_info = random.choice(LA_GANGS)
    enemy_rep = random.randint(10, 500)
    player_rep = gang['rep']

    rolling_display = "\n".join(f"`{m['name']}`" for m in rolling)

    intro_desc = random.choice([
        f"**{gang['name']}** got word that **{enemy_info['name']}** has been running their mouth. Time to pull up.",
        f"**{enemy_info['name']}** crossed a line they can't uncross. **{gang['name']}** is loading up and heading out.",
        f"The disrespect from **{enemy_info['name']}** has been building for weeks. Tonight **{gang['name']}** settles it.",
        f"**{gang['name']}** got intel on where **{enemy_info['name']}** is posted. The crew is rolling out right now.",
    ])

    intro = discord.Embed(title="Slide", color=discord.Color.dark_red())
    intro.description = (
        f"{intro_desc}\n\n"
        f"**{gang['name']}** — Cred: {player_rep}\n"
        f"Rolling {actual} deep\n"
        f"{rolling_display}\n\n"
        f"**vs {enemy_info['name']}** — Cred: {enemy_rep}"
    )
    intro.set_footer(text="It's on...")
    await safe_send(message.channel, embed=intro)
    await asyncio.sleep(MSG_DELAY)

    alive_before = {m['name'] for m in get_alive_members(gang)}
    result = calculate_slide_outcome(gang, rolling, enemy_rep)
    alive_after = {m['name'] for m in get_alive_members(gang)}

    if alive_before - alive_after:
        add_revenge_target(gang, random.choice([m['name'] for m in generate_ai_members(1)]), enemy_info, enemy_rep)

    check_and_mark_dead(code)
    await send_slide_result(message.channel, gang, enemy_info, result)


async def handle_revenge(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `revenge <code>` — Example: `revenge XKRV`")
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
        await safe_send(message.channel, content=f"**{gang['name']}** has no blood owed right now.")
        return

    free = get_free_members(gang)
    if not free:
        await safe_send(message.channel, content=f"**{gang['name']}** has nobody free to roll out for revenge right now.")
        return

    target = random.choice(targets)
    enemy_info = target['gang_info']
    enemy_rep = target.get('enemy_rep', random.randint(10, 500))
    player_rep = gang['rep']

    rolling = random.sample(free, random.randint(1, min(3, len(free))))
    rolling_display = "\n".join(f"`{m['name']}`" for m in rolling)

    remaining = [t for t in targets if t['gang'] != enemy_info['name']]
    still_owed = ""
    if remaining:
        still_owed = "\n\nStill owed after this:\n" + "\n".join(f"**{t['gang']}** | `{t['name']}`" for t in remaining)

    intro_desc = random.choice([
        f"**{gang['name']}** hasn't slept right since they lost one of their own. Tonight they found **{enemy_info['name']}** and the crew is moving.",
        f"The grief turned to fire. **{gang['name']}** has been watching and waiting. Tonight that silence ends.",
        f"There is only one thing on **{gang['name']}**'s mind right now. **{enemy_info['name']}** is about to feel it.",
        f"**{gang['name']}** went quiet for a week — no moves, no noise, just planning. Tonight that ends.",
    ])

    intro = discord.Embed(title="Revenge", color=discord.Color.dark_red())
    intro.description = (
        f"{intro_desc}\n\n"
        f"**{gang['name']}** — Cred: {player_rep}\n"
        f"Rolling {len(rolling)} deep\n"
        f"{rolling_display}\n\n"
        f"**vs {enemy_info['name']}** — Cred: {enemy_rep}\n"
        f"Target: `{target['name']}`"
        + still_owed
    )
    intro.set_footer(text="This one is personal...")
    await safe_send(message.channel, embed=intro)
    await asyncio.sleep(MSG_DELAY)

    alive_before = {m['name'] for m in get_alive_members(gang)}
    result = calculate_slide_outcome(gang, rolling, enemy_rep, is_revenge=True)
    alive_after = {m['name'] for m in get_alive_members(gang)}

    if result['won']:
        remove_revenge_target(gang, enemy_info['name'])
    elif alive_before - alive_after:
        add_revenge_target(gang, target['name'], enemy_info, enemy_rep)

    check_and_mark_dead(code)
    await send_slide_result(message.channel, gang, enemy_info, result, is_revenge=True)

    remaining_after = get_revenge_targets(gang)
    if remaining_after:
        followup = discord.Embed(
            title="Blood Still Owed",
            description=f"**{gang['name']}** still has debts to collect.\n\n" +
                        "\n".join(f"**{t['gang']}** | `{t['name']}`" for t in remaining_after),
            color=discord.Color.dark_red()
        )
        followup.set_footer(text=f"Type `revenge {code}` again to go after another one.")
        await safe_send(message.channel, embed=followup)


async def handle_solo(message, args):
    if len(args) < 2:
        await safe_send(message.channel, content="Usage: `solo <code> <member name>` — Example: `solo XKRV Joker`")
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
        await safe_send(message.channel, content=f"No member named `{member_name}` in **{gang['name']}**.\nRoster: {roster}")
        return
    if not target['alive']:
        await safe_send(message.channel, content=f"`{target['name']}` is dead.")
        return
    if is_jailed(target):
        await safe_send(message.channel, content=f"`{target['name']}` is locked up right now.")
        return

    enemy_info = random.choice(LA_GANGS)
    enemy_rep = random.randint(10, 500)
    player_rep = gang['rep']
    win_chance = max(10, min(75, 40 + int(((player_rep - enemy_rep) / 500) * 30)))
    roll = random.randint(1, 100)

    send_off = random.choice([
        f"`{target['name']}` told nobody where they were going. Grabbed what they needed and walked out alone into the night.",
        f"No crew. No backup. No plan B. `{target['name']}` moved out solo into **{enemy_info['name']}** territory.",
        f"`{target['name']}` had been sitting on this for days. Didn't say a word to anyone. Just went. Alone.",
        f"The rest of the set didn't even know `{target['name']}` had left until the door was already closed.",
    ])

    intro = discord.Embed(title="Solo Mission", color=discord.Color.dark_red())
    intro.description = (
        f"{send_off}\n\n"
        f"Soldier: `{target['name']}` | Kills: {target['kills']}\n"
        f"Target: {enemy_info['name']} — {enemy_info['hood']}"
    )
    intro.set_footer(text="One man. No backup.")
    await safe_send(message.channel, embed=intro)
    await asyncio.sleep(MSG_DELAY)

    if roll <= win_chance:
        target['kills'] += 1
        target['missions_survived'] += 1
        rep_gain = random.randint(15, 60)
        gang['rep'] = player_rep + rep_gain
        story = random.choice(SOLO_WIN_LINES).replace("{m}", f"`{target['name']}`")
        embed = discord.Embed(title="Solo Mission — Target Down", description=story, color=discord.Color.green())
        embed.description += (
            f"\n\nSoldier: `{target['name']}` | Kills: {target['kills']}\n"
            f"Cred: {player_rep} → {gang['rep']} (+{rep_gain})"
        )
        embed.set_footer(text="Solo work. The set eats off one man's courage tonight.")

    elif roll <= win_chance + 30:
        target['missions_survived'] += 1
        rep_loss = random.randint(5, 25)
        gang['rep'] = max(1, player_rep - rep_loss)
        story = random.choice(SOLO_SURVIVED_LINES).replace("{m}", f"`{target['name']}`")
        embed = discord.Embed(title="Solo Mission — Made It Back", description=story, color=discord.Color.orange())
        embed.description += (
            f"\n\nSoldier: `{target['name']}` | Kills: {target['kills']}\n"
            f"Cred: {player_rep} → {gang['rep']} (-{rep_loss})"
        )
        embed.set_footer(text="Came back alive. That has to count for something.")

    elif roll <= win_chance + 50:
        s = send_to_jail(target)
        rep_loss = random.randint(10, 35)
        gang['rep'] = max(1, player_rep - rep_loss)
        story = random.choice(SOLO_JAILED_LINES).replace("{m}", f"`{target['name']}`").replace("{s}", s)
        embed = discord.Embed(title="Solo Mission — Knocked", description=story, color=discord.Color.blue())
        embed.description += (
            f"\n\nSoldier: `{target['name']}` | Sentence: {s}\n"
            f"Cred: {player_rep} → {gang['rep']} (-{rep_loss})"
        )
        embed.set_footer(text="One man down. The set carries on.")

    else:
        rep_loss = random.randint(20, 60)
        gang['rep'] = max(1, player_rep - rep_loss)
        story = random.choice(SOLO_KILLED_LINES).replace("{m}", f"`{target['name']}`")

        if len(get_alive_members(gang)) > 1:
            target['alive'] = False
            target['deaths'] += 1
            check_and_mark_dead(code)
            embed = discord.Embed(title="Solo Mission — Fallen", description=story, color=discord.Color.dark_grey())
            embed.description += (
                f"\n\nSoldier: `{target['name']}` | Kills: {target['kills']}\n"
                f"Cred: {player_rep} → {gang['rep']} (-{rep_loss})\n"
                f"Members Alive: {len(get_alive_members(gang))}"
            )
            embed.set_footer(text="The set lost a soldier tonight. That name stays on the wall.")
        else:
            s = send_to_jail(target)
            story = random.choice(SOLO_JAILED_LINES).replace("{m}", f"`{target['name']}`").replace("{s}", s)
            embed = discord.Embed(title="Solo Mission — Knocked", description=story, color=discord.Color.blue())
            embed.description += (
                f"\n\nSoldier: `{target['name']}` | Sentence: {s}\n"
                f"Cred: {player_rep} → {gang['rep']} (-{rep_loss})"
            )
            embed.set_footer(text="Last man standing is locked up. Hold it down.")

    await safe_send(message.channel, embed=embed)


async def handle_block(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `block <code>` — Example: `block XKRV`")
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
        await safe_send(message.channel, content=f"**{gang['name']}** has no free members to run the block party.")
        return

    host = random.choice(free)
    old_rep = gang['rep']

    setup_desc = random.choice([
        f"**{gang['name']}** is setting up on {gang['hood']}. `{host['name']}` is running point — speakers out, tables up, word spreading.",
        f"`{host['name']}` has been planning this for a week. **{gang['name']}** is about to show the hood what they're really about.",
        f"The whole crew is outside setting up. `{host['name']}` is directing everything.",
        f"**{gang['name']}** shut down the block for the night. `{host['name']}` called it three days ago.",
    ])

    setup_embed = discord.Embed(title="Block Party", color=discord.Color.dark_gold())
    setup_embed.description = (
        f"{setup_desc}\n\n"
        f"Hood: {gang['hood']}\n"
        f"Host: `{host['name']}`\n"
        f"Street Cred: {old_rep}"
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
        featured = random.choice(current_free) if current_free else host
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
                    v['alive'] = False
                    v['deaths'] += 1
                    members_killed.append(v['name'])
                    extra.append(f"`{v['name']}` was hit and didn't make it.")
            add_revenge_target(gang, killer_name, rival, rival_rep)
            ev_embed.description += (
                f"\n\nResponsible: **{rival['name']}** — `{killer_name}` pulled the trigger\n"
                f"Cred: -{loss}"
            )
            if extra:
                ev_embed.description += "\nFallen: " + ", ".join(extra)
            ev_embed.set_footer(text=f"Blood owed. Type `revenge {code}` to see your targets.")

        elif event['type'] == 'brawl':
            rival = random.choice(LA_GANGS)
            rival_rep = random.randint(30, 300)
            crasher = random.choice(STREET_NAMES)
            loss = random.randint(20, 70)
            rep_change -= loss
            cf = get_free_members(gang)
            if cf and random.randint(1, 100) <= 40:
                victim = random.choice(cf)
                s = send_to_jail(victim)
                members_jailed.append((victim['name'], s))
                extra.append(f"`{victim['name']}` got knocked during the brawl — {s}.")
            add_revenge_target(gang, crasher, rival, rival_rep)
            ev_embed.description += (
                f"\n\nWho Crashed It: **{rival['name']}** — `{crasher}` led the charge\n"
                f"Cred: -{loss}"
            )
            if extra:
                ev_embed.description += "\nLocked Up: " + ", ".join(extra)
            ev_embed.set_footer(text=f"They came to your party. Type `revenge {code}` to handle it.")

        elif event['type'] == 'police_harassment':
            loss = random.randint(10, 40)
            rep_change -= loss
            ev_embed.description += f"\n\nCred: -{loss}"

        elif event['type'] == 'police_raid':
            loss = random.randint(30, 80)
            rep_change -= loss
            cf = get_free_members(gang)
            if cf:
                arrested = random.sample(cf, min(random.randint(1, 2), len(cf)))
                for a in arrested:
                    s = send_to_jail(a)
                    members_jailed.append((a['name'], s))
                    extra.append(f"`{a['name']}` taken in — {s}.")
            ev_embed.description += f"\n\nCred: -{loss}"
            if extra:
                ev_embed.description += "\nLocked Up: " + ", ".join(extra)

        elif event['type'] == 'police_arrests':
            loss = random.randint(20, 60)
            rep_change -= loss
            cf = get_free_members(gang)
            if cf:
                arrested = random.sample(cf, min(random.randint(1, 3), len(cf)))
                for a in arrested:
                    s = send_to_jail(a)
                    members_jailed.append((a['name'], s))
                    extra.append(f"`{a['name']}` cuffed — {s}.")
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
    rep_display = f"{old_rep} → {gang['rep']} (+{rep_change})" if rep_change >= 0 else f"{old_rep} → {gang['rep']} ({rep_change})"
    footer = (
        "The hood is talking. That party put the set on a different level." if rep_change >= 80
        else ("Night is over. Block is quiet now." if rep_change >= 0 else "Not the way anyone wanted it to end.")
    )

    summary = discord.Embed(title="Block Party — Night Done", color=color)
    summary.description = (
        f"The **{gang['name']}** block party on {gang['hood']} is wrapped.\n\n"
        f"Street Cred: {rep_display}\n"
        f"Members Alive: {len(get_alive_members(gang))}\n"
        f"Members Free: {len(get_free_members(gang))}"
    )
    if members_killed:
        summary.description += "\n\nFallen Tonight:\n" + "\n".join(f"`{n}`" for n in members_killed)
    if members_jailed:
        summary.description += "\n\nLocked Up Tonight:\n" + "\n".join(f"`{n}` | {s}" for n, s in members_jailed)
    all_targets = get_revenge_targets(gang)
    if all_targets:
        summary.description += "\n\nBlood Owed:\n" + "\n".join(f"**{t['gang']}** | `{t['name']}`" for t in all_targets)
        summary.description += f"\n\nType `revenge {code}` to go after them."
    summary.set_footer(text=footer)
    await safe_send(message.channel, embed=summary)


async def handle_delete(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `delete <code>` — Example: `delete XKRV`")
        return

    code = args[0].upper()
    gang = gangs.get(code)

    if not gang:
        await safe_send(message.channel, content=f"No crew found with code `{code}`.")
        return
    if gang['owner_id'] != message.author.id and not is_admin(message):
        await safe_send(message.channel, content="That ain't your crew. You can't delete it.")
        return

    gang_name = gang['name']
    owner_id = gang['owner_id']
    del gangs[code]

    if not user_has_active_gang(owner_id):
        active_gang_owners.discard(owner_id)

    embed = discord.Embed(
        title="Crew Deleted",
        description=f"**{gang_name}** (`{code}`) has been wiped. That crew never existed. Type `gang` to start fresh.",
        color=discord.Color.dark_red()
    )
    embed.set_footer(text="Type `gang` to start a new crew.")
    await safe_send(message.channel, embed=embed)


# ─── Bot Events ────────────────────────────────────────────────────────────────

COMMANDS = {
    "gang": handle_gang,
    "show": handle_show,
    "mission": handle_mission,
    "slide": handle_slide,
    "recruit": handle_recruit,
    "revenge": handle_revenge,
    "block": handle_block,
    "solo": handle_solo,
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
