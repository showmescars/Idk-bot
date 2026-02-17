import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

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
    "Tepes", "Draculesti", "Karnstein", "De Lioncourt", "Enkil", "Romanus", "Corvinus", "Nightshade",
    "Von Doom", "Bloodworth", "Blackthorn", "Darkmore", "Volturi", "Mikaelson", "Salvatore", "Pierce",
    "Bennett", "Forbes", "Lockwood", "Donovan", "Gilbert", "Fell", "Whitmore", "St. John",
    "Ashford", "Bloodmoon", "Crimson", "Ravencroft", "Shadowend", "Duskbane", "Nocturne", "Grave",
    "Morningstar", "Hellsing", "Alucard", "Belmont", "Blackwood", "Von Carstein", "Draken",
    "Mourning", "Eclipse", "Eventide", "Twilight", "Sanguine", "Hemlock", "Mortis", "Grimwood",
    "Nightfall", "Darkholm"
]

vampires = {}


def generate_power():
    roll = random.randint(1, 100)
    if roll <= 45:
        return random.randint(10, 900)
    elif roll <= 75:
        return random.randint(901, 2200)
    elif roll <= 90:
        return random.randint(2201, 3600)
    else:
        return random.randint(3601, 4500)


def generate_code():
    while True:
        code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
        if code not in vampires:
            return code


def get_tier(power):
    if power <= 900:
        return "Fledgling", discord.Color.dark_grey()
    elif power <= 2200:
        return "Experienced", discord.Color.blue()
    elif power <= 3600:
        return "Ancient", discord.Color.purple()
    else:
        return "Primordial", discord.Color.gold()


def generate_ai_vampire():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"
    power = generate_power()
    return {"name": name, "power": power}


