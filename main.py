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

# Generate AI opponent with DYNAMIC and VARIED power levels
def generate_ai_opponent(player_power):
    """Generate an AI opponent with truly random power variance - NOT always matched"""
    
    # Expanded AI names pool
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
        "Isolde the Vengeful", "Draven the Malevolent", "Xander the Apostate",
        "Thorn the Bloodthirsty", "Raven the Nightstalker", "Viktor the Unholy",
        "Lilith the Temptress", "Vladmir the Impaler", "Selene the Moonborn"
    ]
    
    # DYNAMIC POWER SCALING - Multiple tiers with different probabilities
    # This creates varied matchups instead of always matched opponents
    
    roll = random.randint(1, 100)
    
    if roll <= 15:  # 15% chance - Much weaker opponent (easy win)
        min_power = max(50, int(player_power * 0.30))
        max_power = max(80, int(player_power * 0.60))
        difficulty = "Weak"
        
    elif roll <= 35:  # 20% chance - Weaker opponent
        min_power = max(60, int(player_power * 0.60))
        max_power = max(90, int(player_power * 0.85))
        difficulty = "Below Average"
        
    elif roll <= 65:  # 30% chance - Fairly matched (±15%)
        min_power = max(70, int(player_power * 0.85))
        max_power = int(player_power * 1.15)
        difficulty = "Matched"
        
    elif roll <= 85:  # 20% chance - Stronger opponent
        min_power = int(player_power * 1.15)
        max_power = int(player_power * 1.50)
        difficulty = "Strong"
        
    else:  # 15% chance - Much stronger opponent (challenge)
        min_power = int(player_power * 1.50)
        max_power = int(player_power * 2.00)
        difficulty = "Powerful"
    
    # Ensure bounds
    min_power = max(50, min(min_power, 100000))
    max_power = max(min_power + 10, min(max_power, 100000))
    
    # Generate final AI power with some randomness within the range
    ai_power = random.randint(min_power, max_power)
    
    # Add additional random variance (±5%) to make it less predictable
    variance = random.uniform(0.95, 1.05)
    ai_power = int(ai_power * variance)
    
    # Final bounds check
    ai_power = max(50, min(ai_power, 100000))
    
    ai_opponent = {
        "name": random.choice(ai_names),
        "power": ai_power,
        "difficulty": difficulty,
        "is_ai": True
    }
    
    return ai_opponent

# Generate random starting power for new vampires (MORE VARIED)
def generate_starting_power():
    """Generate varied starting power - not always the same"""
    
    # Multiple tiers for starting power
    roll = random.randint(1, 100)
    
    if roll <= 40:  # 40% chance - Low starter
        return random.randint(80, 120)
    elif roll <= 75:  # 35% chance - Medium starter
        return random.randint(120, 180)
    elif roll <= 95:  # 20% chance - High starter
        return random.randint(180, 250)
    else:  # 5% chance - Lucky starter
        return random.randint(250, 350)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is ready to battle!')

@bot.command(name='make')
async def make_vampire(ctx):
    """Create a new vampire with VARIED starting power"""
    
    # Block command in specific channel
    if ctx.channel.id == BLOCKED_CHANNEL_ID:
        await ctx.send("❌ This command is disabled in this channel.")
        return
    
    vampires = load_vampires()
    user_id = str(ctx.author.id)
    
    # Check if user already has a vampire
    if user_id in vampires:
        await ctx.send(f"❌ You already have a vampire! Use `?stats` to view it.")
        return
    
    # Generate varied starting power
    starting_power = generate_starting_power()
    
    # Create new vampire
    vampire_id = generate_vampire_id(vampires)
    vampires[user_id] = {
        "id": vampire_id,
        "username": ctx.author.name,
        "power": starting_power,
        "wins": 0,
        "losses": 0,
        "created_at": datetime.now().isoformat()
    }
    
    save_vampires(vampires)
    
    embed = discord.Embed(
        title="🧛 Vampire Created!",
        description=f"**{ctx.author.name}** has risen from the shadows!",
        color=discord.Color.red()
    )
    embed.add_field(name="Vampire ID", value=f"`{vampire_id}`", inline=True)
    embed.add_field(name="Power Level", value=f"⚡ **{starting_power}**", inline=True)
    embed.add_field(name="Record", value="0-0", inline=True)
    embed.set_footer(text="Use ?fight to battle other vampires!")
    
    await ctx.send(embed=embed)

