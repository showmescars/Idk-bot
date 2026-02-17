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

# Street member nicknames
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

# Real LA Gangs
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
    {"name": "Mara Salvatrucha", "hood": "Multiple, LA"},
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


def generate_ai_member():
    name = random.choice(STREET_NAMES)
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
    {"name": "Corner Locked Down", "description": "{name} and the crew muscled out the competition and took over a profitable corner on Figueroa. Word spreads fast.", "type": "rep_up", "value": (20, 80), "color": discord.Color.green()},
    {"name": "Successful Lick", "description": "{name} pulled off a clean job and everyone on the block heard about it. Rep climbing.", "type": "rep_up", "value": (30, 100), "color": discord.Color.green()},
    {"name": "Street Fight Victory", "description": "{name} ran up on the opposition and sent them running. Block is locked down.", "type": "rep_up", "value": (20, 60), "color": discord.Color.green()},
    {"name": "Territory Claimed", "description": "{name} planted the flag on a new block nobody dared touch. Territory expanding.", "type": "rep_up", "value": (40, 120), "color": discord.Color.green()},
    {"name": "OG Vouched", "description": "A respected OG from the neighborhood publicly backed {name}. That name now carries weight.", "type": "rep_up", "value": (50, 150), "color": discord.Color.green()},
    {"name": "Retaliation Hit", "description": "{name} answered disrespect with action. Nobody on the streets is laughing now.", "type": "rep_up", "value": (60, 180), "color": discord.Color.green()},
    {"name": "Prison Connects Made", "description": "{name} linked up with connects inside. The reach just got longer.", "type": "rep_up", "value": (40, 100), "color": discord.Color.green()},
    {"name": "Rival Scattered", "description": "The opposition got hit so hard they stopped showing up. {name} owns that side now.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    {"name": "Hood Documentary", "description": "A street doc filmmaker put {name} on camera. The streets are watching.", "type": "rep_up", "value": (30, 90), "color": discord.Color.green()},
    {"name": "Rapper Shoutout", "description": "A local rapper dropped a track shouting out {name} by name. Everyone knows who they are now.", "type": "rep_up", "value": (50, 130), "color": discord.Color.green()},
    {"name": "Fed the Block", "description": "{name} threw a block party and fed the whole neighborhood. Community loyalty locked in.", "type": "rep_up", "value": (25, 70), "color": discord.Color.green()},
    {"name": "New Homies Jumped In", "description": "{name} grew the crew after a wave of young bloods wanted in. Strength in numbers.", "type": "rep_up", "value": (35, 95), "color": discord.Color.green()},
    {"name": "Big Score", "description": "{name} came up on a major score that set the whole crew right. Money and respect flowing.", "type": "rep_up", "value": (60, 160), "color": discord.Color.green()},
    {"name": "Took the Block Back", "description": "{name} reclaimed territory that was lost and made it clear who runs it.", "type": "rep_up", "value": (70, 170), "color": discord.Color.green()},
    {"name": "Put in Work", "description": "{name} handled business that needed handling. No questions asked. Respect earned.", "type": "rep_up", "value": (80, 200), "color": discord.Color.green()},
    # REP DOWNS
    {"name": "Snitch in the Ranks", "description": "Word got out that someone around {name} is talking to the feds. Trust is broken and rep is taking a hit.", "type": "rep_down", "value": (30, 100), "color": discord.Color.orange()},
    {"name": "Botched Mission", "description": "{name} tried to make a move and it went sideways. The streets are talking.", "type": "rep_down", "value": (20, 80), "color": discord.Color.orange()},
    {"name": "Homie Got Knocked", "description": "One of {name}'s most trusted people got picked up by LAPD. Operations are hurting.", "type": "rep_down", "value": (40, 120), "color": discord.Color.orange()},
    {"name": "Ran Off the Block", "description": "Opps rolled through deep and {name} had to fall back. That block is gone.", "type": "rep_down", "value": (50, 150), "color": discord.Color.orange()},
    {"name": "Internal Beef", "description": "Two people in {name}'s crew got into it publicly. The whole hood saw the disorganization.", "type": "rep_down", "value": (25, 75), "color": discord.Color.orange()},
    {"name": "LAPD Raid", "description": "Task force ran up on {name}'s spot. Everything gone, crew scattered.", "type": "rep_down", "value": (60, 180), "color": discord.Color.orange()},
    {"name": "Caught Lacking", "description": "Opps caught {name} slipping in public and nothing got done about it. Soft energy on the street.", "type": "rep_down", "value": (30, 90), "color": discord.Color.orange()},
    {"name": "Lost the Package", "description": "{name} lost a major package on the way in. Money and rep both took a hit.", "type": "rep_down", "value": (45, 130), "color": discord.Color.orange()},
    {"name": "Homie Flipped", "description": "Someone close to {name} switched sides and took connects with them. Deep betrayal.", "type": "rep_down", "value": (50, 160), "color": discord.Color.orange()},
    {"name": "Jumped by Opps", "description": "{name} got caught slipping and took an L in broad daylight. Everybody saw.", "type": "rep_down", "value": (35, 110), "color": discord.Color.orange()},
    {"name": "Dry Snitching", "description": "Someone around {name} been running their mouth indirectly. Word got back. Trust is shot.", "type": "rep_down", "value": (25, 80), "color": discord.Color.orange()},
    {"name": "Fronted and Folded", "description": "{name} made a big threat publicly and didn't follow through. The streets remember.", "type": "rep_down", "value": (40, 100), "color": discord.Color.orange()},
    # DEATHS
    {"name": "LAPD Task Force Sweep", "description": "A specialized LAPD task force had been watching {name} for months. Every connect got swept up in one night. It's over.", "type": "death", "color": discord.Color.dark_red()},
    {"name": "Wiped Out by Opps", "description": "A coordinated hit by the opposition left {name} with nothing. No crew, no block, no future.", "type": "death", "color": discord.Color.dark_red()},
    {"name": "Federal RICO Case", "description": "The feds dropped a RICO on {name}. Leadership gone, homies flipped, operation dissolved.", "type": "death", "color": discord.Color.dark_red()},
    {"name": "All Out War", "description": "{name} got pulled into a full scale war they couldn't survive. The last of the crew scattered or got buried.", "type": "death", "color": discord.Color.dark_red()},
    {"name": "Shot Callers Taken Out", "description": "Everyone holding it down for {name} got hit in a single week. With no leadership the crew fell apart overnight.", "type": "death", "color": discord.Color.dark_red()},
    # NOTHING
    {"name": "Quiet Night", "description": "{name} held down the block but nothing major went down tonight. Sometimes the streets are still.", "type": "nothing", "color": discord.Color.greyple()},
    {"name": "Laying Low", "description": "{name} kept it low key. Too much heat in the area so everybody stayed off the corners.", "type": "nothing", "color": discord.Color.greyple()},
    # RECRUIT
    {"name": "Young Blood Walks Up", "description": "A young guy from the neighborhood approached {name} looking to get put on. Crew just got a new member.", "type": "recruit", "color": discord.Color.teal()},
    {"name": "Opp Defected", "description": "A guy from the other side got tired of his people and came over to {name}. Bringing info and connects with him.", "type": "recruit", "color": discord.Color.teal()},
    {"name": "OG Came Home", "description": "A respected OG just touched down from Pelican Bay and linked back up with {name}. Old school connects and wisdom.", "type": "recruit", "color": discord.Color.teal()},
    {"name": "Rider Found", "description": "{name} met someone at the right time who proved themselves immediately. Solid addition to the crew.", "type": "recruit", "color": discord.Color.teal()},
    {"name": "Cousin Came Through", "description": "A cousin from out of town with serious street credentials linked up with {name}. Family ties run deep.", "type": "recruit", "color": discord.Color.teal()},
]

