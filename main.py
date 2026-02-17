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
    "Tepes", "Drăculești", "Karnstein", "De Lioncourt", "Enkil", "Romanus", "Corvinus", "Nightshade",
    "Von Doom", "Bloodworth", "Blackthorn", "Darkmore", "Volturi", "Mikaelson", "Salvatore", "Pierce",
    "Bennett", "Forbes", "Lockwood", "Donovan", "Gilbert", "Fell", "Whitmore", "St. John",
    "Ashford", "Bloodmoon", "Crimson", "Ravencroft", "Shadowend", "Duskbane", "Nocturne", "Grave",
    "Morningstar", "Hellsing", "Alucard", "Belmont", "Blackwood", "Von Carstein", "Draken",
    "Mourning", "Eclipse", "Eventide", "Twilight", "Sanguine", "Hemlock", "Mortis", "Grimwood",
    "Nightfall", "Darkholm"
]


def generate_power():
    roll = random.randint(1, 100)
    if roll <= 45:
        return random.randint(10, 400)
    elif roll <= 75:
        return random.randint(401, 1000)
    elif roll <= 90:
        return random.randint(1001, 1600)
    else:
        return random.randint(1601, 2000)


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

    if power <= 400:
        tier = "Fledgling"
        color = discord.Color.dark_grey()
    elif power <= 1000:
        tier = "Experienced"
        color = discord.Color.blue()
    elif power <= 1600:
        tier = "Ancient"
        color = discord.Color.purple()
    else:
        tier = "Primordial"
        color = discord.Color.gold()

    embed = discord.Embed(
        title="A Vampire Has Risen",
        description=f"**{name}**",
        color=color
    )
    embed.add_field(name="Owner", value=ctx.author.name, inline=True)
    embed.add_field(name="Power Level", value=str(power), inline=True)
    embed.add_field(name="Tier", value=tier, inline=True)
    embed.set_footer(text="A new vampire emerges from the darkness...")

    await ctx.send(embed=embed)


if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env")
    else:
        bot.run(TOKEN)
