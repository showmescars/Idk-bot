import discord
from discord.ext import commands, tasks
import json
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

VAMPIRES_FILE = 'vampires.json'
BATTLES_FILE = 'battle_logs.json'
SETTINGS_FILE = 'settings.json'

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

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

vampires = load_vampires()
battles = load_battles()
settings = load_settings()

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
        "id": f"vamp_{owner_id}_{int(datetime.now().timestamp() * 1000)}",
        "name": f"{first_name} {last_name}",
        "clan": clan,
        "abilities": abilities,
        "stats": stats,
        "power": calculate_power(stats),
        "level": 1,
        "xp": 0,
        "owner_id": owner_id,
        "owner_name": owner_name,
        "wins": 0,
        "losses": 0,
        "kills": 0,
        "created_at": datetime.now().isoformat(),
        "last_trained": None,
        "alive": True
    }
    
    return vampire

def level_up_vampire(vampire):
    vampire['level'] += 1
    
    stat_increases = {
        "strength": random.randint(5, 15),
        "speed": random.randint(5, 15),
        "intelligence": random.randint(5, 15),
        "blood_power": random.randint(5, 15),
        "defense": random.randint(5, 15)
    }
    
    for stat, increase in stat_increases.items():
        vampire['stats'][stat] += increase
    
    vampire['power'] = calculate_power(vampire['stats'])
    vampire['xp'] = 0
    
    return stat_increases

def calculate_xp_needed(level):
    return level * 100

def simulate_battle(vampire1, vampire2):
    v1_combat = (
        vampire1['stats']['strength'] * 0.3 +
        vampire1['stats']['speed'] * 0.2 +
        vampire1['stats']['blood_power'] * 0.3 +
        vampire1['stats']['defense'] * 0.2
    ) * random.uniform(0.8, 1.2) * (1 + (vampire1['level'] * 0.05))
    
    v2_combat = (
        vampire2['stats']['strength'] * 0.3 +
        vampire2['stats']['speed'] * 0.2 +
        vampire2['stats']['blood_power'] * 0.3 +
        vampire2['stats']['defense'] * 0.2
    ) * random.uniform(0.8, 1.2) * (1 + (vampire2['level'] * 0.05))
    
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
    print('Command prefix: ?')
    auto_battle.start()

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True