EVENT_WEIGHTS = [200 for _ in EVENTS]


async def handle_gang(message, args):
    user_id = message.author.id

    if not is_admin(message):
        if user_has_active_gang(user_id):
            await message.channel.send(
                "You already got a crew running. Type `show` to see them."
            )
            return

    # Pick a real LA gang
    la_gang = random.choice(LA_GANGS)
    gang_name = la_gang["name"]
    hood = la_gang["hood"]
    code = generate_code()
    rep = random.randint(10, 100)
    leader = random.choice(STREET_NAMES)

    gangs[code] = {
        "name": gang_name,
        "hood": hood,
        "leader": leader,
        "rep": rep,
        "owner_id": user_id,
        "owner_name": message.author.name,
        "code": code,
        "alive": True,
        "kills": 0,
        "fights_won": 0,
        "fights_lost": 0,
        "members": [leader],
    }

    if not is_admin(message):
        active_gang_owners.add(user_id)

    embed = discord.Embed(
        title="You're In",
        description=f"You just got put on with **{gang_name}**.",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="Hood", value=hood, inline=True)
    embed.add_field(name="Shot Caller", value=leader, inline=True)
    embed.add_field(name="Street Cred", value=str(rep), inline=True)
    embed.add_field(name="Members", value=str(len(gangs[code]['members'])), inline=True)
    embed.add_field(name="Code", value=f"`{code}`", inline=False)
    embed.set_footer(text="Hold your block. Type: mission <code> | beef <code> | show")
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
        description=f"Active: {len(alive)}  |  Disbanded: {dead_count}",
        color=discord.Color.dark_grey()
    )

    if alive:
        for g in alive:
            fights_won = g.get('fights_won', 0)
            fights_lost = g.get('fights_lost', 0)
            total = fights_won + fights_lost
            win_rate = f"{int((fights_won / total) * 100)}%" if total > 0 else "N/A"
            members = g.get('members', [g.get('leader', 'Unknown')])

            embed.add_field(
                name=g['name'],
                value=(
                    f"Hood: {g.get('hood', 'Unknown')}\n"
                    f"Code: `{g['code']}`\n"
                    f"Shot Caller: {g.get('leader', 'Unknown')}\n"
                    f"Members: {len(members)}\n"
                    f"Street Cred: {g['rep']}\n"
                    f"Bodies: {g.get('kills', 0)}\n"
                    f"Record: {fights_won}W - {fights_lost}L\n"
                    f"Win Rate: {win_rate}"
                ),
                inline=True
            )
    else:
        embed.add_field(
            name="No Active Crew",
            value="Your crew got disbanded. Type `gang` to start fresh.",
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
        await message.channel.send(f"No crew found with code `{code}`.")
        return

    gang = gangs[code]

    if gang['owner_id'] != message.author.id:
        await message.channel.send("That ain't your crew.")
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
    embed.add_field(name="Crew", value=name, inline=True)
    embed.add_field(name="Code", value=f"`{code}`", inline=True)

    if event['type'] == 'rep_up':
        gain = random.randint(*event['value'])
        new_rep = rep + gain
        gang['rep'] = new_rep
        embed.add_field(name="Street Cred", value=f"{rep} → **{new_rep}** (+{gain})", inline=False)
        embed.set_footer(text="Rep rising on the streets...")

    elif event['type'] == 'rep_down':
        loss = random.randint(*event['value'])
        new_rep = max(1, rep - loss)
        actual_loss = rep - new_rep
        gang['rep'] = new_rep
        embed.add_field(name="Street Cred", value=f"{rep} → **{new_rep}** (-{actual_loss})", inline=False)
        embed.set_footer(text="Taking an L on the streets...")

    elif event['type'] == 'death':
        mark_gang_dead(code)
        embed.add_field(name="Final Street Cred", value=str(rep), inline=False)
        embed.add_field(name="Final Record", value=f"{gang.get('fights_won', 0)}W - {gang.get('fights_lost', 0)}L", inline=True)
        embed.add_field(name="Bodies", value=str(gang.get('kills', 0)), inline=True)
        embed.set_footer(text="Crew is done. Type gang to start over.")

    elif event['type'] == 'nothing':
        embed.add_field(name="Street Cred", value=str(rep), inline=True)
        embed.set_footer(text="Nothing popped off tonight.")

    elif event['type'] == 'recruit':
        new_member = random.choice(STREET_NAMES)
        # Add the new member to the existing gang instead of creating a new one
        if 'members' not in gang:
            gang['members'] = [gang.get('leader', 'Unknown')]
        gang['members'].append(new_member)
        member_count = len(gang['members'])

        embed.add_field(name="New Member Jumped In", value=new_member, inline=True)
        embed.add_field(name="Total Members", value=str(member_count), inline=True)
        embed.add_field(name="Gang", value=f"{name} — {gang.get('hood', '')}", inline=False)
        embed.set_footer(text="The set is growing.")

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

    enemy = generate_ai_member()
    player_rep = gang['rep']
    enemy_rep = enemy['rep']

    intro_embed = discord.Embed(
        title="Beef",
        description=f"**{gang['name']}** is going to war with **{enemy['name']}** and his crew...",
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

    result_embed = None

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
                title="Won — But the Retaliation Was Too Much",
                description=f"**{gang['name']}** smoked **{enemy['name']}** but the blowback that followed was too heavy. Crew didn't survive.",
                color=discord.Color.dark_red()
            )
            result_embed.add_field(name="Final Street Cred", value=str(player_rep), inline=True)
            result_embed.add_field(name="Final Bodies", value=str(gang['kills']), inline=True)
            result_embed.set_footer(text="Type gang to start over.")
        else:
            result_embed = discord.Embed(
                title="Won the Beef",
                description=f"**{gang['name']}** ran **{enemy['name']}** and his crew off the block. Streets know who runs it now.",
                color=discord.Color.green()
            )
            result_embed.add_field(name="Opp Cred", value=str(enemy_rep), inline=True)
            result_embed.add_field(name="Cred Gained", value=f"+{rep_gain}", inline=True)
            result_embed.add_field(name="New Street Cred", value=f"{player_rep} → **{new_rep}**", inline=False)
            result_embed.add_field(name="Total Bodies", value=str(gang['kills']), inline=True)
            result_embed.set_footer(text="Hold that block.")
    else:
        death_chance = 20 + int(abs(rep_diff) / 500 * 40)
        death_chance = max(20, min(60, death_chance))
        death_roll = random.randint(1, 100)

        if death_roll <= death_chance:
            gang['fights_lost'] = gang.get('fights_lost', 0) + 1
            mark_gang_dead(code)
            result_embed = discord.Embed(
                title="Lost the Beef — Crew Disbanded",
                description=f"**{gang['name']}** got wiped out by **{enemy['name']}** and his crew. Nothing left.",
                color=discord.Color.dark_red()
            )
            result_embed.add_field(name="Opp Cred", value=str(enemy_rep), inline=True)
            result_embed.add_field(name="Your Cred", value=str(player_rep), inline=True)
            result_embed.add_field(name="Final Bodies", value=str(gang.get('kills', 0)), inline=True)
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
            result_embed.add_field(name="Opp Cred", value=str(enemy_rep), inline=True)
            result_embed.add_field(name="Cred Lost", value=f"-{player_rep - new_rep}", inline=True)
            result_embed.add_field(name="New Street Cred", value=f"{player_rep} → **{new_rep}**", inline=False)
            result_embed.set_footer(text="Regroup and come back.")

    if result_embed:
        await message.channel.send(embed=result_embed)
    else:
        await message.channel.send("Something went wrong with the beef. Try again.")


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
