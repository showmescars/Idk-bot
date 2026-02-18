import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
import os
import asyncio
import time

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
            "kills": 0,
            "deaths": 0,
            "jail_until": None,
            "jail_sentence": None,
        })
    return members


def get_alive_members(gang):
    return [m for m in gang.get('members', []) if m['alive']]


def get_free_members(gang):
    now = time.time()
    return [
        m for m in gang.get('members', [])
        if m['alive'] and (m.get('jail_until') is None or now >= m['jail_until'])
    ]


def get_gang_bodies(gang):
    return sum(m.get('kills', 0) for m in gang.get('members', []))


def get_gang_deaths(gang):
    return sum(m.get('deaths', 0) for m in gang.get('members', []))


def check_and_mark_dead(code):
    gang = gangs[code]
    if len(get_alive_members(gang)) == 0:
        gang['alive'] = False
        owner_id = gang['owner_id']
        if not user_has_active_gang(owner_id):
            active_gang_owners.discard(owner_id)


def send_to_jail(member):
    tier = random.choices(SENTENCE_TIERS, weights=SENTENCE_WEIGHTS, k=1)[0]
    member['jail_until'] = time.time() + (tier['minutes'] * 60)
    member['jail_sentence'] = tier['label']
    return tier['label']


def get_member_status(m):
    if not m['alive']:
        return "Dead"
    now = time.time()
    if m.get('jail_until') and now < m['jail_until']:
        return f"Locked Up ({m['jail_sentence']})"
    return "Free"


def format_member_list(members):
    if not members:
        return "None left"
    lines = []
    for m in members:
        status = get_member_status(m)
        kills = m.get('kills', 0)
        lines.append(f"{m['name']}  —  {kills} kills  |  {status}")
    return "\n".join(lines)