@bot.check
async def check_allowed_channel(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    
    guild_id = str(ctx.guild.id)
    if guild_id in settings and 'allowed_channel' in settings[guild_id]:
        allowed_channel_id = settings[guild_id]['allowed_channel']
        if ctx.channel.id != allowed_channel_id:
            return False
    
    return True

@bot.command(name='setchannel')
@commands.has_permissions(administrator=True)
async def set_channel(ctx, channel: discord.TextChannel = None):
    """Set the allowed channel for vampire commands"""
    if channel is None:
        channel = ctx.channel
    
    guild_id = str(ctx.guild.id)
    if guild_id not in settings:
        settings[guild_id] = {}
    
    settings[guild_id]['allowed_channel'] = channel.id
    save_settings(settings)
    
    await ctx.send(f"✅ Vampire commands can now only be used in {channel.mention}\n(Admins can still use commands anywhere)")

@bot.command(name='removechannel')
@commands.has_permissions(administrator=True)
async def remove_channel(ctx):
    """Remove channel restriction"""
    guild_id = str(ctx.guild.id)
    if guild_id in settings and 'allowed_channel' in settings[guild_id]:
        del settings[guild_id]['allowed_channel']
        save_settings(settings)
        await ctx.send("✅ Channel restriction removed. Commands can be used anywhere.")
    else:
        await ctx.send("No channel restriction is set.")

@bot.command(name='i')
async def info_command(ctx):
    is_admin = ctx.author.guild_permissions.administrator

    if is_admin:
        info_text = """VAMPIRE BATTLE BOT - ALL COMMANDS

USER COMMANDS:
?gv [amount] - Generate vampires (unlimited, default: 1)
?mv - View all your vampires
?v <vampire_id> - View details of a specific vampire
?fight <your_vamp_id> <target_vamp_id> - Challenge another vampire to battle
?war @user - All your vampires fight all of another player's vampires!
?train <vampire_id> - Train your vampire (once per hour, +10-20 XP)
?feed <vampire_id> - Feed your vampire (+5-15 XP, once per 30 min)
?lb - View leaderboard (top vampires by level & wins)
?delete <vampire_id> - Delete one of your vampires
?i - Display this command list

ADMIN COMMANDS:
?setchannel [#channel] - Set allowed channel for commands
?removechannel - Remove channel restriction
?bl [limit] - View recent battles
?va - View all vampires in the realm
?rv <vampire_id> - Revive a dead vampire
?kv <vampire_id> - Kill a vampire
?givexp <vampire_id> <amount> - Give XP to a vampire
"""
    else:
        info_text = """VAMPIRE BATTLE BOT - COMMANDS

?gv [amount] - Generate vampires (unlimited, default: 1)
?mv - View all your vampires
?v <vampire_id> - View details of a specific vampire
?fight <your_vamp_id> <target_vamp_id> - Challenge another vampire to battle
?war @user - All your vampires fight all of another player's vampires!
?train <vampire_id> - Train your vampire (once per hour, +10-20 XP)
?feed <vampire_id> - Feed your vampire (+5-15 XP, once per 30 min)
?lb - View leaderboard (top vampires by level & wins)
?delete <vampire_id> - Delete one of your vampires
?i - Display this command list

TIP: Level up your vampires by battling, training, and feeding!
XP needed to level up: Level x 100
"""

    await ctx.send(f"```{info_text}```")

@bot.command(name='gv')
async def generate_vampire(ctx, amount: int = 1):
    """Generate vampires (unlimited)"""
    user_id = str(ctx.author.id)

    if amount < 1:
        await ctx.send("Amount must be at least 1")
        return
    
    if amount > 20:
        await ctx.send("Maximum 20 vampires per command")
        return

    new_vampires = []
    for i in range(amount):
        vampire = create_vampire(user_id, str(ctx.author))
        
        if user_id not in vampires:
            vampires[user_id] = []
        
        vampires[user_id].append(vampire)
        new_vampires.append(vampire)
    
    save_vampires(vampires)

    if amount == 1:
        v = new_vampires[0]
        embed = discord.Embed(
            title="🧛 Vampire Created!",
            description=f"**{v['name']}** has risen from the grave!",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Clan", value=v['clan'], inline=True)
        embed.add_field(name="Level", value=v['level'], inline=True)
        embed.add_field(name="Power", value=v['power'], inline=True)
        embed.add_field(name="ID", value=f"`{v['id']}`", inline=False)
        embed.add_field(name="Abilities", value=", ".join(v['abilities']), inline=False)
        embed.add_field(name="Stats", value=f"STR: {v['stats']['strength']} | SPD: {v['stats']['speed']} | INT: {v['stats']['intelligence']} | BP: {v['stats']['blood_power']} | DEF: {v['stats']['defense']}", inline=False)
        
        await ctx.send(embed=embed)
    else:
        msg = f"**{amount} vampires created!**\n\n"
        for v in new_vampires:
            msg += f"• **{v['name']}** (Clan: {v['clan']}, Power: {v['power']}, Level: {v['level']})\n"
        
        await ctx.send(msg)

@bot.command(name='mv')
async def my_vampires(ctx):
    """View all your vampires"""
    user_id = str(ctx.author.id)
    
    if user_id not in vampires or len(vampires[user_id]) == 0:
        await ctx.send("You don't have any vampires yet! Use `?gv` to create one")
        return
    
    user_vamps = vampires[user_id]
    
    embed = discord.Embed(
        title=f"🧛 {ctx.author.name}'s Vampires",
        description=f"Total: {len(user_vamps)} vampires",
        color=discord.Color.dark_red()
    )
    
    for v in user_vamps:
        status = "💀 DEAD" if not v['alive'] else "✅ ALIVE"
        xp_needed = calculate_xp_needed(v['level'])
        embed.add_field(
            name=f"{v['name']} {status}",
            value=f"Clan: {v['clan']}\nLevel: {v['level']} | XP: {v['xp']}/{xp_needed}\nPower: {v['power']} | W/L: {v['wins']}/{v['losses']}\nID: `{v['id']}`",
            inline=True
        )
    
    await ctx.send(embed=embed)

@bot.command(name='v')
async def view_vampire(ctx, vampire_id: str):
    """View details of a specific vampire"""
    
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
    xp_needed = calculate_xp_needed(v['level'])
    
    embed = discord.Embed(
        title=f"🧛 {v['name']} {status}",
        description=f"**Clan:** {v['clan']}",
        color=discord.Color.dark_red() if v['alive'] else discord.Color.dark_gray()
    )
    
    embed.add_field(name="Owner", value=v['owner_name'], inline=True)
    embed.add_field(name="Level", value=v['level'], inline=True)
    embed.add_field(name="XP", value=f"{v['xp']}/{xp_needed}", inline=True)
    embed.add_field(name="Total Power", value=v['power'], inline=True)
    embed.add_field(name="Record", value=f"{v['wins']}W - {v['losses']}L", inline=True)
    embed.add_field(name="Kills", value=v['kills'], inline=True)
    embed.add_field(name="Created", value=datetime.fromisoformat(v['created_at']).strftime('%Y-%m-%d'), inline=True)
    embed.add_field(name="ID", value=f"`{v['id']}`", inline=True)
    
    embed.add_field(name="Abilities", value=", ".join(v['abilities']), inline=False)
    
    stats_text = f"**Strength:** {v['stats']['strength']}\n**Speed:** {v['stats']['speed']}\n**Intelligence:** {v['stats']['intelligence']}\n**Blood Power:** {v['stats']['blood_power']}\n**Defense:** {v['stats']['defense']}"
    embed.add_field(name="Stats", value=stats_text, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='fight')
async def fight_vampire(ctx, your_vamp_id: str, target_vamp_id: str):
    """Challenge another vampire to battle"""
    
    your_vamp = None
    target_vamp = None
    
    for user_id, user_vamps in vampires.items():
        for v in user_vamps:
            if v['id'] == your_vamp_id:
                your_vamp = v
            if v['id'] == target_vamp_id:
                target_vamp = v
    
    if not your_vamp:
        await ctx.send(f"Your vampire ({your_vamp_id}) not found!")
        return
    
    if not target_vamp:
        await ctx.send(f"Target vampire ({target_vamp_id}) not found!")
        return
    
    if your_vamp['owner_id'] != str(ctx.author.id):
        await ctx.send("You don't own that vampire!")
        return
    
    if not your_vamp['alive']:
        await ctx.send(f"{your_vamp['name']} is dead!")
        return
    
    if not target_vamp['alive']:
        await ctx.send(f"{target_vamp['name']} is dead!")
        return
    
    if your_vamp_id == target_vamp_id:
        await ctx.send("A vampire cannot fight itself!")
        return
    
    result = simulate_battle(your_vamp, target_vamp)
    
    result['winner']['wins'] += 1
    result['loser']['losses'] += 1
    
    winner_xp = random.randint(30, 50)
    loser_xp = random.randint(10, 20)
    
    result['winner']['xp'] += winner_xp
    result['loser']['xp'] += loser_xp
    
    winner_leveled = False
    loser_leveled = False
    winner_increases = None
    loser_increases = None
    
    if result['winner']['xp'] >= calculate_xp_needed(result['winner']['level']):
        winner_increases = level_up_vampire(result['winner'])
        winner_leveled = True
    
    if result['loser']['xp'] >= calculate_xp_needed(result['loser']['level']):
        loser_increases = level_up_vampire(result['loser'])
        loser_leveled = True
    
    death_msg = ""
    if random.random() < 0.1:
        result['loser']['alive'] = False
        result['winner']['kills'] += 1
        death_msg = f"\n💀 **{result['loser']['name']} has been slain!**"
    
    save_vampires(vampires)
    
    battle_log = {
        "attacker": your_vamp['name'],
        "defender": target_vamp['name'],
        "winner": result['winner']['name'],
        "loser": result['loser']['name'],
        "narrative": result['narrative'],
        "timestamp": datetime.now().isoformat(),
        "player_initiated": True
    }
    battles.append(battle_log)
    save_battles(battles)
    
    embed = discord.Embed(
        title="⚔️ VAMPIRE BATTLE!",
        description=result['narrative'],
        color=discord.Color.red()
    )
    
    embed.add_field(
        name="Winner", 
        value=f"{result['winner']['name']} (Lvl {result['winner']['level']})\nOwner: {result['winner']['owner_name']}\n+{winner_xp} XP", 
        inline=True
    )
    embed.add_field(
        name="Loser", 
        value=f"{result['loser']['name']} (Lvl {result['loser']['level']})\nOwner: {result['loser']['owner_name']}\n+{loser_xp} XP", 
        inline=True
    )
    
    if winner_leveled:
        embed.add_field(
            name="🎉 LEVEL UP!", 
            value=f"{result['winner']['name']} reached level {result['winner']['level']}!", 
            inline=False
        )
    
    if loser_leveled:
        embed.add_field(
            name="🎉 LEVEL UP!", 
            value=f"{result['loser']['name']} reached level {result['loser']['level']}!", 
            inline=False
        )
    
    if death_msg:
        embed.add_field(name="Death!", value=death_msg, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='war')
async def vampire_war(ctx, opponent: discord.Member):
    """All your vampires fight all of another player's vampires!"""
    
    attacker_id = str(ctx.author.id)
    defender_id = str(opponent.id)
    
    if attacker_id == defender_id:
        await ctx.send("You cannot declare war on yourself!")
        return
    
    # Get all alive vampires for both players
    attacker_vamps = []
    defender_vamps = []
    
    if attacker_id in vampires:
        attacker_vamps = [v for v in vampires[attacker_id] if v['alive']]
    
    if defender_id in vampires:
        defender_vamps = [v for v in vampires[defender_id] if v['alive']]
    
    if not attacker_vamps:
        await ctx.send("You don't have any alive vampires!")
        return
    
    if not defender_vamps:
        await ctx.send(f"{opponent.name} doesn't have any alive vampires!")
        return
    
    # Start the war
    await ctx.send(f"⚔️ **WAR HAS BEGUN!** ⚔️\n{ctx.author.name} ({len(attacker_vamps)} vampires) vs {opponent.name} ({len(defender_vamps)} vampires)\n\nBattles commencing...")
    
    battle_results = []
    total_battles = 0
    
    # Each vampire from attacker fights each vampire from defender
    for att_vamp in attacker_vamps:
        for def_vamp in defender_vamps:
            if not att_vamp['alive'] or not def_vamp['alive']:
                continue
            
            result = simulate_battle(att_vamp, def_vamp)
            
            result['winner']['wins'] += 1
            result['loser']['losses'] += 1
            
            # Award XP
            winner_xp = random.randint(20, 40)
            loser_xp = random.randint(5, 15)
            
            result['winner']['xp'] += winner_xp
            result['loser']['xp'] += loser_xp
            
            # Check for level ups
            if result['winner']['xp'] >= calculate_xp_needed(result['winner']['level']):
                level_up_vampire(result['winner'])
            
            if result['loser']['xp'] >= calculate_xp_needed(result['loser']['level']):
                level_up_vampire(result['loser'])
            
            # 15% chance of death in war
            death_occurred = False
            if random.random() < 0.15:
                result['loser']['alive'] = False
                result['winner']['kills'] += 1
                death_occurred = True
            
            battle_results.append({
                'narrative': result['narrative'],
                'winner': result['winner']['name'],
                'loser': result['loser']['name'],
                'death': death_occurred
            })
            
            total_battles += 1
            
            # Log battle
            battle_log = {
                "attacker": att_vamp['name'],
                "defender": def_vamp['name'],
                "winner": result['winner']['name'],
                "loser": result['loser']['name'],
                "narrative": result['narrative'],
                "timestamp": datetime.now().isoformat(),
                "war": True,
                "player_initiated": True
            }
            battles.append(battle_log)
    
    save_vampires(vampires)
    save_battles(battles)
    
    # Count survivors
    attacker_survivors = sum(1 for v in attacker_vamps if v['alive'])
    defender_survivors = sum(1 for v in defender_vamps if v['alive'])
    
    # Determine war winner
    if attacker_survivors > defender_survivors:
        war_winner = ctx.author.name
        war_result = "VICTORY"
        result_color = discord.Color.gold()
    elif defender_survivors > attacker_survivors:
        war_winner = opponent.name
        war_result = "DEFEAT"
        result_color = discord.Color.dark_gray()
    else:
        war_winner = "TIE"
        war_result = "STALEMATE"
        result_color = discord.Color.blue()
    
    # Create summary embed
    embed = discord.Embed(
        title=f"⚔️ WAR RESULTS - {war_result}!",
        description=f"**{total_battles}** battles were fought!",
        color=result_color
    )
    
    embed.add_field(
        name=f"{ctx.author.name}'s Army",
        value=f"Started: {len(attacker_vamps)}\nSurvivors: {attacker_survivors}\nCasualties: {len(attacker_vamps) - attacker_survivors}",
        inline=True
    )
    
    embed.add_field(
        name=f"{opponent.name}'s Army",
        value=f"Started: {len(defender_vamps)}\nSurvivors: {defender_survivors}\nCasualties: {len(defender_vamps) - defender_survivors}",
        inline=True
    )
    
    if war_winner != "TIE":
        embed.add_field(
            name="Victor",
            value=f"🏆 **{war_winner}**",
            inline=False
        )
    
    # Show some battle highlights (max 5)
    highlights = random.sample(battle_results, min(5, len(battle_results)))
    battle_text = ""
    for br in highlights:
        death_icon = " 💀" if br['death'] else ""
        battle_text += f"• {br['narrative']}{death_icon}\n"
    
    if battle_text:
        embed.add_field(name="Battle Highlights", value=battle_text, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='train')
async def train_vampire(ctx, vampire_id: str):
    """Train your vampire to gain XP (once per hour)"""
    
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
    
    if v['owner_id'] != str(ctx.author.id):
        await ctx.send("You don't own that vampire!")
        return
    
    if not v['alive']:
        await ctx.send(f"{v['name']} is dead and cannot train!")
        return
    
    if v['last_trained']:
        last_trained_time = datetime.fromisoformat(v['last_trained'])
        time_since = datetime.now() - last_trained_time
        if time_since < timedelta(hours=1):
            remaining = timedelta(hours=1) - time_since
            minutes = int(remaining.total_seconds() / 60)
            await ctx.send(f"⏰ {v['name']} is tired! Can train again in {minutes} minutes")
            return
    
    xp_gain = random.randint(10, 20)
    v['xp'] += xp_gain
    v['last_trained'] = datetime.now().isoformat()
    
    leveled = False
    stat_increases = None
    xp_needed = calculate_xp_needed(v['level'])
    
    if v['xp'] >= xp_needed:
        stat_increases = level_up_vampire(v)
        leveled = True
    
    save_vampires(vampires)
    
    if leveled:
        embed = discord.Embed(
            title="🎉 LEVEL UP!",
            description=f"**{v['name']}** trained hard and leveled up!",
            color=discord.Color.gold()
        )
        embed.add_field(name="New Level", value=v['level'], inline=True)
        embed.add_field(name="New Power", value=v['power'], inline=True)
        embed.add_field(name="XP Gained", value=f"+{xp_gain}", inline=True)
        
        stat_text = "\n".join([f"+{inc} {stat.upper()}" for stat, inc in stat_increases.items()])
        embed.add_field(name="Stat Increases", value=stat_text, inline=False)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"💪 **{v['name']}** trained hard! +{xp_gain} XP ({v['xp']}/{xp_needed})")

@bot.command(name='feed')
async def feed_vampire(ctx, vampire_id: str):
    """Feed your vampire to gain XP (once per 30 minutes)"""
    
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
    
    if v['owner_id'] != str(ctx.author.id):
        await ctx.send("You don't own that vampire!")
        return
    
    if not v['alive']:
        await ctx.send(f"{v['name']} is dead!")
        return
    
    if 'last_fed' not in v:
        v['last_fed'] = None
    
    if v['last_fed']:
        last_fed_time = datetime.fromisoformat(v['last_fed'])
        time_since = datetime.now() - last_fed_time
        if time_since < timedelta(minutes=30):
            remaining = timedelta(minutes=30) - time_since
            minutes = int(remaining.total_seconds() / 60)
            await ctx.send(f"🩸 {v['name']} is not hungry yet! Can feed again in {minutes} minutes")
            return
    
    xp_gain = random.randint(5, 15)
    v['xp'] += xp_gain
    v['last_fed'] = datetime.now().isoformat()
    
    leveled = False
    stat_increases = None
    xp_needed = calculate_xp_needed(v['level'])
    
    if v['xp'] >= xp_needed:
        stat_increases = level_up_vampire(v)
        leveled = True
    
    save_vampires(vampires)
    
    if leveled:
        embed = discord.Embed(
            title="🎉 LEVEL UP!",
            description=f"**{v['name']}** feasted and grew stronger!",
            color=discord.Color.gold()
        )
        embed.add_field(name="New Level", value=v['level'], inline=True)
        embed.add_field(name="New Power", value=v['power'], inline=True)
        embed.add_field(name="XP Gained", value=f"+{xp_gain}", inline=True)
        
        stat_text = "\n".join([f"+{inc} {stat.upper()}" for stat, inc in stat_increases.items()])
        embed.add_field(name="Stat Increases", value=stat_text, inline=False)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"🩸 **{v['name']}** fed on fresh blood! +{xp_gain} XP ({v['xp']}/{xp_needed})")

