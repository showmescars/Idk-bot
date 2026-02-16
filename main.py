import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

WOLVES_FILE = 'wolves.json'

WOLF_FIRST_NAMES = [
    "Fenrir", "Lycaon", "Ragnar", "Alaric", "Gunnar", "Bjorn", "Sigurd", "Leif",
    "Ulfric", "Thorin", "Aldric", "Wulfgar", "Draven", "Kael", "Zephyr", "Cain",
    "Lucan", "Darian", "Vance", "Rowan", "Hadrian", "Cormac", "Bram", "Eldric",
    "Soren", "Magnus", "Ragnor", "Ivar", "Floki", "Orm", "Vidar", "Tyr",
    "Hati", "Skoll", "Geri", "Freki", "Amarok", "Akela", "Lobo", "Fang"
]

WOLF_LAST_NAMES = [
    "Blackfang", "Ironpelt", "Bloodmoon", "Grayclaw", "Darkwood", "Stonehowl",
    "Nightprowl", "Ashcoat", "Embermane", "Frostbite", "Duskrunner", "Grimclaw",
    "Shadowpelt", "Ravencoat", "Thornfang", "Wolfsbane", "Moonshard", "Starclaw",
    "Wildmane", "Bonecrusher", "Icefang", "Firepelt", "Stormhowl", "Voidclaw",
    "Splitfang", "Rustcoat", "Mudpelt", "Copperback", "Slateclaw", "Cragmane"
]

PACK_NAMES = [
    "Ironwood Pack", "Bloodmoon Pack", "Ashfall Pack", "Stormridge Pack", "Frostclaw Pack",
    "Emberpelt Pack", "Duskwood Pack", "Thornback Pack", "Grimhowl Pack", "Nightfall Pack",
    "Ravenspire Pack", "Cragmoon Pack", "Stonefang Pack", "Blackridge Pack", "Wolfsbane Pack",
    "Shadowrun Pack", "Copperback Pack", "Rustmane Pack", "Voidhowl Pack", "Splitrock Pack"
]

PACK_RANKS = ["Omega", "Delta", "Beta", "Alpha", "Prime Alpha"]

WELCOME_LINES = [
    "The pack circles you slowly before parting to let you through.",
    "A low howl rises from the pack as you approach. You are accepted.",
    "The Alpha steps forward, sniffs the air, and nods. You belong here.",
    "One by one the wolves of the pack acknowledge you. You are home.",
    "The pack's howls echo through the trees. You have found your family.",
    "Eyes glow in the dark all around you. Then the tension breaks. Welcome.",
    "The Beta nudges you with a shoulder. No words needed. You are in.",
    "A chorus of howls splits the night sky. The pack has spoken.",
    "The youngest wolves run circles around you. The elders simply watch and accept.",
    "You step into the clearing. The pack does not move. Then the Alpha howls once. Enough."
]


