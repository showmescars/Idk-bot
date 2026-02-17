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

CHARACTERS_FILE = 'characters.json'
GRAVEYARD_FILE = 'graveyard.json'

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


def generate_vampire_lore(vampire_name, power_level):
    origin = random.choice(ORIGINS)
    personality = random.choice(PERSONALITIES)
    ability_source = random.choice(ABILITIES_LORE)
    goal = random.choice(GOALS)
    weakness = random.choice(WEAKNESSES)

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

    kills = random.randint(10, 500)

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

    lore_bonus = random.randint(50, 150)

    return {
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


def load_characters():
    if os.path.exists(CHARACTERS_FILE):
        with open(CHARACTERS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_characters(characters):
    with open(CHARACTERS_FILE, 'w') as f:
        json.dump(characters, f, indent=4)


def load_graveyard():
    if os.path.exists(GRAVEYARD_FILE):
        with open(GRAVEYARD_FILE, 'r') as f:
            return json.load(f)
    return []


def save_graveyard(graveyard):
    with open(GRAVEYARD_FILE, 'w') as f:
        json.dump(graveyard, f, indent=4)


def generate_unique_id():
    characters = load_characters()
    graveyard = load_graveyard()
    existing_ids = [char.get('character_id') for char in characters.values() if 'character_id' in char]
    existing_ids += [char.get('character_id') for char in graveyard if 'character_id' in char]
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing_ids:
            return new_id


def generate_ai_power():
    roll = random.randint(1, 100)
    if roll <= 50:
        return random.randint(10, 800)
    elif roll <= 75:
        return random.randint(801, 1400)
    elif roll <= 90:
        return random.randint(1401, 1800)
    else:
        return random.randint(1801, 2000)


def generate_random_vampire_power():
    roll = random.randint(1, 100)
    if roll <= 45:
        return random.randint(10, 400)
    elif roll <= 75:
        return random.randint(401, 1000)
    elif roll <= 90:
        return random.randint(1001, 1600)
    else:
        return random.randint(1601, 2000)


def calculate_death_chance(player_power, enemy_power, player_won):
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
    return int(max(5, min(80, base_chance)))


def simulate_battle(player_name, player_power, enemy_name, enemy_power, lore_revealed=False):
    effective_player_power = player_power
    if lore_revealed:
        lore_bonus_multiplier = random.uniform(1.05, 1.15)
        effective_player_power = int(player_power * lore_bonus_multiplier)

    power_diff = effective_player_power - enemy_power
    win_probability = 50 + (power_diff / 20)
    win_probability = max(5, min(95, win_probability))
    roll = random.randint(1, 100)
    player_won = roll <= win_probability

    return {
        "player_won": player_won,
        "win_probability": int(win_probability),
        "roll": roll,
        "lore_bonus_applied": lore_revealed,
        "effective_power": effective_player_power if lore_revealed else player_power
    }


characters = load_characters()
graveyard = load_graveyard()


@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Vampire Battle System Ready')


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
    user_id = str(ctx.author.id)

    # Always reload fresh to prevent stale cache bug
    fresh_characters = load_characters()
    user_members = [char for char in fresh_characters.values() if char.get('user_id') == user_id]
    if user_members:
        await ctx.send("You already have a vampire! Use `?show` to see your current vampire.")
        return

    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    character_name = f"{first_name} {last_name}"
    character_id = generate_unique_id()
    power_level = generate_random_vampire_power()
    lore_data = generate_vampire_lore(character_name, power_level)

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

    fresh_characters[character_id] = character_data
    save_characters(fresh_characters)
    characters.update(fresh_characters)

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
    embed.set_footer(text=f"Use ?random {character_id} to trigger a dark street event")

    await ctx.send(embed=embed)


# Random command - trigger a vampire street event
@bot.command(name='random')
@commands.cooldown(1, 30, commands.BucketType.user)
async def random_event(ctx, character_id: str = None):
    if character_id is None:
        await ctx.send("Usage: `?random <character_id>`\nExample: `?random 123456`")
        return

    fresh_characters = load_characters()

    if character_id not in fresh_characters:
        await ctx.send(f"Vampire ID `{character_id}` not found!")
        return

    vampire = fresh_characters[character_id]
    user_id = str(ctx.author.id)

    if vampire.get('user_id') != user_id:
        await ctx.send("You don't own this vampire!")
        return

    graveyard = load_graveyard()

    event_type = random.choice([
        "ambushed_by_hunters",
        "rival_vampire_challenges",
        "blood_moon_ritual",
        "coven_attack",
        "ancient_vampire_encounter",
        "daylight_trap",
        "witch_curse",
        "blood_feast",
        "vampire_hunter_raid",
        "forbidden_blood",
        "territory_dispute",
        "sire_returns",
        "dark_gift_offer",
        "mortal_falls_in_love",
        "church_confrontation",
        "bounty_on_blood",
        "underground_fighting_ring",
        "cursed_artifact"
    ])

    notify_embed = discord.Embed(
        title="DARK EVENT INCOMING",
        description=f"Something stirs in the night for **{vampire['name']}**...",
        color=discord.Color.dark_purple()
    )
    notify_embed.set_footer(text="The darkness never sleeps")
    await ctx.send(embed=notify_embed)
    await asyncio.sleep(2)

    # Generate rival info
    rival_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    rival_power = generate_ai_power()

    lore_revealed = False
    if 'lore' in vampire:
        lore_revealed = vampire['lore'].get('lore_revealed', False)

    if event_type == "ambushed_by_hunters":
        num_hunters = random.randint(2, 6)
        event_embed = discord.Embed(
            title="VAMPIRE HUNTER AMBUSH",
            description=f"**{vampire['name']}** has been ambushed by {num_hunters} vampire hunters armed with stakes and holy water!",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="Threat", value=f"{num_hunters} hunters closing in from all sides", inline=False)
        event_embed.set_footer(text="Fight or flee...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        survival_roll = random.randint(1, 100)
        survives = survival_roll <= 60
        death_roll = random.randint(1, 100)
        dies = death_roll <= 40 if not survives else death_roll <= 8

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if dies:
            death_embed = discord.Embed(
                title="STAKED BY HUNTERS",
                description=f"**{vampire['name']}** was overwhelmed by the hunters and staked through the heart",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Power: {vampire['power_level']}\nRecord: {vampire.get('wins', 0)}-{vampire.get('losses', 0)}\nStatus: DESTROYED", inline=False)
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = "Vampire Hunter Ambush"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        elif survives:
            survive_embed = discord.Embed(
                title="HUNTERS DEFEATED",
                description=f"**{vampire['name']}** tore through the hunters and left them broken in the darkness",
                color=discord.Color.green()
            )
            survive_embed.add_field(name="Outcome", value=f"Fought off {num_hunters} hunters and survived", inline=False)
            await ctx.send(embed=survive_embed)
        else:
            escape_embed = discord.Embed(
                title="BARELY ESCAPED",
                description=f"**{vampire['name']}** fled into the shadows as the hunters closed in",
                color=discord.Color.orange()
            )
            escape_embed.add_field(name="Outcome", value="Escaped with wounds - the hunters know your face now", inline=False)
            await ctx.send(embed=escape_embed)

    elif event_type == "rival_vampire_challenges":
        event_embed = discord.Embed(
            title="RIVAL VAMPIRE CHALLENGE",
            description=f"**{rival_name}** (Power: {rival_power}) has stepped into **{vampire['name']}'s** territory and issued a direct challenge",
            color=discord.Color.red()
        )
        event_embed.add_field(name="Challenger", value=f"{rival_name}\nPower: {rival_power}", inline=True)
        event_embed.add_field(name="Your Vampire", value=f"{vampire['name']}\nPower: {vampire['power_level']}", inline=True)
        event_embed.set_footer(text="Only one walks away...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle(vampire['name'], vampire['power_level'], rival_name, rival_power, lore_revealed)
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(vampire['power_level'], rival_power, won)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="CHALLENGER DESTROYED",
                description=f"**{vampire['name']}** defeated **{rival_name}** and defended their territory",
                color=discord.Color.green()
            )
            vampire['wins'] = vampire.get('wins', 0) + 1
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            win_embed.add_field(name="New Record", value=f"{vampire['wins']}-{vampire.get('losses', 0)}", inline=True)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="DESTROYED BY THE CHALLENGER",
                description=f"**{rival_name}** overpowered **{vampire['name']}** and turned them to ash",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Power: {vampire['power_level']}\nRecord: {vampire.get('wins', 0)}-{vampire.get('losses', 0)}\nStatus: DESTROYED", inline=False)
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = f"{rival_name} (Territory Challenge)"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="DEFEATED BUT ALIVE",
                description=f"**{rival_name}** bested **{vampire['name']}** but let them live as a warning",
                color=discord.Color.orange()
            )
            vampire['losses'] = vampire.get('losses', 0) + 1
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            loss_embed.add_field(name="Outcome", value="Lost the challenge but survived - territory now contested", inline=False)
            await ctx.send(embed=loss_embed)

    elif event_type == "blood_moon_ritual":
        event_embed = discord.Embed(
            title="BLOOD MOON RITUAL",
            description=f"A blood moon rises and **{vampire['name']}** feels ancient power surge through their veins",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="Cosmic Event", value="The blood moon amplifies all vampire abilities for a brief window", inline=False)
        event_embed.set_footer(text="Power flows through the darkness...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        outcome_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if outcome_roll <= 60:
            power_gain = random.randint(50, 200)
            vampire['power_level'] = min(2000, vampire['power_level'] + power_gain)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            gain_embed = discord.Embed(
                title="POWER SURGE",
                description=f"**{vampire['name']}** absorbed the blood moon's energy and grew stronger",
                color=discord.Color.gold()
            )
            gain_embed.add_field(name="Power Gained", value=f"+{power_gain}", inline=True)
            gain_embed.add_field(name="New Power Level", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=gain_embed)
        elif outcome_roll <= 85:
            neutral_embed = discord.Embed(
                title="BLOOD MOON FADES",
                description=f"**{vampire['name']}** felt the surge but could not fully absorb the ancient energy",
                color=discord.Color.orange()
            )
            neutral_embed.add_field(name="Outcome", value="The blood moon passed without lasting effect", inline=False)
            await ctx.send(embed=neutral_embed)
        else:
            power_loss = random.randint(20, 100)
            vampire['power_level'] = max(10, vampire['power_level'] - power_loss)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            loss_embed = discord.Embed(
                title="BLOOD MOON OVERWHELM",
                description=f"The blood moon's energy was too intense - **{vampire['name']}** was weakened by the overload",
                color=discord.Color.red()
            )
            loss_embed.add_field(name="Power Lost", value=f"-{power_loss}", inline=True)
            loss_embed.add_field(name="New Power Level", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=loss_embed)

    elif event_type == "coven_attack":
        coven_size = random.randint(3, 8)
        event_embed = discord.Embed(
            title="COVEN ATTACK",
            description=f"A rival coven of {coven_size} vampires has descended on **{vampire['name']}** in the night",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="Attackers", value=f"{coven_size} coven vampires moving as one", inline=False)
        event_embed.set_footer(text="Outnumbered in the dark...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        survival_roll = random.randint(1, 100)
        survives = survival_roll <= 45
        death_roll = random.randint(1, 100)
        dies = death_roll <= 50 if not survives else death_roll <= 10

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if dies:
            death_embed = discord.Embed(
                title="DESTROYED BY THE COVEN",
                description=f"**{vampire['name']}** was overwhelmed by the coven and destroyed",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Power: {vampire['power_level']}\nRecord: {vampire.get('wins', 0)}-{vampire.get('losses', 0)}\nStatus: DESTROYED", inline=False)
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = "Rival Coven Attack"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        elif survives:
            survive_embed = discord.Embed(
                title="COVEN REPELLED",
                description=f"**{vampire['name']}** fought off all {coven_size} coven members single-handedly",
                color=discord.Color.green()
            )
            survive_embed.add_field(name="Outcome", value=f"Stood alone against {coven_size} and survived - legend grows", inline=False)
            await ctx.send(embed=survive_embed)
        else:
            flee_embed = discord.Embed(
                title="FLED THE COVEN",
                description=f"**{vampire['name']}** escaped into the night before the coven could finish the job",
                color=discord.Color.orange()
            )
            flee_embed.add_field(name="Outcome", value="Made it out alive but the coven will return", inline=False)
            await ctx.send(embed=flee_embed)

    elif event_type == "ancient_vampire_encounter":
        ancient_power = random.randint(1500, 2000)
        ancient_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        event_embed = discord.Embed(
            title="ANCIENT ONE APPEARS",
            description=f"**{ancient_name}**, an ancient vampire of immense power ({ancient_power}), has taken notice of **{vampire['name']}**",
            color=discord.Color.dark_purple()
        )
        event_embed.add_field(name="The Ancient", value=f"{ancient_name}\nPower: {ancient_power}", inline=True)
        event_embed.add_field(name="Their Interest", value="Unknown - could be mentor, rival, or executioner", inline=True)
        event_embed.set_footer(text="When ancients take notice...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        outcome_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if outcome_roll <= 40:
            power_grant = random.randint(100, 300)
            vampire['power_level'] = min(2000, vampire['power_level'] + power_grant)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            mentor_embed = discord.Embed(
                title="ANCIENT MENTOR",
                description=f"**{ancient_name}** was impressed and shared forbidden knowledge with **{vampire['name']}**",
                color=discord.Color.gold()
            )
            mentor_embed.add_field(name="Power Granted", value=f"+{power_grant}", inline=True)
            mentor_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=mentor_embed)
        elif outcome_roll <= 70:
            warning_embed = discord.Embed(
                title="ANCIENT WARNING",
                description=f"**{ancient_name}** issued a chilling warning and vanished into the night",
                color=discord.Color.orange()
            )
            warning_embed.add_field(name="Message", value=f"'Stay out of my territory, {vampire['name']}. Next time I will not be so merciful.'", inline=False)
            await ctx.send(embed=warning_embed)
        else:
            attack_embed = discord.Embed(
                title="ANCIENT ATTACKS",
                description=f"**{ancient_name}** decided **{vampire['name']}** was a threat and attacked without warning",
                color=discord.Color.dark_red()
            )

            death_roll = random.randint(1, 100)
            if death_roll <= 55:
                attack_embed.add_field(name="Result", value=f"**{vampire['name']}** was destroyed by the ancient's overwhelming power", inline=False)
                attack_embed.add_field(name="Final Stats", value=f"Power: {vampire['power_level']}\nStatus: DESTROYED", inline=False)
                dead_vampire = vampire.copy()
                dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_vampire['killed_by'] = f"{ancient_name} (Ancient Vampire)"
                graveyard.append(dead_vampire)
                save_graveyard(graveyard)
                del fresh_characters[character_id]
                save_characters(fresh_characters)
                characters.update(fresh_characters)
            else:
                attack_embed.add_field(name="Result", value=f"**{vampire['name']}** barely escaped the ancient's wrath", inline=False)
            await ctx.send(embed=attack_embed)

    elif event_type == "daylight_trap":
        event_embed = discord.Embed(
            title="DAYLIGHT TRAP",
            description=f"**{vampire['name']}** was lured into a building that hunters then exposed to sunlight through shattered windows",
            color=discord.Color.orange()
        )
        event_embed.add_field(name="Danger", value="Sunlight flooding in from all directions - seconds to escape", inline=False)
        event_embed.set_footer(text="The sun burns...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        escape_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if escape_roll <= 30:
            death_embed = discord.Embed(
                title="BURNED BY SUNLIGHT",
                description=f"**{vampire['name']}** could not escape in time and was destroyed by the sunlight",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Power: {vampire['power_level']}\nStatus: DESTROYED", inline=False)
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = "Daylight Trap"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        elif escape_roll <= 65:
            wound_embed = discord.Embed(
                title="BURNED BUT ESCAPED",
                description=f"**{vampire['name']}** burst through the wall and escaped, badly burned",
                color=discord.Color.orange()
            )
            power_loss = random.randint(10, 50)
            vampire['power_level'] = max(10, vampire['power_level'] - power_loss)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            wound_embed.add_field(name="Wounds", value=f"Sunlight burns cost {power_loss} power", inline=True)
            wound_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=wound_embed)
        else:
            escape_embed = discord.Embed(
                title="CLEAN ESCAPE",
                description=f"**{vampire['name']}** found a shadow passage and escaped before a single ray touched them",
                color=discord.Color.green()
            )
            escape_embed.add_field(name="Outcome", value="Escaped the trap unscathed - the hunters failed", inline=False)
            await ctx.send(embed=escape_embed)

    elif event_type == "witch_curse":
        event_embed = discord.Embed(
            title="WITCH CURSE",
            description=f"A powerful witch has placed a curse on **{vampire['name']}** for trespassing in her domain",
            color=discord.Color.dark_purple()
        )
        event_embed.add_field(name="The Curse", value="Ancient magic binds the vampire - their power wavers", inline=False)
        event_embed.set_footer(text="Magic older than most vampires...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        curse_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if curse_roll <= 35:
            power_loss = random.randint(50, 150)
            vampire['power_level'] = max(10, vampire['power_level'] - power_loss)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            curse_embed = discord.Embed(
                title="CURSE TAKES HOLD",
                description=f"The witch's curse weakened **{vampire['name']}** significantly",
                color=discord.Color.red()
            )
            curse_embed.add_field(name="Power Lost", value=f"-{power_loss}", inline=True)
            curse_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=curse_embed)
        elif curse_roll <= 70:
            resist_embed = discord.Embed(
                title="CURSE RESISTED",
                description=f"**{vampire['name']}** fought off the witch's magic through sheer force of will",
                color=discord.Color.orange()
            )
            resist_embed.add_field(name="Outcome", value="The curse failed to take hold - ancient blood runs strong", inline=False)
            await ctx.send(embed=resist_embed)
        else:
            turn_embed = discord.Embed(
                title="CURSE BACKFIRES",
                description=f"**{vampire['name']}** absorbed the witch's curse and converted it into raw power",
                color=discord.Color.gold()
            )
            power_gain = random.randint(30, 100)
            vampire['power_level'] = min(2000, vampire['power_level'] + power_gain)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            turn_embed.add_field(name="Power Gained", value=f"+{power_gain}", inline=True)
            turn_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=turn_embed)

    elif event_type == "blood_feast":
        event_embed = discord.Embed(
            title="BLOOD FEAST",
            description=f"**{vampire['name']}** stumbles upon an unguarded blood supply - an opportunity to feed and grow stronger",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="Opportunity", value="Rich blood waiting - feed and grow powerful", inline=False)
        event_embed.set_footer(text="The hunger calls...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        power_gain = random.randint(30, 150)
        vampire['power_level'] = min(2000, vampire['power_level'] + power_gain)
        fresh_characters[character_id] = vampire
        save_characters(fresh_characters)
        characters.update(fresh_characters)

        feast_embed = discord.Embed(
            title="POWER FROM THE FEAST",
            description=f"**{vampire['name']}** fed deeply and grew stronger",
            color=discord.Color.green()
        )
        feast_embed.add_field(name="Power Gained", value=f"+{power_gain}", inline=True)
        feast_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
        await ctx.send(embed=feast_embed)

    elif event_type == "vampire_hunter_raid":
        num_hunters = random.randint(4, 10)
        event_embed = discord.Embed(
            title="HUNTER RAID ON LAIR",
            description=f"A full hunter squad of {num_hunters} has raided **{vampire['name']}'s** lair with silver weapons and holy fire",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="Raid Force", value=f"{num_hunters} hunters - heavily armed", inline=False)
        event_embed.set_footer(text="They know where you sleep...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        outcome_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if outcome_roll <= 25:
            death_embed = discord.Embed(
                title="LAIR OVERRUN",
                description=f"**{vampire['name']}** was caught off guard and destroyed in their own lair",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Power: {vampire['power_level']}\nStatus: DESTROYED", inline=False)
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = f"Hunter Raid ({num_hunters} hunters)"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        elif outcome_roll <= 60:
            escape_embed = discord.Embed(
                title="ESCAPED THE RAID",
                description=f"**{vampire['name']}** fled through a hidden passage as the hunters swarmed the lair",
                color=discord.Color.orange()
            )
            escape_embed.add_field(name="Outcome", value="Lost the lair but kept their life - must find new territory", inline=False)
            await ctx.send(embed=escape_embed)
        else:
            defend_embed = discord.Embed(
                title="LAIR DEFENDED",
                description=f"**{vampire['name']}** slaughtered the hunter squad before they could complete the raid",
                color=discord.Color.green()
            )
            defend_embed.add_field(name="Outcome", value=f"All {num_hunters} hunters destroyed - lair remains secure", inline=False)
            await ctx.send(embed=defend_embed)

    elif event_type == "forbidden_blood":
        event_embed = discord.Embed(
            title="FORBIDDEN BLOOD OFFER",
            description=f"A mysterious figure offers **{vampire['name']}** a vial of forbidden ancient blood - immense power but unknown risk",
            color=discord.Color.dark_purple()
        )
        event_embed.add_field(name="The Offer", value="Ancient blood of unknown origin - could grant great power or destruction", inline=False)
        event_embed.set_footer(text="Some power comes at a price...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        drink_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if drink_roll <= 30:
            power_surge = random.randint(200, 500)
            vampire['power_level'] = min(2000, vampire['power_level'] + power_surge)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            surge_embed = discord.Embed(
                title="ANCIENT POWER AWAKENED",
                description=f"The forbidden blood transformed **{vampire['name']}** - ancient power flows through their veins",
                color=discord.Color.gold()
            )
            surge_embed.add_field(name="Power Surge", value=f"+{power_surge}", inline=True)
            surge_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=surge_embed)
        elif drink_roll <= 55:
            loss_embed = discord.Embed(
                title="BLOOD POISON",
                description=f"The forbidden blood was a trap - it burned through **{vampire['name']}** like acid",
                color=discord.Color.red()
            )
            power_loss = random.randint(100, 300)
            vampire['power_level'] = max(10, vampire['power_level'] - power_loss)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            loss_embed.add_field(name="Power Lost", value=f"-{power_loss}", inline=True)
            loss_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=loss_embed)
        elif drink_roll <= 75:
            nothing_embed = discord.Embed(
                title="BLOOD REJECTED",
                description=f"**{vampire['name']}**'s body rejected the forbidden blood with no lasting effect",
                color=discord.Color.orange()
            )
            nothing_embed.add_field(name="Outcome", value="The ancient blood had no effect - neither gain nor loss", inline=False)
            await ctx.send(embed=nothing_embed)
        else:
            death_embed = discord.Embed(
                title="BLOOD DESTROYS",
                description=f"The forbidden blood was lethal - **{vampire['name']}** dissolved from within",
                color=discord.Color.dark_red()
            )
            death_embed.add_field(name="Final Stats", value=f"Power: {vampire['power_level']}\nStatus: DESTROYED", inline=False)
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = "Forbidden Blood"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)

    elif event_type == "territory_dispute":
        event_embed = discord.Embed(
            title="TERRITORY DISPUTE",
            description=f"**{rival_name}** (Power: {rival_power}) claims the hunting grounds **{vampire['name']}** controls",
            color=discord.Color.red()
        )
        event_embed.add_field(name="The Dispute", value=f"{rival_name} has been feeding in your territory without permission", inline=False)
        event_embed.set_footer(text="Territory means everything in the night...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle(vampire['name'], vampire['power_level'], rival_name, rival_power, lore_revealed)
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(vampire['power_level'], rival_power, won)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="TERRITORY HELD",
                description=f"**{vampire['name']}** drove **{rival_name}** out of their territory permanently",
                color=discord.Color.green()
            )
            vampire['wins'] = vampire.get('wins', 0) + 1
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            win_embed.add_field(name="Outcome", value="Territory secured - rivals will think twice", inline=False)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="TERRITORY LOST - DESTROYED",
                description=f"**{rival_name}** not only took the territory but destroyed **{vampire['name']}**",
                color=discord.Color.dark_red()
            )
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = f"{rival_name} (Territory Dispute)"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="TERRITORY LOST",
                description=f"**{vampire['name']}** was driven from their own territory by **{rival_name}**",
                color=discord.Color.orange()
            )
            vampire['losses'] = vampire.get('losses', 0) + 1
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            loss_embed.add_field(name="Outcome", value="Survived but homeless - must reclaim territory", inline=False)
            await ctx.send(embed=loss_embed)

    elif event_type == "sire_returns":
        sire_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        sire_power = random.randint(800, 2000)
        event_embed = discord.Embed(
            title="SIRE RETURNS",
            description=f"**{sire_name}** (Power: {sire_power}), the vampire who created **{vampire['name']}**, has returned after centuries",
            color=discord.Color.dark_purple()
        )
        event_embed.add_field(name="The Sire", value=f"{sire_name}\nPower: {sire_power}", inline=True)
        event_embed.add_field(name="Their Mood", value="Unknown - creator and creation reunite", inline=True)
        event_embed.set_footer(text="The blood bond never breaks...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        outcome_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if outcome_roll <= 45:
            power_gift = random.randint(100, 250)
            vampire['power_level'] = min(2000, vampire['power_level'] + power_gift)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            gift_embed = discord.Embed(
                title="SIRE'S GIFT",
                description=f"**{sire_name}** was pleased with their creation and granted **{vampire['name']}** ancient power",
                color=discord.Color.gold()
            )
            gift_embed.add_field(name="Power Gift", value=f"+{power_gift}", inline=True)
            gift_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=gift_embed)
        elif outcome_roll <= 75:
            warn_embed = discord.Embed(
                title="SIRE'S WARNING",
                description=f"**{sire_name}** appeared only to deliver a warning before vanishing again",
                color=discord.Color.orange()
            )
            warn_embed.add_field(name="The Warning", value="'You are being watched. Do not disappoint me.'", inline=False)
            await ctx.send(embed=warn_embed)
        else:
            attack_embed = discord.Embed(
                title="SIRE TURNS HOSTILE",
                description=f"**{sire_name}** returned to destroy what they created - the sire has gone mad",
                color=discord.Color.dark_red()
            )
            death_roll = random.randint(1, 100)
            if death_roll <= 45:
                attack_embed.add_field(name="Result", value=f"**{vampire['name']}** was destroyed by their own creator", inline=False)
                dead_vampire = vampire.copy()
                dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dead_vampire['killed_by'] = f"{sire_name} (Sire Betrayal)"
                graveyard.append(dead_vampire)
                save_graveyard(graveyard)
                del fresh_characters[character_id]
                save_characters(fresh_characters)
                characters.update(fresh_characters)
            else:
                attack_embed.add_field(name="Result", value=f"**{vampire['name']}** barely escaped their sire's wrath", inline=False)
            await ctx.send(embed=attack_embed)

    elif event_type == "dark_gift_offer":
        event_embed = discord.Embed(
            title="DARK GIFT OFFERED",
            description=f"A demon offers **{vampire['name']}** a dark gift - enhanced power in exchange for a piece of their immortal soul",
            color=discord.Color.dark_purple()
        )
        event_embed.add_field(name="The Deal", value="Demonic power on offer - but souls are precious even to vampires", inline=False)
        event_embed.set_footer(text="Every deal has a price...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        deal_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if deal_roll <= 40:
            power_gain = random.randint(150, 400)
            vampire['power_level'] = min(2000, vampire['power_level'] + power_gain)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            deal_embed = discord.Embed(
                title="DARK DEAL ACCEPTED",
                description=f"**{vampire['name']}** made the deal and gained tremendous power",
                color=discord.Color.gold()
            )
            deal_embed.add_field(name="Power Gained", value=f"+{power_gain}", inline=True)
            deal_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            deal_embed.add_field(name="Cost", value="A fragment of their immortal soul - consequences unknown", inline=False)
            await ctx.send(embed=deal_embed)
        elif deal_roll <= 70:
            refuse_embed = discord.Embed(
                title="DEAL REFUSED",
                description=f"**{vampire['name']}** rejected the demon's offer and drove it away",
                color=discord.Color.green()
            )
            refuse_embed.add_field(name="Outcome", value="Soul intact - no power gained but no price paid", inline=False)
            await ctx.send(embed=refuse_embed)
        else:
            trick_embed = discord.Embed(
                title="DEMON TRICK",
                description=f"The demon tricked **{vampire['name']}** and stole power without granting anything in return",
                color=discord.Color.red()
            )
            power_loss = random.randint(50, 200)
            vampire['power_level'] = max(10, vampire['power_level'] - power_loss)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            trick_embed.add_field(name="Power Stolen", value=f"-{power_loss}", inline=True)
            trick_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=trick_embed)

    elif event_type == "mortal_falls_in_love":
        mortal_name = f"{random.choice(['Elena', 'Isabella', 'Mina', 'Lucy', 'Lydia', 'Rose', 'Clara', 'James', 'Edward', 'Thomas', 'William', 'Henry'])} {random.choice(LAST_NAMES)}"
        event_embed = discord.Embed(
            title="MORTAL OBSESSION",
            description=f"A mortal named **{mortal_name}** has discovered **{vampire['name']}**'s true nature and become dangerously obsessed",
            color=discord.Color.purple()
        )
        event_embed.add_field(name="The Mortal", value=f"{mortal_name} - knows your secret and won't stay quiet", inline=False)
        event_embed.set_footer(text="Mortals who know the truth are dangerous...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        outcome_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if outcome_roll <= 35:
            turn_embed = discord.Embed(
                title="MORTAL TURNED",
                description=f"**{vampire['name']}** turned **{mortal_name}** to silence them - a new vampire born",
                color=discord.Color.dark_purple()
            )
            turn_embed.add_field(name="Outcome", value="The secret is safe but now there is another mouth to feed", inline=False)
            await ctx.send(embed=turn_embed)
        elif outcome_roll <= 65:
            useful_embed = discord.Embed(
                title="MORTAL BECOMES USEFUL",
                description=f"**{mortal_name}** proved useful - providing information and a daytime spy",
                color=discord.Color.green()
            )
            money_gain = random.randint(0, 0)
            power_gain = random.randint(20, 60)
            vampire['power_level'] = min(2000, vampire['power_level'] + power_gain)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            useful_embed.add_field(name="Intelligence Gained", value=f"Power boost from mortal knowledge: +{power_gain}", inline=False)
            await ctx.send(embed=useful_embed)
        else:
            hunter_embed = discord.Embed(
                title="MORTAL TIPS OFF HUNTERS",
                description=f"**{mortal_name}** panicked and told vampire hunters about **{vampire['name']}**",
                color=discord.Color.red()
            )
            hunter_embed.add_field(name="Consequence", value="Hunter squads now have your location - increased danger", inline=False)
            await ctx.send(embed=hunter_embed)

    elif event_type == "church_confrontation":
        priest_power = random.randint(200, 800)
        event_embed = discord.Embed(
            title="CHURCH CONFRONTATION",
            description=f"**{vampire['name']}** was cornered by a holy warrior priest wielding sacred relics and blessed weapons",
            color=discord.Color.blue()
        )
        event_embed.add_field(name="Holy Warrior", value=f"Priest armed with blessed silver and holy fire\nEstimated Threat: {priest_power}", inline=False)
        event_embed.set_footer(text="Faith versus darkness...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        battle = simulate_battle(vampire['name'], vampire['power_level'], "Holy Warrior Priest", priest_power, lore_revealed)
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= (calculate_death_chance(vampire['power_level'], priest_power, won) + 10)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if won and not dies:
            win_embed = discord.Embed(
                title="DARKNESS OVERCOMES FAITH",
                description=f"**{vampire['name']}** overpowered the holy warrior despite the sacred weapons",
                color=discord.Color.green()
            )
            vampire['wins'] = vampire.get('wins', 0) + 1
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            win_embed.add_field(name="Outcome", value="The priest was defeated - faith alone could not stop this vampire", inline=False)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="DESTROYED BY HOLY POWER",
                description=f"**{vampire['name']}** was destroyed by the holy warrior's blessed weapons",
                color=discord.Color.dark_red()
            )
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = "Holy Warrior Priest"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            flee_embed = discord.Embed(
                title="FLED FROM HOLY GROUND",
                description=f"**{vampire['name']}** could not withstand the holy warrior's power and retreated",
                color=discord.Color.orange()
            )
            vampire['losses'] = vampire.get('losses', 0) + 1
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            flee_embed.add_field(name="Outcome", value="Escaped but wounded by blessed silver", inline=False)
            await ctx.send(embed=flee_embed)

    elif event_type == "bounty_on_blood":
        bounty_amount = random.randint(500, 3000)
        event_embed = discord.Embed(
            title="BOUNTY PLACED",
            description=f"A powerful vampire lord has placed a blood bounty of {bounty_amount} on **{vampire['name']}**",
            color=discord.Color.gold()
        )
        event_embed.add_field(name="Bounty", value=f"{bounty_amount} in ancient coin", inline=True)
        event_embed.add_field(name="Who Wants You Dead", value="A vampire lord whose territory you violated", inline=True)
        event_embed.add_field(name="Warning", value="Every vampire and hunter in the region now knows your face", inline=False)
        event_embed.set_footer(text="There is a price on your head...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        bounty_hunter_power = generate_ai_power()
        bounty_hunter_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

        hunter_embed = discord.Embed(
            title="BOUNTY HUNTER ARRIVES",
            description=f"**{bounty_hunter_name}** (Power: {bounty_hunter_power}) has already tracked down **{vampire['name']}** to collect",
            color=discord.Color.red()
        )
        await ctx.send(embed=hunter_embed)
        await asyncio.sleep(3)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        battle = simulate_battle(vampire['name'], vampire['power_level'], bounty_hunter_name, bounty_hunter_power, lore_revealed)
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(vampire['power_level'], bounty_hunter_power, won)

        if won and not dies:
            win_embed = discord.Embed(
                title="BOUNTY HUNTER DESTROYED",
                description=f"**{vampire['name']}** killed the bounty hunter - sending a message to the vampire lord",
                color=discord.Color.green()
            )
            vampire['wins'] = vampire.get('wins', 0) + 1
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="COLLECTED BY THE HUNTER",
                description=f"**{bounty_hunter_name}** collected the bounty - **{vampire['name']}** is no more",
                color=discord.Color.dark_red()
            )
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = f"{bounty_hunter_name} (Bounty Hunter)"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            escape_embed = discord.Embed(
                title="ESCAPED THE HUNTER",
                description=f"**{vampire['name']}** lost the fight but escaped before the hunter could finish the job",
                color=discord.Color.orange()
            )
            vampire['losses'] = vampire.get('losses', 0) + 1
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=escape_embed)

    elif event_type == "underground_fighting_ring":
        event_embed = discord.Embed(
            title="UNDERGROUND VAMPIRE FIGHT RING",
            description=f"**{vampire['name']}** has been dragged into an underground vampire fighting ring and forced to compete",
            color=discord.Color.dark_red()
        )
        event_embed.add_field(name="The Ring", value="Ancient vampires betting on supernatural combat - no escape", inline=False)
        event_embed.set_footer(text="Fight or be destroyed for their entertainment...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        opponent_power = generate_ai_power()
        opponent_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

        match_embed = discord.Embed(
            title="OPPONENT ANNOUNCED",
            description=f"**{vampire['name']}** vs **{opponent_name}** (Power: {opponent_power})",
            color=discord.Color.orange()
        )
        await ctx.send(embed=match_embed)
        await asyncio.sleep(3)

        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        battle = simulate_battle(vampire['name'], vampire['power_level'], opponent_name, opponent_power, lore_revealed)
        won = battle['player_won']
        death_roll = random.randint(1, 100)
        dies = death_roll <= calculate_death_chance(vampire['power_level'], opponent_power, won)

        if won and not dies:
            prize = random.randint(100, 300)
            power_gain = random.randint(20, 80)
            vampire['wins'] = vampire.get('wins', 0) + 1
            vampire['power_level'] = min(2000, vampire['power_level'] + power_gain)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            win_embed = discord.Embed(
                title="RING CHAMPION",
                description=f"**{vampire['name']}** defeated **{opponent_name}** and earned the crowd's respect",
                color=discord.Color.gold()
            )
            win_embed.add_field(name="Power Gained", value=f"+{power_gain} from combat experience", inline=True)
            win_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=win_embed)
        elif dies:
            death_embed = discord.Embed(
                title="DESTROYED IN THE RING",
                description=f"**{opponent_name}** destroyed **{vampire['name']}** for the crowd's entertainment",
                color=discord.Color.dark_red()
            )
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = f"{opponent_name} (Underground Fight Ring)"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)
        else:
            loss_embed = discord.Embed(
                title="DEFEATED IN THE RING",
                description=f"**{vampire['name']}** lost to **{opponent_name}** but the crowd let them live",
                color=discord.Color.orange()
            )
            vampire['losses'] = vampire.get('losses', 0) + 1
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            loss_embed.add_field(name="Outcome", value="Defeated and humiliated but alive - crawled out of the ring", inline=False)
            await ctx.send(embed=loss_embed)

    elif event_type == "cursed_artifact":
        artifact_names = [
            "the Crimson Chalice", "a cursed ring of ancient blood", "the Obsidian Fang",
            "a shard of the first vampire's coffin", "the Bloodstone Amulet",
            "a vial of sunlight trapped in glass", "the Shadow Crown",
            "a mirror that shows your true death", "the Bone Dagger of St. Marcus"
        ]
        artifact = random.choice(artifact_names)
        event_embed = discord.Embed(
            title="CURSED ARTIFACT FOUND",
            description=f"**{vampire['name']}** discovered {artifact} in an abandoned crypt",
            color=discord.Color.dark_purple()
        )
        event_embed.add_field(name="The Artifact", value=f"{artifact} - radiates ancient power and dark energy", inline=False)
        event_embed.set_footer(text="Ancient objects carry ancient curses...")
        await ctx.send(embed=event_embed)
        await asyncio.sleep(3)

        artifact_roll = random.randint(1, 100)
        fresh_characters = load_characters()
        if character_id not in fresh_characters:
            return
        vampire = fresh_characters[character_id]

        if artifact_roll <= 40:
            power_gain = random.randint(80, 250)
            vampire['power_level'] = min(2000, vampire['power_level'] + power_gain)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            bless_embed = discord.Embed(
                title="ARTIFACT EMPOWERS",
                description=f"{artifact} resonated with **{vampire['name']}**'s blood and granted power",
                color=discord.Color.gold()
            )
            bless_embed.add_field(name="Power Gained", value=f"+{power_gain}", inline=True)
            bless_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=bless_embed)
        elif artifact_roll <= 65:
            curse_embed = discord.Embed(
                title="ARTIFACT CURSES",
                description=f"{artifact} released a dark curse on **{vampire['name']}**",
                color=discord.Color.red()
            )
            power_loss = random.randint(40, 150)
            vampire['power_level'] = max(10, vampire['power_level'] - power_loss)
            fresh_characters[character_id] = vampire
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            curse_embed.add_field(name="Power Lost", value=f"-{power_loss}", inline=True)
            curse_embed.add_field(name="New Power", value=f"{vampire['power_level']}", inline=True)
            await ctx.send(embed=curse_embed)
        elif artifact_roll <= 85:
            neutral_embed = discord.Embed(
                title="ARTIFACT DORMANT",
                description=f"{artifact} did nothing - its power may be sealed or simply not compatible",
                color=discord.Color.orange()
            )
            neutral_embed.add_field(name="Outcome", value="No effect - the artifact remains a mystery", inline=False)
            await ctx.send(embed=neutral_embed)
        else:
            death_embed = discord.Embed(
                title="ARTIFACT DESTROYS",
                description=f"{artifact} unleashed a catastrophic curse that destroyed **{vampire['name']}**",
                color=discord.Color.dark_red()
            )
            dead_vampire = vampire.copy()
            dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dead_vampire['killed_by'] = f"Cursed Artifact - {artifact}"
            graveyard.append(dead_vampire)
            save_graveyard(graveyard)
            del fresh_characters[character_id]
            save_characters(fresh_characters)
            characters.update(fresh_characters)
            await ctx.send(embed=death_embed)


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