@bot.command(name='delete')
async def delete_vampire(ctx, vampire_id: str):
    """Delete one of your vampires"""
    
    user_id = str(ctx.author.id)
    
    if user_id not in vampires:
        await ctx.send("You don't have any vampires!")
        return
    
    found = False
    for i, v in enumerate(vampires[user_id]):
        if v['id'] == vampire_id:
            vampire_name = v['name']
            vampires[user_id].pop(i)
            found = True
            break
    
    if not found:
        await ctx.send("Vampire not found or you don't own it!")
        return
    
    save_vampires(vampires)
    await ctx.send(f"💀 **{vampire_name}** has been removed from your collection")

@bot.command(name='lb')
async def leaderboard(ctx):
    """View top vampires by level and wins"""
    
    all_vampires = []
    for user_id, user_vamps in vampires.items():
        all_vampires.extend(user_vamps)
    
    if not all_vampires:
        await ctx.send("No vampires exist yet!")
        return
    
    top_vampires = sorted(all_vampires, key=lambda v: (v['level'], v['wins']), reverse=True)[:10]
    
    embed = discord.Embed(
        title="🏆 Vampire Leaderboard",
        description="Top 10 vampires by level & wins",
        color=discord.Color.gold()
    )
    
    for idx, v in enumerate(top_vampires, 1):
        status = "💀" if not v['alive'] else "🧛"
        embed.add_field(
            name=f"{idx}. {v['name']} {status}",
            value=f"Level: {v['level']} | Wins: {v['wins']} | Power: {v['power']}\nClan: {v['clan']} | Owner: {v['owner_name']}",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='bl')