EVENTS = [
    # POWER UPS
    {
        "id": 1,
        "name": "Ancient Tome Discovered",
        "description": "{name} stumbles upon a forbidden ancient tome deep in a crumbling castle library. The dark knowledge within surges through their veins.",
        "type": "power_up",
        "value": (100, 300),
        "color": discord.Color.green()
    },
    {
        "id": 4,
        "name": "Blood Moon Ritual",
        "description": "{name} participates in a rare blood moon ritual with elder vampires. The ceremony floods them with primordial energy.",
        "type": "power_up",
        "value": (200, 600),
        "color": discord.Color.green()
    },
    {
        "id": 6,
        "name": "Consumed an Ancient's Blood",
        "description": "{name} found a dying ancient vampire and drained them completely. Their power floods into your vampire's body.",
        "type": "power_up",
        "value": (300, 800),
        "color": discord.Color.green()
    },
    {
        "id": 9,
        "name": "Formed a Dark Alliance",
        "description": "{name} allied with a powerful vampire coven. Through shared blood rituals, their power has grown significantly.",
        "type": "power_up",
        "value": (150, 400),
        "color": discord.Color.green()
    },
    {
        "id": 12,
        "name": "Discovered a Blood Spring",
        "description": "{name} discovered a mythical blood spring hidden beneath an old cathedral. Drinking from it restored and amplified their power.",
        "type": "power_up",
        "value": (400, 1000),
        "color": discord.Color.green()
    },
    {
        "id": 15,
        "name": "Mastered a New Ability",
        "description": "{name} spent weeks in isolation practicing dark arts. They have awakened a new supernatural ability, boosting their combat power.",
        "type": "power_up",
        "value": (200, 500),
        "color": discord.Color.green()
    },
    {
        "id": 18,
        "name": "Fed on a Powerful Mage",
        "description": "{name} fed on a powerful blood mage. The magical blood surging through them granted an extraordinary power boost.",
        "type": "power_up",
        "value": (250, 700),
        "color": discord.Color.green()
    },
    {
        "id": 20,
        "name": "Awakened Dormant Powers",
        "description": "{name} experienced a near-death moment that cracked open a dormant power deep within their bloodline. They emerge transformed.",
        "type": "power_up",
        "value": (600, 1200),
        "color": discord.Color.green()
    },
    {
        "id": 23,
        "name": "Bonded with a Familiar",
        "description": "{name} bonded with a powerful supernatural familiar that enhances their senses and combat abilities beyond normal limits.",
        "type": "power_up",
        "value": (150, 400),
        "color": discord.Color.green()
    },
    {
        "id": 25,
        "name": "Absorbed a Dying Bloodline",
        "description": "{name} was the last to find a dying vampire bloodline and absorbed their entire lineage's power in a single night.",
        "type": "power_up",
        "value": (500, 1100),
        "color": discord.Color.green()
    },
    {
        "id": 26,
        "name": "Bathed in Dragon's Blood",
        "description": "{name} discovered a slain dragon deep in a mountain cave and bathed in its still-warm blood. Ancient power unlike anything vampiric courses through them.",
        "type": "power_up",
        "value": (700, 1500),
        "color": discord.Color.green()
    },
    {
        "id": 27,
        "name": "Consumed a Fallen Angel",
        "description": "{name} found a dying fallen angel and drained it completely. Divine and dark power merge within them creating something terrifying.",
        "type": "power_up",
        "value": (800, 1800),
        "color": discord.Color.green()
    },
    {
        "id": 28,
        "name": "Eclipse Empowerment",
        "description": "{name} stood beneath a full solar eclipse and absorbed the rare dark energy that only surfaces during total darkness. They feel limitless.",
        "type": "power_up",
        "value": (400, 900),
        "color": discord.Color.green()
    },
    {
        "id": 29,
        "name": "Unlocked Blood Memory",
        "description": "{name} fell into a trance and unlocked centuries of suppressed blood memory from their sire's lineage. Every ancestor's power is now accessible.",
        "type": "power_up",
        "value": (350, 800),
        "color": discord.Color.green()
    },
    {
        "id": 30,
        "name": "Feasted on a God's Champion",
        "description": "{name} hunted down a mortal chosen by the gods themselves and drained them dry. The divine energy within the blood supercharged everything.",
        "type": "power_up",
        "value": (600, 1300),
        "color": discord.Color.green()
    },
    {
        "id": 31,
        "name": "Discovered a Vampire Vault",
        "description": "{name} broke into an ancient sealed vault beneath a ruined city and consumed vials of preserved blood from long-dead primordial vampires.",
        "type": "power_up",
        "value": (500, 1000),
        "color": discord.Color.green()
    },
    {
        "id": 32,
        "name": "Survived a Holy Weapon",
        "description": "{name} was struck by a holy weapon and should have died but did not. Surviving the wound caused their body to adapt and grow exponentially stronger.",
        "type": "power_up",
        "value": (300, 700),
        "color": discord.Color.green()
    },
    # POWER DOWNS
    {
        "id": 2,
        "name": "Ambushed by Hunters",
        "description": "{name} is ambushed by a squad of elite vampire hunters armed with holy weapons. They barely escape but are gravely weakened.",
        "type": "power_down",
        "value": (100, 400),
        "color": discord.Color.orange()
    },
    {
        "id": 5,
        "name": "Cursed by a Witch",
        "description": "{name} crossed into a witch's territory uninvited. She placed a draining curse on them, sapping their strength.",
        "type": "power_down",
        "value": (150, 500),
        "color": discord.Color.orange()
    },
    {
        "id": 7,
        "name": "Exposed to Sunlight",
        "description": "{name} was trapped outside at dawn by a cunning enemy. The sunlight scorched away a portion of their power before they escaped.",
        "type": "power_down",
        "value": (200, 600),
        "color": discord.Color.orange()
    },
    {
        "id": 10,
        "name": "Betrayed by a Thrall",
        "description": "{name}'s most trusted human thrall betrayed them to vampire hunters. In the struggle, they were wounded by holy water.",
        "type": "power_down",
        "value": (100, 350),
        "color": discord.Color.orange()
    },
    {
        "id": 13,
        "name": "Afflicted with Bloodlust Madness",
        "description": "{name} lost control to bloodlust and went on a rampage, drawing the attention of every hunter in the region. They barely survived.",
        "type": "power_down",
        "value": (300, 700),
        "color": discord.Color.orange()
    },
    {
        "id": 16,
        "name": "Rival Vampire Attack",
        "description": "{name} was attacked by a rival vampire clan in their own territory. They survived, but the battle drained significant power.",
        "type": "power_down",
        "value": (200, 600),
        "color": discord.Color.orange()
    },
    {
        "id": 19,
        "name": "Trapped in a Silver Cage",
        "description": "{name} was lured into a silver cage trap. Days of exposure to silver drained their supernatural strength before they escaped.",
        "type": "power_down",
        "value": (250, 550),
        "color": discord.Color.orange()
    },
    {
        "id": 21,
        "name": "Exorcism Ritual Performed",
        "description": "{name} was caught in the crossfire of a massive exorcism ritual. The holy energy tore through them, stripping away their power.",
        "type": "power_down",
        "value": (400, 900),
        "color": discord.Color.orange()
    },
    {
        "id": 24,
        "name": "Poisoned with Wolfsbane",
        "description": "{name} was poisoned with a concentrated wolfsbane and mountain ash mixture slipped into their blood supply. Recovery cost them dearly.",
        "type": "power_down",
        "value": (150, 450),
        "color": discord.Color.orange()
    },
    {
        "id": 33,
        "name": "Drained by a Succubus",
        "description": "{name} was lured into the lair of a succubus who fed on their supernatural energy throughout the night. They awoke hollow and weakened.",
        "type": "power_down",
        "value": (300, 750),
        "color": discord.Color.orange()
    },
    {
        "id": 34,
        "name": "Ancient Seal Triggered",
        "description": "{name} broke into a sealed tomb and triggered a powerful ancient ward. The magical backlash tore through their body and drained their power.",
        "type": "power_down",
        "value": (350, 800),
        "color": discord.Color.orange()
    },
    {
        "id": 35,
        "name": "Blood Starved for Weeks",
        "description": "{name} was hunted so relentlessly they could not feed for weeks. The starvation withered their power to a fraction of what it was.",
        "type": "power_down",
        "value": (200, 600),
        "color": discord.Color.orange()
    },
    {
        "id": 36,
        "name": "Cursed Relic Touched",
        "description": "{name} picked up a cursed relic designed to weaken vampires. By the time they realized the trap it had already siphoned a great deal of their strength.",
        "type": "power_down",
        "value": (250, 650),
        "color": discord.Color.orange()
    },
    {
        "id": 37,
        "name": "Forced into Torpor",
        "description": "{name} was overwhelmed and forced into an involuntary torpor by a group of elder vampires. They awoke days later drained and disoriented.",
        "type": "power_down",
        "value": (400, 1000),
        "color": discord.Color.orange()
    },
    # DEATHS
    {
        "id": 3,
        "name": "Slain by a Vampire Hunter",
        "description": "{name} encountered the legendary hunter Van Hellward and lost. A silver stake finds its mark. Your vampire is dead.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
    },
    {
        "id": 8,
        "name": "Burned at the Stake",
        "description": "{name} was captured by a vengeful mob and burned. Not even vampire regeneration could save them from the sacred fire.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
    },
    {
        "id": 14,
        "name": "Devoured by an Elder",
        "description": "{name} wandered into an Elder's feeding ground. The ancient creature showed no mercy. Your vampire has been consumed.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
    },
    {
        "id": 17,
        "name": "Decapitated by a Slayer",
        "description": "{name} underestimated a lone slayer who carried an enchanted blade. One swift strike ends their undead existence permanently.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
    },
    {
        "id": 22,
        "name": "Heart Ripped Out by an Ancient",
        "description": "{name} challenged an Ancient vampire to a duel and paid the ultimate price. Their heart was ripped from their chest.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
    },
    {
        "id": 38,
        "name": "Consumed by a Hellfire Trap",
        "description": "{name} walked into a hunter compound rigged with hellfire. The sacred flames engulfed them entirely leaving nothing but ash.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
    },
    {
        "id": 39,
        "name": "Destroyed by a Vampire Lord",
        "description": "{name} trespassed in the domain of an ancient Vampire Lord who crushed them without effort. Their remains were scattered to the winds.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
    },
    {
        "id": 40,
        "name": "Drowned in Holy Water",
        "description": "{name} was ambushed and submerged in a massive reservoir of blessed holy water by a cult of hunters. They could not escape.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
    },
    {
        "id": 41,
        "name": "Obliterated by a Witch Coven",
        "description": "{name} made an enemy of an entire witch coven. They gathered and unleashed a combined spell that unmade your vampire at a molecular level.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
    },
    {
        "id": 42,
        "name": "Sealed Away Forever",
        "description": "{name} was trapped in an enchanted iron coffin sealed with a thousand spells and buried a mile underground. Effectively dead. Gone forever.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
    },
    # NOTHING
    {
        "id": 11,
        "name": "Nothing Happens",
        "description": "{name} roams the night and finds nothing. The evening passes without incident. Sometimes darkness is just quiet.",
        "type": "nothing",
        "value": None,
        "color": discord.Color.greyple()
    },
    {
        "id": 43,
        "name": "A Quiet Night",
        "description": "{name} stalks the city rooftops for hours but finds no prey, no enemies, no events. The world sleeps undisturbed.",
        "type": "nothing",
        "value": None,
        "color": discord.Color.greyple()
    },
    # RECRUIT
    {
        "id": 44,
        "name": "A Wandering Vampire Appears",
        "description": "{name} encounters a lone vampire wandering without a coven. After a tense standoff, the stranger offers to join forces.",
        "type": "recruit",
        "value": None,
        "color": discord.Color.teal()
    },
    {
        "id": 45,
        "name": "Rescued a Captured Vampire",
        "description": "{name} stumbled upon a vampire being held captive by hunters. After freeing them, the grateful vampire swears loyalty.",
        "type": "recruit",
        "value": None,
        "color": discord.Color.teal()
    },
    {
        "id": 46,
        "name": "Survivor of a Destroyed Coven",
        "description": "{name} finds the sole survivor of a coven that was wiped out by hunters. With nowhere left to go, they pledge themselves to your cause.",
        "type": "recruit",
        "value": None,
        "color": discord.Color.teal()
    },
    {
        "id": 47,
        "name": "A Fledgling Seeks a Sire",
        "description": "{name} encounters a newly turned vampire alone and confused. Recognizing {name}'s power they beg to follow them.",
        "type": "recruit",
        "value": None,
        "color": discord.Color.teal()
    },
    {
        "id": 48,
        "name": "Impressed a Rival",
        "description": "{name} crossed paths with a rival vampire who challenged them to a show of strength. Impressed by what they saw, the rival defects and joins willingly.",
        "type": "recruit",
        "value": None,
        "color": discord.Color.teal()
    },
]