def calculate_beef_outcome(gang, rolling_members, enemy_rep):
    player_rep = gang['rep']
    rep_diff = player_rep - enemy_rep
    win_chance = 50 + int((rep_diff / 500) * 40)
    win_chance = max(10, min(90, win_chance))
    player_won = random.randint(1, 100) <= win_chance

    outcome_lines = []

    if player_won:
        rep_gain = random.randint(20, int(max(1, enemy_rep * 0.4)))
        gang['rep'] = player_rep + rep_gain
        gang['fights_won'] = gang.get('fights_won', 0) + 1

        win_kill_lines = [
            "{member} pulled out first and aired it out — they never even got a shot off.",
            "{member} rushed their whole line solo and sent three of them running with their tails tucked.",
            "{member} caught the lead opp slipping at the light and handled business on the spot.",
            "{member} crept up from the cut and laid two of them down before they even knew what hit them.",
            "{member} emptied the whole clip and walked back to the car without looking back.",
            "{member} ran down on their block mid-day and didn't care who was watching.",
            "{member} cornered their shot caller in the alley and made sure that message got delivered.",
            "{member} rolled up with no mask, no hesitation — caught bodies and disappeared into the night.",
        ]

        for m in rolling_members:
            m['kills'] = m.get('kills', 0) + 1
            line = random.choice(win_kill_lines).replace("{member}", m['name'])
            outcome_lines.append(line)

        if len(get_alive_members(gang)) > 1 and random.randint(1, 100) <= 20:
            still_alive = [m for m in rolling_members if m['alive']]
            if still_alive:
                casualty = random.choice(still_alive)
                casualty['alive'] = False
                casualty['deaths'] = casualty.get('deaths', 0) + 1
                friendly_fire_lines = [
                    f"{casualty['name']} caught a stray on the way out — didn't make it back to the car.",
                    f"{casualty['name']} took one in the chest during the exchange. They didn't survive the night.",
                    f"{casualty['name']} was the last one out and the opps got a shot off — it was fatal.",
                    f"{casualty['name']} went down in the crossfire. Won the beef but paid the price.",
                    f"{casualty['name']} got clipped right as the crew was pulling out. Gone before sunrise.",
                ]
                outcome_lines.append(random.choice(friendly_fire_lines))

        if random.randint(1, 100) <= 15:
            now = time.time()
            still_free = [m for m in rolling_members if m['alive'] and (m.get('jail_until') is None or now >= m['jail_until'])]
            if still_free:
                jailed = random.choice(still_free)
                sentence = send_to_jail(jailed)
                jail_lines = [
                    f"{jailed['name']} thought they were clean but the boys had eyes on the whole block — picked up leaving the scene. {sentence} sentence.",
                    f"{jailed['name']} got pulled over two blocks away with the strap still on them. DA didn't play — {sentence}.",
                    f"Someone on the block talked. {jailed['name']} got snatched up the next morning. Facing {sentence}.",
                    f"Cameras caught {jailed['name']}'s face clear as day. Task force was at the door by morning. {sentence} sentence.",
                    f"{jailed['name']} went back to celebrate and got bagged at the trap. {sentence} — no bail.",
                ]
                outcome_lines.append(random.choice(jail_lines))

        return {
            "won": True,
            "rep_gain": rep_gain,
            "old_rep": player_rep,
            "new_rep": gang['rep'],
            "enemy_rep": enemy_rep,
            "outcome_lines": outcome_lines,
            "total_bodies": get_gang_bodies(gang),
            "total_deaths": get_gang_deaths(gang),
            "members_alive": len(get_alive_members(gang)),
        }

    else:
        gang['fights_lost'] = gang.get('fights_lost', 0) + 1

        for m in rolling_members:
            if len(get_alive_members(gang)) > 1 and random.randint(1, 100) <= 40:
                m['alive'] = False
                m['deaths'] = m.get('deaths', 0) + 1
                death_lines = [
                    f"{m['name']} took the first shot and didn't get back up. Left on the pavement.",
                    f"{m['name']} tried to hold the line but the opps were too deep — got dropped right there.",
                    f"{m['name']} ran into the cut but it was a dead end. They found the body an hour later.",
                    f"{m['name']} caught three in the back trying to make it to the car. Didn't survive.",
                    f"{m['name']} stood their ground but the numbers weren't there — went out swinging.",
                    f"{m['name']} got hit running across the street. Pronounced dead at the scene.",
                ]
                outcome_lines.append(random.choice(death_lines))
            else:
                if random.randint(1, 100) <= 30 and m['alive']:
                    sentence = send_to_jail(m)
                    escape_jail_lines = [
                        f"{m['name']} made it out but caught a case on the way — task force had the block locked. {sentence}.",
                        f"{m['name']} escaped the shootout but got pulled over two exits down. They found everything. {sentence} sentence.",
                        f"{m['name']} hopped a fence but landed right in front of a patrol car. {sentence} — no getting out of this one.",
                        f"{m['name']} survived the beef but a witness called it in. Picked up at home the next day. Facing {sentence}.",
                    ]
                    outcome_lines.append(random.choice(escape_jail_lines))
                else:
                    escape_lines = [
                        f"{m['name']} took a graze to the arm but kept moving — made it back to the hood barely breathing.",
                        f"{m['name']} dove behind a parked car and crawled out when it went quiet. Lucky to be alive.",
                        f"{m['name']} got hit but the vest caught most of it — bruised up bad but still standing.",
                        f"{m['name']} ducked through a backyard and lost them in the dark. Made it home at 3am.",
                        f"{m['name']} got clipped in the leg but dragged themselves to the car and pulled out.",
                        f"{m['name']} took a hit to the shoulder but walked it off. Streets know they survived though.",
                    ]
                    outcome_lines.append(random.choice(escape_lines))

        rep_loss = random.randint(20, int(max(1, player_rep * 0.25)))
        gang['rep'] = max(1, player_rep - rep_loss)

        return {
            "won": False,
            "rep_loss": player_rep - gang['rep'],
            "old_rep": player_rep,
            "new_rep": gang['rep'],
            "enemy_rep": enemy_rep,
            "outcome_lines": outcome_lines,
            "total_bodies": get_gang_bodies(gang),
            "total_deaths": get_gang_deaths(gang),
            "members_alive": len(get_alive_members(gang)),
        }


