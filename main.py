import discord
from discord.ext import commands, tasks
import json
import os
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

VAMPIRES_FILE = 'vampires.json'
BATTLES_FILE = 'battle_logs.json'
CREDITS_FILE = 'credits.json'
WHITELIST_FILE = 'whitelist.json'

BLOCKED_CHANNEL_ID = None

STARTING_CREDITS = 30
GEN_COST = 10

VAMPIRE_FIRST_NAMES = [
    "Dracula", "Vlad", "Lestat", "Armand", "Louis", "Akasha", "Marius", "Kain",
    "Alucard", "Selene", "Blade", "Viktor", "Marcus", "Amelia", "Sonja", "Lucian",
    "Nosferatu", "Carmilla", "Erzsebet", "Lilith", "Cain", "Abel", "Seras", "Integra",
    "D", "Rayne", "Astaroth", "Malachi", "Corvinus", "Demetrius", "Theron", "Sanctus",
    "Nyx", "Raven", "Eclipse", "Crimson", "Shadow", "Obsidian", "Scarlet", "Vesper"
]

VAMPIRE_LAST_NAMES = [
    "Tepes", "Drăculești", "de Lioncourt", "Romanus", "de Pointe du Lac", "Blackwood",
    "Nightshade", "Bloodmoon", "Darkholme", "von Carstein", "Ravenscroft", "Thornheart",
    "Ashborne", "Grimveil", "Shadowfang", "Crimsonbane", "Duskwalker", "Bloodworth",
    "Blackthorn", "Nightingale", "Darkmore", "Bloodstone", "Shadowmere", "Ravenclaw",
    "Grimshaw", "Nightfall", "Duskwood", "Ashwood", "Ironblood", "Stormveil"
]

VAMPIRE_CLANS = [
    "Nosferatu", "Ventrue", "Tremere", "Toreador", "Brujah", "Malkavian",
    "Gangrel", "Tzimisce", "Lasombra", "Setite", "Giovanni", "Ravnos",
    "Assamite", "Salubri", "Cappadocian", "Blood Moon", "Shadow Council",
    "Crimson Court", "Night Legion", "Dark Covenant"
]

ABILITIES = [
    "Blood Rage", "Shadow Step", "Hypnotic Gaze", "Regeneration", "Night Vision",
    "Blood Shield", "Celerity", "Domination", "Auspex", "Obfuscate",
    "Potence", "Protean", "Thaumaturgy", "Necromancy", "Dementation",
    "Animalism", "Fortitude", "Presence", "Quietus", "Vicissitude"
]