@bot.event
async def on_ready():
    print(f'{bot.user} is online')


@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs.")
        return False
    return True


@bot.command(name='vampire')
async def make_vampire(ctx):
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    power = generate_power()
    code = generate_code()
    tier, color = get_tier(power)

    vampires[code] = {
        "name": name,
        "power": power,
        "owner_id": ctx.author.id,
        "owner_name": ctx.author.name,
        "code": code,
        "alive": True
    }

    embed = discord.Embed(
        title="A Vampire Has Risen",
        description=f"**{name}**",
        color=color
    )
    embed.add_field(name="Owner", value=ctx.author.name, inline=True)
    embed.add_field(name="Power Level", value=str(power), inline=True)
    embed.add_field(name="Tier", value=tier, inline=True)
    embed.add_field(name="Code", value=f"`{code}`", inline=False)
    embed.set_footer(text="Use your code to perform actions with this vampire")

    await ctx.send(embed=embed)


@bot.command(name='show')
async def show_vampires(ctx):
    user_id = ctx.author.id
    user_vampires = [v for v in vampires.values() if v['owner_id'] == user_id]

    if not user_vampires:
        await ctx.send("You have no vampires. Use `?vampire` to create one.")
        return

    alive = [v for v in user_vampires if v['alive']]
    dead_count = len(user_vampires) - len(alive)

    embed = discord.Embed(
        title=f"{ctx.author.name}'s Vampires",
        description=f"Alive: {len(alive)}  |  Dead: {dead_count}",
        color=discord.Color.dark_purple()
    )

    if alive:
        for v in alive:
            tier, _ = get_tier(v['power'])
            embed.add_field(
                name=v['name'],
                value=f"Code: `{v['code']}`\nPower: {v['power']}\nTier: {tier}",
                inline=True
            )
    else:
        embed.add_field(
            name="No Alive Vampires",
            value="All your vampires have perished. Use `?vampire` to create a new one.",
            inline=False
        )

    embed.set_footer(text="Use ?random <code> to trigger events | ?fight <code> to battle")

    await ctx.send(embed=embed)


