import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import os

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


EVENTS = [
    {
        "id": 1,
        "name": "Ancient Tome Discovered",
        "description": "{name} stumbles upon a forbidden ancient tome deep in a crumbling castle library. The dark knowledge within surges through their veins.",
        "type": "power_up",
        "value": (100, 300),
        "color": discord.Color.green()
    },
    {
        "id": 2,
        "name": "Ambushed by Hunters",
        "description": "{name} is ambushed by a squad of elite vampire hunters armed with holy weapons. They barely escape but are gravely weakened.",
        "type": "power_down",
        "value": (100, 400),
        "color": discord.Color.orange()
    },
    {
        "id": 3,
        "name": "Slain by a Vampire Hunter",
        "description": "{name} encountered the legendary hunter Van Hellward and lost. A silver stake finds its mark. Your vampire is dead.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
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
        "id": 5,
        "name": "Cursed by a Witch",
        "description": "{name} crossed into a witch's territory uninvited. She placed a draining curse on them, sapping their strength.",
        "type": "power_down",
        "value": (150, 500),
        "color": discord.Color.orange()
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
        "id": 7,
        "name": "Exposed to Sunlight",
        "description": "{name} was trapped outside at dawn by a cunning enemy. The sunlight scorched away a portion of their power before they escaped.",
        "type": "power_down",
        "value": (200, 600),
        "color": discord.Color.orange()
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
        "id": 9,
        "name": "Formed a Dark Alliance",
        "description": "{name} allied with a powerful vampire coven. Through shared blood rituals, their power has grown significantly.",
        "type": "power_up",
        "value": (150, 400),
        "color": discord.Color.green()
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
        "id": 11,
        "name": "Nothing Happens",
        "description": "{name} roams the night and finds nothing. The evening passes without incident. Sometimes darkness is just quiet.",
        "type": "nothing",
        "value": None,
        "color": discord.Color.greyple()
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
        "id": 13,
        "name": "Afflicted with Bloodlust Madness",
        "description": "{name} lost control to bloodlust and went on a rampage, drawing the attention of every hunter in the region. They barely survived.",
        "type": "power_down",
        "value": (300, 700),
        "color": discord.Color.orange()
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
        "id": 15,
        "name": "Mastered a New Ability",
        "description": "{name} spent weeks in isolation practicing dark arts. They have awakened a new supernatural ability, boosting their combat power.",
        "type": "power_up",
        "value": (200, 500),
        "color": discord.Color.green()
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
        "id": 17,
        "name": "Decapitated by a Slayer",
        "description": "{name} underestimated a lone slayer who carried an enchanted blade. One swift strike ends their undead existence permanently.",
        "type": "death",
        "value": None,
        "color": discord.Color.dark_red()
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
        "id": 19,
        "name": "Trapped in a Silver Cage",
        "description": "{name} was lured into a silver cage trap. Days of exposure to silver drained their supernatural strength before they escaped.",
        "type": "power_down",
        "value": (250, 550),
        "color": discord.Color.orange()
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
        "id": 21,
        "name": "Exorcism Ritual Performed",
        "description": "{name} was caught in the crossfire of a massive exorcism ritual. The holy energy tore through them, stripping away their power.",
        "type": "power_down",
        "value": (400, 900),
        "color": discord.Color.orange()
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
        "id": 23,
        "name": "Bonded with a Familiar",
        "description": "{name} bonded with a powerful supernatural familiar that enhances their senses and combat abilities beyond normal limits.",
        "type": "power_up",
        "value": (150, 400),
        "color": discord.Color.green()
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
        "id": 25,
        "name": "Absorbed a Dying Bloodline",
        "description": "{name} was the last to find a dying vampire bloodline and absorbed their entire lineage's power in a single night.",
        "type": "power_up",
        "value": (500, 1100),
        "color": discord.Color.green()
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
    dead_count = len([v for v in user_vampires if not v['alive']])

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

    embed.set_footer(text="Use ?random <code> to trigger events for your vampires")

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

    await ctx.send(embed=embed)


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env")
    else:
        bot.run(TOKEN)
