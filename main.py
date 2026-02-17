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

# Real LA gangs
LA_GANGS = [
    "Rollin 60s Crips", "Grape Street Watts Crips", "East Coast Crips",
    "Compton Crips", "Long Beach Insane Crips", "Hoover Criminals",
    "Bloods of Piru", "Bounty Hunter Bloods", "Fruit Town Brims",
    "Inglewood Family Bloods", "Van Ness Gangster Bloods", "Denver Lane Bloods",
    "18th Street", "MS-13", "White Fence", "Florencia 13",
    "East LA 13", "Barrio Van Nuys", "Harpys", "Avenues",
    "Mara Salvatrucha", "South Side Compton Crips", "Watts Varrio Grape",
    "Shotgun Crips", "Raymond Avenue Crips"
]

# Gang name parts for user gangs
GANG_PREFIX = [
    "Eastside", "Westside", "Northside", "Southside", "Original",
    "Young", "Tiny", "Big", "Street", "Block",
    "Project", "Avenue", "Hillside", "Valley", "Harbor"
]

GANG_SUFFIX = [
    "Boys", "Gang", "Mob", "Squad", "Crew",
    "Family", "Nation", "Click", "Set", "Mafia"
]

gangs = {}
active_gang_owners = set()


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


def generate_ai_gang():
    name = random.choice(LA_GANGS)
    rep = random.randint(10, 500)
    return {"name": name, "rep": rep}


def mark_gang_dead(code):
    if code in gangs:
        gangs[code]['alive'] = False
        owner_id = gangs[code]['owner_id']
        if not user_has_active_gang(owner_id):
            active_gang_owners.discard(owner_id)