def load_wolves():
    if os.path.exists(WOLVES_FILE):
        with open(WOLVES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_wolves(wolves):
    with open(WOLVES_FILE, 'w') as f:
        json.dump(wolves, f, indent=4)

def generate_unique_id():
    wolves = load_wolves()
    existing_ids = {w.get('wolf_id') for w in wolves.values() if 'wolf_id' in w}
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing_ids:
            return new_id

def get_strength_label(strength):
    if strength <= 20:   return "Pup"
    elif strength <= 40: return "Scrapper"
    elif strength <= 60: return "Packmate"
    elif strength <= 80: return "Alpha"
    else:                return "Apex"

def assign_pack_rank(player_strength, pack_members):
    """Assign a rank based on where the player's strength falls within the pack"""
    strengths = sorted([m['strength'] for m in pack_members])
    below = sum(1 for s in strengths if s < player_strength)
    ratio = below / len(strengths)

    if ratio >= 0.9:
        return "Prime Alpha"
    elif ratio >= 0.7:
        return "Alpha"
    elif ratio >= 0.4:
        return "Beta"
    elif ratio >= 0.15:
        return "Delta"
    else:
        return "Omega"

def generate_pack_members():
    """Generate 4 to 7 AI wolves for the pack"""
    count   = random.randint(4, 7)
    members = []
    for _ in range(count):
        name     = f"{random.choice(WOLF_FIRST_NAMES)} {random.choice(WOLF_LAST_NAMES)}"
        strength = random.randint(1, 100)
        members.append({
            "name":     name,
            "strength": strength,
            "rank":     None
        })

    # Assign ranks to AI members among themselves
    sorted_members = sorted(members, key=lambda x: x['strength'])
    total          = len(sorted_members)
    for i, member in enumerate(sorted_members):
        ratio = i / total
        if ratio >= 0.85:
            member['rank'] = "Alpha"
        elif ratio >= 0.6:
            member['rank'] = "Beta"
        elif ratio >= 0.3:
            member['rank'] = "Delta"
        else:
            member['rank'] = "Omega"

    return members


@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Werewolf Bot Ready')

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs.")
        return False
    return True


@bot.command(name='wolf')
async def make_wolf(ctx):
    """Create a new werewolf. Usage: ?wolf"""
    wolves  = load_wolves()
    wolf_id = generate_unique_id()

    name     = f"{random.choice(WOLF_FIRST_NAMES)} {random.choice(WOLF_LAST_NAMES)}"
    strength = random.randint(1, 100)
    label    = get_strength_label(strength)

    wolf_data = {
        "wolf_id":    wolf_id,
        "name":       name,
        "username":   str(ctx.author),
        "user_id":    str(ctx.author.id),
        "strength":   strength,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    wolves[wolf_id] = wolf_data
    save_wolves(wolves)

    embed = discord.Embed(
        title=name,
        description=f"Owner: {ctx.author.name}\nID: `{wolf_id}`",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="Strength", value=str(strength), inline=True)
    embed.add_field(name="Class",    value=label,          inline=True)

    await ctx.send(embed=embed)


@bot.command(name='pack')
async def find_pack(ctx, wolf_id: str = None):
    """Go out and find a pack to join. Usage: ?pack <wolf_id>"""
    if wolf_id is None:
        await ctx.send("Usage: `?pack <wolf_id>`\nExample: `?pack 123456`\n\nUse `?wolf` to create a wolf first.")
        return

    wolves = load_wolves()

    if wolf_id not in wolves:
        await ctx.send(f"Wolf ID `{wolf_id}` not found.")
        return

    player_wolf = wolves[wolf_id]
    user_id     = str(ctx.author.id)

    if player_wolf.get('user_id') != user_id:
        await ctx.send("You don't own this wolf.")
        return

    if player_wolf.get('pack'):
        pack = player_wolf['pack']
        await ctx.send(
            f"**{player_wolf['name']}** is already a member of **{pack['pack_name']}** "
            f"holding the rank of **{pack['player_rank']}**."
        )
        return

    # Generate the pack
    pack_name    = random.choice(PACK_NAMES)
    members      = generate_pack_members()
    player_rank  = assign_pack_rank(player_wolf['strength'], members)
    welcome_line = random.choice(WELCOME_LINES)

    # Save pack info onto the wolf
    player_wolf['pack'] = {
        "pack_name":   pack_name,
        "player_rank": player_rank,
        "members":     members,
        "joined_at":   datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    wolves[wolf_id] = player_wolf
    save_wolves(wolves)

    # Sort members by strength descending for display
    display_members = sorted(members, key=lambda x: x['strength'], reverse=True)

    embed = discord.Embed(
        title=pack_name,
        description=welcome_line,
        color=discord.Color.dark_grey()
    )

    embed.add_field(
        name="Your Wolf",
        value=f"{player_wolf['name']}\nStrength: {player_wolf['strength']} | Rank: **{player_rank}**",
        inline=False
    )

    member_lines = "\n".join(
        f"{m['name']} - Strength: {m['strength']} | {m['rank']}"
        for m in display_members
    )

    embed.add_field(
        name=f"Pack Members ({len(members)})",
        value=member_lines,
        inline=False
    )

    embed.set_footer(text=f"ID: {wolf_id} | Use ?wolf to create another wolf")

    await ctx.send(embed=embed)


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
