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

STREET_NAMES = [
    "Lil Menace", "Big Loc", "Joker", "Tiny", "Demon", "Ghost", "Lil Creep",
    "Youngsta", "Lil Caps", "Big Hurt", "Shadow", "Lil Diablo", "Cisco",
    "Drowsy", "Spanky", "Lil Wicked", "Chuco", "Travieso", "Sleepy",
    "Lil Payaso", "Boxer", "Dopey", "Scrappy", "Sinner", "Lil Evil",
    "Big Trigg", "Lil Trigg", "Cartoon", "Psycho", "Lil Psycho",
    "Big Psycho", "Casper", "Lil Casper", "Smiley", "Lil Smiley",
    "Big Smiley", "Termite", "Lil Monster", "Big Monster", "Lil Lobo",
    "Big Lobo", "Pnut", "Lil Pnut", "Wino", "Lil Wino", "Coyote",
    "Lil Coyote", "Grumpy", "Lil Grumpy", "Chino", "Lil Chino",
    "Big Chino", "Stomper", "Lil Stomper", "Danger", "Lil Danger",
    "Vicious", "Lil Vicious", "Puppet", "Lil Puppet", "Sad Eyes",
    "Lil Sad Eyes", "Trigger", "Lil Trigger", "Mosco", "Lil Mosco",
    "Huero", "Lil Huero", "Big Huero", "Flaco", "Lil Flaco",
    "Gordo", "Lil Gordo", "Speedy", "Lil Speedy", "Terminator",
    "Lil Terminator", "Mugsy", "Lil Mugsy", "Sniper", "Lil Sniper",
    "Looney", "Lil Looney", "Big Looney", "Crazy", "Lil Crazy",
    "Big Crazy", "Silent", "Lil Silent", "Savage", "Lil Savage",
    "Big Savage", "Bandit", "Lil Bandit", "Sinister", "Lil Sinister",
    "Diablo", "Big Diablo", "Capone", "Lil Capone", "Scarface",
    "Lil Scarface", "Hitman", "Lil Hitman", "Naughty", "Lil Naughty"
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
            "kills": 0
        })
    return members


def get_alive_members(gang):
    return [m for m in gang.get('members', []) if m['alive']]


def get_gang_bodies(gang):
    return sum(m.get('kills', 0) for m in gang.get('members', []))


def check_and_mark_dead(code):
    """Mark gang as dead only if all members are dead."""
    gang = gangs[code]
    if len(get_alive_members(gang)) == 0:
        gang['alive'] = False
        owner_id = gang['owner_id']
        if not user_has_active_gang(owner_id):
            active_gang_owners.discard(owner_id)


def format_member_list(members):
    if not members:
        return "None left"
    lines = []
    for m in members:
        lines.append(f"{m['name']}  —  {m.get('kills', 0)} bodies")
    return "\n".join(lines)


