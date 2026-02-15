import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# Files
VAMPIRES_FILE = 'vampires.json'
BATTLE_LOGS_FILE = 'battle_logs.json'
CREDITS_FILE = 'credits.json'

# Blocked channel ID
BLOCKED_CHANNEL_ID = 1470843481177198876

# Credit settings
MAX_CREDITS = 3
CREDIT_COST = 1
CREDIT_COOLDOWN_MINUTES = 30

# Load vampires
def load_vampires():
    if os.path.exists(VAMPIRES_FILE):
        with open(VAMPIRES_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save vampires
def save_vampires(vampires):
    with open(VAMPIRES_FILE, 'w') as f:
        json.dump(vampires, f, indent=4)

# Load battle logs
def load_battle_logs():
    if os.path.exists(BATTLE_LOGS_FILE):
        with open(BATTLE_LOGS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save battle logs
def save_battle_logs(logs):
    with open(BATTLE_LOGS_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

# Load credits
def load_credits():
    if os.path.exists(CREDITS_FILE):
        with open(CREDITS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save credits
def save_credits(credits):
    with open(CREDITS_FILE, 'w') as f:
        json.dump(credits, f, indent=4)

# Check and update credits
def check_credits(user_id):
    """Check if user has credits available or if cooldown has passed"""
    credits = load_credits()
    
    if user_id not in credits:
        # New user, give them max credits
        credits[user_id] = {
            "credits": MAX_CREDITS,
            "last_refill": datetime.now().isoformat()
        }
        save_credits(credits)
        return MAX_CREDITS, None
    
    user_data = credits[user_id]
    current_credits = user_data["credits"]
    
    # If they have credits, return them
    if current_credits > 0:
        return current_credits, None
    
    # Check if cooldown has passed
    last_refill = datetime.fromisoformat(user_data["last_refill"])
    time_passed = datetime.now() - last_refill
    cooldown_duration = timedelta(minutes=CREDIT_COOLDOWN_MINUTES)
    
    if time_passed >= cooldown_duration:
        # Cooldown passed, refill credits
        credits[user_id]["credits"] = MAX_CREDITS
        credits[user_id]["last_refill"] = datetime.now().isoformat()
        save_credits(credits)
        return MAX_CREDITS, None
    else:
        # Still on cooldown
        time_remaining = cooldown_duration - time_passed
        return 0, time_remaining

# Use a credit
def use_credit(user_id):
    """Deduct one credit from user"""
    credits = load_credits()
    
    if user_id not in credits:
        credits[user_id] = {
            "credits": MAX_CREDITS,
            "last_refill": datetime.now().isoformat()
        }
    
    credits[user_id]["credits"] -= CREDIT_COST
    
    # If credits hit 0, start the cooldown timer
    if credits[user_id]["credits"] == 0:
        credits[user_id]["last_refill"] = datetime.now().isoformat()
    
    save_credits(credits)

# Generate unique 6-digit ID
def generate_vampire_id(vampires):
    while True:
        vampire_id = str(random.randint(100000, 999999))
        if vampire_id not in vampires:
            return vampire_id

# Generate AI opponent based on player power
def generate_ai_opponent(player_power):
    """Generate an AI opponent that scales with player power"""
    
    # AI names pool (expanded)
    ai_names = [
        "Marcus the Merciless", "Elena the Ruthless", "Drakon the Savage", 
        "Nyx the Deadly", "Kain the Brutal", "Sable the Vicious",
        "Cyrus the Cruel", "Morrigan the Fierce", "Vex the Relentless",
        "Azrael the Destroyer", "Valeria the Bloodletter", "Theron the Merciless",
        "Ravenna the Shadow", "Darius the Ancient", "Lysandra the Wicked",
        "Cain the Accursed", "Octavia the Dread", "Grimwald the Eternal",
        "Seraphine the Void", "Lucien the Plague", "Morgath the Fallen",
        "Vesper the Nightbane", "Zephyr the Sinister", "Alaric the Cursed",
        "Belladonna the Profane", "Cassius the Corrupted", "Nero the Vile",
        "Isolde the Vengeful", "Draven the Malevolent", "Xander the Apostate"
    ]
    
    ai_name = random.choice(ai_names)
    
    # Scale AI power based on player power
    if player_power < 100:
        # Weak opponents for struggling vampires
        ai_power = random.randint(60, 90)
        difficulty = "Novice"
    elif player_power < 120:
        # Balanced opponents
        ai_power = random.randint(80, 110)
        difficulty = "Apprentice"
    elif player_power < 150:
        # Moderate challenge
        ai_power = random.randint(100, 140)
        difficulty = "Adept"
    elif player_power < 180:
        # Tough opponents
        ai_power = random.randint(130, 170)
        difficulty = "Veteran"
    elif player_power < 220:
        # Very strong opponents
        ai_power = random.randint(160, 210)
        difficulty = "Master"
    elif player_power < 280:
        # Elite opponents
        ai_power = random.randint(200, 260)
        difficulty = "Elite"
    else:
        # Legendary opponents for the strongest
        ai_power = random.randint(250, 320)
        difficulty = "Legendary"
    
    return ai_name, ai_power, difficulty

vampires = load_vampires()
battle_logs = load_battle_logs()

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Vampire Character Bot Ready')

# Check to block DM commands
@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not in the shadows of DMs...")
        return False
    return True

# Check to block specific channel (admins bypass this)
@bot.check
async def block_specific_channel(ctx):
    # Allow admins to use commands anywhere
    if ctx.author.guild_permissions.administrator:
        return True
    
    # Block non-admins from using commands in the blocked channel
    if ctx.channel.id == BLOCKED_CHANNEL_ID:
        return False
    return True

# Credits command - Check your credits
@bot.command(name='credits')
async def check_user_credits(ctx):
    """Check your available credits"""
    
    # Admins don't use credits
    if ctx.author.guild_permissions.administrator:
        await ctx.send("As an admin, you have unlimited vampire creation credits.")
        return
    
    user_id = str(ctx.author.id)
    current_credits, time_remaining = check_credits(user_id)
    
    embed = discord.Embed(
        title="Your Credits",
        color=0x8B0000
    )
    
    embed.add_field(
        name="Available Credits",
        value=f"{current_credits}/{MAX_CREDITS}",
        inline=True
    )
    
    if current_credits == 0 and time_remaining:
        minutes = int(time_remaining.total_seconds() // 60)
        seconds = int(time_remaining.total_seconds() % 60)
        embed.add_field(
            name="Next Refill",
            value=f"{minutes}m {seconds}s",
            inline=True
        )
        embed.set_footer(text=f"Credits refill every {CREDIT_COOLDOWN_MINUTES} minutes")
    else:
        embed.set_footer(text=f"Each vampire costs {CREDIT_COST} credit to create")
    
    await ctx.send(embed=embed)

# Make command - Vampire character creator
@bot.command(name='make')
async def make_vampire(ctx):
    """Create a random vampire character with backstory"""
    
    user_id = str(ctx.author.id)
    is_admin = ctx.author.guild_permissions.administrator
    
    # Check credits for non-admins
    if not is_admin:
        current_credits, time_remaining = check_credits(user_id)
        
        if current_credits < CREDIT_COST:
            minutes = int(time_remaining.total_seconds() // 60)
            seconds = int(time_remaining.total_seconds() % 60)
            
            embed = discord.Embed(
                title="Not Enough Credits",
                description=f"You need {CREDIT_COST} credit to create a vampire.",
                color=0xFF0000
            )
            embed.add_field(
                name="Your Credits",
                value=f"{current_credits}/{MAX_CREDITS}",
                inline=True
            )
            embed.add_field(
                name="Next Refill",
                value=f"{minutes}m {seconds}s",
                inline=True
            )
            embed.set_footer(text=f"Credits refill every {CREDIT_COOLDOWN_MINUTES} minutes")
            
            await ctx.send(embed=embed)
            return
    
    # Vampire name components (expanded)
    first_names = [
        "Vladislav", "Crimson", "Nocturne", "Draven", "Lazarus", 
        "Seraphina", "Raven", "Lucian", "Morgana", "Viktor",
        "Evangeline", "Thorne", "Lilith", "Dante", "Isolde",
        "Damien", "Celeste", "Raphael", "Selene", "Corvus",
        "Cassius", "Belladonna", "Alaric", "Nyx", "Soren",
        "Valentina", "Dorian", "Mystique", "Kieran", "Octavia",
        "Zephyr", "Persephone", "Caine", "Rowena", "Lucien"
    ]
    
    last_names = [
        "Bloodworth", "Nightshade", "Darkmore", "Ravencroft", "Blackthorn",
        "Shadowmere", "Duskwood", "Grimwood", "Moonwhisper", "Darkholme",
        "Bloodmoon", "Nightbane", "Ashenmoor", "Crowley", "Blackwell",
        "Thornfield", "Nightfall", "Veilwalker", "Deathwhisper", "Shadowveil",
        "Grimsbane", "Darkhaven", "Nightfang", "Bloodraven", "Darkwyn"
    ]
    
    titles = [
        "The Eternal", "The Cursed", "The Ancient", "The Forsaken", "The Immortal",
        "The Undying", "The Bloodthirsty", "The Shadowed", "The Forgotten", "The Damned",
        "Lord of Shadows", "Mistress of Night", "The Moonborn", "The Nightstalker", "The Pale",
        "The Profane", "The Sinister", "The Dreadful", "The Malevolent", "The Corrupted",
        "The Vile", "The Wretched", "The Accursed", "The Harbinger", "The Scourge"
    ]
    
    origins = [
        "the foggy streets of Victorian London",
        "a crumbling castle in the Carpathian Mountains",
        "the catacombs beneath Paris",
        "a forgotten monastery in Transylvania",
        "the dark forests of Eastern Europe",
        "an ancient tomb in Egypt",
        "the ruins of a Romanian fortress",
        "a haunted manor in Scotland",
        "the underground crypts of Prague",
        "a cursed bloodline dating back to the Crusades",
        "the plague-ridden streets of medieval Venice",
        "an abandoned cathedral in the Black Forest",
        "the frozen wastes of Siberia",
        "the blood-soaked battlefields of the Ottoman Empire",
        "a secret society in Renaissance Italy",
        "the haunted moors of Ireland",
        "an occult ritual gone wrong in Salem",
        "the shadowy alleys of Constantinople"
    ]
    
    powers = [
        "control over shadows and darkness",
        "the ability to transform into a swarm of bats",
        "hypnotic charm that bends mortals to their will",
        "superhuman strength and speed",
        "mastery of blood magic",
        "the power to walk through walls",
        "control over wolves and ravens",
        "the gift of prophecy through blood",
        "immunity to most mortal weapons",
        "the ability to drain life force from a distance",
        "manipulation of weather and storms",
        "the power to induce nightmares in victims",
        "shapeshifting into mist or fog",
        "telekinetic control over objects",
        "the ability to speak with the dead",
        "regeneration from near-fatal wounds",
        "mind reading and thought manipulation",
        "summoning of undead servants"
    ]
    
    weaknesses = [
        "sunlight burns their flesh to ash",
        "cannot cross running water",
        "obsessively counts spilled seeds",
        "repelled by garlic and holy symbols",
        "cannot enter a home uninvited",
        "weakened by silver",
        "loses power during the new moon",
        "vulnerable to fire",
        "bound to their ancestral bloodline",
        "cursed to feel the pain of every life they've taken",
        "must sleep in their native soil",
        "cannot see their reflection",
        "weakened by the sound of church bells",
        "vulnerable to hawthorn stakes",
        "loses strength in the presence of pure love",
        "cursed to count grains of rice when spilled",
        "cannot cross salt lines",
        "weakened during daylight hours even indoors"
    ]
    
    personalities = [
        "brooding and melancholic, haunted by centuries of loss",
        "seductive and manipulative, viewing mortals as playthings",
        "noble and tragic, fighting against their dark nature",
        "ruthless and cunning, building an empire in the shadows",
        "philosophical and detached, weary of immortality",
        "vengeful and bitter, seeking revenge for their curse",
        "elegant and refined, clinging to aristocratic traditions",
        "chaotic and unpredictable, reveling in their monstrous nature",
        "remorseful and seeking redemption for past sins",
        "calculating and strategic, playing the long game of immortality",
        "sadistic and cruel, taking pleasure in suffering",
        "mysterious and enigmatic, hiding their true intentions",
        "honorable yet deadly, following an ancient code",
        "obsessive and possessive over their territory",
        "charming yet dangerous, a perfect predator"
    ]
    
    # Generate random vampire
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    title = random.choice(titles)
    origin = random.choice(origins)
    power = random.choice(powers)
    weakness = random.choice(weaknesses)
    personality = random.choice(personalities)
    age = random.randint(150, 1500)
    
    # Generate unique ID
    vampire_id = generate_vampire_id(vampires)
    
    # Store vampire data
    vampire_data = {
        "id": vampire_id,
        "first_name": first_name,
        "last_name": last_name,
        "title": title,
        "age": age,
        "origin": origin,
        "power": power,
        "weakness": weakness,
        "personality": personality,
        "created_by": str(ctx.author.id),
        "created_at": datetime.now().isoformat(),
        "power_level": 100,
        "wins": 0,
        "losses": 0,
        "status": "alive",
        "earned_titles": [],
        "total_power_gained": 0,
        "total_power_lost": 0,
        "highest_power": 100,
        "kill_count": 0
    }
    
    vampires[vampire_id] = vampire_data
    save_vampires(vampires)
    
    # Deduct credit for non-admins
    if not is_admin:
        use_credit(user_id)
        remaining_credits, _ = check_credits(user_id)
    
    # Create embed
    embed = discord.Embed(
        title=f"{first_name} {last_name}",
        description=f"*{title}*",
        color=0x8B0000
    )
    
    embed.add_field(
        name="ID",
        value=f"``{vampire_id}``",
        inline=True
    )
    
    embed.add_field(
        name="Age",
        value=f"{age} years old",
        inline=True
    )
    
    embed.add_field(
        name="Power Level",
        value=f"{vampire_data['power_level']}",
        inline=True
    )
    
    embed.add_field(
        name="Origin",
        value=f"Born from {origin}",
        inline=False
    )
    
    embed.add_field(
        name="Dark Gift",
        value=f"Possesses {power}",
        inline=False
    )
    
    embed.add_field(
        name="Fatal Flaw",
        value=f"However, {weakness}",
        inline=False
    )
    
    embed.add_field(
        name="Nature",
        value=personality.capitalize(),
        inline=False
    )
    
    # Show remaining credits for non-admins
    if not is_admin:
        embed.set_footer(text=f"Credits remaining: {remaining_credits}/{MAX_CREDITS} | The night is eternal...")
    else:
        embed.set_footer(text="The night is eternal, and so are we...")
    
    embed.timestamp = datetime.now()
    
    await ctx.send(embed=embed)

# Transfer Soul command - Combine two vampires (FIXED)
@bot.command(name='transfer')
async def transfer_soul(ctx, *, args=None):
    """Combine two vampires into one powerful entity. Both vampires will be sacrificed."""
    
    if args is None:
        await ctx.send("Usage: ``?transfer <vampire_id_1> <vampire_id_2>``\nExample: ``?transfer 123456 789012``")
        return
    
    # Split the arguments
    parts = args.split()
    
    if len(parts) != 2:
        await ctx.send(f"You provided {len(parts)} argument(s). Please provide exactly 2 vampire IDs.\nUsage: ``?transfer <vampire_id_1> <vampire_id_2>``")
        return
    
    vampire_id_1 = parts[0].strip()
    vampire_id_2 = parts[1].strip()
    
    # Check if both vampires exist
    if vampire_id_1 not in vampires:
        await ctx.send(f"Vampire with ID ``{vampire_id_1}`` not found. Use ``?list`` to see your vampires.")
        return
    
    if vampire_id_2 not in vampires:
        await ctx.send(f"Vampire with ID ``{vampire_id_2}`` not found. Use ``?list`` to see your vampires.")
        return
    
    # Can't transfer same vampire
    if vampire_id_1 == vampire_id_2:
        await ctx.send("You cannot transfer a vampire's soul into itself.")
        return
    
    vampire_1 = vampires[vampire_id_1]
    vampire_2 = vampires[vampire_id_2]
    
    user_id = str(ctx.author.id)
    
    # Check ownership
    if vampire_1["created_by"] != user_id:
        await ctx.send(f"You don't own the vampire with ID ``{vampire_id_1}``.")
        return
    
    if vampire_2["created_by"] != user_id:
        await ctx.send(f"You don't own the vampire with ID ``{vampire_id_2}``.")
        return
    
    # Check if both are alive
    if vampire_1.get("status") == "dead":
        await ctx.send(f"**{vampire_1['first_name']} {vampire_1['last_name']}** is already dead and cannot be used in soul transfer.")
        return
    
    if vampire_2.get("status") == "dead":
        await ctx.send(f"**{vampire_2['first_name']} {vampire_2['last_name']}** is already dead and cannot be used in soul transfer.")
        return
    
    # Calculate new vampire stats
    combined_power = vampire_1["power_level"] + vampire_2["power_level"]
    # Add bonus power for the ritual (20-30% of combined power)
    bonus_multiplier = random.uniform(1.20, 1.30)
    new_power = int(combined_power * bonus_multiplier)
    
    combined_wins = vampire_1.get("wins", 0) + vampire_2.get("wins", 0)
    combined_losses = vampire_1.get("losses", 0) + vampire_2.get("losses", 0)
    combined_kills = vampire_1.get("kill_count", 0) + vampire_2.get("kill_count", 0)
    
    # Collect all earned titles
    all_titles = vampire_1.get("earned_titles", []) + vampire_2.get("earned_titles", [])
    
    # Generate new vampire with combined aspects
    first_names = [
        "Vladislav", "Crimson", "Nocturne", "Draven", "Lazarus", 
        "Seraphina", "Raven", "Lucian", "Morgana", "Viktor",
        "Evangeline", "Thorne", "Lilith", "Dante", "Isolde",
        "Damien", "Celeste", "Raphael", "Selene", "Corvus",
        "Cassius", "Belladonna", "Alaric", "Nyx", "Soren",
        "Valentina", "Dorian", "Mystique", "Kieran", "Octavia",
        "Zephyr", "Persephone", "Caine", "Rowena", "Lucien"
    ]
    
    last_names = [
        "Bloodworth", "Nightshade", "Darkmore", "Ravencroft", "Blackthorn",
        "Shadowmere", "Duskwood", "Grimwood", "Moonwhisper", "Darkholme",
        "Bloodmoon", "Nightbane", "Ashenmoor", "Crowley", "Blackwell",
        "Thornfield", "Nightfall", "Veilwalker", "Deathwhisper", "Shadowveil",
        "Grimsbane", "Darkhaven", "Nightfang", "Bloodraven", "Darkwyn"
    ]
    
    # Special titles for transferred souls
    transfer_titles = [
        "The Reborn",
        "The Amalgamation",
        "The Twin Soul",
        "The Transcendent",
        "The Ascended",
        "The Unified",
        "The Fused",
        "The Evolved",
        "The Merged",
        "The Combined Essence"
    ]
    
    new_first_name = random.choice(first_names)
    new_last_name = random.choice(last_names)
    new_title = random.choice(transfer_titles)
    new_age = max(vampire_1["age"], vampire_2["age"]) + random.randint(100, 500)
    
    # Combine origins
    origin_text = f"a forbidden soul transfer ritual between {vampire_1['first_name']} {vampire_1['last_name']} and {vampire_2['first_name']} {vampire_2['last_name']}"
    
    # Choose random power and weakness from both
    new_power_ability = random.choice([vampire_1["power"], vampire_2["power"]])
    new_weakness = random.choice([vampire_1["weakness"], vampire_2["weakness"]])
    new_personality = random.choice([vampire_1["personality"], vampire_2["personality"]])
    
    # Generate new ID
    new_vampire_id = generate_vampire_id(vampires)
    
    # Create new vampire
    new_vampire_data = {
        "id": new_vampire_id,
        "first_name": new_first_name,
        "last_name": new_last_name,
        "title": new_title,
        "age": new_age,
        "origin": origin_text,
        "power": new_power_ability,
        "weakness": new_weakness,
        "personality": new_personality,
        "created_by": user_id,
        "created_at": datetime.now().isoformat(),
        "power_level": new_power,
        "wins": combined_wins,
        "losses": combined_losses,
        "status": "alive",
        "earned_titles": all_titles,
        "total_power_gained": vampire_1.get("total_power_gained", 0) + vampire_2.get("total_power_gained", 0),
        "total_power_lost": vampire_1.get("total_power_lost", 0) + vampire_2.get("total_power_lost", 0),
        "highest_power": new_power,
        "kill_count": combined_kills,
        "transferred_from": [vampire_id_1, vampire_id_2]
    }
    
    # Delete old vampires
    del vampires[vampire_id_1]
    del vampires[vampire_id_2]
    
    # Add new vampire
    vampires[new_vampire_id] = new_vampire_data
    save_vampires(vampires)
    
    # Create ritual embed
    embed = discord.Embed(
        title="SOUL TRANSFER RITUAL COMPLETE",
        description=f"The souls of **{vampire_1['first_name']} {vampire_1['last_name']}** and **{vampire_2['first_name']} {vampire_2['last_name']}** have been fused in a dark ritual. Both have perished, but from their essence rises a new being of immense power...",
        color=0x9400D3  # Dark purple for mystical ritual
    )
    
    embed.add_field(
        name="",
        value="",
        inline=False
    )
    
    embed.add_field(
        name="The Reborn Vampire",
        value=f"**{new_first_name} {new_last_name}**\n*{new_title}*",
        inline=False
    )
    
    embed.add_field(
        name="ID",
        value=f"``{new_vampire_id}``",
        inline=True
    )
    
    embed.add_field(
        name="Power Level",
        value=f"**{new_power}**",
        inline=True
    )
    
    embed.add_field(
        name="Age",
        value=f"{new_age} years",
        inline=True
    )
    
    embed.add_field(
        name="Ritual Results",
        value=f"Combined Power: {combined_power}\n"
              f"Ritual Bonus: +{new_power - combined_power}\n"
              f"Total Power: **{new_power}**",
        inline=False
    )
    
    embed.add_field(
        name="Inherited Record",
        value=f"Wins: {combined_wins} | Losses: {combined_losses} | Kills: {combined_kills}",
        inline=False
    )
    
    if all_titles:
        embed.add_field(
            name="Inherited Titles",
            value=" | ".join(all_titles),
            inline=False
        )
    
    embed.add_field(
        name="Origin",
        value=f"Born from {origin_text}",
        inline=False
    )
    
    embed.add_field(
        name="Inherited Gift",
        value=f"Possesses {new_power_ability}",
        inline=False
    )
    
    embed.add_field(
        name="Inherited Flaw",
        value=f"However, {new_weakness}",
        inline=False
    )
    
    embed.set_footer(text="Two souls become one... The ritual is complete.")
    embed.timestamp = datetime.now()
    
    await ctx.send(embed=embed)

# Fight command - Battle against AI vampire
@bot.command(name='fight')
async def fight_vampire(ctx, vampire_id: str = None):
    """Fight your vampire against an AI opponent"""
    
    if vampire_id is None:
        await ctx.send("Usage: ``?fight <vampire_id>``")
        return
    
    # Check if vampire exists
    if vampire_id not in vampires:
        await ctx.send(f"Vampire with ID ``{vampire_id}`` not found.")
        return
    
    player_vampire = vampires[vampire_id]
    
    # Check if vampire is alive
    if player_vampire.get("status") == "dead":
        await ctx.send(f"**{player_vampire['first_name']} {player_vampire['last_name']}** has fallen in battle and cannot fight anymore.")
        return
    
    # Check if user owns this vampire
    if str(ctx.author.id) != player_vampire["created_by"]:
        await ctx.send("You can only fight with vampires you created.")
        return
    
    # Generate AI opponent that scales with player power
    player_power = player_vampire["power_level"]
    ai_name, ai_power, difficulty = generate_ai_opponent(player_power)
    
    # Calculate win chance based on power levels
    power_diff = player_power - ai_power
    base_chance = 50
    
    # Adjust chance by power difference (each point = 0.5% chance adjustment)
    win_chance = base_chance + (power_diff * 0.5)
    
    # Clamp between 20% and 80%
    win_chance = max(20, min(80, win_chance))
    
    # Determine outcome
    random_roll = random.randint(1, 100)
    player_wins = random_roll <= win_chance
    
    # Battle narrative (expanded)
    battle_actions = [
        "lunges forward with supernatural speed",
        "unleashes a torrent of dark magic",
        "transforms into mist to dodge an attack",
        "strikes with ancient fury",
        "summons shadows to bind their opponent",
        "moves with predatory grace",
        "channels centuries of bloodlust",
        "delivers a devastating blow",
        "conjures a storm of blood",
        "phases through reality itself",
        "calls upon the power of the damned",
        "strikes with unholy precision",
        "manipulates time to gain advantage",
        "drains the very life from the air",
        "unleashes a primal scream that shakes the earth",
        "summons spectral wolves to attack",
        "creates illusions to confuse their foe",
        "channels raw vampiric essence"
    ]
    
    battle_locations = [
        "beneath a blood moon in an abandoned graveyard",
        "in the ruins of an ancient cathedral",
        "atop a fog-shrouded mountain peak",
        "within the depths of a forgotten crypt",
        "in the shadows of a cursed forest",
        "on the battlements of a crumbling castle",
        "in a realm between life and death",
        "within a circle of standing stones"
    ]
    
    location = random.choice(battle_locations)
    
    embed = discord.Embed(
        title="BATTLE OF THE DAMNED",
        description=f"*{location}*",
        color=0x8B0000
    )
    
    embed.add_field(
        name="Your Vampire",
        value=f"**{player_vampire['first_name']} {player_vampire['last_name']}**\nPower: {player_power}",
        inline=True
    )
    
    embed.add_field(
        name="Opponent",
        value=f"**{ai_name}**\nPower: {ai_power}\nDifficulty: {difficulty}",
        inline=True
    )
    
    embed.add_field(
        name="",
        value="",
        inline=False
    )
    
    action1 = random.choice(battle_actions)
    action2 = random.choice(battle_actions)
    
    battle_story = f"**{player_vampire['first_name']}** {action1}, while **{ai_name}** {action2}. "
    battle_story += "The night trembles with their clash. "
    
    title_earned = False
    new_title = ""
    
    if player_wins:
        # Player wins
        # Scale power gain based on difficulty
        if difficulty == "Novice":
            power_gain = random.randint(3, 8)
        elif difficulty == "Apprentice":
            power_gain = random.randint(5, 12)
        elif difficulty == "Adept":
            power_gain = random.randint(8, 15)
        elif difficulty == "Veteran":
            power_gain = random.randint(12, 20)
        elif difficulty == "Master":
            power_gain = random.randint(15, 25)
        elif difficulty == "Elite":
            power_gain = random.randint(20, 30)
        else:  # Legendary
            power_gain = random.randint(25, 40)
        
        player_vampire["power_level"] += power_gain
        player_vampire["wins"] = player_vampire.get("wins", 0) + 1
        player_vampire["total_power_gained"] = player_vampire.get("total_power_gained", 0) + power_gain
        
        # Update highest power
        if player_vampire["power_level"] > player_vampire.get("highest_power", 100):
            player_vampire["highest_power"] = player_vampire["power_level"]
        
        # 50% chance to increase kill count
        if random.randint(1, 2) == 1:
            player_vampire["kill_count"] = player_vampire.get("kill_count", 0) + 1
        
        # Check if vampire earned a title (10+ wins and no title yet)
        if player_vampire["wins"] >= 10 and len(player_vampire.get("earned_titles", [])) == 0:
            # Award a legendary title
            legendary_titles = [
                "The Conqueror",
                "The Invincible",
                "The Legend",
                "The Champion",
                "The Destroyer",
                "The Undefeated",
                "The Terror",
                "The Sovereign",
                "The Apex Predator",
                "The Warlord",
                "The Dominator",
                "The Supreme",
                "The Vanquisher",
                "The Dreadlord",
                "The Immortal King",
                "The Deathbringer",
                "The Unstoppable",
                "The Merciless",
                "The Absolute",
                "The Executioner"
            ]
            
            new_title = random.choice(legendary_titles)
            
            if "earned_titles" not in player_vampire:
                player_vampire["earned_titles"] = []
            
            player_vampire["earned_titles"].append(new_title)
            title_earned = True
        
        outcome = f"\n\n**VICTORY**\n\n**{player_vampire['first_name']} {player_vampire['last_name']}** emerges victorious, growing stronger from the battle.\n\n"
        outcome += f"Power Level: {player_power} → {player_vampire['power_level']} (+{power_gain})"
        
        if title_earned:
            outcome += f"\n\n**LEGENDARY ACHIEVEMENT UNLOCKED**\n"
            outcome += f"After {player_vampire['wins']} victories, **{player_vampire['first_name']}** has earned the title:\n"
            outcome += f"**{new_title}**"
        
        embed.color = 0x00FF00  # Green for victory
        
    else:
        # Check if vampire dies (30% chance on loss)
        death_roll = random.randint(1, 100)
        if death_roll <= 30:
            # Vampire dies
            player_vampire["status"] = "dead"
            player_vampire["losses"] = player_vampire.get("losses", 0) + 1
            
            outcome = f"\n\n**DEFEATED**\n\n**{player_vampire['first_name']} {player_vampire['last_name']}** has fallen in battle. "
            outcome += f"The ancient vampire crumbles to dust, their immortal life finally ended.\n\nThis vampire can no longer fight."
            
            embed.color = 0x000000  # Black for death
        else:
            # Vampire survives but loses power
            power_loss = random.randint(5, 10)
            player_vampire["power_level"] = max(50, player_vampire["power_level"] - power_loss)
            player_vampire["losses"] = player_vampire.get("losses", 0) + 1
            player_vampire["total_power_lost"] = player_vampire.get("total_power_lost", 0) + power_loss
            
            outcome = f"\n\n**DEFEAT**\n\n**{player_vampire['first_name']} {player_vampire['last_name']}** is defeated but survives to fight another night.\n\n"
            outcome += f"Power Level: {player_power} → {player_vampire['power_level']} (-{power_loss})"
            
            embed.color = 0xFF0000  # Red for defeat
    
    embed.add_field(
        name="Battle Report",
        value=battle_story + outcome,
        inline=False
    )
    
    embed.add_field(
        name="Record",
        value=f"Wins: {player_vampire.get('wins', 0)} | Losses: {player_vampire.get('losses', 0)} | Kills: {player_vampire.get('kill_count', 0)}",
        inline=False
    )
    
    # Save updated vampire data
    vampires[vampire_id] = player_vampire
    save_vampires(vampires)
    
    # Log battle
    battle_log = {
        "vampire_id": vampire_id,
        "vampire_name": f"{player_vampire['first_name']} {player_vampire['last_name']}",
        "opponent": ai_name,
        "player_power": player_power,
        "opponent_power": ai_power,
        "difficulty": difficulty,
        "outcome": "win" if player_wins else "loss",
        "died": player_vampire.get("status") == "dead",
        "title_earned": new_title if title_earned else None,
        "timestamp": datetime.now().isoformat()
    }
    
    battle_logs.append(battle_log)
    save_battle_logs(battle_logs)
    
    embed.set_footer(text="Only the strongest survive the eternal night...")
    embed.timestamp = datetime.now()
    
    await ctx.send(embed=embed)

# List command - Show all your vampires
@bot.command(name='list')
async def list_vampires(ctx):
    """Display all vampires you have created"""
    
    user_id = str(ctx.author.id)
    
    # Filter vampires by creator
    user_vampires = {vid: vdata for vid, vdata in vampires.items() if vdata.get("created_by") == user_id}
    
    if not user_vampires:
        await ctx.send("You have not created any vampires yet. Use ``?make`` to create one.")
        return
    
    # Separate alive and dead vampires
    alive_vampires = {vid: vdata for vid, vdata in user_vampires.items() if vdata.get("status") == "alive"}
    dead_vampires = {vid: vdata for vid, vdata in user_vampires.items() if vdata.get("status") == "dead"}
    
    # Create embed
    embed = discord.Embed(
        title=f"{ctx.author.name}'s Vampire Coven",
        color=0x8B0000
    )
    
    # Add alive vampires
    if alive_vampires:
        alive_list = ""
        for vid, vdata in alive_vampires.items():
            name = f"{vdata['first_name']} {vdata['last_name']}"
            power = vdata.get('power_level', 100)
            wins = vdata.get('wins', 0)
            losses = vdata.get('losses', 0)
            kills = vdata.get('kill_count', 0)
            
            # Check for earned titles
            earned_titles = vdata.get('earned_titles', [])
            title_display = f" - {earned_titles[0]}" if earned_titles else ""
            
            alive_list += f"``{vid}`` - **{name}**{title_display}\n"
            alive_list += f"Power: {power} | Record: {wins}W - {losses}L | Kills: {kills}\n\n"
        
        embed.add_field(
            name="Active Vampires",
            value=alive_list,
            inline=False
        )
    
    # Add dead vampires
    if dead_vampires:
        dead_list = ""
        for vid, vdata in dead_vampires.items():
            name = f"{vdata['first_name']} {vdata['last_name']}"
            wins = vdata.get('wins', 0)
            losses = vdata.get('losses', 0)
            highest_power = vdata.get('highest_power', 100)
            
            # Check for earned titles
            earned_titles = vdata.get('earned_titles', [])
            title_display = f" - {earned_titles[0]}" if earned_titles else ""
            
            dead_list += f"``{vid}`` - **{name}**{title_display} [FALLEN]\n"
            dead_list += f"Final Record: {wins}W - {losses}L | Peak Power: {highest_power}\n\n"
        
        embed.add_field(
            name="Fallen Vampires",
            value=dead_list,
            inline=False
        )
    
    # Add summary
    total = len(user_vampires)
    alive_count = len(alive_vampires)
    dead_count = len(dead_vampires)
    
    embed.set_footer(text=f"Total: {total} | Active: {alive_count} | Fallen: {dead_count}")
    embed.timestamp = datetime.now()
    
    await ctx.send(embed=embed)

# Stats command - Show detailed vampire stats
@bot.command(name='stats')
async def vampire_stats(ctx, vampire_id: str = None):
    """Display detailed statistics for a specific vampire"""
    
    if vampire_id is None:
        await ctx.send("Usage: ``?stats <vampire_id>``")
        return
    
    # Check if vampire exists
    if vampire_id not in vampires:
        await ctx.send(f"Vampire with ID ``{vampire_id}`` not found.")
        return
    
    vampire = vampires[vampire_id]
    
    # Check if user owns this vampire
    if str(ctx.author.id) != vampire["created_by"]:
        await ctx.send("You can only view stats for vampires you created.")
        return
    
    # Create detailed stats embed
    embed = discord.Embed(
        title=f"{vampire['first_name']} {vampire['last_name']}",
        description=f"*{vampire['title']}*",
        color=0x8B0000 if vampire.get('status') == 'alive' else 0x000000
    )
    
    # Check for earned titles
    earned_titles = vampire.get('earned_titles', [])
    if earned_titles:
        embed.description += f"\n**{earned_titles[0]}**"
    
    embed.add_field(
        name="ID",
        value=f"``{vampire_id}``",
        inline=True
    )
    
    embed.add_field(
        name="Status",
        value=vampire.get('status', 'alive').upper(),
        inline=True
    )
    
    embed.add_field(
        name="Age",
        value=f"{vampire['age']} years",
        inline=True
    )
    
    embed.add_field(
        name="Combat Statistics",
        value=f"Power Level: **{vampire.get('power_level', 100)}**\n"
              f"Peak Power: **{vampire.get('highest_power', 100)}**\n"
              f"Wins: **{vampire.get('wins', 0)}**\n"
              f"Losses: **{vampire.get('losses', 0)}**\n"
              f"Kills: **{vampire.get('kill_count', 0)}**\n"
              f"Win Rate: **{round((vampire.get('wins', 0) / max(1, vampire.get('wins', 0) + vampire.get('losses', 0))) * 100, 1)}%**",
        inline=True
    )
    
    embed.add_field(
        name="Power Progression",
        value=f"Total Gained: **+{vampire.get('total_power_gained', 0)}**\n"
              f"Total Lost: **-{vampire.get('total_power_lost', 0)}**\n"
              f"Net Change: **{vampire.get('total_power_gained', 0) - vampire.get('total_power_lost', 0):+d}**",
        inline=True
    )
    
    embed.add_field(
        name="Origin",
        value=f"Born from {vampire['origin']}",
        inline=False
    )
    
    embed.add_field(
        name="Dark Gift",
        value=f"Possesses {vampire['power']}",
        inline=False
    )
    
    embed.add_field(
        name="Fatal Flaw",
        value=f"However, {vampire['weakness']}",
        inline=False
    )
    
    embed.add_field(
        name="Nature",
        value=vampire['personality'].capitalize(),
        inline=False
    )
    
    # Check if this vampire was created from soul transfer
    if "transferred_from" in vampire:
        embed.add_field(
            name="Soul Transfer Legacy",
            value=f"Created from the souls of vampires ``{vampire['transferred_from'][0]}`` and ``{vampire['transferred_from'][1]}``",
            inline=False
        )
    
    # Calculate created time
    created_at = datetime.fromisoformat(vampire['created_at'])
    embed.set_footer(text=f"Created on {created_at.strftime('%B %d, %Y')}")
    embed.timestamp = datetime.now()
    
    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    # Try to load from .env file (for local development)
    load_dotenv()
    
    # Get token from environment (works for both local and Railway)
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found!")
        print("For local: Create a .env file with DISCORD_TOKEN=your_token")
        print("For Railway: Add DISCORD_TOKEN in the Variables tab")
    else:
        print("Token found! Starting bot...")
        bot.run(TOKEN)