@commands.has_permissions(administrator=True)
async def battle_logs(ctx, limit: int = 10):
    """View recent battles"""
    
    if not battles:
        await ctx.send("No battles have occurred yet")
        return
    
    recent = battles[-limit:]
    recent.reverse()
    
    msg = f"**RECENT BATTLES (Last {len(recent)}):**\n\n"
    for b in recent:
        timestamp = datetime.fromisoformat(b['timestamp']).strftime('%Y-%m-%d %H:%M')
        battle_type = "[WAR]" if b.get('war', False) else "[PLAYER]" if b.get('player_initiated', False) else "[AUTO]"
        msg += f"`{timestamp}` {battle_type} - {b['narrative']}\n"
    
    await ctx.send(msg)

@bot.command(name='va')
@commands.has_permissions(administrator=True)
async def view_all_vampires(ctx):
    """View all vampires in the realm"""
    
    total = 0
    alive = 0
    
    for user_id, user_vamps in vampires.items():
        total += len(user_vamps)
        alive += sum(1 for v in user_vamps if v['alive'])
    
    await ctx.send(f"**Total Vampires:** {total}\n**Alive:** {alive}\n**Dead:** {total - alive}")

@bot.command(name='rv')
@commands.has_permissions(administrator=True)
async def revive_vampire(ctx, vampire_id: str):
    """Revive a dead vampire"""
    
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
    """Kill a vampire"""
    
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