EVENTS = [
    # REP UPS
    {"name": "Corner Locked Down", "description": "{member} stepped up and muscled out the competition, locking down a corner on Figueroa for **{name}**. Word spreads fast.", "type": "rep_up", "value": (20, 80), "color": discord.Color.green()},
    {"name": "Successful Lick", "description": "{member} pulled off a clean job and put the whole **{name}** set on. Rep climbing.", "type": "rep_up", "value": (30, 100), "color": discord.Color.green()},
    {"name": "Street Fight Victory", "description": "{member} ran up on the opposition solo and sent them running. **{name}** owns that block now.", "type": "rep_up", "value": (20, 60), "color": discord.Color.green()},
    {"name": "Territory Claimed", "description": "**{name}** planted the flag on a new block. {member} led the push nobody dared stop.", "type": "rep_up", "value": (40, 120), "color": discord.Color.green()},
    {"name": "OG Vouched", "description": "A respected OG publicly backed {member} and the whole **{name}** set. That name now carries weight.", "type": "rep_up", "value": (50, 150), "color": discord.Color.green()},
    {"name": "Retaliation Hit", "description": "{member} answered disrespect with action on behalf of **{name}**. Nobody on the streets is laughing now.", "type": "rep_up", "value": (60, 180), "color": discord.Color.green()},
    {"name": "Prison Connects Made", "description": "{member} linked up with connects inside. **{name}**'s reach just got longer.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Rival Scattered", "description": "{member} hit the opposition so hard they stopped showing up. **{name}** owns that side now.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    {"name": "Hood Documentary", "description": "A street doc filmmaker put {member} on camera repping **{name}**. The streets are watching.", "type": "rep_up", "value": (30, 90), "color": discord.Color.green()},
    {"name": "Rapper Shoutout", "description": "A local rapper dropped a track shouting out {member} and **{name}** by name. Everyone knows who they are now.", "type": "rep_up", "value": (50, 130), "color": discord.Color.green()},
    {"name": "Fed the Block", "description": "{member} threw a block party for the whole neighborhood repping **{name}**. Community loyalty locked in.", "type": "rep_up", "value": (25, 70), "color": discord.Color.green()},
    {"name": "Big Score", "description": "{member} came up on a major score that set the whole **{name}** crew right. Money and respect flowing.", "type": "rep_up", "value": (60, 160), "color": discord.Color.green()},
    {"name": "Took the Block Back", "description": "{member} reclaimed territory for **{name}** that was lost and made it clear who runs it.", "type": "rep_up", "value": (70, 170), "color": discord.Color.green()},
    {"name": "Put in Work", "description": "{member} handled business that needed handling for **{name}**. No questions asked. Respect earned.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    # REP DOWNS
    {"name": "Snitch in the Ranks", "description": "Word got out that {member} is talking to the feds. **{name}** trust is broken and rep is taking a hit.", "type": "rep_down", "value": (30, 100), "color": discord.Color.orange()},
    {"name": "Botched Mission", "description": "{member} tried to make a move for **{name}** and it went sideways. The streets are talking.", "type": "rep_down", "value": (20, 80), "color": discord.Color.orange()},
    {"name": "Homie Got Knocked", "description": "{member}, one of **{name}**'s most trusted, got picked up by LAPD. Operations are hurting.", "type": "rep_down", "value": (40, 120), "color": discord.Color.orange()},
    {"name": "Ran Off the Block", "description": "Opps rolled through deep and {member} had to fall back. **{name}** lost that block.", "type": "rep_down", "value": (50, 150), "color": discord.Color.orange()},
    {"name": "Internal Beef", "description": "{member} and another homie got into it publicly. The whole hood saw **{name}**'s disorganization.", "type": "rep_down", "value": (25, 75), "color": discord.Color.orange()},
    {"name": "LAPD Raid", "description": "Task force ran up on **{name}**'s spot. {member} and the rest scattered. Everything gone.", "type": "rep_down", "value": (60, 180), "color": discord.Color.orange()},
    {"name": "Caught Lacking", "description": "Opps caught {member} slipping in public repping **{name}** and nothing got done about it.", "type": "rep_down", "value": (30, 90), "color": discord.Color.orange()},
    {"name": "Lost the Package", "description": "{member} lost a major package on the way in. **{name}** took a hit in money and rep.", "type": "rep_down", "value": (45, 130), "color": discord.Color.orange()},
    {"name": "Homie Flipped", "description": "{member} switched sides and took connects with them. Deep betrayal inside **{name}**.", "type": "rep_down", "value": (50, 160), "color": discord.Color.orange()},
    {"name": "Jumped by Opps", "description": "{member} got caught slipping for **{name}** and took an L in broad daylight. Everybody saw.", "type": "rep_down", "value": (35, 110), "color": discord.Color.orange()},
    {"name": "Fronted and Folded", "description": "{member} made a big threat publicly for **{name}** and didn't follow through. The streets remember.", "type": "rep_down", "value": (40, 100), "color": discord.Color.orange()},
    # NOTHING
    {"name": "Quiet Night", "description": "{member} held down the block for **{name}** but nothing major went down tonight. Sometimes the streets are still.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Laying Low", "description": "{member} kept it low key. Too much heat in the area so **{name}** stayed off the corners.", "type": "nothing", "color": discord.Color.greyple()},
]

EVENT_WEIGHTS = [200 for _ in EVENTS]


async def handle_gang(message, args):
    user_id = message.author.id

    if not is_admin(message):
        if user_has_active_gang(user_id):
            await message.channel.send("You already got a crew running. Type `show` to see them.")
            return

    la_gang = random.choice(LA_GANGS)
    gang_name = la_gang["name"]
    hood = la_gang["hood"]
    code = generate_code()
    rep = random.randint(10, 100)

    members = generate_ai_members(random.randint(4, 7))
    leader = members[0]['name']

    gangs[code] = {
        "name": gang_name,
        "hood": hood,
        "leader": leader,
        "rep": rep,
        "owner_id": user_id,
        "owner_name": message.author.name,
        "code": code,
        "alive": True,
        "fights_won": 0,
        "fights_lost": 0,
        "members": members,
    }

    if not is_admin(message):
        active_gang_owners.add(user_id)

    member_list = "\n".join([m['name'] for m in members])

    embed = discord.Embed(
        title="You're In",
        description=f"You just got put on with **{gang_name}**.",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="Hood", value=hood, inline=True)
    embed.add_field(name="Shot Caller", value=leader, inline=True)
    embed.add_field(name="Street Cred", value=str(rep), inline=True)
    embed.add_field(name="Members", value=str(len(members)), inline=True)
    embed.add_field(name="Code", value=f"`{code}`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Crew", value=member_list, inline=False)
    embed.set_footer(text="Type: mission <code> | beef <code> | recruit <code> | show")
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
            alive_members = get_alive_members(g)
            total_bodies = get_gang_bodies(g)
            member_block = format_member_list(alive_members)

            embed.add_field(
                name=f"{g['name']}",
                value=(
                    f"Hood: {g.get('hood', 'Unknown')}\n"
                    f"Code: `{g['code']}`\n"
                    f"Shot Caller: {g.get('leader', 'Unknown')}\n"
                    f"Street Cred: {g['rep']}\n"
                    f"Record: {fights_won}W - {fights_lost}L   |   Win Rate: {win_rate}\n"
                    f"Total Bodies: {total_bodies}"
                ),
                inline=False
            )
            embed.add_field(
                name=f"Alive Members ({len(alive_members)})",
                value=member_block,
                inline=False
            )
            embed.add_field(name="\u200b", value="\u200b", inline=False)
    else:
        embed.add_field(
            name="No Active Crew",
            value="Your crew got disbanded. Type `gang` to start fresh.",
            inline=False
        )

    embed.set_footer(text="Type: mission <code> | beef <code> | recruit <code> | show")
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

    alive_members = get_alive_members(gang)
    if not alive_members:
        await message.channel.send(f"**{gang['name']}** has no members left.")
        return

    featured_member = random.choice(alive_members)
    event = random.choices(EVENTS, weights=EVENT_WEIGHTS, k=1)[0]
    name = gang['name']
    rep = gang['rep']

    embed = discord.Embed(
        title=event['name'],
        description=event['description'].format(name=name, member=featured_member['name']),
        color=event['color']
    )
    embed.add_field(name="Crew", value=name, inline=True)
    embed.add_field(name="Code", value=f"`{code}`", inline=True)

    if event['type'] == 'rep_up':
        gain = random.randint(*event['value'])
        new_rep = rep + gain
        gang['rep'] = new_rep
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Member", value=featured_member['name'], inline=True)
        embed.add_field(name="Street Cred", value=f"{rep} -> **{new_rep}** (+{gain})", inline=True)
        embed.set_footer(text="Rep rising on the streets...")

    elif event['type'] == 'rep_down':
        loss = random.randint(*event['value'])
        new_rep = max(1, rep - loss)
        actual_loss = rep - new_rep
        gang['rep'] = new_rep

        # Only kill a member on rep_down if more than 1 alive — never wipe the gang
        if random.randint(1, 100) <= 15 and len(alive_members) > 1:
            featured_member['alive'] = False
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="Member Lost", value=featured_member['name'], inline=True)
            embed.add_field(name="Street Cred", value=f"{rep} -> **{new_rep}** (-{actual_loss})", inline=True)
        else:
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="Street Cred", value=f"{rep} -> **{new_rep}** (-{actual_loss})", inline=False)

        embed.set_footer(text="Taking an L on the streets...")

    elif event['type'] == 'nothing':
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Member", value=featured_member['name'], inline=True)
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
        await message.channel.send(f"**{gang['name']}** roster is already full. No new names left.")
        return

    success = random.randint(1, 2) == 1

    if success:
        new_name = random.choice(available)
        new_member = {
            "name": new_name,
            "rep": random.randint(10, 150),
            "alive": True,
            "kills": 0
        }
        gang['members'].append(new_member)
        alive_count = len(get_alive_members(gang))

        embed = discord.Embed(
            title="New Member",
            description=f"**{new_name}** just got put on with **{gang['name']}**. The set is growing.",
            color=discord.Color.teal()
        )
        embed.add_field(name="Gang", value=gang['name'], inline=True)
        embed.add_field(name="New Member", value=new_name, inline=True)
        embed.add_field(name="Total Members", value=str(alive_count), inline=True)
        embed.set_footer(text="Keep building the set.")
    else:
        embed = discord.Embed(
            title="Nobody Came Through",
            description=f"**{gang['name']}** put the word out but nobody stepped up. Try again.",
            color=discord.Color.dark_grey()
        )
        embed.add_field(name="Gang", value=gang['name'], inline=True)
        embed.add_field(name="Members", value=str(len(get_alive_members(gang))), inline=True)
        embed.set_footer(text="50/50. Try again.")

    await message.channel.send(embed=embed)