@bot.command(name='random')
async def random_event(ctx, code: str = None):
    if code is None:
        await ctx.send("Usage: `?random <code>`\nExample: `?random XKRV`")
        return

    code = code.upper()

    if code not in vampires:
        await ctx.send(f"No vampire found with code `{code}`.")
        return

    vampire = vampires[code]

    if vampire['owner_id'] != ctx.author.id:
        await ctx.send("You don't own this vampire!")
        return

    if not vampire['alive']:
        await ctx.send(f"**{vampire['name']}** is dead and cannot experience events anymore.")
        return

    event = random.choice(EVENTS)
    name = vampire['name']
    power = vampire['power']

    embed = discord.Embed(
        title=event['name'],
        description=event['description'].format(name=name),
        color=event['color']
    )

    embed.add_field(name="Vampire", value=name, inline=True)
    embed.add_field(name="Code", value=f"`{code}`", inline=True)

    if event['type'] == 'power_up':
        gain = random.randint(*event['value'])
        new_power = min(4500, power + gain)
        actual_gain = new_power - power
        vampire['power'] = new_power
        tier, _ = get_tier(new_power)
        embed.add_field(name="Power Change", value=f"{power} → **{new_power}** (+{actual_gain})", inline=False)
        embed.add_field(name="New Tier", value=tier, inline=True)
        embed.set_footer(text="Your vampire grows stronger...")

    elif event['type'] == 'power_down':
        loss = random.randint(*event['value'])
        new_power = max(10, power - loss)
        actual_loss = power - new_power
        vampire['power'] = new_power
        tier, _ = get_tier(new_power)
        embed.add_field(name="Power Change", value=f"{power} → **{new_power}** (-{actual_loss})", inline=False)
        embed.add_field(name="New Tier", value=tier, inline=True)
        embed.set_footer(text="Your vampire has been weakened...")

    elif event['type'] == 'death':
        vampire['alive'] = False
        embed.add_field(name="Power at Death", value=str(power), inline=False)
        embed.set_footer(text="This vampire is gone. Use ?vampire to create a new one.")

    elif event['type'] == 'nothing':
        tier, _ = get_tier(power)
        embed.add_field(name="Power", value=str(power), inline=True)
        embed.add_field(name="Tier", value=tier, inline=True)
        embed.set_footer(text="The night was uneventful...")

    elif event['type'] == 'recruit':
        recruited = generate_ai_vampire()
        new_code = generate_code()
        vampires[new_code] = {
            "name": recruited['name'],
            "power": recruited['power'],
            "owner_id": ctx.author.id,
            "owner_name": ctx.author.name,
            "code": new_code,
            "alive": True
        }
        recruited_tier, _ = get_tier(recruited['power'])
        embed.add_field(name="New Recruit", value=recruited['name'], inline=True)
        embed.add_field(name="Recruit Power", value=str(recruited['power']), inline=True)
        embed.add_field(name="Recruit Tier", value=recruited_tier, inline=True)
        embed.add_field(name="Recruit Code", value=f"`{new_code}`", inline=False)
        embed.set_footer(text="A new vampire has joined your ranks. Use their code to command them.")

    await ctx.send(embed=embed)