def build_result_embed(gang, enemy_gang_info, result):
    outcome_text = "\n".join(result['outcome_lines']) if result['outcome_lines'] else ("Cleaned up the block without a scratch." if result['won'] else "Barely made it back with their lives.")

    if result['won']:
        win_descriptions = [
            f"**{gang['name']}** ran **{enemy_gang_info['name']}** off the block and claimed everything they had. The hood knows who runs it now.",
            f"**{gang['name']}** pulled up on **{enemy_gang_info['name']}** and left no doubt — that block belongs to them now. Word spread before the sun came up.",
            f"**{enemy_gang_info['name']}** thought they could hold their ground but **{gang['name']}** came through and showed them different. The streets are talking.",
            f"**{gang['name']}** caught **{enemy_gang_info['name']}** lacking and made them pay for every act of disrespect. Flags flying high tonight.",
            f"It wasn't even close. **{gang['name']}** dismantled **{enemy_gang_info['name']}** piece by piece and walked away with their reputation sky high.",
        ]
        embed = discord.Embed(
            title="🏆 Beef Won — Block Secured",
            description=random.choice(win_descriptions),
            color=discord.Color.green()
        )
        embed.add_field(name="What Went Down", value=outcome_text, inline=False)
        embed.add_field(name="Opp Cred", value=str(result['enemy_rep']), inline=True)
        embed.add_field(name="Cred Gained", value=f"+{result['rep_gain']}", inline=True)
        embed.add_field(name="New Street Cred", value=f"{result['old_rep']} → **{result['new_rep']}**", inline=True)
        embed.add_field(name="Gang Kills", value=str(result['total_bodies']), inline=True)
        embed.add_field(name="Gang Deaths", value=str(result['total_deaths']), inline=True)
        embed.add_field(name="Members Alive", value=str(result['members_alive']), inline=True)
        embed.set_footer(text="Hold that block. Don't let nobody take what's yours.")
    else:
        loss_descriptions = [
            f"**{gang['name']}** got run off by **{enemy_gang_info['name']}** tonight. Took heavy losses but the set is still breathing.",
            f"**{enemy_gang_info['name']}** came ready and **{gang['name']}** wasn't prepared for what they brought. Lived to fight another day — barely.",
            f"**{gang['name']}** underestimated **{enemy_gang_info['name']}** and paid the price. The block is lost for now but the war ain't over.",
            f"It was a bad night for **{gang['name']}**. **{enemy_gang_info['name']}** outgunned them and made sure the whole hood knew it.",
            f"**{gang['name']}** walked into something they weren't ready for. **{enemy_gang_info['name']}** sent them back to their side with a clear message.",
        ]
        embed = discord.Embed(
            title="💀 Beef Lost — Took an L",
            description=random.choice(loss_descriptions),
            color=discord.Color.orange()
        )
        embed.add_field(name="What Went Down", value=outcome_text, inline=False)
        embed.add_field(name="Opp Cred", value=str(result['enemy_rep']), inline=True)
        embed.add_field(name="Cred Lost", value=f"-{result['rep_loss']}", inline=True)
        embed.add_field(name="New Street Cred", value=f"{result['old_rep']} → **{result['new_rep']}**", inline=True)
        embed.add_field(name="Gang Kills", value=str(result['total_bodies']), inline=True)
        embed.add_field(name="Gang Deaths", value=str(result['total_deaths']), inline=True)
        embed.add_field(name="Members Alive", value=str(result['members_alive']), inline=True)
        embed.set_footer(text="Regroup. Get your head right. Come back harder.")

    return embed