async def handle_beef(message, args):
    if not args:
        await message.channel.send("Usage: `beef <code>`\nExample: `beef XKRV`")
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

    alive_members = get_alive_members(gang)
    if not alive_members:
        await message.channel.send(f"**{gang['name']}** has no members left to beef.")
        return

    max_rollers = min(3, len(alive_members))
    roll_count = random.randint(1, max_rollers)
    rolling_members = random.sample(alive_members, roll_count)

    enemy_gang_info = random.choice(LA_GANGS)
    enemy_count = random.randint(1, 3)
    enemy_members = generate_ai_members(enemy_count)
    enemy_rep = random.randint(10, 500)
    player_rep = gang['rep']

    rolling_names = "\n".join([m['name'] for m in rolling_members])
    enemy_names = "\n".join([m['name'] for m in enemy_members])

    intro_embed = discord.Embed(
        title="Beef",
        description=f"**{gang['name']}** is rolling out against **{enemy_gang_info['name']}**...",
        color=discord.Color.dark_red()
    )
    intro_embed.add_field(name=f"{gang['name']}", value=f"Street Cred: {player_rep}\n\n{rolling_names}", inline=True)
    intro_embed.add_field(name="VS", value="\u200b", inline=True)
    intro_embed.add_field(name=f"{enemy_gang_info['name']}", value=f"Street Cred: {enemy_rep}\n\n{enemy_names}", inline=True)
    intro_embed.set_footer(text="It's on...")
    await message.channel.send(embed=intro_embed)

    await asyncio.sleep(3)

    rep_diff = player_rep - enemy_rep
    win_chance = 50 + int((rep_diff / 500) * 40)
    win_chance = max(10, min(90, win_chance))
    roll = random.randint(1, 100)
    player_won = roll <= win_chance

    outcome_lines = []
    result_embed = discord.Embed(color=discord.Color.dark_grey())

    if player_won:
        rep_gain = random.randint(20, int(max(1, enemy_rep * 0.4)))
        new_rep = player_rep + rep_gain
        gang['rep'] = new_rep
        gang['fights_won'] = gang.get('fights_won', 0) + 1

        for m in rolling_members:
            m['kills'] = m.get('kills', 0) + 1
            outcome_lines.append(f"{m['name']} caught a body")

        # Casualty on a win — only if it won't wipe the gang
        remaining_alive = get_alive_members(gang)
        if random.randint(1, 100) <= 20 and len(remaining_alive) > 1:
            casualty = random.choice(rolling_members)
            if casualty['alive']:
                casualty['alive'] = False
                outcome_lines.append(f"{casualty['name']} got hit and didn't make it back")

        total_bodies = get_gang_bodies(gang)

        result_embed = discord.Embed(
            title="Won the Beef",
            description=f"**{gang['name']}** ran **{enemy_gang_info['name']}** off the block. Streets know who runs it now.",
            color=discord.Color.green()
        )
        result_embed.add_field(name="What Went Down", value="\n".join(outcome_lines) if outcome_lines else "Clean sweep.", inline=False)
        result_embed.add_field(name="Opp Cred", value=str(enemy_rep), inline=True)
        result_embed.add_field(name="Cred Gained", value=f"+{rep_gain}", inline=True)
        result_embed.add_field(name="New Street Cred", value=f"{player_rep} -> **{new_rep}**", inline=True)
        result_embed.add_field(name="Total Bodies", value=str(total_bodies), inline=True)
        result_embed.add_field(name="Members Alive", value=str(len(get_alive_members(gang))), inline=True)
        result_embed.set_footer(text="Hold that block.")

    else:
        gang['fights_lost'] = gang.get('fights_lost', 0) + 1

        # On a loss, rolling members can get hit — but never wipe all members
        for m in rolling_members:
            remaining_alive = get_alive_members(gang)
            if random.randint(1, 100) <= 40 and len(remaining_alive) > 1:
                m['alive'] = False
                outcome_lines.append(f"{m['name']} got bodied")
            else:
                outcome_lines.append(f"{m['name']} took a hit but made it out")

        rep_loss = random.randint(20, int(max(1, player_rep * 0.25)))
        new_rep = max(1, player_rep - rep_loss)
        gang['rep'] = new_rep
        total_bodies = get_gang_bodies(gang)

        result_embed = discord.Embed(
            title="Lost the Beef - Still Standing",
            description=f"**{gang['name']}** took an L against **{enemy_gang_info['name']}** but lived to fight another day.",
            color=discord.Color.orange()
        )
        result_embed.add_field(name="What Went Down", value="\n".join(outcome_lines) if outcome_lines else "Barely made it.", inline=False)
        result_embed.add_field(name="Opp Cred", value=str(enemy_rep), inline=True)
        result_embed.add_field(name="Cred Lost", value=f"-{player_rep - new_rep}", inline=True)
        result_embed.add_field(name="New Street Cred", value=f"{player_rep} -> **{new_rep}**", inline=True)
        result_embed.add_field(name="Total Bodies", value=str(total_bodies), inline=True)
        result_embed.add_field(name="Members Alive", value=str(len(get_alive_members(gang))), inline=True)
        result_embed.set_footer(text="Regroup and come back.")

    # Check after everything if all members are now dead — only then mark gang dead
    check_and_mark_dead(code)

    await message.channel.send(embed=result_embed)


COMMANDS = {
    "gang": handle_gang,
    "show": handle_show,
    "mission": handle_mission,
    "beef": handle_beef,
    "recruit": handle_recruit,
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