@bot.command(name='fight')
async def fight(ctx, code: str = None):
    if code is None:
        await ctx.send("Usage: `?fight <code>`\nExample: `?fight XKRV`")
        return

    code = code.upper()

    if code not in vampires:
        await ctx.send(f"No vampire found with code `{code}`.")
        return

    vampire = vampires[code]

    if vampire['owner_id'] != ctx.author.id:
        await ctx.send("You don't own this vampire!")
        return

    if not vampire['alive']:
        await ctx.send(f"**{vampire['name']}** is dead and cannot fight.")
        return

    enemy = generate_ai_vampire()
    player_power = vampire['power']
    enemy_power = enemy['power']
    player_tier, _ = get_tier(player_power)
    enemy_tier, _ = get_tier(enemy_power)

    # Battle intro
    intro_embed = discord.Embed(
        title="Blood Battle",
        description=f"**{vampire['name']}** faces off against **{enemy['name']}** in the darkness...",
        color=discord.Color.dark_red()
    )
    intro_embed.add_field(name=vampire['name'], value=f"Power: {player_power}\nTier: {player_tier}", inline=True)
    intro_embed.add_field(name="VS", value="\u200b", inline=True)
    intro_embed.add_field(name=enemy['name'], value=f"Power: {enemy_power}\nTier: {enemy_tier}", inline=True)
    intro_embed.set_footer(text="The battle begins...")
    await ctx.send(embed=intro_embed)
    await asyncio.sleep(3)

    # Calculate outcome
    # Win chance scales with power difference, capped between 10% and 90%
    power_diff = player_power - enemy_power
    win_chance = 50 + int((power_diff / 4500) * 80)
    win_chance = max(10, min(90, win_chance))
    roll = random.randint(1, 100)
    player_won = roll <= win_chance

    if player_won:
        # Win: gain some power, small death chance
        power_gain = random.randint(50, int(enemy_power * 0.3))
        new_power = min(4500, player_power + power_gain)
        vampire['power'] = new_power
        new_tier, color = get_tier(new_power)

        # Small chance to die even in victory (5-15%)
        death_on_win_roll = random.randint(1, 100)
        if death_on_win_roll <= 10:
            vampire['alive'] = False
            result_embed = discord.Embed(
                title="Pyrrhic Victory",
                description=f"**{vampire['name']}** defeated **{enemy['name']}** but sustained fatal wounds in the process. They crumble to ash moments after victory.",
                color=discord.Color.dark_red()
            )
            result_embed.add_field(name="Result", value="Won the fight, lost their life", inline=False)
            result_embed.add_field(name="Enemy Power", value=str(enemy_power), inline=True)
            result_embed.add_field(name="Power at Death", value=str(player_power), inline=True)
            result_embed.set_footer(text="Use ?vampire to create a new vampire.")
        else:
            result_embed = discord.Embed(
                title="Victory",
                description=f"**{vampire['name']}** has defeated **{enemy['name']}** and drained their power!",
                color=discord.Color.green()
            )
            result_embed.add_field(name="Enemy Power", value=str(enemy_power), inline=True)
            result_embed.add_field(name="Power Gained", value=f"+{new_power - player_power}", inline=True)
            result_embed.add_field(name="New Power", value=f"{player_power} → **{new_power}**", inline=False)
            result_embed.add_field(name="New Tier", value=new_tier, inline=True)
            result_embed.set_footer(text="Your vampire grows stronger with each kill.")
    else:
        # Loss: lose some power, higher death chance
        death_roll = random.randint(1, 100)

        # Death chance scales: bigger the power gap, higher the chance (20-65%)
        death_chance = 20 + int(abs(power_diff) / 4500 * 45)
        death_chance = max(20, min(65, death_chance))

        if death_roll <= death_chance:
            vampire['alive'] = False
            result_embed = discord.Embed(
                title="Defeated",
                description=f"**{vampire['name']}** was overpowered by **{enemy['name']}** and has been destroyed.",
                color=discord.Color.dark_red()
            )
            result_embed.add_field(name="Enemy Power", value=str(enemy_power), inline=True)
            result_embed.add_field(name="Your Power", value=str(player_power), inline=True)
            result_embed.add_field(name="Death Roll", value=f"Rolled {death_roll} — death at {death_chance}% or below", inline=False)
            result_embed.set_footer(text="Use ?vampire to create a new vampire.")
        else:
            power_loss = random.randint(50, int(player_power * 0.25))
            new_power = max(10, player_power - power_loss)
            vampire['power'] = new_power
            new_tier, _ = get_tier(new_power)
            result_embed = discord.Embed(
                title="Defeated — But Alive",
                description=f"**{vampire['name']}** was beaten by **{enemy['name']}** and barely escaped with their life.",
                color=discord.Color.orange()
            )
            result_embed.add_field(name="Enemy Power", value=str(enemy_power), inline=True)
            result_embed.add_field(name="Power Lost", value=f"-{player_power - new_power}", inline=True)
            result_embed.add_field(name="New Power", value=f"{player_power} → **{new_power}**", inline=False)
            result_embed.add_field(name="New Tier", value=new_tier, inline=True)
            result_embed.add_field(name="Death Roll", value=f"Rolled {death_roll} — death at {death_chance}% or below — survived", inline=False)
            result_embed.set_footer(text="Your vampire fled into the shadows, wounded.")

    await ctx.send(embed=result_embed)


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env")
    else:
        bot.run(TOKEN)
