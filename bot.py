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

covens = {}
active_coven_lords = set()

VAMPIRE_NAMES = [
    "Malachar", "Seraphel", "Vexor", "Duskrane", "Noctis", "Crimson", "Lazarus",
    "Mordecai", "Belrath", "Shadowfang", "Ashveil", "Darkmore", "Vesper", "Lucian",
    "Gravian", "Thornwick", "Obsidian", "Sable", "Raven", "Phantom",
    "Wraithbone", "Nightshade", "Bloodmoon", "Dreadclaw", "Silverthorn",
    "Voidwalker", "Soulreaper", "Grimholt", "Darkspire", "Ashencroft",
    "Vlad", "Drakon", "Morbius", "Lestat", "Armand", "Kain", "Raziel",
    "Selene", "Lilith", "Morticia", "Elvira", "Carmilla", "Countess",
    "Dorian", "Damien", "Sebastian", "Lucius", "Valerian", "Caius",
    "Ptolemy", "Corvus", "Magnus", "Cassius", "Octavian", "Severus",
    "Erebus", "Thanatos", "Styx", "Acheron", "Charon", "Nemesis",
    "Orpheus", "Hermes", "Ares", "Hades", "Pluto", "Kronos",
    "Balthazar", "Mephistopheles", "Azazel", "Belial", "Abaddon", "Samael",
    "Remiel", "Uriel", "Sariel", "Raguel", "Zerachiel", "Jeremiel",
    "Fenrir", "Skoll", "Hati", "Jormungandr", "Nidhogg", "Ratatoskr",
    "Bram", "Varney", "Ruthven", "Polidori", "Byronesque", "Walpurga",
    "Desmond", "Alaric", "Godric", "Eric", "Pam", "Lorena",
    "Reginald", "Marcel", "Klaus", "Elijah", "Kol", "Finn",
    "Mikael", "Esther", "Freya", "Rebekah", "Henrik", "Niklaus",
    "Silas", "Qetsiyah", "Amara", "Tatia", "Katerina", "Nadia",
    "Isobel", "Jenna", "Alaric", "Damon", "Stefan", "Enzo",
    "Kai", "Luke", "Jo", "Liv", "Tyler", "Mason",
    "Hayley", "Jackson", "Aiden", "Paige", "Oliver", "Eve",
    "Davina", "Kara", "Genevieve", "Monique", "Abigail", "Cassie",
    "Rupert", "Giles", "Wesley", "Gunn", "Lorne", "Connor",
    "Cordelia", "Fred", "Illyria", "Harmony", "Spike", "Drusilla",
    "Darla", "Angelus", "Penn", "James", "Elizabeth", "Holden",
    "Zacharias", "Mordred", "Galahad", "Percival", "Gawain", "Tristan",
    "Lancelot", "Bedivere", "Gareth", "Lamorak", "Bors", "Pellinore",
    "Vortigern", "Uther", "Gorlois", "Lot", "Leodegrance", "Pelham",
    "Nightcrawler", "Shadowstep", "Moonwhisper", "Starfang", "Cosmidian",
    "Vantablack", "Solstice", "Equinox", "Aphelion", "Perihelion",
    "Noctivagant", "Crepuscular", "Tenebrous", "Umbral", "Penumbral",
    "Strigoi", "Revenant", "Lich", "Wraith", "Specter", "Shade",
    "Banshee", "Poltergeist", "Apparition", "Manifestation", "Haunt",
    "Gravedigger", "Tombstone", "Epitaph", "Requiem", "Elegy", "Dirge",
]

VAMPIRE_COVENS = [
    {"name": "The Crimson Court", "lair": "Castle Vanthorpe, Transylvania"},
    {"name": "Order of the Black Rose", "lair": "Abandoned Cathedral, Prague"},
    {"name": "The Nightborn Covenant", "lair": "Sunken Mansion, New Orleans"},
    {"name": "Brotherhood of Eternal Dusk", "lair": "Underground Catacombs, Paris"},
    {"name": "The Sanguine Circle", "lair": "Gothic Tower, Edinburgh"},
    {"name": "Clan Darkwater", "lair": "Fog-Shrouded Docks, London"},
    {"name": "The Obsidian Throne", "lair": "Black Fortress, Carpathian Mountains"},
    {"name": "Covenant of the Pale Moon", "lair": "Moonlit Mausoleum, Vienna"},
    {"name": "The Ashen Veil", "lair": "Ruined Abbey, Whitby"},
    {"name": "House of Eternal Night", "lair": "Underground Palace, Rome"},
    {"name": "The Bloodmoon Syndicate", "lair": "Gothic Penthouse, New York"},
    {"name": "Order of the Withered Hand", "lair": "Decaying Estate, Boston"},
    {"name": "The Shadow Conclave", "lair": "Hidden Library, Alexandria"},
    {"name": "Clan Ravenmoor", "lair": "Clifftop Manor, Cornwall"},
    {"name": "The Nocturn Assembly", "lair": "Subterranean Vault, Budapest"},
    {"name": "The Crimson Veil", "lair": "Haunted Theatre, Venice"},
    {"name": "Brotherhood of the Sleeping Dead", "lair": "Ancient Tomb, Cairo"},
    {"name": "The Umbral Court", "lair": "Mirror Palace, Versailles"},
    {"name": "Covenant of Endless Night", "lair": "Storm-Wracked Lighthouse, Ireland"},
    {"name": "House Nocturnus", "lair": "Labyrinthine Sewers, Barcelona"},
    {"name": "The Eternal Hunger", "lair": "Mountain Monastery, Bavaria"},
    {"name": "Clan Ashenveil", "lair": "Fog-Choked Marshland, Netherlands"},
    {"name": "The Dusk Sovereignty", "lair": "Marble Necropolis, Athens"},
    {"name": "Order of the Red Chalice", "lair": "Wine-Cellar Dungeon, Bordeaux"},
    {"name": "The Midnight Compact", "lair": "Clocktower Lair, Geneva"},
    {"name": "Clan Moonshroud", "lair": "Seaside Crypt, Dubrovnik"},
    {"name": "The Hollow Throne", "lair": "Frozen Fortress, Norway"},
    {"name": "Brotherhood of the Grave", "lair": "Cemetery Chapel, New England"},
    {"name": "The Bloodline Eternal", "lair": "Ancient Aqueduct, Istanbul"},
    {"name": "Covenant of the Dark Flame", "lair": "Volcano Fortress, Sicily"},
    {"name": "The Pale Dominion", "lair": "Ivory Tower, Moscow"},
    {"name": "Clan Dreadthorn", "lair": "Thorn-Choked Castle, Wales"},
    {"name": "The Veiled Congregation", "lair": "Masked Ball Hall, Florence"},
    {"name": "Order of Eternal Thirst", "lair": "Desert Tomb, Morocco"},
    {"name": "The Night Sovereignty", "lair": "Jungle Pyramid, Yucatan"},
    {"name": "Clan Voidheart", "lair": "Obsidian Monolith, Iceland"},
    {"name": "The Sable Dominion", "lair": "Underground Network, Chicago"},
    {"name": "Brotherhood of the Undying", "lair": "Sunless Cathedral, Montreal"},
    {"name": "The Gravemind Council", "lair": "Bone-Lined Catacombs, Palermo"},
    {"name": "Covenant of the Black Sun", "lair": "Eclipsed Observatory, Prague"},
    {"name": "The Immortal Court", "lair": "Floating Barge, Thames River"},
    {"name": "Clan Nightfall", "lair": "Penthouse Spire, Tokyo"},
    {"name": "The Crimson Ascendancy", "lair": "Skyscraper Lair, Dubai"},
    {"name": "Order of the Starless Sky", "lair": "Subterranean Lake, Slovenia"},
    {"name": "The Hungering Dark", "lair": "Collapsed Mine, Appalachia"},
    {"name": "Clan Ashblood", "lair": "Ashen Ruin, Pompeii"},
    {"name": "The Deathless Society", "lair": "Secret Club, Hong Kong"},
    {"name": "Brotherhood of the Red Night", "lair": "Cliffside Abbey, Amalfi"},
    {"name": "The Sepulchre Court", "lair": "Sunken Tomb, Alexandria"},
    {"name": "Covenant of Pale Fire", "lair": "Aurora-Lit Fortress, Scandinavia"},
    {"name": "The Neverdawn Compact", "lair": "Eternal Midnight Realm, Unknown"},
    {"name": "Clan Shadowmere", "lair": "Lake-Bottom Palace, Scotland"},
    {"name": "The Waning Crescent", "lair": "Desert Oasis Lair, Sahara"},
    {"name": "Order of the Bone Chalice", "lair": "Reliquary Cathedral, Toledo"},
    {"name": "The Blackwater Conclave", "lair": "Sunken Ship Graveyard, Caribbean"},
    {"name": "Clan Darkspire", "lair": "Iron Tower, Rhine Valley"},
    {"name": "The Cursed Assembly", "lair": "Cursed Village, Romania"},
    {"name": "Brotherhood of the Night Wind", "lair": "Windswept Ruin, Patagonia"},
    {"name": "The Eternal Conclave", "lair": "Timeless Vault, Somewhere Ancient"},
    {"name": "Covenant of the Bleeding Moon", "lair": "Lunar Observatory, Tibet"},
    {"name": "The Dread Sovereignty", "lair": "Arctic Ice Fortress, Greenland"},
    {"name": "Clan Vexmoor", "lair": "Moorland Ruin, Yorkshire"},
    {"name": "The Immortal Syndicate", "lair": "Hidden Bunker, Switzerland"},
    {"name": "Order of the Final Dark", "lair": "World's Edge Citadel, Unknown"},
    {"name": "The Bloodsworn Compact", "lair": "Sealed Vault, Vatican Depths"},
    {"name": "Clan Nocturnis", "lair": "Ancient Forum, Rome Underground"},
    {"name": "The Starless Covenant", "lair": "Lightless Abyss, Ocean Floor"},
    {"name": "Brotherhood of the Undead King", "lair": "Throne Room of Bones, Unknown"},
    {"name": "The Pale Assembly", "lair": "White Marble Crypt, Florence"},
    {"name": "Covenant of the Long Sleep", "lair": "Hibernation Vault, Switzerland"},
    {"name": "The Crimson Dynasty", "lair": "Dynastic Mausoleum, China"},
    {"name": "Clan Eventide", "lair": "Twilight Fortress, Scotland"},
    {"name": "The Dusk Collective", "lair": "Rooftop Network, Berlin"},
    {"name": "Order of the Pale Chalice", "lair": "Mountain Hermitage, Himalayas"},
    {"name": "The Wraithkin Council", "lair": "Ghost-Haunted Manor, Ireland"},
    {"name": "Clan Vexmourne", "lair": "Mourning Chapel, Brittany"},
    {"name": "The Sanguine Throne", "lair": "Blood-Stained Palace, Warsaw"},
    {"name": "Brotherhood of Endless Hunger", "lair": "Empty Cathedral, Detroit"},
    {"name": "The Midnight Sovereignty", "lair": "Clock Tower Spire, London"},
    {"name": "Covenant of the Black Moon", "lair": "Obsidian Temple, Mexico"},
    {"name": "The Deathless Court", "lair": "Timeless Manor, Untraceable"},
    {"name": "Clan Grimshroud", "lair": "Shrouded Hilltop Castle, Austria"},
    {"name": "The Noctivagant Order", "lair": "Night-Wanderer Sanctum, Undisclosed"},
    {"name": "Brotherhood of the Red Veil", "lair": "Veiled Temple, Istanbul"},
    {"name": "The Hungering Conclave", "lair": "Starving City Underbelly, Naples"},
    {"name": "Covenant of the Sleeping King", "lair": "Coffin Vault, Romania"},
    {"name": "The Cursed Dominion", "lair": "Hexed Estate, Salem"},
    {"name": "Clan Nightborn", "lair": "Birthplace of Darkness, Unknown"},
    {"name": "The Eternal Shroud", "lair": "Shrouded Mountain, Nepal"},
    {"name": "Order of the Bleeding Rose", "lair": "Rose Garden Tomb, Seville"},
    {"name": "The Black Covenant", "lair": "Void Sanctum, Beyond the Veil"},
    {"name": "Clan Ashenthorn", "lair": "Thornfield Ruin, Derbyshire"},
    {"name": "The Pale Fire Society", "lair": "Luminous Crypt, Reykjavik"},
    {"name": "Brotherhood of the Grave Moon", "lair": "Graveyard Observatory, Salem"},
    {"name": "The Undying Assembly", "lair": "Parliament of the Dead, London"},
    {"name": "Covenant of the Final Hunger", "lair": "Last Feeding Ground, Unknown"},
    {"name": "The Sunless Court", "lair": "Lightless Palace, Beneath the Earth"},
    {"name": "Clan Vexor", "lair": "Labyrinth of Bone, Crete"},
    {"name": "The Immortal Flame", "lair": "Eternal Pyre Temple, Greece"},
    {"name": "Order of the Endless Night", "lair": "Night Without End Sanctum, Void"},
]