EVENTS = [
    {
        "name": "Corner Locked Down",
        "description": "{member} spent the whole night putting in work on Figueroa, muscling every last corner boy off the strip until nobody dared step foot on it. By morning, **{name}** owned every inch of that block and the whole neighborhood knew it.",
        "type": "rep_up", "value": (20, 80), "color": discord.Color.green()
    },
    {
        "name": "Successful Lick",
        "description": "{member} moved quiet and precise — scoped the target for two days, waited for the perfect moment, and walked away clean with enough to keep **{name}** comfortable for months. Nobody saw a thing. Nobody said a thing.",
        "type": "rep_up", "value": (30, 100), "color": discord.Color.green()
    },
    {
        "name": "Street Fight Victory",
        "description": "{member} ran into four of the opps outside the liquor store on Central and didn't hesitate for a second. Squared up solo, dropped two of them, and walked away without a scratch. **{name}**'s name rang out before the night was over.",
        "type": "rep_up", "value": (20, 60), "color": discord.Color.green()
    },
    {
        "name": "Territory Claimed",
        "description": "**{name}** moved on a new block that the opps had been sitting on for months. {member} led the crew in, posted up in broad daylight, and dared anyone to say something. Nobody did. That block is **{name}**'s now.",
        "type": "rep_up", "value": (40, 120), "color": discord.Color.green()
    },
    {
        "name": "OG Vouched",
        "description": "One of the most respected OGs in the city pulled {member} aside after church and told him straight — he'd been watching **{name}** and they were doing it right. He made a few calls that same night. Doors opened that nobody even knew existed.",
        "type": "rep_up", "value": (50, 150), "color": discord.Color.green()
    },
    {
        "name": "Retaliation Hit",
        "description": "The opps disrespected **{name}** at a vigil last week. {member} didn't forget. Waited a full week so nobody would expect it, then showed up at exactly the right time and delivered the message personally. The streets went quiet after that.",
        "type": "rep_up", "value": (60, 180), "color": discord.Color.green()
    },
    {
        "name": "Prison Connects Made",
        "description": "{member} got word inside through a cousin doing a stretch at Corcoran. Made the right introductions, passed the right messages, and now **{name}** has connects in three different facilities. Business don't stop just because somebody's locked up.",
        "type": "rep_up", "value": (40, 100), "color": discord.Color.green()
    },
    {
        "name": "Rival Scattered",
        "description": "{member} pulled up on the opposition's main corner with the whole crew and gave them one warning. They didn't take it seriously. **{name}** hit back so hard and so fast that within 48 hours the opps had abandoned three blocks without a single shot being fired.",
        "type": "rep_up", "value": (80, 200), "color": discord.Color.green()
    },
    {
        "name": "Hood Documentary",
        "description": "A filmmaker from outside the city came through to document real street life and {member} let them follow for a week. The footage went viral — raw and uncut. Now everyone knows {member}'s face and **{name}**'s name. Respect flowing in from all directions.",
        "type": "rep_up", "value": (30, 90), "color": discord.Color.green()
    },
    {
        "name": "Rapper Shoutout",
        "description": "A certified street rapper dropped a project and buried {member}'s name in two different tracks — name, hood, and **{name}** repped fully. The comment sections went crazy. People from three cities were asking about the set by the next morning.",
        "type": "rep_up", "value": (50, 130), "color": discord.Color.green()
    },
    {
        "name": "Fed the Block",
        "description": "{member} pulled out of pocket and threw a full cookout on the block — ribs, cases of water, music, the whole thing. Families came out, elders dapped up the crew, and kids who never talked to **{name}** before were showing love. Community locked in solid.",
        "type": "rep_up", "value": (25, 70), "color": discord.Color.green()
    },
    {
        "name": "Big Score",
        "description": "{member} linked up with a connect that came through a third party and set up the biggest score **{name}** had seen in years. Everything went smooth — product moved fast, money came back clean, and every member of the crew ate well for the first time in a long time.",
        "type": "rep_up", "value": (60, 160), "color": discord.Color.green()
    },
    {
        "name": "Took the Block Back",
        "description": "The opps had been sitting on a block that used to belong to **{name}** for six months. {member} organized the whole thing — right time, right numbers, right message. They moved at 2am and by sunrise that block was flying **{name}**'s colors again like it never stopped.",
        "type": "rep_up", "value": (70, 170), "color": discord.Color.green()
    },
    {
        "name": "Put in Work",
        "description": "There was a name on a list that needed to be handled. {member} didn't ask questions, didn't ask for extra. Just said when and where and got it done quietly, cleanly, with no trail left behind. **{name}** moves different because of soldiers like that.",
        "type": "rep_up", "value": (80, 200), "color": discord.Color.green()
    },
    {
        "name": "Snitch in the Ranks",
        "description": "The feds had been watching **{name}** for weeks and nobody could figure out how they knew so much. Then a sealed document leaked through a lawyer's office — {member}'s name was on it. Cooperating since the summer. The set is fractured. Trust is gone. Rep is in the dirt.",
        "type": "rep_down", "value": (30, 100), "color": discord.Color.orange()
    },
    {
        "name": "Botched Mission",
        "description": "{member} had one job — get in, handle it, get out. Instead they froze at the wrong moment, dropped something they shouldn't have, and had to abort. Three people on the block filmed the whole thing from their porch. **{name}** is a punchline on the streets right now.",
        "type": "rep_down", "value": (20, 80), "color": discord.Color.orange()
    },
    {
        "name": "Homie Got Knocked",
        "description": "Task force rolled up on {member} while they were sitting outside with product on them and a warrant already signed. Bail was denied at the hearing. **{name}** lost one of their most solid members overnight and the whole operation slowed down to a crawl.",
        "type": "rep_down", "value": (40, 120), "color": discord.Color.orange()
    },
    {
        "name": "Ran Off the Block",
        "description": "The opps pulled up three cars deep right at shift change when **{name}** only had two people on the corner. {member} tried to hold it but the math wasn't there. Had to fall back and watch them take over the block. Whole hood saw it happen in real time.",
        "type": "rep_down", "value": (50, 150), "color": discord.Color.orange()
    },
    {
        "name": "Internal Beef",
        "description": "{member} and another member of **{name}** got into a bad argument over money that turned physical right outside the trap house. Neighbors recorded it. Other sets are sharing the video and laughing. Nothing breaks a crew's reputation faster than airing out internal problems in public.",
        "type": "rep_down", "value": (25, 75), "color": discord.Color.orange()
    },
    {
        "name": "LAPD Raid",
        "description": "Forty officers hit **{name}**'s main spot at 5am with a no-knock warrant and body cams rolling. {member} and two others barely got out the back before the doors came down. Everything inside got seized — product, cash, phones, weapons. The whole operation is on pause.",
        "type": "rep_down", "value": (60, 180), "color": discord.Color.orange()
    },
    {
        "name": "Caught Lacking",
        "description": "The opps caught {member} alone at a gas station on the wrong side of town, repping **{name}** loud with nowhere to run. Took everything off them, recorded the whole thing, and posted it online before {member} even made it back to the hood. The comments are brutal.",
        "type": "rep_down", "value": (30, 90), "color": discord.Color.orange()
    },
    {
        "name": "Lost the Package",
        "description": "{member} was moving a major package cross-town and made a wrong decision that cost everything. Whether it got taken by the opps or seized at a checkpoint, the result was the same — **{name}** lost the product, lost the money, and the connect is threatening to cut them off.",
        "type": "rep_down", "value": (45, 130), "color": discord.Color.orange()
    },
    {
        "name": "Homie Flipped",
        "description": "{member} had been facing a fifteen-year bid and nobody knew they had been cooperating for months. The DA announced the indictments on a Tuesday morning. **{name}** lost four members to federal charges in one day. {member} is in witness protection. The betrayal runs deep.",
        "type": "rep_down", "value": (50, 160), "color": discord.Color.orange()
    },
    {
        "name": "Jumped by Opps",
        "description": "Eight of the opposition cornered {member} two blocks from home in the middle of the afternoon with witnesses everywhere. Beat them down for a full minute while people recorded on their phones. **{name}**'s name is attached to that video and the streets are not letting it go.",
        "type": "rep_down", "value": (35, 110), "color": discord.Color.orange()
    },
    {
        "name": "Fronted and Folded",
        "description": "{member} got on social media and called out a rival set by name — specific threats, specific locations, specific times. The whole city was watching. When the moment came, {member} was nowhere to be found. **{name}** hasn't heard the end of it. Empty threats cost more than silence.",
        "type": "rep_down", "value": (40, 100), "color": discord.Color.orange()
    },
    {
        "name": "Quiet Night",
        "description": "{member} held down the corner all night from sundown to sunrise — stayed alert, watched the block, kept things moving. But there was nothing to report. No moves, no incidents, no problems. Sometimes the streets just go still. **{name}** is positioned and ready, just waiting for the moment.",
        "type": "nothing", "color": discord.Color.greyple()
    },
    {
        "name": "Laying Low",
        "description": "There's been too much heat in the area lately — patrol cars circling every hour, a couple of unfamiliar faces asking questions, and word that the task force has been running plates. {member} made the call to keep **{name}** off the corners for the night. Smart move. Live to eat another day.",
        "type": "nothing", "color": discord.Color.greyple()
    },
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
            free_members = get_free_members(g)
            total_bodies = get_gang_bodies(g)
            total_deaths = get_gang_deaths(g)
            member_block = format_member_list(g['members'])

            embed.add_field(
                name=f"{g['name']}",
                value=(
                    f"Hood: {g.get('hood', 'Unknown')}\n"
                    f"Code: `{g['code']}`\n"
                    f"Shot Caller: {g.get('leader', 'Unknown')}\n"
                    f"Street Cred: {g['rep']}\n"
                    f"Record: {fights_won}W - {fights_lost}L   |   Win Rate: {win_rate}\n"
                    f"Gang Kills: {total_bodies}   |   Gang Deaths: {total_deaths}\n"
                    f"Members Alive: {len(alive_members)}   |   Members Free: {len(free_members)}"
                ),
                inline=False
            )
            embed.add_field(name="Roster", value=member_block, inline=False)
            embed.add_field(name="\u200b", value="\u200b", inline=False)
    else:
        embed.add_field(name="No Active Crew", value="Your crew got disbanded. Type `gang` to start fresh.", inline=False)

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

    free_members = get_free_members(gang)
    if not free_members:
        await message.channel.send(f"**{gang['name']}** has no free members right now. Everyone is locked up or dead.")
        return

    featured_member = random.choice(free_members)
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
        if random.randint(1, 100) <= 20:
            featured_member['kills'] = featured_member.get('kills', 0) + 1
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="Member", value=f"{featured_member['name']} (+1 kill)", inline=True)
        else:
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="Member", value=featured_member['name'], inline=True)
        embed.add_field(name="Street Cred", value=f"{rep} → **{new_rep}** (+{gain})", inline=True)
        embed.set_footer(text="Rep rising on the streets...")

    elif event['type'] == 'rep_down':
        loss = random.randint(*event['value'])
        new_rep = max(1, rep - loss)
        actual_loss = rep - new_rep
        gang['rep'] = new_rep
        extra_info = []
        if random.randint(1, 100) <= 15 and len(get_alive_members(gang)) > 1:
            featured_member['alive'] = False
            featured_member['deaths'] = featured_member.get('deaths', 0) + 1
            extra_info.append(f"{featured_member['name']} didn't make it out — body found two blocks away")
        elif random.randint(1, 100) <= 25:
            sentence = send_to_jail(featured_member)
            extra_info.append(f"{featured_member['name']} got knocked and is facing {sentence}")
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        if extra_info:
            embed.add_field(name="What Happened", value="\n".join(extra_info), inline=True)
        embed.add_field(name="Street Cred", value=f"{rep} → **{new_rep}** (-{actual_loss})", inline=True)
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
        await message.channel.send(f"**{gang['name']}** roster is already full.")
        return

    success = random.randint(1, 2) == 1

    if success:
        new_name = random.choice(available)
        gang['members'].append({
            "name": new_name,
            "rep": random.randint(10, 150),
            "alive": True,
            "kills": 0,
            "deaths": 0,
            "jail_until": None,
            "jail_sentence": None,
        })
        recruit_descriptions = [
            f"**{new_name}** had been hanging around the block for weeks watching how **{gang['name']}** moved. Finally pulled them aside, looked them in the eye, and put them on. They didn't hesitate.",
            f"Word got to **{new_name}** through a mutual that **{gang['name']}** was looking. They showed up the next day ready to work. No questions, no hesitation — just loyalty.",
            f"**{new_name}** proved themselves during a situation last month that nobody forgot. After that, the decision to put them on with **{gang['name']}** was unanimous.",
            f"**{new_name}** grew up two blocks over and always had love for **{gang['name']}**. When the invitation finally came, they were ready — had been ready for a long time.",
        ]
        embed = discord.Embed(
            title="New Member",
            description=random.choice(recruit_descriptions),
            color=discord.Color.teal()
        )
        embed.add_field(name="Gang", value=gang['name'], inline=True)
        embed.add_field(name="New Member", value=new_name, inline=True)
        embed.add_field(name="Total Members", value=str(len(get_alive_members(gang))), inline=True)
        embed.set_footer(text="Keep building the set.")
    else:
        no_show_descriptions = [
            f"**{gang['name']}** put the word out through three different people but nobody came through. Either the timing is wrong or the streets aren't feeling it right now. Try again.",
            f"There was a candidate — seemed solid, seemed interested. Then they just stopped answering. **{gang['name']}** can't afford dead weight anyway. Try again.",
            f"The recruitment process hit a wall. People are either already committed elsewhere or they're too scared to make the move. The set needs to keep pushing.",
            f"Word didn't travel the way it needed to. **{gang['name']}** is out there but not everyone is ready to step up. The right one is out there somewhere.",
        ]
        embed = discord.Embed(
            title="Nobody Came Through",
            description=random.choice(no_show_descriptions),
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

    free_members = get_free_members(gang)
    if not free_members:
        await message.channel.send(f"**{gang['name']}** has nobody free to roll out right now.")
        return

    max_rollers = min(3, len(free_members))
    roll_count = random.randint(1, max_rollers)
    rolling_members = random.sample(free_members, roll_count)

    enemy_gang_info = random.choice(LA_GANGS)
    enemy_members = generate_ai_members(random.randint(1, 3))
    enemy_rep = random.randint(10, 500)
    player_rep = gang['rep']

    rolling_names = "\n".join([m['name'] for m in rolling_members])
    enemy_names = "\n".join([m['name'] for m in enemy_members])

    beef_intros = [
        f"**{gang['name']}** got word that **{enemy_gang_info['name']}** has been running their mouth. Time to pull up and make it clear.",
        f"**{enemy_gang_info['name']}** crossed a line they can't uncross. **{gang['name']}** is loading up and heading out.",
        f"The disrespect from **{enemy_gang_info['name']}** has been building for weeks. Tonight **{gang['name']}** settles it.",
        f"**{gang['name']}** got intel on where **{enemy_gang_info['name']}** is posted. The crew is rolling out right now.",
    ]

    intro_embed = discord.Embed(
        title="🔴 Beef",
        description=random.choice(beef_intros),
        color=discord.Color.dark_red()
    )
    intro_embed.add_field(name=gang['name'], value=f"Street Cred: {player_rep}\n\n{rolling_names}", inline=True)
    intro_embed.add_field(name="VS", value="\u200b", inline=True)
    intro_embed.add_field(name=enemy_gang_info['name'], value=f"Street Cred: {enemy_rep}\n\n{enemy_names}", inline=True)
    intro_embed.set_footer(text="It's on...")
    await message.channel.send(embed=intro_embed)

    result = calculate_beef_outcome(gang, rolling_members, enemy_rep)
    check_and_mark_dead(code)
    result_embed = build_result_embed(gang, enemy_gang_info, result)

    await asyncio.sleep(3)
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