def load_vampires():
    if os.path.exists(VAMPIRES_FILE):
        with open(VAMPIRES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_vampires(vampires):
    with open(VAMPIRES_FILE, 'w') as f:
        json.dump(vampires, f, indent=4)

def load_battles():
    if os.path.exists(BATTLES_FILE):
        with open(BATTLES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_battles(battles):
    with open(BATTLES_FILE, 'w') as f:
        json.dump(battles, f, indent=4)

def load_credits():
    if os.path.exists(CREDITS_FILE):
        with open(CREDITS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_credits(credits):
    with open(CREDITS_FILE, 'w') as f:
        json.dump(credits, f, indent=4)

def load_whitelist():
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, 'r') as f:
            return json.load(f)
    return []

def save_whitelist(whitelist):
    with open(WHITELIST_FILE, 'w') as f:
        json.dump(whitelist, f, indent=4)

vampires = load_vampires()
battles = load_battles()
credits = load_credits()
whitelist = load_whitelist()

def generate_vampire_stats():
    return {
        "strength": random.randint(50, 100),
        "speed": random.randint(50, 100),
        "intelligence": random.randint(50, 100),
        "blood_power": random.randint(50, 100),
        "defense": random.randint(50, 100)
    }

def calculate_power(stats):
    return sum(stats.values())

def create_vampire(owner_id, owner_name):
    first_name = random.choice(VAMPIRE_FIRST_NAMES)
    last_name = random.choice(VAMPIRE_LAST_NAMES)
    clan = random.choice(VAMPIRE_CLANS)
    abilities = random.sample(ABILITIES, k=3)
    stats = generate_vampire_stats()
    
    vampire = {
        "id": f"vamp_{owner_id}_{datetime.now().timestamp()}",
        "name": f"{first_name} {last_name}",
        "clan": clan,
        "abilities": abilities,
        "stats": stats,
        "power": calculate_power(stats),
        "owner_id": owner_id,
        "owner_name": owner_name,
        "wins": 0,
        "losses": 0,
        "kills": 0,
        "created_at": datetime.now().isoformat(),
        "alive": True
    }
    
    return vampire

def simulate_battle(vampire1, vampire2):
    v1_combat = (
        vampire1['stats']['strength'] * 0.3 +
        vampire1['stats']['speed'] * 0.2 +
        vampire1['stats']['blood_power'] * 0.3 +
        vampire1['stats']['defense'] * 0.2
    ) * random.uniform(0.8, 1.2)
    
    v2_combat = (
        vampire2['stats']['strength'] * 0.3 +
        vampire2['stats']['speed'] * 0.2 +
        vampire2['stats']['blood_power'] * 0.3 +
        vampire2['stats']['defense'] * 0.2
    ) * random.uniform(0.8, 1.2)
    
    if v1_combat > v2_combat:
        winner = vampire1
        loser = vampire2
        margin = v1_combat - v2_combat
    else:
        winner = vampire2
        loser = vampire1
        margin = v2_combat - v1_combat
    
    ability1 = random.choice(vampire1['abilities'])
    ability2 = random.choice(vampire2['abilities'])
    
    narratives = [
        f"{winner['name']} unleashed {random.choice(winner['abilities'])} and overwhelmed {loser['name']}!",
        f"After a fierce exchange, {winner['name']} dominated {loser['name']} with superior {random.choice(['strength', 'speed', 'cunning'])}!",
        f"{loser['name']} fought valiantly with {ability2}, but {winner['name']}'s {ability1} proved too powerful!",
        f"The blood moon witnessed {winner['name']} of clan {winner['clan']} defeat {loser['name']}!",
        f"In a devastating display of power, {winner['name']} crushed {loser['name']} in combat!"
    ]
    
    return {
        "winner": winner,
        "loser": loser,
        "margin": margin,
        "narrative": random.choice(narratives),
        "critical": margin > 50
    }

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Vampire Battle Bot Ready')
    auto_battle.start()

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True

@bot.command(name='i')
async def info_command(ctx):
    is_admin = ctx.author.guild_permissions.administrator

    if is_admin:
        info_text = """VAMPIRE BATTLE BOT - ALL COMMANDS

USER COMMANDS:
!gv - Generate a vampire (costs 10 credits, whitelist required)
!mv - View all your vampires
!v <vampire_id> - View details of a specific vampire
!lb - View leaderboard (top vampires by wins)
!c - Check your credit balance
!i - Display this command list

ADMIN COMMANDS:
!gv [amount] - Generate vampires (no credit cost, optional amount)
!ac @user <amount> - Give credits to a user
!rc @user <amount> - Remove credits from a user
!vc - View all users and their credits
!aw @user - Add user to whitelist
!rw @user - Remove user from whitelist
!vw - View all whitelisted users
!bl [limit] - View recent battles
!va - View all vampires in the realm
!fb <vampire1_id> <vampire2_id> - Force a battle between two vampires
!rv <vampire_id> - Revive a dead vampire (admin only)
!kv <vampire_id> - Kill a vampire (admin only)
"""
    else:
        info_text = """VAMPIRE BATTLE BOT - COMMANDS

!gv - Generate a vampire (costs 10 credits, whitelist required)
!mv - View all your vampires
!v <vampire_id> - View details of a specific vampire
!lb - View leaderboard (top vampires by wins)
!c - Check your credit balance
!i - Display this command list

Note: Vampires automatically battle each other every 5 minutes!
Each vampire costs 10 credits. You start with 30 credits.
"""

    await ctx.send(f"```{info_text}```")

@bot.command(name='c')
async def check_credits(ctx):
    user_id = str(ctx.author.id)
    
    if user_id not in credits:
        credits[user_id] = STARTING_CREDITS
        save_credits(credits)
    
    user_credits = credits[user_id]
    await ctx.send(f"You have **{user_credits}** credits")

@bot.command(name='ac')
@commands.has_permissions(administrator=True)
async def add_credits(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("Amount must be greater than 0")
        return
    
    user_id = str(member.id)
    
    if user_id not in credits:
        credits[user_id] = STARTING_CREDITS
    
    credits[user_id] += amount
    save_credits(credits)
    
    await ctx.send(f"Added **{amount}** credits to **{member.name}**\nNew balance: **{credits[user_id]}** credits")

@bot.command(name='rc')
@commands.has_permissions(administrator=True)
async def remove_credits(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("Amount must be greater than 0")
        return
    
    user_id = str(member.id)
    
    if user_id not in credits:
        credits[user_id] = STARTING_CREDITS
    
    credits[user_id] -= amount
    if credits[user_id] < 0:
        credits[user_id] = 0
    
    save_credits(credits)
    
    await ctx.send(f"Removed **{amount}** credits from **{member.name}**\nNew balance: **{credits[user_id]}** credits")

@bot.command(name='vc')
@commands.has_permissions(administrator=True)
async def view_credits(ctx):
    if not credits:
        await ctx.send("No users have credits yet")
        return

    msg = "ALL USER CREDITS:\n\n"
    sorted_credits = sorted(credits.items(), key=lambda x: x[1], reverse=True)
    
    for user_id, user_credits in sorted_credits:
        try:
            user = await bot.fetch_user(int(user_id))
            whitelist_status = " [WHITELISTED]" if user_id in whitelist else ""
            msg += f"{user.name}{whitelist_status} - {user_credits} credits\n"
        except:
            whitelist_status = " [WHITELISTED]" if user_id in whitelist else ""
            msg += f"Unknown User ({user_id}){whitelist_status} - {user_credits} credits\n"

    if len(msg) > 1900:
        await ctx.send("**ALL USER CREDITS:**")
        for i in range(0, len(msg), 1900):
            await ctx.send(f"```{msg[i:i+1900]}```")
    else:
        await ctx.send(f"```{msg}```")

@bot.command(name='aw')
@commands.has_permissions(administrator=True)
async def add_whitelist(ctx, member: discord.Member):
    user_id = str(member.id)

    if user_id in whitelist:
        await ctx.send(f"**{member.name}** is already whitelisted")
        return

    whitelist.append(user_id)
    save_whitelist(whitelist)
    
    if user_id not in credits:
        credits[user_id] = STARTING_CREDITS
        save_credits(credits)
    
    await ctx.send(f"Added **{member.name}** to whitelist with **{STARTING_CREDITS}** starting credits")

@bot.command(name='rw')
@commands.has_permissions(administrator=True)
async def remove_whitelist(ctx, member: discord.Member):
    user_id = str(member.id)

    if user_id not in whitelist:
        await ctx.send(f"**{member.name}** is not whitelisted")
        return

    whitelist.remove(user_id)
    save_whitelist(whitelist)
    await ctx.send(f"Removed **{member.name}** from whitelist")

@bot.command(name='vw')
@commands.has_permissions(administrator=True)
async def view_whitelist(ctx):
    if not whitelist:
        await ctx.send("Whitelist is empty")
        return

    msg = "WHITELISTED USERS:\n\n"
    for user_id in whitelist:
        try:
            user = await bot.fetch_user(int(user_id))
            user_credits = credits.get(user_id, STARTING_CREDITS)
            msg += f"{user.name} - {user_credits} credits\n"
        except:
            user_credits = credits.get(user_id, STARTING_CREDITS)
            msg += f"Unknown User ({user_id}) - {user_credits} credits\n"

    await ctx.send(f"```{msg}```")

@bot.command(name='gv')
async def generate_vampire(ctx, amount: int = 1):
    user_id = str(ctx.author.id)
    is_admin = ctx.author.guild_permissions.administrator

    if not is_admin and user_id not in whitelist:
        await ctx.send("You are not whitelisted to use this command")
        return

    if not is_admin and amount > 1:
        await ctx.send("Only admins can generate multiple vampires at once")
        return

    if amount < 1 or amount > 10:
        await ctx.send("Amount must be between 1 and 10")
        return

    if not is_admin:
        if user_id not in credits:
            credits[user_id] = STARTING_CREDITS
            save_credits(credits)
        
        total_cost = GEN_COST * amount
        
        if credits[user_id] < total_cost:
            await ctx.send(f"Not enough credits! You have **{credits[user_id]}** credits but need **{total_cost}** credits")
            return

    new_vampires = []
    for i in range(amount):
        vampire = create_vampire(user_id, str(ctx.author))
        
        if user_id not in vampires:
            vampires[user_id] = []
        
        vampires[user_id].append(vampire)
        new_vampires.append(vampire)
    
    save_vampires(vampires)

    if not is_admin:
        total_cost = GEN_COST * amount
        credits[user_id] -= total_cost
        save_credits(credits)

    if amount == 1:
        v = new_vampires[0]
        embed = discord.Embed(
            title="🧛 Vampire Created!",
            description=f"**{v['name']}** has risen from the grave!",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Clan", value=v['clan'], inline=True)
        embed.add_field(name="Power", value=v['power'], inline=True)
        embed.add_field(name="ID", value=f"`{v['id']}`", inline=False)
        embed.add_field(name="Abilities", value=", ".join(v['abilities']), inline=False)
        embed.add_field(name="Stats", value=f"STR: {v['stats']['strength']} | SPD: {v['stats']['speed']} | INT: {v['stats']['intelligence']} | BP: {v['stats']['blood_power']} | DEF: {v['stats']['defense']}", inline=False)
        
        if not is_admin:
            embed.set_footer(text=f"Credits remaining: {credits[user_id]}")
        
        await ctx.send(embed=embed)
    else:
        msg = f"**{amount} vampires created!**\n\n"
        for v in new_vampires:
            msg += f"• **{v['name']}** (Clan: {v['clan']}, Power: {v['power']})\n"
        
        if not is_admin:
            msg += f"\nCredits remaining: **{credits[user_id]}**"
        
        await ctx.send(msg)

@bot.command(name='mv')
async def my_vampires(ctx):
    user_id = str(ctx.author.id)
    
    if user_id not in vampires or len(vampires[user_id]) == 0:
        await ctx.send("You don't have any vampires yet! Use `!gv` to create one")
        return
    
    user_vamps = vampires[user_id]
    
    embed = discord.Embed(
        title=f"🧛 {ctx.author.name}'s Vampires",
        description=f"Total: {len(user_vamps)} vampires",
        color=discord.Color.dark_red()
    )
    
    for v in user_vamps:
        status = "💀 DEAD" if not v['alive'] else "✅ ALIVE"
        embed.add_field(
            name=f"{v['name']} {status}",
            value=f"Clan: {v['clan']}\nPower: {v['power']}\nW/L: {v['wins']}/{v['losses']}\nID: `{v['id']}`",
            inline=True
        )
    
    await ctx.send(embed=embed)

@bot.command(name='v')
async def view_vampire(ctx, vampire_id: str):
    found_vampire = None
    for user_id, user_vamps in vampires.items():
        for v in user_vamps:
            if v['id'] == vampire_id:
                found_vampire = v
                break
        if found_vampire:
            break
    
    if not found_vampire:
        await ctx.send("Vampire not found!")
        return
    
    v = found_vampire
    status = "💀 DEAD" if not v['alive'] else "✅ ALIVE"
    
    embed = discord.Embed(
        title=f"🧛 {v['name']} {status}",
        description=f"**Clan:** {v['clan']}",
        color=discord.Color.dark_red() if v['alive'] else discord.Color.dark_gray()
    )
    
    embed.add_field(name="Owner", value=v['owner_name'], inline=True)
    embed.add_field(name="Total Power", value=v['power'], inline=True)
    embed.add_field(name="Record", value=f"{v['wins']}W - {v['losses']}L", inline=True)
    embed.add_field(name="Kills", value=v['kills'], inline=True)
    embed.add_field(name="Created", value=datetime.fromisoformat(v['created_at']).strftime('%Y-%m-%d'), inline=True)
    embed.add_field(name="ID", value=f"`{v['id']}`", inline=True)
    
    embed.add_field(name="Abilities", value=", ".join(v['abilities']), inline=False)
    
    stats_text = f"**Strength:** {v['stats']['strength']}\n**Speed:** {v['stats']['speed']}\n**Intelligence:** {v['stats']['intelligence']}\n**Blood Power:** {v['stats']['blood_power']}\n**Defense:** {v['stats']['defense']}"
    embed.add_field(name="Stats", value=stats_text, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='lb')
async def leaderboard(ctx):
    all_vampires = []
    for user_id, user_vamps in vampires.items():
        all_vampires.extend(user_vamps)
    
    if not all_vampires:
        await ctx.send("No vampires exist yet!")
        return
    
    top_vampires = sorted(all_vampires, key=lambda v: v['wins'], reverse=True)[:10]
    
    embed = discord.Embed(
        title="🏆 Vampire Leaderboard",
        description="Top 10 vampires by wins",
        color=discord.Color.gold()
    )
    
    for idx, v in enumerate(top_vampires, 1):
        status = "💀" if not v['alive'] else "🧛"
        embed.add_field(
            name=f"{idx}. {v['name']} {status}",
            value=f"Wins: {v['wins']} | Power: {v['power']} | Clan: {v['clan']}\nOwner: {v['owner_name']}",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='bl')
@commands.has_permissions(administrator=True)
async def battle_logs(ctx, limit: int = 10):
    if not battles:
        await ctx.send("No battles have occurred yet")
        return
    
    recent = battles[-limit:]
    recent.reverse()
    
    msg = f"**RECENT BATTLES (Last {len(recent)}):**\n\n"
    for b in recent:
        timestamp = datetime.fromisoformat(b['timestamp']).strftime('%Y-%m-%d %H:%M')
        msg += f"`{timestamp}` - {b['narrative']}\n"
    
    await ctx.send(msg)

@bot.command(name='va')
@commands.has_permissions(administrator=True)
async def view_all_vampires(ctx):
    total = 0
    alive = 0
    
    for user_id, user_vamps in vampires.items():
        total += len(user_vamps)
        alive += sum(1 for v in user_vamps if v['alive'])
    
    await ctx.send(f"**Total Vampires:** {total}\n**Alive:** {alive}\n**Dead:** {total - alive}")

@bot.command(name='fb')
@commands.has_permissions(administrator=True)
async def force_battle(ctx, vamp1_id: str, vamp2_id: str):
    v1 = None
    v2 = None
    
    for user_id, user_vamps in vampires.items():
        for v in user_vamps:
            if v['id'] == vamp1_id:
                v1 = v
            if v['id'] == vamp2_id:
                v2 = v
    
    if not v1:
        await ctx.send(f"Vampire 1 ({vamp1_id}) not found!")
        return
    
    if not v2:
        await ctx.send(f"Vampire 2 ({vamp2_id}) not found!")
        return
    
    if not v1['alive']:
        await ctx.send(f"{v1['name']} is dead!")
        return
    
    if not v2['alive']:
        await ctx.send(f"{v2['name']} is dead!")
        return
    
    result = simulate_battle(v1, v2)
    
    result['winner']['wins'] += 1
    result['loser']['losses'] += 1
    
    if random.random() < 0.2:
        result['loser']['alive'] = False
        result['winner']['kills'] += 1
        death_msg = f"\n💀 **{result['loser']['name']} has been slain!**"
    else:
        death_msg = ""
    
    save_vampires(vampires)
    
    battle_log = {
        "winner": result['winner']['name'],
        "loser": result['loser']['name'],
        "narrative": result['narrative'],
        "timestamp": datetime.now().isoformat(),
        "forced": True
    }
    battles.append(battle_log)
    save_battles(battles)
    
    embed = discord.Embed(
        title="⚔️ FORCED BATTLE!",
        description=result['narrative'],
        color=discord.Color.red()
    )
    
    embed.add_field(name="Winner", value=f"{result['winner']['name']} ({result['winner']['owner_name']})", inline=True)
    embed.add_field(name="Loser", value=f"{result['loser']['name']} ({result['loser']['owner_name']})", inline=True)
    
    if death_msg:
        embed.add_field(name="Death!", value=death_msg, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='rv')
@commands.has_permissions(administrator=True)
async def revive_vampire(ctx, vampire_id: str):
    found = False
    for user_id, user_vamps in vampires.items():
        for v in user_vamps:
            if v['id'] == vampire_id:
                if v['alive']:
                    await ctx.send(f"{v['name']} is already alive!")
                    return
                v['alive'] = True
                found = True
                await ctx.send(f"🧛 **{v['name']}** has been revived!")
                break
        if found:
            break
    
    if not found:
        await ctx.send("Vampire not found!")
        return
    
    save_vampires(vampires)

@bot.command(name='kv')
@commands.has_permissions(administrator=True)
async def kill_vampire(ctx, vampire_id: str):
    found = False
    for user_id, user_vamps in vampires.items():
        for v in user_vamps:
            if v['id'] == vampire_id:
                if not v['alive']:
                    await ctx.send(f"{v['name']} is already dead!")
                    return
                v['alive'] = False
                found = True
                await ctx.send(f"💀 **{v['name']}** has been slain!")
                break
        if found:
            break
    
    if not found:
        await ctx.send("Vampire not found!")
        return
    
    save_vampires(vampires)

@tasks.loop(minutes=5)
async def auto_battle():
    alive_vampires = []
    for user_id, user_vamps in vampires.items():
        for v in user_vamps:
            if v['alive']:
                alive_vampires.append(v)
    
    if len(alive_vampires) < 2:
        return
    
    v1, v2 = random.sample(alive_vampires, 2)
    
    result = simulate_battle(v1, v2)
    
    result['winner']['wins'] += 1
    result['loser']['losses'] += 1
    
    death_occurred = False
    if random.random() < 0.2:
        result['loser']['alive'] = False
        result['winner']['kills'] += 1
        death_occurred = True
    
    save_vampires(vampires)
    
    battle_log = {
        "winner": result['winner']['name'],
        "loser": result['loser']['name'],
        "narrative": result['narrative'],
        "timestamp": datetime.now().isoformat(),
        "death": death_occurred
    }
    battles.append(battle_log)
    save_battles(battles)
    
    print(f"Auto-battle: {result['winner']['name']} defeated {result['loser']['name']}")

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found!")
        print("Create a .env file with DISCORD_TOKEN=your_token")
    else:
        print("Token found! Starting Vampire Battle Bot...")
        bot.run(TOKEN)