SENTENCE_TIERS = [
    {"label": "2 decades",  "minutes": 2},
    {"label": "5 decades",  "minutes": 5},
    {"label": "a century", "minutes": 10},
    {"label": "15 decades", "minutes": 15},
    {"label": "25 decades", "minutes": 25},
    {"label": "4 centuries", "minutes": 40},
    {"label": "5 centuries", "minutes": 50},
]
SENTENCE_WEIGHTS = [30, 25, 20, 12, 8, 3, 2]

MSG_DELAY = 2.1
EMBED_DESC_LIMIT = 4000
EMBED_FIELD_LIMIT = 1024

HUNT_LOCATIONS = [
    "a masquerade ball in the old quarter",
    "a fog-drenched cemetery at midnight",
    "a candlelit opera house",
    "a decadent noble's feast",
    "a moonlit riverbank",
    "a shadowy tavern in the undercity",
    "a torchlit crypt below the cathedral",
    "a cursed manor on the hill",
    "an ancient library at the witching hour",
    "a plague-ridden village square",
    "a moonless forest clearing",
    "a crumbling aqueduct at dusk",
    "a gaslit alley in the merchant district",
    "a secret society's ritual chamber",
    "a fog-choked harbor at low tide",
    "a gothic ballroom in an abandoned estate",
    "a midnight market in the cursed bazaar",
    "a torchlit dungeon beneath the castle",
    "a moonlit cliff overlooking the sea",
    "a vampire-held casino in the shadow city",
]

# --- Helpers ---

def is_admin(message):
    return isinstance(message.author, discord.Member) and message.author.guild_permissions.administrator

def user_has_active_coven(user_id):
    return any(g['owner_id'] == user_id and g['alive'] for g in covens.values())

def generate_code():
    while True:
        code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
        if code not in covens:
            return code

def make_member(name):
    return {
        "name": name, "alive": True, "kills": 0, "deaths": 0,
        "times_imprisoned": 0, "times_betrayed": 0, "hunts_survived": 0,
        "imprisoned_until": None, "imprisonment_sentence": None,
    }

def generate_vampire_members(count=5):
    names = random.sample(VAMPIRE_NAMES, min(count, len(VAMPIRE_NAMES)))
    return [make_member(n) for n in names]

def get_alive_members(coven):
    return [m for m in coven['members'] if m['alive']]

def get_dead_members(coven):
    return [m for m in coven['members'] if not m['alive']]

def is_imprisoned(member):
    return bool(member['imprisoned_until'] and time.time() < member['imprisoned_until'])

def get_free_members(coven):
    return [m for m in coven['members'] if m['alive'] and not is_imprisoned(m)]

def get_coven_kills(coven):
    return sum(m['kills'] for m in coven['members'])

def get_coven_deaths(coven):
    return sum(m['deaths'] for m in coven['members'])

def update_coven_lord(coven):
    alive = get_alive_members(coven)
    if not alive:
        return
    top = max(alive, key=lambda m: m['kills'])
    coven['leader'] = top['name']

def check_and_mark_dead(code):
    coven = covens.get(code)
    if not coven:
        return
    if not get_alive_members(coven):
        coven['alive'] = False
        if not user_has_active_coven(coven['owner_id']):
            active_coven_lords.discard(coven['owner_id'])

def imprison_member(member):
    tier = random.choices(SENTENCE_TIERS, weights=SENTENCE_WEIGHTS, k=1)[0]
    member['imprisoned_until'] = time.time() + tier['minutes'] * 60
    member['imprisonment_sentence'] = tier['label']
    member['times_imprisoned'] += 1
    return tier['label']

def get_member_status(m):
    if not m['alive']:
        return "Destroyed"
    if is_imprisoned(m):
        return f"Imprisoned ({m['imprisonment_sentence']})"
    return "Free"

def add_blood_debt(coven, slayer_name, enemy_info, enemy_power):
    targets = coven.setdefault('blood_debts', [])
    for t in targets:
        if t['coven'] == enemy_info['name']:
            t['name'] = slayer_name
            t['enemy_power'] = enemy_power
            return
    targets.append({"name": slayer_name, "coven": enemy_info['name'], "coven_info": enemy_info, "enemy_power": enemy_power})

def get_blood_debts(coven):
    return coven.get('blood_debts', [])

def remove_blood_debt(coven, coven_name):
    coven['blood_debts'] = [t for t in coven.get('blood_debts', []) if t['coven'] != coven_name]

async def safe_send(channel, embed=None, content=None):
    try:
        if embed:
            if embed.description and len(embed.description) > EMBED_DESC_LIMIT:
                embed.description = embed.description[:EMBED_DESC_LIMIT - 3] + "..."
            for i, field in enumerate(embed.fields):
                if len(field.value) > EMBED_FIELD_LIMIT:
                    embed.set_field_at(i, name=field.name, value=field.value[:EMBED_FIELD_LIMIT - 3] + "...", inline=field.inline)
            await channel.send(embed=embed)
        elif content:
            if len(content) > 2000:
                chunks = [content[i:i+1990] for i in range(0, len(content), 1990)]
                for chunk in chunks:
                    await channel.send(chunk)
                    await asyncio.sleep(0.5)
            else:
                await channel.send(content)
    except discord.HTTPException as e:
        print(f"safe_send error: {e}")

async def send_chunked_embed(channel, title, lines, color, footer=None, chunk_size=20):
    chunks = [lines[i:i+chunk_size] for i in range(0, len(lines), chunk_size)]
    for idx, chunk in enumerate(chunks):
        embed = discord.Embed(
            title=title if idx == 0 else f"{title} (cont.)",
            description="\n".join(chunk),
            color=color
        )
        if footer and idx == len(chunks) - 1:
            embed.set_footer(text=footer)
        await safe_send(channel, embed=embed)
        if idx < len(chunks) - 1:
            await asyncio.sleep(0.5)

def member_result_line(name, outcome, sentence=None):
    if outcome == "kill":
        return random.choice([
            f"`{name}` — drained the target dry. Another soul claimed.",
            f"`{name}` — struck from the shadows. The prey never saw it coming.",
            f"`{name}` — fed well. The mission is complete.",
        ])
    elif outcome == "friendly_kill":
        return random.choice([
            f"`{name}` — caught in the bloodlust. Destroyed by their own kin.",
            f"`{name}` — turned to ash retreating. Gone.",
            f"`{name}` — the frenzy claimed them. Lost to the night.",
        ])
    elif outcome == "death":
        return random.choice([
            f"`{name}` — staked through the heart. Dust.",
            f"`{name}` — outnumbered and destroyed. The sun took what was left.",
            f"`{name}` — slain. Their ashes scatter on the wind.",
        ])
    elif outcome == "imprisoned":
        return random.choice([
            f"`{name}` — captured by vampire hunters. Sealed away for {sentence}.",
            f"`{name}` — caught in a silver trap. Imprisoned for {sentence}.",
            f"`{name}` — the church's soldiers got them. Locked away for {sentence}.",
        ])
    elif outcome == "survived":
        return random.choice([
            f"`{name}` — wounded but not destroyed. Still standing.",
            f"`{name}` — caught a silver bolt but clawed free.",
            f"`{name}` — escaped into the mist. Alive.",
        ])
    return f"`{name}` — fate unknown."

# --- Raid Logic ---

def calculate_raid_outcome(coven, raiding_members, enemy_power, is_blood_oath=False):
    player_power = coven['power']
    power_diff = player_power - enemy_power
    win_chance = max(10, min(90, 50 + int((power_diff / 500) * 40)))
    if is_blood_oath:
        win_chance = min(95, win_chance + 10)

    player_won = random.randint(1, 100) <= win_chance
    member_lines = []
    kills_this_fight = {}
    fallen = []
    imprisoned = []

    if player_won:
        power_gain = random.randint(20, max(21, int(enemy_power * 0.4)))
        if is_blood_oath:
            power_gain = int(power_gain * 1.25)
        coven['power'] = player_power + power_gain
        coven['raids_won'] = coven.get('raids_won', 0) + 1

        for m in raiding_members:
            m['kills'] += 1
            m['hunts_survived'] += 1
            kills_this_fight[m['name']] = kills_this_fight.get(m['name'], 0) + 1
            member_lines.append(member_result_line(m['name'], "kill"))

        free_raiding = [m for m in raiding_members if not is_imprisoned(m)]
        if len(get_alive_members(coven)) > 1 and random.randint(1, 100) <= 20 and free_raiding:
            c = random.choice(free_raiding)
            c['alive'] = False
            c['deaths'] += 1
            fallen.append(c['name'])
            member_lines.append(member_result_line(c['name'], "friendly_kill"))

        if random.randint(1, 100) <= 15:
            free_raiding2 = [m for m in raiding_members if m['alive'] and not is_imprisoned(m)]
            if free_raiding2:
                j = random.choice(free_raiding2)
                s = imprison_member(j)
                imprisoned.append((j['name'], s))
                member_lines.append(member_result_line(j['name'], "imprisoned", s))

        update_coven_lord(coven)
        return {
            "won": True, "power_gain": power_gain, "old_power": player_power, "new_power": coven['power'],
            "enemy_power": enemy_power, "member_lines": member_lines, "kills_this_fight": kills_this_fight,
            "members_alive": len(get_alive_members(coven)), "fallen": fallen, "imprisoned": imprisoned,
        }
    else:
        coven['raids_lost'] = coven.get('raids_lost', 0) + 1

        for m in raiding_members:
            if is_imprisoned(m):
                continue
            if len(get_alive_members(coven)) > 1 and random.randint(1, 100) <= 40:
                m['alive'] = False
                m['deaths'] += 1
                fallen.append(m['name'])
                member_lines.append(member_result_line(m['name'], "death"))
            elif random.randint(1, 100) <= 30:
                s = imprison_member(m)
                imprisoned.append((m['name'], s))
                member_lines.append(member_result_line(m['name'], "imprisoned", s))
            else:
                m['hunts_survived'] += 1
                member_lines.append(member_result_line(m['name'], "survived"))

        power_loss = random.randint(20, max(21, int(player_power * 0.25)))
        coven['power'] = max(1, player_power - power_loss)

        update_coven_lord(coven)
        return {
            "won": False, "power_loss": player_power - coven['power'], "old_power": player_power, "new_power": coven['power'],
            "enemy_power": enemy_power, "member_lines": member_lines, "kills_this_fight": kills_this_fight,
            "members_alive": len(get_alive_members(coven)), "fallen": fallen, "imprisoned": imprisoned,
        }


async def send_raid_result(channel, coven, enemy_info, result, raiding, is_blood_oath=False):
    overall_color = discord.Color.dark_red() if result['won'] else discord.Color.dark_grey()
    title = ("Blood Oath Fulfilled" if is_blood_oath else "Raid Victorious") if result['won'] else ("Blood Oath Failed" if is_blood_oath else "Raid Failed")
    power_line = (
        f"{result['old_power']} -> {result['new_power']} (+{result['power_gain']})"
        if result['won']
        else f"{result['old_power']} -> {result['new_power']} (-{result['power_loss']})"
    )

    raiding_names = ", ".join(f"`{m['name']}`" for m in raiding)
    intro = discord.Embed(title="Night Raid", color=discord.Color.dark_red())
    intro.description = (
        f"**{coven['name']}** vs **{enemy_info['name']}**\n"
        f"Your Dark Power: {result['old_power']}  |  Enemy Power: {result['enemy_power']}\n\n"
        f"Raiding: {raiding_names}"
    )
    await safe_send(channel, embed=intro)
    await asyncio.sleep(MSG_DELAY)

    crew_lines = result['member_lines'] if result['member_lines'] else ["Nothing to report."]
    kills_lines = (
        [f"`{n}` — {k} soul{'s' if k != 1 else ''} drained" for n, k in result['kills_this_fight'].items()]
        if result['kills_this_fight'] else ["No kills."]
    )

    base_desc = (
        f"**Dark Power:** {power_line}\n"
        f"**Still Undead:** {result['members_alive']}\n"
        f"**Coven Lord:** `{coven['leader']}`\n"
    )
    if result['fallen']:
        base_desc += "\n**Destroyed:** " + ", ".join(f"`{n}`" for n in result['fallen'])
    if result['imprisoned']:
        base_desc += "\n**Imprisoned:** " + ", ".join(f"`{n}` ({s})" for n, s in result['imprisoned'])

    result_embed = discord.Embed(title=title, color=overall_color)
    result_embed.description = base_desc

    crew_text = "\n".join(crew_lines)
    kills_text = "\n".join(kills_lines)

    if len(crew_text) <= EMBED_FIELD_LIMIT:
        result_embed.add_field(name="Coven", value=crew_text, inline=False)
    else:
        chunks = [crew_lines[i:i+10] for i in range(0, len(crew_lines), 10)]
        for idx, chunk in enumerate(chunks):
            result_embed.add_field(
                name="Coven" if idx == 0 else "Coven (cont.)",
                value="\n".join(chunk),
                inline=False
            )

    if len(kills_text) <= EMBED_FIELD_LIMIT:
        result_embed.add_field(name="Souls Drained", value=kills_text, inline=False)
    else:
        chunks = [kills_lines[i:i+10] for i in range(0, len(kills_lines), 10)]
        for idx, chunk in enumerate(chunks):
            result_embed.add_field(
                name="Souls Drained" if idx == 0 else "Souls Drained (cont.)",
                value="\n".join(chunk),
                inline=False
            )

    result_embed.set_footer(text="The night is ours." if result['won'] else "Regroup in the shadows. Dawn is coming.")
    await safe_send(channel, embed=result_embed)