@bot.command(name='givexp')
@commands.has_permissions(administrator=True)
async def give_xp(ctx, vampire_id: str, amount: int):
    """Give XP to a vampire"""
    
    if amount < 1:
        await ctx.send("Amount must be positive!")
        return
    
    found = False
    for user_id, user_vamps in vampires.items():
        for v in user_vamps:
            if v['id'] == vampire_id:
                v['xp'] += amount
                
                levels_gained = 0
                while v['xp'] >= calculate_xp_needed(v['level']):
                    level_up_vampire(v)
                    levels_gained += 1
                
                found = True
                
                if levels_gained > 0:
                    await ctx.send(f"✅ Gave {amount} XP to **{v['name']}**\n🎉 Leveled up {levels_gained} time(s)! Now level {v['level']}")
                else:
                    await ctx.send(f"✅ Gave {amount} XP to **{v['name']}** ({v['xp']}/{calculate_xp_needed(v['level'])})")
                break
        if found:
            break
    
    if not found:
        await ctx.send("Vampire not found!")
        return
    
    save_vampires(vampires)

@tasks.loop(minutes=10)
async def auto_battle():
    """Automatically run battles between random vampires"""
    
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
    
    result['winner']['xp'] += random.randint(20, 30)
    result['loser']['xp'] += random.randint(5, 10)
    
    if result['winner']['xp'] >= calculate_xp_needed(result['winner']['level']):
        level_up_vampire(result['winner'])
    
    if result['loser']['xp'] >= calculate_xp_needed(result['loser']['level']):
        level_up_vampire(result['loser'])
    
    death_occurred = False
    if random.random() < 0.05:
        result['loser']['alive'] = False
        result['winner']['kills'] += 1
        death_occurred = True
    
    save_vampires(vampires)
    
    battle_log = {
        "winner": result['winner']['name'],
        "loser": result['loser']['name'],
        "narrative": result['narrative'],
        "timestamp": datetime.now().isoformat(),
        "death": death_occurred,
        "player_initiated": False
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