EVENTS = [
    # REP UPS
    {"name": "Drug Spot Takeover", "description": "{name} muscled out a rival crew and took over a profitable corner on Figueroa. Word spreads fast.", "type": "rep_up", "value": (20, 80), "color": discord.Color.green()},
    {"name": "Successful Lick", "description": "{name} pulled off a clean job and everyone on the block heard about it. Rep climbing.", "type": "rep_up", "value": (30, 100), "color": discord.Color.green()},
    {"name": "Street Fight Victory", "description": "{name} ran up on a crew from the other side and sent them packing. Block is locked down.", "type": "rep_up", "value": (20, 60), "color": discord.Color.green()},
    {"name": "Territory Claimed", "description": "{name} planted their flag on a new block nobody dared touch. Territory expanding.", "type": "rep_up", "value": (40, 120), "color": discord.Color.green()},
    {"name": "Big Homie Vouched", "description": "A respected OG from the neighborhood publicly backed {name}. That name now carries weight.", "type": "rep_up", "value": (50, 150), "color": discord.Color.green()},
    {"name": "Retaliation Hit", "description": "{name} answered disrespect with action. Nobody on the streets is laughing now.", "type": "rep_up", "value": (60, 180), "color": discord.Color.green()},
    {"name": "Prison Connections Made", "description": "{name} linked up with connects inside. The reach just got longer.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Rival Crew Scattered", "description": "A rival set got hit so hard they stopped showing up. {name} owns that side now.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    {"name": "Hood Documentary", "description": "A street doc filmmaker put {name} on camera. The streets are watching.", "type": "rep_up", "value": (30, 90), "color": discord.Color.green()},
    {"name": "Rapper Shoutout", "description": "A local rapper dropped a track shouting out {name} by name. Everyone knows who they are now.", "type": "rep_up", "value": (50, 130), "color": discord.Color.green()},
    {"name": "Block Party Respect", "description": "{name} threw a block party and fed the whole neighborhood. Community loyalty locked in.", "type": "rep_up", "value": (25, 70), "color": discord.Color.green()},
    {"name": "Jumped In New Members", "description": "{name} grew their numbers after a wave of young bloods wanted in. Strength in numbers.", "type": "rep_up", "value": (35, 95), "color": discord.Color.green()},
    # REP DOWNS
    {"name": "Snitch in the Ranks", "description": "Word got out that someone in {name} is talking to the feds. Trust is broken and rep is taking a hit.", "type": "rep_down", "value": (30, 100), "color": discord.Color.orange()},
    {"name": "Botched Mission", "description": "{name} tried to make a move and it went sideways. The streets are talking.", "type": "rep_down", "value": (20, 80), "color": discord.Color.orange()},
    {"name": "Key Member Arrested", "description": "One of {name}'s most important members got knocked by the LAPD. Operations are hurting.", "type": "rep_down", "value": (40, 120), "color": discord.Color.orange()},
    {"name": "Ran Off the Block", "description": "A rival crew rolled through deep and {name} had to fall back. That block is gone.", "type": "rep_down", "value": (50, 150), "color": discord.Color.orange()},
    {"name": "Internal Beef", "description": "Two members of {name} got into it publicly. The whole hood saw the disorganization.", "type": "rep_down", "value": (25, 75), "color": discord.Color.orange()},
    {"name": "LAPD Raid", "description": "The feds ran up on {name}'s spot. Product gone, members scattered.", "type": "rep_down", "value": (60, 180), "color": discord.Color.orange()},
    {"name": "Disrespected Publicly", "description": "A rival crew talked crazy about {name} in public and nobody did anything about it. Soft energy.", "type": "rep_down", "value": (30, 90), "color": discord.Color.orange()},
    {"name": "Lost a Shipment", "description": "{name} lost a major package on the way in. Money and rep both took a hit.", "type": "rep_down", "value": (45, 130), "color": discord.Color.orange()},
    {"name": "Member Flipped", "description": "Someone from {name} switched sides and took connects with them. Deep betrayal.", "type": "rep_down", "value": (50, 160), "color": discord.Color.orange()},
    {"name": "Jumped by Rivals", "description": "{name} got caught slipping and took an L in broad daylight. Everybody saw.", "type": "rep_down", "value": (35, 110), "color": discord.Color.orange()},
    # DEATHS
    {"name": "LAPD Task Force", "description": "A specialized LAPD task force built a case on {name} for months. Every member got swept up in a RICO charge. The gang is finished.", "type": "death", "color": discord.Color.dark_red()},
    {"name": "Wiped Out by Rivals", "description": "A massive coordinated hit by a rival gang left {name} with nothing. No members, no territory, no future.", "type": "death", "color": discord.Color.dark_red()},
    {"name": "Federal RICO Case", "description": "The feds finally dropped a RICO case on {name}. Leadership gone, members flipped, operation dissolved.", "type": "death", "color": discord.Color.dark_red()},
    {"name": "Gang War Annihilation", "description": "{name} got pulled into a full scale gang war they couldn't survive. The last members scattered or got buried.", "type": "death", "color": discord.Color.dark_red()},
    {"name": "Leadership Assassinated", "description": "Every shot caller in {name} got hit in a single night. With no leadership the gang crumbled overnight.", "type": "death", "color": discord.Color.dark_red()},
    # NOTHING
    {"name": "Quiet Night", "description": "{name} held down the block but nothing major went down tonight. Sometimes the streets are still.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Laying Low", "description": "{name} kept it low key. Heat was in the area so everybody stayed off the corners.", "type": "nothing", "color": discord.Color.greyple()},
    # RECRUIT
    {"name": "New Blood Walks In", "description": "A group of young guys from the neighborhood approached {name} looking to get put on. Crew just got bigger.", "type": "recruit", "color": discord.Color.teal()},
    {"name": "Rival Set Defected", "description": "A small crew from a rival gang got tired of their leadership and switched over to {name}. Bringing connects with them.", "type": "recruit", "color": discord.Color.teal()},
    {"name": "OG Came Home", "description": "A respected OG just got out of Pelican Bay and linked back up with {name}. Brings wisdom and old school connects.", "type": "recruit", "color": discord.Color.teal()},
]

EVENT_WEIGHTS = [200 for _ in EVENTS]


async def handle_gang(message, args):
    user_id = message.author.id

    if not is_admin(message):
        if user_has_active_gang(user_id):
            await message.channel.send(
                "You already have an active gang. Type `show` to see them."
            )
            return

    prefix = random.choice(GANG_PREFIX)
    suffix = random.choice(GANG_SUFFIX)
    name = f"{prefix} {suffix}"
    code = generate_code()
    rep = random.randint(10, 100)

    gangs[code] = {
        "name": name,
        "rep": rep,
        "owner_id": user_id,
        "owner_name": message.author.name,
        "code": code,
        "alive": True,
        "kills": 0,
        "fights_won": 0,
        "fights_lost": 0,
    }

    if not is_admin(message):
        active_gang_owners.add(user_id)

    embed = discord.Embed(
        title="Gang Created",
        description=f"**{name}** is now on the streets.",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="Owner", value=message.author.name, inline=True)
    embed.add_field(name="Street Cred", value=str(rep), inline=True)
    embed.add_field(name="Code", value=f"`{code}`", inline=False)
    embed.set_footer(text="Hold your block. Type: mission <code> | beef <code> | show")
    await message.channel.send(embed=embed)


async def handle_show(message, args):
    user_id = message.author.id
    user_gangs = [g for g in gangs.values() if g['owner_id'] == user_id]

    if not user_gangs:
        await message.channel.send("You have no gang. Type `gang` to start one.")
        return

    alive = [g for g in user_gangs if g['alive']]
    dead_count = len(user_gangs) - len(alive)

    embed = discord.Embed(
        title=f"{message.author.name}'s Gang",
        description=f"Active: {len(alive)}  |  Disbanded: {dead_count}",
        color=discord.Color.dark_grey()
    )

    if alive:
        for g in alive:
            fights_won = g.get('fights_won', 0)
            fights_lost = g.get('fights_lost', 0)
            total = fights_won + fights_lost
            win_rate = f"{int((fights_won / total) * 100)}%" if total > 0 else "N/A"

            embed.add_field(
                name=g['name'],
                value=(
                    f"Code: `{g['code']}`\n"
                    f"Street Cred: {g['rep']}\n"
                    f"Kills: {g.get('kills', 0)}\n"
                    f"Record: {fights_won}W - {fights_lost}L\n"
                    f"Win Rate: {win_rate}"
                ),
                inline=True
            )
    else:
        embed.add_field(
            name="No Active Gang",
            value="Your gang has been disbanded. Type `gang` to start fresh.",
            inline=False
        )

    embed.set_footer(text="Type: mission <code> | beef <code> | show")
    await message.channel.send(embed=embed)


async def handle_mission(message, args):
    if not args:
        await message.channel.send("Usage: `mission <code>`\nExample: `mission XKRV`")
        return

    code = args[0].upper()

    if code not in gangs:
        await message.channel.send(f"No gang found with code `{code}`.")
        return

    gang = gangs[code]

    if gang['owner_id'] != message.author.id:
        await message.channel.send("That's not your gang.")
        return

    if not gang['alive']:
        await message.channel.send(f"**{gang['name']}** has been disbanded.")
        return

    event = random.choices(EVENTS, weights=EVENT_WEIGHTS, k=1)[0]
    name = gang['name']
    rep = gang['rep']

    embed = discord.Embed(
        title=event['name'],
        description=event['description'].format(name=name),
        color=event['color']
    )
    embed.add_field(name="Gang", value=name, inline=True)
    embed.add_field(name="Code", value=f"`{code}`", inline=True)

    if event['type'] == 'rep_up':
        gain = random.randint(*event['value'])
        new_rep = rep + gain
        gang['rep'] = new_rep
        embed.add_field(name="Street Cred", value=f"{rep} → **{new_rep}** (+{gain})", inline=False)
        embed.set_footer(text="Reputation rising on the streets...")

    elif event['type'] == 'rep_down':
        loss = random.randint(*event['value'])
        new_rep = max(1, rep - loss)
        actual_loss = rep - new_rep
        gang['rep'] = new_rep
        embed.add_field(name="Street Cred", value=f"{rep} → **{new_rep}** (-{actual_loss})", inline=False)
        embed.set_footer(text="Taking an L on the streets...")

    elif event['type'] == 'death':
        mark_gang_dead(code)
        embed.add_field(name="Street Cred at Disbandment", value=str(rep), inline=False)
        embed.add_field(name="Final Record", value=f"{gang.get('fights_won', 0)}W - {gang.get('fights_lost', 0)}L", inline=True)
        embed.set_footer(text="Gang is done. Type gang to start over.")

    elif event['type'] == 'nothing':
        embed.add_field(name="Street Cred", value=str(rep), inline=True)
        embed.set_footer(text="Nothing popped off tonight.")

    elif event['type'] == 'recruit':
        new_code = generate_code()
        new_rep = random.randint(10, 80)
        prefix = random.choice(GANG_PREFIX)
        suffix = random.choice(GANG_SUFFIX)
        new_name = f"{prefix} {suffix}"
        gangs[new_code] = {
            "name": new_name,
            "rep": new_rep,
            "owner_id": message.author.id,
            "owner_name": message.author.name,
            "code": new_code,
            "alive": True,
            "kills": 0,
            "fights_won": 0,
            "fights_lost": 0,
        }
        active_gang_owners.add(message.author.id)
        embed.add_field(name="New Set", value=new_name, inline=True)
        embed.add_field(name="Their Cred", value=str(new_rep), inline=True)
        embed.add_field(name="Code", value=f"`{new_code}`", inline=False)
        embed.set_footer(text="A new set is under your umbrella.")

    await message.channel.send(embed=embed)


async def handle_beef(message, args):
    if not args:
        await message.channel.send("Usage: `beef <code>`\nExample: `beef XKRV`")
        return

    code = args[0].upper()

    if code not in gangs:
        await message.channel.send(f"No gang found with code `{code}`.")
        return

    gang = gangs[code]

    if gang['owner_id'] != message.author.id:
        await message.channel.send("That's not your gang.")
        return

    if not gang['alive']:
        await message.channel.send(f"**{gang['name']}** has been disbanded.")
        return

    enemy = generate_ai_gang()
    player_rep = gang['rep']
    enemy_rep = enemy['rep']

    intro_embed = discord.Embed(
        title="Beef",
        description=f"**{gang['name']}** is going to war with **{enemy['name']}**...",
        color=discord.Color.dark_red()
    )
    intro_embed.add_field(name=gang['name'], value=f"Street Cred: {player_rep}", inline=True)
    intro_embed.add_field(name="VS", value="\u200b", inline=True)
    intro_embed.add_field(name=enemy['name'], value=f"Street Cred: {enemy_rep}", inline=True)
    intro_embed.set_footer(text="It's on...")
    await message.channel.send(embed=intro_embed)
    await asyncio.sleep(3)

    rep_diff = player_rep - enemy_rep
    win_chance = 50 + int((rep_diff / 500) * 40)
    win_chance = max(10, min(90, win_chance))
    roll = random.randint(1, 100)
    player_won = roll <= win_chance

    if player_won:
        rep_gain = random.randint(20, int(max(1, enemy_rep * 0.4)))
        new_rep = player_rep + rep_gain
        gang['rep'] = new_rep
        gang['kills'] = gang.get('kills', 0) + 1
        gang['fights_won'] = gang.get('fights_won', 0) + 1

        death_roll = random.randint(1, 100)
        if death_roll <= 8:
            mark_gang_dead(code)
            result_embed = discord.Embed(
                title="Won the Beef — But Lost Everything",
                description=f"**{gang['name']}** beat **{enemy['name']}** but the retaliation that followed was too much. The gang didn't survive the aftermath.",
                color=discord.Color.dark_red()
            )
            result_embed.add_field(name="Final Street Cred", value=str(player_rep), inline=True)
            result_embed.add_field(name="Final Kills", value=str(gang['kills']), inline=True)
            result_embed.set_footer(text="Type gang to start over.")
        else:
            result_embed = discord.Embed(
                title="Won the Beef",
                description=f"**{gang['name']}** ran **{enemy['name']}** off the block. Streets know who runs it now.",
                color=discord.Color.green()
            )
            result_embed.add_field(name="Enemy Cred", value=str(enemy_rep), inline=True)
            result_embed.add_field(name="Cred Gained", value=f"+{rep_gain}", inline=True)
            result_embed.add_field(name="New Street Cred", value=f"{player_rep} → **{new_rep}**", inline=False)
            result_embed.add_field(name="Total Kills", value=str(gang['kills']), inline=True)
            result_embed.set_footer(text="Hold that block.")
    else:
        death_chance = 20 + int(abs(rep_diff) / 500 * 40)
        death_chance = max(20, min(60, death_chance))
        death_roll = random.randint(1, 100)

        if death_roll <= death_chance:
            gang['fights_lost'] = gang.get('fights_lost', 0) + 1
            mark_gang_dead(code)
            result_embed = discord.Embed(
                title="Lost the Beef — Gang Disbanded",
                description=f"**{gang['name']}** got wiped out by **{enemy['name']}**. No members, no block, no future.",
                color=discord.Color.dark_red()
            )
            result_embed.add_field(name="Enemy Cred", value=str(enemy_rep), inline=True)
            result_embed.add_field(name="Your Cred", value=str(player_rep), inline=True)
            result_embed.add_field(name="Final Kills", value=str(gang.get('kills', 0)), inline=True)
            result_embed.set_footer(text="Type gang to start over.")
        else:
            rep_loss = random.randint(20, int(max(1, player_rep * 0.25)))
            new_rep = max(1, player_rep - rep_loss)
            gang['rep'] = new_rep
            gang['fights_lost'] = gang.get('fights_lost', 0) + 1
            result_embed = discord.Embed(
                title="Lost the Beef — Still Standing",
                description=f"**{gang['name']}** took an L against **{enemy['name']}** but lived to fight another day.",
                color=discord.Color.orange()
            )
            result_embed.add_field(name="Enemy Cred", value=str(enemy_rep), inline=True)
            result_embed.add_field(name="Cred Lost", value=f"-{player_rep - new_rep}", inline=True)
            result_embed.add_field(name="New Street Cred", value=f"{player_rep} → **{new_rep}**", inline=False)
            result_embed.set_footer(text="Regroup and come back stronger.")

    await message.channel.send(embed=result_embed)


COMMANDS = {
    "gang": handle_gang,
    "show": handle_show,
    "mission": handle_mission,
    "beef": handle_beef,
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
        bot.run(TOKEN)