# --- Hunt handler ---

async def handle_hunt(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `hunt <code>`")
        return

    code = args[0].upper()
    coven = covens.get(code)
    if not coven:
        await safe_send(message.channel, content=f"No coven found with code `{code}`.")
        return
    if coven['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That is not your coven.")
        return
    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed.")
        return

    free = get_free_members(coven)
    if not free:
        imprisoned_count = len([m for m in coven['members'] if m['alive'] and is_imprisoned(m)])
        if imprisoned_count > 0:
            await safe_send(message.channel, content=f"**{coven['name']}** has no free members. {imprisoned_count} imprisoned.")
        else:
            await safe_send(message.channel, content=f"**{coven['name']}** has no members left.")
        return

    member = random.choice(free)

    if random.randint(1, 100) <= 40:
        await run_feeding_hunt(message.channel, coven, member, code)
    else:
        event = random.choice(EVENTS)
        power = coven['power']
        desc = event['description'].format(name=coven['name'], member=f"`{member['name']}`")
        embed = discord.Embed(title=event['name'], description=desc, color=event['color'])

        if event['type'] == 'power_up':
            gain = random.randint(*event['value'])
            coven['power'] = power + gain
            member['hunts_survived'] += 1
            if random.randint(1, 100) <= 20:
                member['kills'] += 1
            update_coven_lord(coven)
            embed.description += f"\n\nDark Power: {power} -> {coven['power']} (+{gain})"
            embed.set_footer(text="The coven grows stronger.")

        elif event['type'] == 'power_down':
            loss = random.randint(*event['value'])
            new_power = max(1, power - loss)
            actual_loss = power - new_power
            coven['power'] = new_power
            if event.get('betrayal'):
                member['times_betrayed'] += 1
            extra = []
            if random.randint(1, 100) <= 15 and len(get_alive_members(coven)) > 1:
                member['alive'] = False
                member['deaths'] += 1
                check_and_mark_dead(code)
                extra.append(f"`{member['name']}` was destroyed.")
            elif random.randint(1, 100) <= 25:
                s = imprison_member(member)
                extra.append(f"`{member['name']}` was captured — {s}.")
            update_coven_lord(coven)
            if extra:
                embed.description += "\n\n" + "\n".join(extra)
            embed.description += f"\n\nDark Power: {power} -> {coven['power']} (-{actual_loss})"
            embed.set_footer(text="The coven suffers.")

        elif event['type'] == 'nothing':
            embed.description += f"\n\nDark Power: {power} (no change)"
            embed.set_footer(text="The night passes without incident.")

        if len(embed.description) > EMBED_DESC_LIMIT:
            embed.description = embed.description[:EMBED_DESC_LIMIT - 3] + "..."

        await safe_send(message.channel, embed=embed)


async def run_feeding_hunt(channel, coven, member, code):
    power = coven['power']
    event = random.choice(BLOOD_EVENTS)
    desc = event['description'].format(name=coven['name'], member=f"`{member['name']}`")
    embed = discord.Embed(title=event['name'], description=desc, color=event['color'])

    if event['type'] == 'blood_win':
        gain = random.randint(*event['value'])
        coven['power'] = power + gain
        member['hunts_survived'] += 1
        update_coven_lord(coven)
        embed.description += f"\n\nDark Power: {power} -> {coven['power']} (+{gain})"
        embed.set_footer(text="Blood flows. The coven is fed.")

    elif event['type'] == 'blood_imprisoned':
        loss = random.randint(*event.get('value', (20, 60)))
        coven['power'] = max(1, power - loss)
        s = imprison_member(member)
        update_coven_lord(coven)
        embed.description += f"\n\n`{member['name']}` was captured — {s}.\nDark Power: {power} -> {coven['power']} (-{loss})"
        embed.set_footer(text="One vampire lost to the hunters. The feeding grounds go quiet.")

    elif event['type'] == 'blood_killed':
        loss = random.randint(*event.get('value', (30, 80)))
        coven['power'] = max(1, power - loss)
        if len(get_alive_members(coven)) > 1:
            member['alive'] = False
            member['deaths'] += 1
            check_and_mark_dead(code)
            update_coven_lord(coven)
            embed.description += (
                f"\n\n`{member['name']}` was staked and did not return.\n"
                f"Dark Power: {power} -> {coven['power']} (-{loss})\n"
                f"Still Undead: {len(get_alive_members(coven))}"
            )
        else:
            s = imprison_member(member)
            update_coven_lord(coven)
            embed.description += f"\n\n`{member['name']}` was captured — {s}.\nDark Power: {power} -> {coven['power']} (-{loss})"
        embed.set_footer(text="The night claimed one of our own.")

    elif event['type'] == 'blood_nothing':
        embed.description += f"\n\nDark Power: {power} (no change)"
        embed.set_footer(text="A bloodless night. The hunger grows.")

    if len(embed.description) > EMBED_DESC_LIMIT:
        embed.description = embed.description[:EMBED_DESC_LIMIT - 3] + "..."

    await safe_send(channel, embed=embed)


# --- Commands ---

async def handle_coven(message, args):
    user_id = message.author.id
    if not is_admin(message) and user_has_active_coven(user_id):
        await safe_send(message.channel, content="You already have a coven. Type `show` to see them.")
        return

    vampire_coven = random.choice(VAMPIRE_COVENS)
    code = generate_code()
    members = generate_vampire_members(random.randint(4, 7))
    power = random.randint(10, 100)

    covens[code] = {
        "name": vampire_coven["name"], "lair": vampire_coven["lair"],
        "leader": members[0]['name'], "power": power,
        "owner_id": user_id, "owner_name": message.author.name,
        "code": code, "alive": True,
        "raids_won": 0, "raids_lost": 0,
        "members": members, "blood_debts": [],
    }

    if not is_admin(message):
        active_coven_lords.add(user_id)

    member_lines = "\n".join(f"`{m['name']}`" for m in members)
    embed = discord.Embed(
        title="You Have Been Turned",
        description=(
            f"You have risen with **{vampire_coven['name']}**.\n\n"
            f"Lair: {vampire_coven['lair']}\n"
            f"Coven Lord: `{members[0]['name']}`\n"
            f"Dark Power: {power}\n"
            f"Members: {len(members)}\n"
            f"Code: `{code}`\n\n"
            f"{member_lines}"
        ),
        color=discord.Color.dark_red()
    )
    embed.set_footer(text="hunt | raid | sire | bloodoath | ritual | solo | dp | gathering | show | disband")
    await safe_send(message.channel, embed=embed)


async def handle_show(message, args):
    user_id = message.author.id

    if args:
        code = args[0].upper()
        target_coven = covens.get(code)
        if not target_coven:
            await safe_send(message.channel, content=f"No coven found with code `{code}`.")
            return
        if target_coven['owner_id'] != user_id and not is_admin(message):
            await safe_send(message.channel, content="That is not your coven.")
            return
        user_covens = [target_coven]
    else:
        user_covens = [g for g in covens.values() if g['owner_id'] == user_id]

    if not user_covens:
        await safe_send(message.channel, content="You have no coven. Type `coven` to rise.")
        return

    alive_covens = [g for g in user_covens if g['alive']]

    if not alive_covens:
        await safe_send(message.channel, content="No active coven. Type `coven` to rise again.")
        return

    for g in alive_covens:
        update_coven_lord(g)
        rw = g.get('raids_won', 0)
        rl = g.get('raids_lost', 0)
        total = rw + rl
        win_rate = f"{int((rw / total) * 100)}%" if total > 0 else "N/A"
        debts = get_blood_debts(g)

        alive = get_alive_members(g)
        dead = get_dead_members(g)

        stats_desc = (
            f"Lair: {g.get('lair', 'Unknown')}\n"
            f"Coven Lord: `{g.get('leader', 'Unknown')}`\n"
            f"Dark Power: {g['power']}\n"
            f"Record: {rw}W — {rl}L   Win Rate: {win_rate}\n"
            f"Souls Drained: {get_coven_kills(g)}   Destroyed: {get_coven_deaths(g)}\n"
            f"Undead: {len(alive)}   Free: {len(get_free_members(g))}"
        )

        if debts:
            stats_desc += "\n\nBlood Debts:\n" + "\n".join(
                f"`{t['name']}` | {t['coven']}" for t in debts
            )

        if alive:
            roster_lines = "\n".join(
                f"`{m['name']}` | {m['kills']} souls | {get_member_status(m)}"
                for m in alive
            )
            if len(roster_lines) > EMBED_FIELD_LIMIT:
                roster_lines = roster_lines[:EMBED_FIELD_LIMIT - 3] + "..."
            stats_desc += f"\n\nActive Roster:\n{roster_lines}"

        stats_embed = discord.Embed(
            title=f"{g['name']} — `{g['code']}`",
            description=stats_desc,
            color=discord.Color.dark_red()
        )
        stats_embed.set_footer(text="hunt | raid | sire | bloodoath | ritual | solo | dp | gathering | show | disband")
        await safe_send(message.channel, embed=stats_embed)

        if dead:
            dead_lines = "\n".join(
                f"`{m['name']}` | {m['kills']} souls | Destroyed"
                for m in dead
            )
            if len(dead_lines) > EMBED_FIELD_LIMIT:
                dead_lines = dead_lines[:EMBED_FIELD_LIMIT - 3] + "..."
            fallen_embed = discord.Embed(
                title=f"{g['name']} — Destroyed",
                description=dead_lines,
                color=discord.Color.dark_grey()
            )
            fallen_embed.set_footer(text="Returned to ash.")
            await safe_send(message.channel, embed=fallen_embed)


async def handle_sire(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `sire <code> <number>` — Example: `sire XKRV 3`")
        return

    code = args[0].upper()
    coven = covens.get(code)
    if not coven:
        await safe_send(message.channel, content=f"No coven found with code `{code}`.")
        return
    if coven['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That is not your coven.")
        return
    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed.")
        return

    requested = 1
    if len(args) >= 2:
        try:
            requested = int(args[1])
        except ValueError:
            await safe_send(message.channel, content="The number must be a whole number. Example: `sire XKRV 3`")
            return
        if requested < 1:
            await safe_send(message.channel, content="Sire at least 1.")
            return
        if requested > 10:
            await safe_send(message.channel, content="Max 10 at once.")
            return

    existing = {m['name'] for m in coven['members']}
    available = [n for n in VAMPIRE_NAMES if n not in existing]
    if not available:
        await safe_send(message.channel, content=f"**{coven['name']}** roster is full — all vampire names are taken.")
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
            coven['members'].append(make_member(new_name))
            joined.append(new_name)
        else:
            failed += 1

    embed = discord.Embed(color=discord.Color.dark_red() if joined else discord.Color.dark_grey())

    if joined and failed == 0:
        embed.title = f"{len(joined)} Rose From the Dark"
        lines = "\n".join(f"`{n}`" for n in joined)
        embed.description = f"{lines}\n\nAll {len(joined)} turned successfully. Total Undead: {len(get_alive_members(coven))}"
    elif joined and failed > 0:
        embed.title = f"{len(joined)} Turned — {failed} Did Not Survive the Bite"
        lines = "\n".join(f"`{n}`" for n in joined)
        embed.description = f"Turned:\n{lines}\n\n{failed} did not survive the transformation. Total Undead: {len(get_alive_members(coven))}"
        embed.color = discord.Color.dark_orange()
    else:
        embed.title = "None Were Turned"
        embed.description = f"Attempted to sire {requested} but none survived the transformation.\nUndead: {len(get_alive_members(coven))}"

    embed.set_footer(text=f"sire {code} <number> to try again.")
    await safe_send(message.channel, embed=embed)


async def handle_raid(message, args):
    if len(args) < 2:
        await safe_send(message.channel, content="Usage: `raid <code> <number>`")
        return

    code = args[0].upper()
    coven = covens.get(code)
    if not coven:
        await safe_send(message.channel, content=f"No coven found with code `{code}`.")
        return
    if coven['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That is not your coven.")
        return
    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed.")
        return

    try:
        requested = int(args[1])
    except ValueError:
        await safe_send(message.channel, content="Needs to be a number. Example: `raid XKRV 3`")
        return

    if requested < 1:
        await safe_send(message.channel, content="Send at least 1.")
        return

    free = get_free_members(coven)
    if not free:
        imprisoned = [m for m in coven['members'] if m['alive'] and is_imprisoned(m)]
        if imprisoned:
            await safe_send(message.channel, content=f"No free members to raid. {len(imprisoned)} imprisoned right now.")
        else:
            await safe_send(message.channel, content="No free members to raid.")
        return

    actual = min(requested, len(free), 10)
    raiding = random.sample(free, actual)
    enemy_info = random.choice(VAMPIRE_COVENS)
    enemy_power = random.randint(10, 500)

    alive_before = {m['name'] for m in get_alive_members(coven)}
    result = calculate_raid_outcome(coven, raiding, enemy_power)
    alive_after = {m['name'] for m in get_alive_members(coven)}

    if alive_before - alive_after:
        slayer_name = random.choice(VAMPIRE_NAMES)
        add_blood_debt(coven, slayer_name, enemy_info, enemy_power)

    check_and_mark_dead(code)
    await send_raid_result(message.channel, coven, enemy_info, result, raiding)

    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed. Type `coven` to rise again.")


async def handle_bloodoath(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `bloodoak <code>`")
        return

    code = args[0].upper()
    coven = covens.get(code)
    if not coven:
        await safe_send(message.channel, content=f"No coven found with code `{code}`.")
        return
    if coven['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That is not your coven.")
        return
    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed.")
        return

    debts = get_blood_debts(coven)
    if not debts:
        await safe_send(message.channel, content="No blood debts to settle. The night is quiet.")
        return

    free = get_free_members(coven)
    if not free:
        imprisoned = [m for m in coven['members'] if m['alive'] and is_imprisoned(m)]
        if imprisoned:
            await safe_send(message.channel, content=f"No free members to send. {len(imprisoned)} imprisoned.")
        else:
            await safe_send(message.channel, content="No free members to send.")
        return

    target = random.choice(debts)
    enemy_info = target['coven_info']
    enemy_power = target.get('enemy_power', random.randint(10, 500))
    raiding = random.sample(free, random.randint(1, min(3, len(free))))

    alive_before = {m['name'] for m in get_alive_members(coven)}
    result = calculate_raid_outcome(coven, raiding, enemy_power, is_blood_oath=True)
    alive_after = {m['name'] for m in get_alive_members(coven)}

    if result['won']:
        remove_blood_debt(coven, enemy_info['name'])
    elif alive_before - alive_after:
        add_blood_debt(coven, target['name'], enemy_info, enemy_power)

    check_and_mark_dead(code)
    await send_raid_result(message.channel, coven, enemy_info, result, raiding, is_blood_oath=True)

    remaining_after = get_blood_debts(coven)
    if remaining_after:
        followup = discord.Embed(
            title="Blood Still Owed",
            description="\n".join(f"**{t['coven']}** | `{t['name']}`" for t in remaining_after) + f"\n\nType `bloodoak {code}` again.",
            color=discord.Color.dark_red()
        )
        await safe_send(message.channel, embed=followup)
    elif result['won']:
        await safe_send(message.channel, content="All blood debts settled. The night is ours.")


async def handle_solo(message, args):
    if len(args) < 2:
        await safe_send(message.channel, content="Usage: `solo <code> <name>`")
        return

    code = args[0].upper()
    member_name = " ".join(args[1:])
    coven = covens.get(code)

    if not coven:
        await safe_send(message.channel, content=f"No coven found with code `{code}`.")
        return
    if coven['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That is not your coven.")
        return
    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed.")
        return

    target = next((m for m in coven['members'] if m['name'].lower() == member_name.lower()), None)
    if not target:
        roster = ", ".join(f"`{m['name']}`" for m in coven['members'])
        if len(roster) > 1800:
            await safe_send(message.channel, content=f"No member named `{member_name}`.")
            lines = [f"`{m['name']}` — {get_member_status(m)}" for m in coven['members']]
            await send_chunked_embed(message.channel, "Roster", lines, discord.Color.dark_red())
        else:
            await safe_send(message.channel, content=f"No member named `{member_name}`.\nRoster: {roster}")
        return
    if not target['alive']:
        await safe_send(message.channel, content=f"`{target['name']}` has been destroyed.")
        return
    if is_imprisoned(target):
        await safe_send(message.channel, content=f"`{target['name']}` is imprisoned.")
        return

    enemy_info = random.choice(VAMPIRE_COVENS)
    enemy_power = random.randint(10, 500)
    player_power = coven['power']
    win_chance = max(10, min(75, 40 + int(((player_power - enemy_power) / 500) * 30)))
    roll = random.randint(1, 100)

    intro = discord.Embed(title="Solo Hunt", color=discord.Color.dark_red())
    intro.description = (
        f"`{target['name']}` stalked alone into **{enemy_info['name']}** territory.\n\n"
        f"Souls Drained: {target['kills']}  |  Lair: {enemy_info['lair']}"
    )
    intro.set_footer(text="One vampire. No backup. The night waits.")
    await safe_send(message.channel, embed=intro)
    await asyncio.sleep(MSG_DELAY)

    if roll <= win_chance:
        target['kills'] += 1
        target['hunts_survived'] += 1
        power_gain = random.randint(15, 60)
        coven['power'] = player_power + power_gain
        update_coven_lord(coven)
        embed = discord.Embed(title="Solo Hunt — Target Drained", color=discord.Color.dark_red())
        embed.description = (
            f"`{target['name']}` moved through the shadows and struck clean. The prey did not scream.\n\n"
            f"Souls Drained: {target['kills']}  |  Dark Power: {player_power} -> {coven['power']} (+{power_gain})\n"
            f"Coven Lord: `{coven['leader']}`"
        )
        embed.set_footer(text="The coven feeds tonight.")
    elif roll <= win_chance + 30:
        target['hunts_survived'] += 1
        power_loss = random.randint(5, 25)
        coven['power'] = max(1, player_power - power_loss)
        embed = discord.Embed(title="Solo Hunt — Escaped", color=discord.Color.dark_orange())
        embed.description = (
            f"`{target['name']}` was wounded but retreated into the mist.\n\n"
            f"Souls Drained: {target['kills']}  |  Dark Power: {player_power} -> {coven['power']} (-{power_loss})"
        )
        embed.set_footer(text="Still undead. That is enough.")
    elif roll <= win_chance + 50:
        s = imprison_member(target)
        power_loss = random.randint(10, 35)
        coven['power'] = max(1, player_power - power_loss)
        update_coven_lord(coven)
        embed = discord.Embed(title="Solo Hunt — Captured", color=discord.Color.blue())
        embed.description = (
            f"`{target['name']}` was caught in a silver trap. Imprisoned for {s}.\n\n"
            f"Dark Power: {player_power} -> {coven['power']} (-{power_loss})\n"
            f"Coven Lord: `{coven['leader']}`"
        )
        embed.set_footer(text="One vampire down.")
    else:
        power_loss = random.randint(20, 60)
        coven['power'] = max(1, player_power - power_loss)
        if len(get_alive_members(coven)) > 1:
            target['alive'] = False
            target['deaths'] += 1
            check_and_mark_dead(code)
            update_coven_lord(coven)
            embed = discord.Embed(title="Solo Hunt — Destroyed", color=discord.Color.dark_grey())
            embed.description = (
                f"`{target['name']}` was staked through the heart. Ash on the wind.\n\n"
                f"Souls Drained: {target['kills']}  |  Dark Power: {player_power} -> {coven['power']} (-{power_loss})\n"
                f"Still Undead: {len(get_alive_members(coven))}\n"
                f"Coven Lord: `{coven['leader']}`"
            )
            embed.set_footer(text="Another name carved into the crypt wall.")
        else:
            s = imprison_member(target)
            update_coven_lord(coven)
            embed = discord.Embed(title="Solo Hunt — Captured", color=discord.Color.blue())
            embed.description = (
                f"`{target['name']}` was captured. Imprisoned for {s}.\n\n"
                f"Dark Power: {player_power} -> {coven['power']} (-{power_loss})\n"
                f"Coven Lord: `{coven['leader']}`"
            )
            embed.set_footer(text="The last free vampire, now in chains.")

    await safe_send(message.channel, embed=embed)


async def handle_ritual(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `ritual <code>`")
        return

    code = args[0].upper()
    coven = covens.get(code)
    if not coven:
        await safe_send(message.channel, content=f"No coven found with code `{code}`.")
        return
    if coven['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That is not your coven.")
        return
    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed.")
        return

    free = get_free_members(coven)
    if not free:
        imprisoned = [m for m in coven['members'] if m['alive'] and is_imprisoned(m)]
        if imprisoned:
            await safe_send(message.channel, content=f"No free vampires to perform the ritual. {len(imprisoned)} imprisoned.")
        else:
            await safe_send(message.channel, content="No free vampires to perform the ritual.")
        return

    host = random.choice(free)
    old_power = coven['power']

    setup_embed = discord.Embed(title="Dark Ritual", color=discord.Color.dark_purple())
    setup_embed.description = (
        f"**{coven['name']}** convenes beneath the blood moon at {coven['lair']}.\n"
        f"Ritualist: `{host['name']}`  |  Dark Power: {old_power}"
    )
    setup_embed.set_footer(text="The ritual begins...")
    await safe_send(message.channel, embed=setup_embed)
    await asyncio.sleep(MSG_DELAY)

    num_events = random.randint(2, 4)
    power_change = 0
    members_imprisoned = []
    members_destroyed = []

    for i in range(num_events):
        await asyncio.sleep(MSG_DELAY)
        current_free = get_free_members(coven)
        if not current_free:
            break
        featured = random.choice(current_free)
        event = random.choice(RITUAL_EVENTS)
        desc = event['description'].replace("{member}", f"`{featured['name']}`").replace("{name}", coven['name'])

        ev_embed = discord.Embed(title=event['name'], description=desc, color=event['color'])
        extra = []

        if event['type'] == 'power_up':
            gain = random.randint(*event['value'])
            power_change += gain
            featured['hunts_survived'] += 1
            ev_embed.description += f"\n\nDark Power: +{gain}"

        elif event['type'] == 'power_down':
            loss = random.randint(*event['value'])
            power_change -= loss
            if event.get('betrayal'):
                featured['times_betrayed'] += 1
            ev_embed.description += f"\n\nDark Power: -{loss}"

        elif event['type'] == 'hunter_raid':
            rival = random.choice(VAMPIRE_COVENS)
            rival_power = random.randint(50, 400)
            slayer_name = random.choice(VAMPIRE_NAMES)
            loss = random.randint(40, 120)
            power_change -= loss
            alive_now = get_alive_members(coven)
            if len(alive_now) > 1:
                num_victims = min(random.randint(1, 2), len(alive_now) - 1)
                victims = random.sample(alive_now, num_victims)
                for v in victims:
                    v['alive'] = False
                    v['deaths'] += 1
                    members_destroyed.append(v['name'])
                    extra.append(f"`{v['name']}` was staked.")
            add_blood_debt(coven, slayer_name, rival, rival_power)
            ev_embed.description += f"\n\n**{rival['name']}** — `{slayer_name}` led the assault. Dark Power: -{loss}"
            if extra:
                ev_embed.description += "\nDestroyed: " + ", ".join(extra)
            ev_embed.set_footer(text=f"Type `bloodoak {code}` to answer.")

        elif event['type'] == 'rival_assault':
            rival = random.choice(VAMPIRE_COVENS)
            rival_power = random.randint(30, 300)
            crasher = random.choice(VAMPIRE_NAMES)
            loss = random.randint(20, 70)
            power_change -= loss
            cf = get_free_members(coven)
            if cf and random.randint(1, 100) <= 40:
                victim = random.choice(cf)
                s = imprison_member(victim)
                members_imprisoned.append((victim['name'], s))
                extra.append(f"`{victim['name']}` captured — {s}.")
            add_blood_debt(coven, crasher, rival, rival_power)
            ev_embed.description += f"\n\n**{rival['name']}** disrupted the ritual. Dark Power: -{loss}"
            if extra:
                ev_embed.description += "\n" + ", ".join(extra)
            ev_embed.set_footer(text=f"Type `bloodoak {code}` to retaliate.")

        elif event['type'] in ('church_patrol', 'inquisition', 'mass_arrest'):
            loss = random.randint(10, 80)
            power_change -= loss
            cf = get_free_members(coven)
            if event['type'] != 'church_patrol' and cf:
                count = 1 if event['type'] == 'inquisition' else random.randint(1, 2)
                arrested = random.sample(cf, min(count, len(cf)))
                for a in arrested:
                    s = imprison_member(a)
                    members_imprisoned.append((a['name'], s))
                    extra.append(f"`{a['name']}` — {s}.")
            ev_embed.description += f"\n\nDark Power: -{loss}"
            if extra:
                ev_embed.description += "\nImprisoned: " + ", ".join(extra)

        elif event['type'] == 'nothing':
            ev_embed.description += "\n\nDark Power: No change"

        if not ev_embed.footer.text:
            ev_embed.set_footer(text=f"Event {i + 1} of {num_events}")

        if len(ev_embed.description) > EMBED_DESC_LIMIT:
            ev_embed.description = ev_embed.description[:EMBED_DESC_LIMIT - 3] + "..."

        await safe_send(message.channel, embed=ev_embed)

    coven['power'] = max(1, coven['power'] + power_change)
    update_coven_lord(coven)
    check_and_mark_dead(code)
    await asyncio.sleep(MSG_DELAY)

    color = discord.Color.dark_red() if power_change >= 0 else discord.Color.dark_grey()
    power_display = (
        f"{old_power} -> {coven['power']} (+{power_change})"
        if power_change >= 0
        else f"{old_power} -> {coven['power']} ({power_change})"
    )

    summary = discord.Embed(title="Ritual — Complete", color=color)
    summary.description = (
        f"**{coven['name']}** at {coven['lair']} — the ritual is done.\n\n"
        f"Dark Power: {power_display}\n"
        f"Coven Lord: `{coven['leader']}`\n"
        f"Undead: {len(get_alive_members(coven))}  |  Free: {len(get_free_members(coven))}"
    )
    if members_destroyed:
        summary.description += "\nDestroyed: " + ", ".join(f"`{n}`" for n in members_destroyed)
    if members_imprisoned:
        summary.description += "\nImprisoned: " + ", ".join(f"`{n}` ({s})" for n, s in members_imprisoned)

    all_debts = get_blood_debts(coven)
    if all_debts:
        debt_text = "\n".join(f"**{t['coven']}** | `{t['name']}`" for t in all_debts)
        summary.description += f"\n\nBlood Debts:\n{debt_text}\n\nType `bloodoak {code}` to go after them."

    if len(summary.description) > EMBED_DESC_LIMIT:
        summary.description = summary.description[:EMBED_DESC_LIMIT - 3] + "..."

    summary.set_footer(text="The ritual is complete." if power_change >= 0 else "Dark forces stirred but not all went to plan.")
    await safe_send(message.channel, embed=summary)

    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed. Type `coven` to rise again.")


async def handle_dp(message, args):
    if len(args) < 2:
        await safe_send(message.channel, content="Usage: `dp <code> <name>`")
        return

    code = args[0].upper()
    member_name = " ".join(args[1:])
    coven = covens.get(code)

    if not coven:
        await safe_send(message.channel, content=f"No coven found with code `{code}`.")
        return
    if coven['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That is not your coven.")
        return
    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed.")
        return

    target = next((m for m in coven['members'] if m['name'].lower() == member_name.lower()), None)
    if not target:
        roster = ", ".join(f"`{m['name']}`" for m in get_alive_members(coven))
        await safe_send(message.channel, content=f"No member named `{member_name}`.\nUndead: {roster}")
        return
    if not target['alive']:
        await safe_send(message.channel, content=f"`{target['name']}` is already destroyed.")
        return
    if is_imprisoned(target):
        await safe_send(message.channel, content=f"`{target['name']}` is imprisoned right now.")
        return

    free = get_free_members(coven)
    judges = [m for m in free if m['name'] != target['name']]

    if not judges:
        await safe_send(message.channel, content="No other vampires free to sit in judgment.")
        return

    num_judges = min(len(judges), random.randint(2, 5))
    selected_judges = random.sample(judges, num_judges)
    judge_names = ", ".join(f"`{m['name']}`" for m in selected_judges)

    intro = discord.Embed(title="Court of Blood", color=discord.Color.dark_red())
    intro.description = (
        f"`{target['name']}` is called before the coven to answer for their transgressions.\n\n"
        f"**{coven['name']}** — {judge_names} preside."
    )
    intro.set_footer(text="The coven judges its own.")
    await safe_send(message.channel, embed=intro)
    await asyncio.sleep(MSG_DELAY)

    roll = random.randint(1, 100)

    if roll <= 15:
        target['alive'] = False
        target['deaths'] += 1
        check_and_mark_dead(code)
        update_coven_lord(coven)

        outcome_lines = random.choice([
            f"`{target['name']}` was dragged into the sunlight by order of the coven. Ash before the sentence was finished.",
            f"The judgment was final. `{target['name']}` was staked by the Coven Lord's own hand in front of all assembled.",
            f"There was no mercy in the chamber. `{target['name']}` met the true death before dawn.",
        ])

        embed = discord.Embed(title="Court of Blood — True Death", color=discord.Color.dark_grey())
        embed.description = (
            f"{outcome_lines}\n\n"
            f"Still Undead: {len(get_alive_members(coven))}\n"
            f"Coven Lord: `{coven['leader']}`"
        )
        embed.set_footer(text="The coven does not speak of what happened.")

    elif roll <= 40:
        coven['members'].remove(target)
        update_coven_lord(coven)

        outcome_lines = random.choice([
            f"`{target['name']}` was cast out from the coven. No lair, no protection, no blood rights. They walk alone now.",
            f"The judgment came down: banishment. `{target['name']}` was stripped of all rank and driven from the lair.",
            f"`{target['name']}` was exiled. Told never to return to **{coven['name']}** territory or face the true death.",
        ])

        embed = discord.Embed(title="Court of Blood — Exiled", color=discord.Color.dark_orange())
        embed.description = (
            f"{outcome_lines}\n\n"
            f"Still Undead: {len(get_alive_members(coven))}\n"
            f"Coven Lord: `{coven['leader']}`"
        )
        embed.set_footer(text="The coven does not claim them anymore.")

    else:
        power_loss = random.randint(5, 20)
        coven['power'] = max(1, coven['power'] - power_loss)

        beat_lines = [
            f"`{target['name']}` endured the Blood Ordeal — three nights of torment overseen by the coven. They emerged diminished but still undead. Still part of the family.",
            f"The punishment was severe and without mercy. `{target['name']}` bore it without breaking. The coven respects that, even now.",
            f"`{target['name']}` faced the full weight of the coven's judgment and did not flee. That counts for something in this dark world.",
            f"Every elder in that chamber put `{target['name']}` through the ordeal. They survived it. The matter is now closed.",
        ]

        embed = discord.Embed(title="Court of Blood — Punished and Kept", color=discord.Color.dark_purple())
        embed.description = (
            f"{random.choice(beat_lines)}\n\n"
            f"Dark Power: {coven['power'] + power_loss} -> {coven['power']} (-{power_loss})\n"
            f"Still Undead: {len(get_alive_members(coven))}\n"
            f"Coven Lord: `{coven['leader']}`"
        )
        embed.set_footer(text="They endured. They remain.")

    await safe_send(message.channel, embed=embed)


async def handle_gathering(message, args):
    if len(args) < 2:
        await safe_send(message.channel, content="Usage: `gathering <code> <number>`")
        return

    code = args[0].upper()
    coven = covens.get(code)

    if not coven:
        await safe_send(message.channel, content=f"No coven found with code `{code}`.")
        return
    if coven['owner_id'] != message.author.id:
        await safe_send(message.channel, content="That is not your coven.")
        return
    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed.")
        return

    try:
        requested = int(args[1])
    except ValueError:
        await safe_send(message.channel, content="Needs to be a number. Example: `gathering XKRV 3`")
        return

    if requested < 1:
        await safe_send(message.channel, content="Send at least 1.")
        return

    free = get_free_members(coven)
    if not free:
        imprisoned = [m for m in coven['members'] if m['alive'] and is_imprisoned(m)]
        if imprisoned:
            await safe_send(message.channel, content=f"No free vampires to attend. {len(imprisoned)} imprisoned right now.")
        else:
            await safe_send(message.channel, content="No free vampires to attend.")
        return

    actual = min(requested, len(free), 10)
    attending = random.sample(free, actual)
    attending_names = ", ".join(f"`{m['name']}`" for m in attending)
    location = random.choice(HUNT_LOCATIONS)
    old_power = coven['power']

    intro_embed = discord.Embed(title="The Gathering", color=discord.Color.dark_purple())
    intro_embed.description = (
        f"**{coven['name']}** descends upon {location}.\n\n"
        f"Attending: {attending_names}"
    )
    intro_embed.set_footer(text="Could be a feast. Could be a trap.")
    await safe_send(message.channel, embed=intro_embed)
    await asyncio.sleep(MSG_DELAY)

    power_change = 0
    fallen = []
    imprisoned_members = []

    rival_appears = random.randint(1, 100) <= 55
    rival_info = random.choice(VAMPIRE_COVENS) if rival_appears else None
    rival_power = random.randint(30, 400) if rival_appears else 0

    if rival_appears:
        rival_count = random.randint(2, 6)
        encounter_embed = discord.Embed(title="Rival Coven Arrives", color=discord.Color.red())
        encounter_embed.description = random.choice([
            f"**{rival_info['name']}** materialized from the shadows — {rival_count} strong. The air turned cold.",
            f"{rival_count} from **{rival_info['name']}** emerged from the darkness. Every eye in the room felt it.",
            f"Word rippled through the gathering — **{rival_info['name']}** had arrived. {rival_count} of them, ancient and hungry.",
            f"**{rival_info['name']}** crashed the gathering. {rival_count} vampires moved through the crowd like wraiths.",
        ])
        encounter_embed.set_footer(text="The outcome depends on power and numbers.")
        await safe_send(message.channel, embed=encounter_embed)
        await asyncio.sleep(MSG_DELAY)

        numbers_advantage = actual - rival_count
        power_diff = coven['power'] - rival_power
        win_chance = max(15, min(85, 50 + int((numbers_advantage / 5) * 20) + int((power_diff / 500) * 25)))
        fight_roll = random.randint(1, 100)

        if fight_roll <= win_chance:
            power_gain = random.randint(30, 100)
            power_change += power_gain
            coven['raids_won'] = coven.get('raids_won', 0) + 1

            for m in attending:
                m['kills'] += 1
                m['hunts_survived'] += 1

            update_coven_lord(coven)

            win_line = random.choice([
                f"**{coven['name']}** drove them into the dawn. Every last one. The gathering continued.",
                f"Claws and fangs met shadow. **{rival_info['name']}** had no answer. They fled or were destroyed.",
                f"The whole coven moved as one ancient predator. **{rival_info['name']}** never had a chance.",
                f"One signal and every vampire from **{coven['name']}** descended. The rival coven scattered into the mist.",
            ])

            if random.randint(1, 100) <= 20:
                victim = random.choice(attending)
                s = imprison_member(victim)
                imprisoned_members.append((victim['name'], s))
                win_line += f"\n\n`{victim['name']}` was caught by hunters who followed the chaos. Imprisoned for {s}."

            fight_embed = discord.Embed(title="Confrontation — Victorious", color=discord.Color.dark_red())
            fight_embed.description = (
                f"{win_line}\n\n"
                f"Dark Power: +{power_gain}\n"
                f"Coven Lord: `{coven['leader']}`"
            )
            fight_embed.set_footer(text="The gathering is ours.")
            await safe_send(message.channel, embed=fight_embed)

        elif fight_roll <= win_chance + 25:
            power_loss = random.randint(20, 60)
            power_change -= power_loss
            coven['raids_lost'] = coven.get('raids_lost', 0) + 1

            chaos_line = random.choice([
                f"The confrontation turned the gathering into a battlefield. **{coven['name']}** survived but not cleanly.",
                f"Chaos erupted. Vampire hunters arrived drawn by the violence. **{coven['name']}** fled into the night.",
                f"Both covens brawled until the sky began to lighten. **{coven['name']}** pulled out but left marks behind.",
            ])

            alive_now = get_alive_members(coven)
            if len(alive_now) > 1 and random.randint(1, 100) <= 35:
                victim = random.choice([m for m in attending if m['alive']])
                victim['alive'] = False
                victim['deaths'] += 1
                fallen.append(victim['name'])
                chaos_line += f"\n\n`{victim['name']}` was staked in the chaos."
                slayer_name = random.choice(VAMPIRE_NAMES)
                add_blood_debt(coven, slayer_name, rival_info, rival_power)

            if random.randint(1, 100) <= 30:
                still_free = [m for m in attending if m['alive'] and not is_imprisoned(m)]
                if still_free:
                    victim = random.choice(still_free)
                    s = imprison_member(victim)
                    imprisoned_members.append((victim['name'], s))
                    chaos_line += f"\n`{victim['name']}` was captured — {s}."

            update_coven_lord(coven)
            chaos_embed = discord.Embed(title="Confrontation — Chaos", color=discord.Color.dark_orange())
            chaos_embed.description = (
                f"{chaos_line}\n\n"
                f"Dark Power: -{power_loss}\n"
                f"Coven Lord: `{coven['leader']}`"
            )
            chaos_embed.set_footer(text="A costly night.")
            await safe_send(message.channel, embed=chaos_embed)

        else:
            power_loss = random.randint(50, 130)
            power_change -= power_loss
            coven['raids_lost'] = coven.get('raids_lost', 0) + 1

            loss_line = random.choice([
                f"**{rival_info['name']}** came prepared for war. **{coven['name']}** was driven from the gathering.",
                f"The numbers were wrong and the power was wrong. **{coven['name']}** took heavy losses and retreated.",
                f"**{rival_info['name']}** moved first and showed no mercy. **{coven['name']}** barely escaped total destruction.",
            ])

            alive_now = get_alive_members(coven)
            victims_count = random.randint(1, min(2, max(1, len(alive_now) - 1)))
            if len(alive_now) > 1:
                victims = random.sample([m for m in attending if m['alive']], min(victims_count, len([m for m in attending if m['alive']])))
                for v in victims:
                    v['alive'] = False
                    v['deaths'] += 1
                    fallen.append(v['name'])
                    loss_line += f"\n`{v['name']}` was destroyed."
                slayer_name = random.choice(VAMPIRE_NAMES)
                add_blood_debt(coven, slayer_name, rival_info, rival_power)

            if random.randint(1, 100) <= 40:
                still_free = [m for m in attending if m['alive'] and not is_imprisoned(m)]
                if still_free:
                    victim = random.choice(still_free)
                    s = imprison_member(victim)
                    imprisoned_members.append((victim['name'], s))
                    loss_line += f"\n`{victim['name']}` was captured fleeing — {s}."

            update_coven_lord(coven)
            loss_embed = discord.Embed(title="Confrontation — Routed", color=discord.Color.dark_grey())
            loss_embed.description = (
                f"{loss_line}\n\n"
                f"Dark Power: -{power_loss}\n"
                f"Coven Lord: `{coven['leader']}`"
            )
            loss_embed.set_footer(text=f"Type `bloodoak {code}` when you are ready.")
            await safe_send(message.channel, embed=loss_embed)

        await asyncio.sleep(MSG_DELAY)

    else:
        clean_lines = []
        for m in attending:
            event_roll = random.randint(1, 100)
            if event_roll <= 50:
                gain = random.randint(5, 25)
                power_change += gain
                m['hunts_survived'] += 1
                clean_lines.append(random.choice([
                    f"`{m['name']}` forged alliances with ancient vampires. +{gain} dark power.",
                    f"`{m['name']}` fed well and represented the coven with authority. +{gain} dark power.",
                    f"`{m['name']}` made contact with powerful undead who owe favors now. +{gain} dark power.",
                    f"`{m['name']}` left an impression on those who matter in these circles. +{gain} dark power.",
                ]))
            elif event_roll <= 65:
                s = imprison_member(m)
                imprisoned_members.append((m['name'], s))
                loss = random.randint(10, 30)
                power_change -= loss
                clean_lines.append(f"`{m['name']}` was seized by hunters on the way out. Imprisoned for {s}. -{loss} dark power.")
            elif event_roll <= 75:
                loss = random.randint(5, 20)
                power_change -= loss
                clean_lines.append(random.choice([
                    f"`{m['name']}` made enemies of the wrong elder vampires. -{loss} dark power.",
                    f"`{m['name']}` caused a scene that embarrassed the coven. -{loss} dark power.",
                ]))
            else:
                clean_lines.append(random.choice([
                    f"`{m['name']}` moved through the gathering quietly. Nothing gained, nothing lost.",
                    f"`{m['name']}` kept to the shadows and observed. A cautious night.",
                    f"`{m['name']}` stayed out of the politics and fed in peace.",
                ]))

        update_coven_lord(coven)
        peaceful_embed = discord.Embed(title="No Rivals Tonight", color=discord.Color.dark_purple())
        peaceful_embed.description = "\n".join(clean_lines) if clean_lines else "Nothing to report."
        peaceful_embed.set_footer(text="A clean night.")
        await safe_send(message.channel, embed=peaceful_embed)
        await asyncio.sleep(MSG_DELAY)

    coven['power'] = max(1, old_power + power_change)
    check_and_mark_dead(code)

    color = discord.Color.dark_red() if power_change >= 0 else discord.Color.dark_grey()
    power_display = (
        f"{old_power} -> {coven['power']} (+{power_change})"
        if power_change >= 0
        else f"{old_power} -> {coven['power']} ({power_change})"
    )

    summary_embed = discord.Embed(title="Gathering — Night Over", color=color)
    summary_embed.description = (
        f"**{coven['name']}** returns from {location}.\n\n"
        f"Dark Power: {power_display}\n"
        f"Coven Lord: `{coven['leader']}`\n"
        f"Undead: {len(get_alive_members(coven))}  |  Free: {len(get_free_members(coven))}"
    )

    if fallen:
        summary_embed.description += "\nDestroyed: " + ", ".join(f"`{n}`" for n in fallen)
    if imprisoned_members:
        summary_embed.description += "\nImprisoned: " + ", ".join(f"`{n}` ({s})" for n, s in imprisoned_members)

    all_debts = get_blood_debts(coven)
    if all_debts:
        debt_text = "\n".join(f"**{t['coven']}** | `{t['name']}`" for t in all_debts)
        summary_embed.description += f"\n\nBlood Debts:\n{debt_text}\n\nType `bloodoak {code}` to collect."

    if len(summary_embed.description) > EMBED_DESC_LIMIT:
        summary_embed.description = summary_embed.description[:EMBED_DESC_LIMIT - 3] + "..."

    summary_embed.set_footer(text="The night is done." if power_change >= 0 else "Losses taken. Regroup before dawn.")
    await safe_send(message.channel, embed=summary_embed)

    if not coven['alive']:
        await safe_send(message.channel, content=f"**{coven['name']}** has been destroyed. Type `coven` to rise again.")


async def handle_disband(message, args):
    if not args:
        await safe_send(message.channel, content="Usage: `disband <code>`")
        return

    code = args[0].upper()
    coven = covens.get(code)

    if not coven:
        await safe_send(message.channel, content=f"No coven found with code `{code}`.")
        return
    if coven['owner_id'] != message.author.id and not is_admin(message):
        await safe_send(message.channel, content="That is not your coven.")
        return

    coven_name = coven['name']
    owner_id = coven['owner_id']
    del covens[code]
    if not user_has_active_coven(owner_id):
        active_coven_lords.discard(owner_id)

    embed = discord.Embed(
        title="Coven Disbanded",
        description=f"**{coven_name}** (`{code}`) has been dissolved into shadow. Type `coven` to rise again.",
        color=discord.Color.dark_grey()
    )
    await safe_send(message.channel, embed=embed)


# --- Blood Feeding Events ---

BLOOD_EVENTS = [
    {"name": "Midnight Feast", "description": "{member} located an isolated manor and fed deeply on the inhabitants. **{name}** is sated and strengthened.", "type": "blood_win", "value": (40, 120), "color": discord.Color.dark_red()},
    {"name": "Mass Feeding", "description": "{member} connected with a contact who provided exclusive access to a blood farm. **{name}** fed without restraint.", "type": "blood_win", "value": (80, 200), "color": discord.Color.dark_red()},
    {"name": "New Hunting Grounds", "description": "{member} claimed an unguarded village on the outskirts. By midnight the coven had a new feeding territory.", "type": "blood_win", "value": (50, 130), "color": discord.Color.dark_red()},
    {"name": "Rare Bloodline Found", "description": "The new prey carried an ancient bloodline more potent than anything **{name}** had tasted before. {member} sampled it and the power was immediate.", "type": "blood_win", "value": (60, 150), "color": discord.Color.dark_red()},
    {"name": "Thrall Network Expanded", "description": "{member} went directly to a high-value thrall who could supply willing victims indefinitely. **{name}**'s feeding operation just scaled up.", "type": "blood_win", "value": (70, 160), "color": discord.Color.dark_red()},
    {"name": "Loyal Blood Cattle", "description": "The willing servants came through all night without prompting. {member} fed well and the power flowed into **{name}**.", "type": "blood_win", "value": (30, 90), "color": discord.Color.dark_red()},
    {"name": "Traveling Merchant Bled", "description": "{member} encountered a wealthy merchant traveling alone and drained them completely. **{name}** bought low and fed for triple the cost.", "type": "blood_win", "value": (90, 220), "color": discord.Color.dark_red()},
    {"name": "Secret Feeding Den", "description": "{member} set up a discreet feeding chamber — no exposure, just a steady stream of mesmerized victims through the night. **{name}** fed without risk.", "type": "blood_win", "value": (45, 110), "color": discord.Color.dark_red()},
    {"name": "Ancient Vitae Secured", "description": "A contact of {member}'s delivered a cache of ancient preserved blood of tremendous potency. **{name}** is fortified.", "type": "blood_win", "value": (55, 140), "color": discord.Color.dark_red()},
    {"name": "First-Time Thralls Bound", "description": "{member} mesmerized three mortals who had never served a vampire before. By morning all three were devoted servants of **{name}**.", "type": "blood_win", "value": (35, 85), "color": discord.Color.dark_red()},
    {"name": "Noble's Blood", "description": "{member} was introduced to a nobleman of exceptional vitae who offered themselves willingly for power and protection. **{name}** has a new high-value source.", "type": "blood_win", "value": (100, 250), "color": discord.Color.dark_red()},
    {"name": "Quick Feed", "description": "{member} found prey, fed efficiently, and was gone before anyone noticed. Clean, quiet, powerful.", "type": "blood_win", "value": (25, 70), "color": discord.Color.dark_red()},
    {"name": "Blood Tax Collected", "description": "A smaller coven was using **{name}**'s hunting ground without permission. {member} paid them a visit and now they tithe monthly.", "type": "blood_win", "value": (40, 100), "color": discord.Color.dark_red()},
    {"name": "Vitae Diluted Perfectly", "description": "{member} stretched the stored vitae without weakening its essence. Same power, twice the volume. **{name}**'s reserves are full.", "type": "blood_win", "value": (50, 120), "color": discord.Color.dark_red()},
    {"name": "Rival Feeding Ground Seized", "description": "The rival coven had prime hunting territory. {member} moved in when they were weakened and claimed it completely. **{name}** feeds there now.", "type": "blood_win", "value": (80, 180), "color": discord.Color.dark_red()},
    {"name": "Van Helsing's Trap", "description": "{member} was closing in on prey when the hunter revealed themselves. A silver-lined cage snapped shut before escape was possible.", "type": "blood_imprisoned", "value": (30, 80), "color": discord.Color.blue()},
    {"name": "Church Patrol Ambush", "description": "{member} was moving through consecrated ground when holy warriors descended. Silver chains and daylight-proof cells await.", "type": "blood_imprisoned", "value": (25, 70), "color": discord.Color.blue()},
    {"name": "Inquisitor's Sting", "description": "The Inquisition had been running controlled hunts on the feeding ground for weeks. {member} didn't know. The imprisonment was planned before they even left the lair.", "type": "blood_imprisoned", "value": (35, 90), "color": discord.Color.blue()},
    {"name": "Lair Location Betrayed", "description": "Someone gave up the location of **{name}**'s feeding den. Hunters hit it with blessed weapons at dawn. {member} was inside with nowhere to go.", "type": "blood_imprisoned", "value": (40, 100), "color": discord.Color.blue()},
    {"name": "Informant in the Thrall Pool", "description": "A regular thrall had been working with hunters for months. Every feeding session {member} conducted was reported. The capture came on a moonless night.", "type": "blood_imprisoned", "value": (50, 120), "color": discord.Color.blue()},
    {"name": "Vatican Special Forces", "description": "The Church had been watching for six months. {member} didn't know the thrall was compromised. Every movement, every feeding location, every victim — all documented. Captured without a fight.", "type": "blood_imprisoned", "value": (60, 150), "color": discord.Color.blue()},
    {"name": "Caught Feeding", "description": "{member} was seized mid-drain by a hunter cell. Simple trespassing became an indefinite imprisonment once they identified what {member} was.", "type": "blood_imprisoned", "value": (20, 60), "color": discord.Color.blue()},
    {"name": "Mesmer Failed", "description": "Hunters built immunity to vampire hypnosis. {member} tried to mesmerize a target and nothing happened. Silver net followed immediately.", "type": "blood_imprisoned", "value": (35, 85), "color": discord.Color.blue()},
    {"name": "Dawn Sweep", "description": "Hunter guilds swept the district at dawn and seized every vampire caught above ground. {member} was one of them.", "type": "blood_imprisoned", "value": (25, 65), "color": discord.Color.blue()},
    {"name": "Vampire Hunter Task Force", "description": "A specialized hunter unit had **{name}**'s operation mapped for months. Hit four lairs simultaneously at sunrise. {member} was at one of them.", "type": "blood_imprisoned", "value": (55, 140), "color": discord.Color.blue()},
    {"name": "Blood Feud Ambush", "description": "A rival coven knew where {member} hunted and hired mortal assassins to wait there. {member} was overwhelmed and did not return.", "type": "blood_killed", "value": (40, 100), "color": discord.Color.dark_grey()},
    {"name": "Rival Coven Struck the Feeding Ground", "description": "The rival coven knew exactly where **{name}** hunted. They came in force and {member} was found alone with no backup and no exit.", "type": "blood_killed", "value": (50, 120), "color": discord.Color.dark_grey()},
    {"name": "Sunlight Trap", "description": "The lair was rigged with mirrors that reflected dawn light. {member} was caught in the beams before the horror registered. Ash before noon.", "type": "blood_killed", "value": (45, 110), "color": discord.Color.dark_grey()},
    {"name": "Staked at the Feeding Ground", "description": "The rival coven returned over a grievance from three months ago and {member} was the one they found. Caught alone without the coven nearby.", "type": "blood_killed", "value": (55, 130), "color": discord.Color.dark_grey()},
    {"name": "Betrayed by the Prey", "description": "The mortal {member} chose to feed from was a willing vessel for a rival coven's trap. Sent there with purpose. No way out.", "type": "blood_killed", "value": (60, 150), "color": discord.Color.dark_grey()},
    {"name": "Bloodless Night", "description": "{member} hunted for six hours and found no suitable prey. Nobody came through the feeding ground. **{name}**'s hunger grows.", "type": "blood_nothing", "color": discord.Color.greyple()},
    {"name": "Too Many Hunters", "description": "Patrols moved through the hunting ground every twenty minutes. {member} kept the hunger at bay rather than risk exposure. A cautious but empty night.", "type": "blood_nothing", "color": discord.Color.greyple()},
    {"name": "Tainted Blood", "description": "The available prey had been drugged or poisoned — a hunter trick. {member} detected it and refused to feed rather than risk corruption. **{name}** protects its own.", "type": "blood_nothing", "color": discord.Color.greyple()},
    {"name": "No-Show Prey", "description": "{member} waited four hours at the arranged feeding location. The mesmerized thrall never arrived. Night wasted.", "type": "blood_nothing", "color": discord.Color.greyple()},
    {"name": "Rival Coven Moved In", "description": "Another coven set up hunting on **{name}**'s grounds and scared all the prey away. {member} went hungry. That coven needs to be dealt with.", "type": "blood_nothing", "color": discord.Color.greyple()},
]

# --- Regular Hunt Events ---

EVENTS = [
    {"name": "Territory Claimed", "description": "{member} moved through every shadow on the road to the old cathedral and established dominion. By morning **{name}** owned that entire district.", "type": "power_up", "value": (20, 80), "color": discord.Color.dark_red()},
    {"name": "Successful Feed", "description": "{member} located a perfect victim and fed deeply. **{name}** is fortified for months.", "type": "power_up", "value": (30, 100), "color": discord.Color.dark_red()},
    {"name": "Blood Duel Victory", "description": "{member} encountered four vampires from a rival coven outside the cathedral, fought them alone, destroyed two, and walked away. **{name}**'s name echoed in the dark.", "type": "power_up", "value": (20, 60), "color": discord.Color.dark_red()},
    {"name": "Lair Expanded", "description": "{member} led **{name}** into catacombs the rival coven had held for centuries. Claimed them in open night. Nobody challenged the claim.", "type": "power_up", "value": (40, 120), "color": discord.Color.dark_red()},
    {"name": "Elder Vampire's Blessing", "description": "An ancient elder pulled {member} aside and made several immortal introductions. Doors opened for **{name}** that no mortal could ever unlock.", "type": "power_up", "value": (50, 150), "color": discord.Color.dark_red()},
    {"name": "Blood Debt Repaid", "description": "{member} waited three decades then delivered the reckoning personally. The immortal world went quiet. **{name}** does not forget.", "type": "power_up", "value": (60, 180), "color": discord.Color.dark_red()},
    {"name": "Underworld Connections Made", "description": "{member} made the right introductions in the shadow courts. **{name}** now has contacts in three vampire councils.", "type": "power_up", "value": (40, 100), "color": discord.Color.dark_red()},
    {"name": "Rival Coven Scattered", "description": "{member} descended on the rival's primary lair with the full coven. One warning. Forty-eight hours later **{name}** controlled three new territories.", "type": "power_up", "value": (80, 200), "color": discord.Color.dark_red()},
    {"name": "Bard Composed a Saga", "description": "A cursed bard composed a saga about {member}'s deeds — **{name}** repped fully. Three kingdoms were speaking the coven's name by dawn.", "type": "power_up", "value": (50, 130), "color": discord.Color.dark_red()},
    {"name": "Mortals Protected", "description": "{member} secretly protected a village from a monster, earning loyalty without revealing what they were. **{name}** has the mortals locked in.", "type": "power_up", "value": (25, 70), "color": discord.Color.dark_red()},
    {"name": "Ancient Score", "description": "{member} orchestrated the biggest feeding since **{name}** was founded. Blood moved fast, power came back enormous. Everyone fed.", "type": "power_up", "value": (60, 160), "color": discord.Color.dark_red()},
    {"name": "Reclaimed Lost Territory", "description": "The rival coven had **{name}**'s old hunting ground for six centuries. {member} moved at the new moon. By sunrise **{name}**'s banner flew there again.", "type": "power_up", "value": (70, 170), "color": discord.Color.dark_red()},
    {"name": "Fulfilled a Blood Contract", "description": "There was a contract. {member} completed it quietly with no witnesses. **{name}** moves differently because of vampires like that.", "type": "power_up", "value": (80, 200), "color": discord.Color.dark_red()},
    {"name": "Trial Collapsed", "description": "The Inquisition's key witness was found thoroughly mesmerized. {member} walked out of the hearing chamber and returned directly to the lair.", "type": "power_up", "value": (40, 110), "color": discord.Color.dark_red()},
    {"name": "Mortal Loyalty Cemented", "description": "Three families swore they saw nothing — and meant it. {member} built that loyalty over lifetimes. **{name}** is protected by the very mortals hunters would question.", "type": "power_up", "value": (35, 95), "color": discord.Color.dark_red()},
    {"name": "New Blood Source", "description": "{member} established contact with a new willing bloodline. First feeding was exceptional. **{name}**'s operation has leveled up.", "type": "power_up", "value": (60, 150), "color": discord.Color.dark_red()},
    {"name": "Relic Recovered", "description": "{member} located an ancient vampire relic buried for centuries and returned it to the coven. **{name}** has something no other coven holds.", "type": "power_up", "value": (55, 140), "color": discord.Color.dark_red()},
    {"name": "Hidden Armory Found", "description": "{member} discovered a cache of weapons and artifacts the rival coven had stored away. Brought everything back. **{name}** is now better armed than ever.", "type": "power_up", "value": (55, 140), "color": discord.Color.dark_red()},
    {"name": "Ransom Collected", "description": "{member} organized the coven to secure a valuable hostage and collect ransom from a noble family. **{name}** operates at every level.", "type": "power_up", "value": (30, 80), "color": discord.Color.dark_red()},
    {"name": "Shadow Tax Enforced", "description": "A merchant caravan had been passing through **{name}**'s territory without tribute. {member} corrected that. Word travels. **{name}** collects from four routes now.", "type": "power_up", "value": (45, 115), "color": discord.Color.dark_red()},
    {"name": "Turned a Promising Mortal", "description": "{member} oversaw the turning of a mortal who had been proving themselves for months. The whole coven watched. **{name}** is growing with purpose.", "type": "power_up", "value": (20, 55), "color": discord.Color.dark_red()},
    {"name": "Shadow Tax Expanded", "description": "Two operations had been ignoring **{name}**'s tribute demands. {member} paid personal visits. Both paid before the next moonrise.", "type": "power_up", "value": (50, 125), "color": discord.Color.dark_red()},
    {"name": "Witness Mesmerized", "description": "There was a trial threatening the coven with a key witness. {member} ensured that witness remembered nothing at all. The case dissolved the next morning.", "type": "power_up", "value": (65, 160), "color": discord.Color.dark_red()},
    {"name": "Lair Assault — Clean", "description": "{member} hit a rival lair that had been observed for two weeks. In and out before the moon moved. No survivors, no trail. **{name}** fed well.", "type": "power_up", "value": (55, 135), "color": discord.Color.dark_red()},
    {"name": "Rival Lord Destroyed", "description": "The rival coven's leader had been a problem for centuries. {member} found them at rest and ensured they would never rise again.", "type": "power_up", "value": (90, 220), "color": discord.Color.dark_red()},
    {"name": "Protected the Lair", "description": "A wandering vampire tried to claim **{name}**'s territory. {member} gathered the coven and drove them out before they grew comfortable. They have not returned.", "type": "power_up", "value": (45, 110), "color": discord.Color.dark_red()},
    {"name": "Elder's Funeral Attended", "description": "{member} organized **{name}**'s presence at a fallen elder's memorial — solemn, organized, respectful. The ancient ones noticed. Old alliances reformed.", "type": "power_up", "value": (30, 75), "color": discord.Color.dark_red()},
    {"name": "Blood Feud Ended", "description": "A centuries-old blood feud with a neighboring coven was costing both sides feeding grounds. {member} brokered a truce. **{name}** now has an alliance where there was only war.", "type": "power_up", "value": (60, 145), "color": discord.Color.dark_red()},
    {"name": "Church Donation", "description": "{member} made a substantial anonymous donation to the cathedral — funds that ensured the bishop would look elsewhere during the next hunt. Divine corruption in service of darkness.", "type": "power_up", "value": (25, 65), "color": discord.Color.dark_red()},
    {"name": "Rival Vitae Stolen", "description": "{member} had been watching the rival's blood reserve for decades. Struck at the perfect moment — took everything and left nothing. **{name}** feasts on the competition's stockpile.", "type": "power_up", "value": (75, 185), "color": discord.Color.dark_red()},
    {"name": "Traitor in the Coven", "description": "A sealed document surfaced — {member}'s name was on it. Cooperating with hunters since the last eclipse. **{name}** is fractured. Trust is ash.", "type": "power_down", "value": (30, 100), "color": discord.Color.dark_orange(), "betrayal": True},
    {"name": "Hunt Gone Wrong", "description": "{member} hesitated at the killing moment. Three mortals witnessed the entire scene. **{name}** is exposed and mocked in the shadow courts.", "type": "power_down", "value": (20, 80), "color": discord.Color.dark_orange()},
    {"name": "Member Captured", "description": "A hunter task force arrived with a warrant already sealed. {member} was taken before dawn. No bail, no rescue. **{name}** lost one of their most formidable vampires overnight.", "type": "power_down", "value": (40, 120), "color": discord.Color.dark_orange()},
    {"name": "Lair Breached", "description": "The hunters arrived in force while the coven slept. {member} tried to hold the entrance but the math was impossible. The whole immortal world witnessed the retreat.", "type": "power_down", "value": (50, 150), "color": discord.Color.dark_orange()},
    {"name": "Internal Power Struggle", "description": "{member} and another vampire clashed over hunting rights in front of mortal thralls. The argument was recorded. Other covens are laughing.", "type": "power_down", "value": (25, 75), "color": discord.Color.dark_orange()},
    {"name": "Inquisition Raid", "description": "Forty soldiers of the Church descended on **{name}**'s lair at dawn. {member} barely escaped through a hidden passage. The lair is lost. The operation pauses.", "type": "power_down", "value": (60, 180), "color": discord.Color.dark_orange()},
    {"name": "Caught Unawares", "description": "The rival coven found {member} alone at a blood market. Took everything, recorded it, distributed it. **{name}**'s shame echoes through three shadow courts.", "type": "power_down", "value": (30, 90), "color": discord.Color.dark_orange()},
    {"name": "Vitae Cache Lost", "description": "{member} lost the entire reserve during a hunter ambush. **{name}** lost the blood, the power, and the blood source is threatening to cut ties.", "type": "power_down", "value": (45, 130), "color": discord.Color.dark_orange()},
    {"name": "Coven Member Turned", "description": "{member} had been feeding information to the Inquisition for months. The arrests came on a Tuesday. **{name}** lost four members to holy imprisonment in a single night.", "type": "power_down", "value": (50, 160), "color": discord.Color.dark_orange(), "betrayal": True},
    {"name": "Overwhelmed by Hunters", "description": "Eight hunters cornered {member} in daylight with witnesses everywhere. Silver nets and blessed bolts. **{name}**'s name is on that report.", "type": "power_down", "value": (35, 110), "color": discord.Color.dark_orange()},
    {"name": "Lair Burned", "description": "Someone gave up the location. Hunters hit it at noon with fire. {member} escaped through a drain. Centuries of accumulated power gone in minutes.", "type": "power_down", "value": (55, 150), "color": discord.Color.dark_orange()},
    {"name": "Blood Duel Lost", "description": "{member} challenged a rival vampire in a formal blood duel and was decisively defeated. Three witnesses, and the word has spread. **{name}** looks weak and the hunters are emboldened.", "type": "power_down", "value": (30, 85), "color": discord.Color.dark_orange()},
    {"name": "Lair Raid Failed", "description": "{member} led an assault on a rival lair that turned out to be heavily defended. Returned empty-handed. The whole shadow court heard about it by morning. **{name}** is catching mockery.", "type": "power_down", "value": (20, 65), "color": discord.Color.dark_orange()},
    {"name": "Banishment Invoked", "description": "{member} violated an ancient compact and a vampire elder invoked formal banishment. **{name}** lost one of their strongest and the insult stings.", "type": "power_down", "value": (30, 80), "color": discord.Color.dark_orange()},
    {"name": "Blood Gold Stolen Internally", "description": "Stored vitae went missing from the lair and all evidence pointed to {member}. Whether they took it or not the trust is destroyed. **{name}** is feeding on itself.", "type": "power_down", "value": (40, 100), "color": discord.Color.dark_orange()},
    {"name": "Marked by the Inquisition", "description": "An Inquisitor appeared at the lair entrance with a formal notice of investigation. Did not enter — just left the notice and stared. **{name}** must move with maximum caution now.", "type": "power_down", "value": (35, 90), "color": discord.Color.dark_orange()},
    {"name": "Desecrated at the Memorial", "description": "The rival coven disrupted **{name}**'s fallen member's memorial rites. {member} could not respond with the elder vampires watching. The disrespect has spread through every shadow court.", "type": "power_down", "value": (45, 110), "color": discord.Color.dark_orange()},
    {"name": "Royal Edict Against the Coven", "description": "The mortal king issued an edict targeting **{name}**'s known territories. {member} cannot move openly, cannot feed publicly, cannot even exist in certain districts without risking discovery.", "type": "power_down", "value": (50, 130), "color": discord.Color.dark_orange()},
    {"name": "Shadow Court Doxed", "description": "{member} argued publicly with a rival and revealed too much — locations, feeding schedules, the identities of thralls. The Inquisition has all of it now. **{name}** is compromised at every level.", "type": "power_down", "value": (25, 70), "color": discord.Color.dark_orange()},
    {"name": "Quiet Night", "description": "{member} kept watch over the lair all night. Nothing moved. **{name}** is vigilant and patient.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Hiding from Hunters", "description": "Too much light. Church patrols every hour. {member} kept **{name}** in the deepest shadows tonight. Wise.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Watching and Waiting", "description": "{member} spent the night mapping the rival coven's movements. No action tonight — intelligence gathering. **{name}** builds a picture slowly.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Regrouping", "description": "{member} gathered all surviving members after recent losses. Honest accounting of what went wrong. **{name}** emerged from the conversation more focused.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Nothing Stirred", "description": "A dead night. {member} sat in the dark for four hours and not a soul passed by. **{name}** endures.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "The Ambush That Never Came", "description": "{member} prepared an ambush that was never triggered. The target did not appear. **{name}** remains ready.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Armory Checked", "description": "{member} catalogued **{name}**'s weapons, relics, and reserves tonight. Everything accounted for. Prepared for what comes next.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Stayed in the Lair", "description": "Word reached the coven that something dangerous was moving through the night but its nature was unclear. {member} kept **{name}** inside. Nothing came. The right call.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Conflicting Omens", "description": "Contradictory signs sent **{name}** in three directions tonight. {member} called off all movement before anyone committed to a wrong path. Cautious.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Dawn Came Early", "description": "The sky lightened faster than predicted. {member} drove everyone underground immediately. The lair is still there tomorrow. That is enough.", "type": "nothing", "color": discord.Color.greyple()},
]

# --- Ritual Events ---

RITUAL_EVENTS = [
    {"name": "Ritual Empowered", "description": "The dark rite reached its crescendo and power flooded into the chamber. {member} completed the final invocation. **{name}** shook with ancient energy.", "type": "power_up", "value": (40, 100), "color": discord.Color.dark_purple()},
    {"name": "Community of Thralls", "description": "Loyal mortals arrived from three districts to offer their blood willingly. {member} oversaw the collection personally.", "type": "power_up", "value": (30, 80), "color": discord.Color.dark_purple()},
    {"name": "Ancient Elder Manifested", "description": "An elder vampire who had not been seen in public in centuries appeared at the ritual. Sat with {member} for hours and confirmed ancient alliances.", "type": "power_up", "value": (50, 130), "color": discord.Color.dark_purple()},
    {"name": "Rival Coven Sent Tribute", "description": "A rival coven sent an emissary through with blood tribute and a written acknowledgment of **{name}**'s supremacy in this territory.", "type": "power_up", "value": (35, 90), "color": discord.Color.dark_purple()},
    {"name": "Ritual Lasts All Night", "description": "Started at the new moon, still burning at cockcrow. {member} maintained the invocations without faltering. People who should have left stayed until the end.", "type": "power_up", "value": (45, 110), "color": discord.Color.dark_purple()},
    {"name": "The Prophecy Heard", "description": "A vampire seer appeared and made a pronouncement in front of all assembled. {member} handled the exchange masterfully. A segment aired in the shadow courts the next night.", "type": "power_up", "value": (40, 100), "color": discord.Color.dark_purple()},
    {"name": "Fledglings Initiated", "description": "Three newly turned vampires watched **{name}**'s ritual with reverence. Before it was over all three had formally pledged their loyalty to the coven.", "type": "power_up", "value": (25, 65), "color": discord.Color.dark_purple()},
    {"name": "Shadow Court Observing", "description": "Representatives of three vampire courts attended uninvited and stood in silence. {member} maintained the ritual without acknowledging them. **{name}** just earned political standing.", "type": "power_up", "value": (35, 85), "color": discord.Color.dark_purple()},
    {"name": "Ancient Relic Activated", "description": "{member} channeled power through an ancient relic during the ritual. Families of thralls brought themselves forward afterward without being asked. **{name}**'s dominion is absolute in this region.", "type": "power_up", "value": (30, 75), "color": discord.Color.dark_purple()},
    {"name": "Blood Mage Performed", "description": "A respected blood mage worked the ritual under **{name}**'s banner. {member} arranged it. The power gathered was three times what was expected.", "type": "power_up", "value": (45, 115), "color": discord.Color.dark_purple()},
    {"name": "Undead Court Convened", "description": "{member} organized a vampire council at the ritual. Elders sat, disputes were settled, and **{name}** emerged as the acknowledged authority in these territories.", "type": "power_up", "value": (30, 80), "color": discord.Color.dark_purple()},
    {"name": "Spirit of the First Vampire", "description": "A manifestation of the first vampire ancestor blessed the ritual. Said **{name}** carried on the true legacy of the undead. That blessing carries weight in every court.", "type": "power_up", "value": (25, 65), "color": discord.Color.dark_purple()},
    {"name": "Blood Feast Concluded", "description": "{member} arranged for a feast of blood after the ritual concluded. Three thrall families came for free in exchange for protection. The coven fed better tonight than in many years.", "type": "power_up", "value": (40, 95), "color": discord.Color.dark_purple()},
    {"name": "Lair Consecrated", "description": "By the ritual's end every vampire in this district knew **{name}**'s name. {member} ensured it — ancient compacts renewed, oaths sworn, power solidified.", "type": "power_up", "value": (35, 90), "color": discord.Color.dark_purple()},
    {"name": "Hunter Raid — Ritual Interrupted", "description": "Armed hunters breached the ritual site with silver and fire. {member} saw it half a second before impact. No time. The sacred rite was shattered.", "type": "hunter_raid", "color": discord.Color.dark_red()},
    {"name": "Second Wave of Hunters", "description": "The first group was a distraction. When the coven focused on them the real hunters came through the back. By the time the ritual ended the losses were severe.", "type": "hunter_raid", "color": discord.Color.dark_red()},
    {"name": "Inquisition Aerial Strike", "description": "Church archers on the rooftops opened fire with blessed bolts simultaneously from both sides. {member} dove for cover. The ritual site is now consecrated ground. Unusable.", "type": "hunter_raid", "color": discord.Color.dark_red()},
    {"name": "Rival Coven Disrupted the Ritual", "description": "Six of them emerged from summoning smoke during the most critical moment. {member} tried to complete the invocation but the disruption was total.", "type": "rival_assault", "color": discord.Color.red()},
    {"name": "Ancient Enemy Broke Through", "description": "An elder vampire of the rival coven forced entry through the warding and started destroying the ritual circle. {member} stepped up and the confrontation turned violent.", "type": "rival_assault", "color": discord.Color.red()},
    {"name": "Power Struggle Mid-Ritual", "description": "A faction within the assembled vampires challenged the leadership during the most exposed moment of the rite. {member} tried to maintain order. Blood was spilled in the ritual chamber.", "type": "rival_assault", "color": discord.Color.red()},
    {"name": "Church Patrol Observed", "description": "Two Inquisition patrols circled the ritual site for hours asking questions that received no answers. {member} kept the coven composed. They left after the ritual concluded.", "type": "church_patrol", "color": discord.Color.blue()},
    {"name": "Holy Watchers Circled", "description": "Church enforcers maintained surveillance on the lair with blessed instruments for the entire ritual. {member} kept everyone calm. They dispersed at dawn.", "type": "church_patrol", "color": discord.Color.blue()},
    {"name": "Inquisitor's Complaint Filed", "description": "A formal complaint was delivered by Church officials during the ritual demanding it cease. {member} had the ritual continue in a deeper chamber. The officials eventually withdrew.", "type": "church_patrol", "color": discord.Color.blue()},
    {"name": "Inquisition Breached the Outer Ward", "description": "Four unmarked Church operatives descended simultaneously. Inquisitors moved through demanding proof of mortality. {member} was detained for hours then released with a warning.", "type": "inquisition", "color": discord.Color.blue()},
    {"name": "Mass Arrest Attempt", "description": "Inquisitors began issuing warrants during the ritual's peak. {member} watched coven members led away in silver chains in front of all who were assembled.", "type": "mass_arrest", "color": discord.Color.blue()},
    {"name": "Spy Within the Circle", "description": "Word came back through a lawyer three nights later — Church spies had been within the ritual circle the entire time recording every word and face. **{name}** went to ground immediately.", "type": "power_down", "value": (30, 80), "color": discord.Color.dark_orange()},
    {"name": "Blood Compact Violated", "description": "Something during the ritual violated an ancient blood compact {member} hadn't known about. The power backlash was immediate and severe.", "type": "power_down", "value": (20, 60), "color": discord.Color.dark_orange()},
    {"name": "Sacrifice Interrupted", "description": "The central act of the ritual was disrupted at the critical moment. Nobody saw who interfered. It happened on **{name}**'s own ground.", "type": "power_down", "value": (40, 100), "color": discord.Color.dark_orange()},
    {"name": "Power Source Failed", "description": "The blood reservoir powering the ritual was drained before the rite reached completion. {member} could not recover the energy. Months of preparation lost in an hour.", "type": "power_down", "value": (15, 45), "color": discord.Color.dark_orange()},
    {"name": "Wrong Moon Phase", "description": "{member} miscalculated the lunar alignment. The ritual was performed at the wrong phase and the dark powers were unresponsive. All that preparation for nothing.", "type": "power_down", "value": (15, 40), "color": discord.Color.dark_orange()},
    {"name": "Elder Caused Chaos", "description": "An elder vampire who was owed a favor attended uninvited and began demanding tribute publicly during the ritual. {member} had to manage them physically. It was witnessed by all.", "type": "power_down", "value": (20, 55), "color": discord.Color.dark_orange()},
    {"name": "Dawn Interrupted Everything", "description": "The sky began to lighten before the ritual concluded. Vampires scattered, the circle broke, power dissipated. **{name}** spent enormous resources for nothing.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Attendance Was Sparse", "description": "The preparations were meticulous but the assembled vampires were too few. {member} maintained the ritual for hours in a mostly empty chamber. Just a hollow night.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Wrong Night", "description": "Two other covens had scheduled rituals in the same region on the same night. The dark energies conflicted and cancelled. {member} didn't know until the power refused to gather. **{name}** will plan better.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Blood Circle Never Completed", "description": "The blood mage backing out at the last minute and the replacement's power was insufficient. {member} attempted to complete it alone. Nobody could maintain the connection.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Ancient Ward Blocked the Ritual", "description": "An old vampire lord had placed a ward on this location centuries ago that prevented dark rites from completing. {member} identified it before the ritual caused harm. The matter is closed but the night is lost.", "type": "nothing", "color": discord.Color.greyple()},
]

# --- Bot Events ---

COMMANDS = {
    "coven": handle_coven,
    "show": handle_show,
    "hunt": handle_hunt,
    "raid": handle_raid,
    "sire": handle_sire,
    "bloodoak": handle_bloodoak,
    "ritual": handle_ritual,
    "solo": handle_solo,
    "dp": handle_dp,
    "gathering": handle_gathering,
    "disband": handle_disband,
}

@bot.event
async def on_ready():
    print(f'{bot.user} is online and ready.')

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
            try:
                await message.channel.send("Something went wrong sending that message. Try again.")
            except:
                pass
        except Exception as e:
            import traceback
            print(f"Error in {cmd}: {e}")
            traceback.print_exc()
            try:
                await message.channel.send("An error occurred. Check the logs.")
            except:
                pass

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env")
    else:
        keep_alive()
        bot.run(TOKEN)