@bot.command(name='stats')
async def show_stats(ctx, member: discord.Member = None):
    """Show vampire stats for yourself or another user"""
    
    target = member or ctx.author
    vampires = load_vampires()
    user_id = str(target.id)
    
    if user_id not in vampires:
        await ctx.send(f"❌ {target.name} doesn't have a vampire yet! Use `?make` to create one.")
        return
    
    vampire = vampires[user_id]
    total_battles = vampire["wins"] + vampire["losses"]
    win_rate = (vampire["wins"] / total_battles * 100) if total_battles > 0 else 0
    
    embed = discord.Embed(
        title=f"🧛 {target.name}'s Vampire Stats",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="Vampire ID", value=f"`{vampire['id']}`", inline=True)
    embed.add_field(name="Power Level", value=f"⚡ **{vampire['power']}**", inline=True)
    embed.add_field(name="Record", value=f"🏆 {vampire['wins']}W - {vampire['losses']}L", inline=True)
    embed.add_field(name="Win Rate", value=f"📊 {win_rate:.1f}%", inline=True)
    embed.add_field(name="Total Battles", value=f"⚔️ {total_battles}", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='fight')
async def fight(ctx):
    """Fight an AI opponent with DYNAMIC power scaling"""
    
    # Block command in specific channel
    if ctx.channel.id == BLOCKED_CHANNEL_ID:
        await ctx.send("❌ This command is disabled in this channel.")
        return
    
    vampires = load_vampires()
    user_id = str(ctx.author.id)
    
    # Check if user has a vampire
    if user_id not in vampires:
        await ctx.send("❌ You need to create a vampire first! Use `?make` to create one.")
        return
    
    # Check credits
    current_credits, time_remaining = check_credits(user_id)
    
    if current_credits == 0:
        minutes = int(time_remaining.total_seconds() // 60)
        seconds = int(time_remaining.total_seconds() % 60)
        await ctx.send(f"❌ You're out of fight credits! Next refill in **{minutes}m {seconds}s**")
        return
    
    # Use a credit
    use_credit(user_id)
    remaining_credits = current_credits - 1
    
    player_vampire = vampires[user_id]
    player_power = player_vampire["power"]
    
    # Generate DYNAMIC AI opponent
    ai_opponent = generate_ai_opponent(player_power)
    ai_power = ai_opponent["power"]
    
    # Battle calculation with some randomness
    power_diff = player_power - ai_power
    
    # Base win chance based on power difference
    if power_diff > 0:
        win_chance = 50 + min(40, power_diff / player_power * 100)
    else:
        win_chance = 50 - min(40, abs(power_diff) / ai_power * 100)
    
    # Add randomness factor (±10%)
    win_chance = max(5, min(95, win_chance + random.uniform(-10, 10)))
    
    # Determine battle outcome
    battle_result = random.random() * 100 < win_chance
    
    # Power gain/loss with VARIED amounts
    if battle_result:  # Player wins
        # Bigger rewards for beating stronger opponents
        if ai_opponent["difficulty"] == "Weak":
            power_gain = random.randint(2, 5)
        elif ai_opponent["difficulty"] == "Below Average":
            power_gain = random.randint(5, 10)
        elif ai_opponent["difficulty"] == "Matched":
            power_gain = random.randint(8, 15)
        elif ai_opponent["difficulty"] == "Strong":
            power_gain = random.randint(15, 25)
        else:  # Powerful
            power_gain = random.randint(25, 40)
        
        vampires[user_id]["power"] += power_gain
        vampires[user_id]["wins"] += 1
        result_color = discord.Color.green()
        result_emoji = "🎉"
        result_text = "VICTORY!"
        power_change = f"+{power_gain}"
        
    else:  # Player loses
        # Smaller losses for losing to stronger opponents
        if ai_opponent["difficulty"] == "Weak":
            power_loss = random.randint(8, 15)
        elif ai_opponent["difficulty"] == "Below Average":
            power_loss = random.randint(5, 12)
        elif ai_opponent["difficulty"] == "Matched":
            power_loss = random.randint(3, 8)
        elif ai_opponent["difficulty"] == "Strong":
            power_loss = random.randint(2, 5)
        else:  # Powerful
            power_loss = random.randint(1, 3)
        
        vampires[user_id]["power"] = max(50, vampires[user_id]["power"] - power_loss)
        vampires[user_id]["losses"] += 1
        result_color = discord.Color.red()
        result_emoji = "💀"
        result_text = "DEFEAT!"
        power_change = f"-{power_loss}"
    
    save_vampires(vampires)
    
    # Log battle
    battle_log = {
        "timestamp": datetime.now().isoformat(),
        "player": ctx.author.name,
        "player_power": player_power,
        "opponent": ai_opponent["name"],
        "opponent_power": ai_power,
        "difficulty": ai_opponent["difficulty"],
        "winner": ctx.author.name if battle_result else ai_opponent["name"],
        "power_change": power_change
    }
    
    logs = load_battle_logs()
    logs.append(battle_log)
    save_battle_logs(logs)
    
    # Create battle embed
    embed = discord.Embed(
        title=f"{result_emoji} {result_text}",
        description=f"**{ctx.author.name}** vs **{ai_opponent['name']}**",
        color=result_color
    )
    
    embed.add_field(
        name="Your Power",
        value=f"⚡ {player_power}",
        inline=True
    )
    embed.add_field(
        name="Opponent Power",
        value=f"⚡ {ai_power}",
        inline=True
    )
    embed.add_field(
        name="Difficulty",
        value=f"🎯 {ai_opponent['difficulty']}",
        inline=True
    )
    embed.add_field(
        name="Power Change",
        value=f"📊 {power_change}",
        inline=True
    )
    embed.add_field(
        name="New Power",
        value=f"⚡ {vampires[user_id]['power']}",
        inline=True
    )
    embed.add_field(
        name="Credits Left",
        value=f"🎫 {remaining_credits}/{MAX_CREDITS}",
        inline=True
    )
    
    # Add win chance indicator
    embed.set_footer(text=f"Win chance was {win_chance:.1f}% | Power diff: {power_diff:+d}")
    
    await ctx.send(embed=embed)

@bot.command(name='credits')
async def check_fight_credits(ctx):
    """Check your remaining fight credits and cooldown"""
    
    user_id = str(ctx.author.id)
    current_credits, time_remaining = check_credits(user_id)
    
    embed = discord.Embed(
        title="🎫 Fight Credits",
        description=f"**{ctx.author.name}'s Credits**",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Available Credits",
        value=f"🎫 {current_credits}/{MAX_CREDITS}",
        inline=True
    )
    
    if current_credits == 0 and time_remaining:
        minutes = int(time_remaining.total_seconds() // 60)
        seconds = int(time_remaining.total_seconds() % 60)
        embed.add_field(
            name="Next Refill",
            value=f"⏰ {minutes}m {seconds}s",
            inline=True
        )
    elif current_credits < MAX_CREDITS:
        embed.add_field(
            name="Cooldown",
            value=f"Use all credits to start timer",
            inline=True
        )
    else:
        embed.add_field(
            name="Status",
            value=f"✅ Fully Charged!",
            inline=True
        )
    
    embed.set_footer(text=f"Credits refill {CREDIT_COOLDOWN_MINUTES} minutes after reaching 0")
    
    await ctx.send(embed=embed)

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    """Show top 10 vampires by power"""
    
    vampires = load_vampires()
    
    if not vampires:
        await ctx.send("❌ No vampires exist yet! Use `?make` to create one.")
        return
    
    # Sort by power
    sorted_vampires = sorted(
        vampires.items(),
        key=lambda x: x[1]["power"],
        reverse=True
    )[:10]
    
    embed = discord.Embed(
        title="🏆 Vampire Leaderboard",
        description="Top 10 Most Powerful Vampires",
        color=discord.Color.gold()
    )
    
    for i, (user_id, vampire) in enumerate(sorted_vampires, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        
        record = f"{vampire['wins']}W-{vampire['losses']}L"
        embed.add_field(
            name=f"{medal} {vampire['username']}",
            value=f"⚡ Power: **{vampire['power']}** | Record: {record}",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='reset')
@commands.has_permissions(administrator=True)
async def reset_vampire(ctx, member: discord.Member):
    """Admin command to reset a user's vampire"""
    
    vampires = load_vampires()
    user_id = str(member.id)
    
    if user_id not in vampires:
        await ctx.send(f"❌ {member.name} doesn't have a vampire.")
        return
    
    del vampires[user_id]
    save_vampires(vampires)
    
    await ctx.send(f"✅ {member.name}'s vampire has been reset. They can create a new one with `?make`.")

# Run the bot
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("ERROR: No bot token found in environment variables!")
    else:
        bot.run(TOKEN)
