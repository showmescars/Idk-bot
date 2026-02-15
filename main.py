import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime
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

# Blocked channel ID
BLOCKED_CHANNEL_ID = 1470843481177198876

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

# Generate unique 6-digit ID
def generate_vampire_id(vampires):
    while True:
        vampire_id = str(random.randint(100000, 999999))
        if vampire_id not in vampires:
            return vampire_id

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

# Make command - Vampire character creator
@bot.command(name='make')
async def make_vampire(ctx):
    """Create a random vampire character with backstory"""
    
    # Vampire name components
    first_names = [
        "Vladislav", "Crimson", "Nocturne", "Draven", "Lazarus", 
        "Seraphina", "Raven", "Lucian", "Morgana", "Viktor",
        "Evangeline", "Thorne", "Lilith", "Dante", "Isolde",
        "Damien", "Celeste", "Raphael", "Selene", "Corvus"
    ]
    
    last_names = [
        "Bloodworth", "Nightshade", "Darkmore", "Ravencroft", "Blackthorn",
        "Shadowmere", "Duskwood", "Grimwood", "Moonwhisper", "Darkholme",
        "Bloodmoon", "Nightbane", "Ashenmoor", "Crowley", "Blackwell"
    ]
    
    titles = [
        "The Eternal", "The Cursed", "The Ancient", "The Forsaken", "The Immortal",
        "The Undying", "The Bloodthirsty", "The Shadowed", "The Forgotten", "The Damned",
        "Lord of Shadows", "Mistress of Night", "The Moonborn", "The Nightstalker", "The Pale"
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
        "a cursed bloodline dating back to the Crusades"
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
        "the ability to drain life force from a distance"
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
        "cursed to feel the pain of every life they've taken"
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
        "calculating and strategic, playing the long game of immortality"
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
        "earned_titles": []
    }
    
    vampires[vampire_id] = vampire_data
    save_vampires(vampires)
    
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
    
    embed.set_footer(text="The night is eternal, and so are we...")
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
    
    # Generate AI opponent
    ai_names = ["Marcus the Merciless", "Elena the Ruthless", "Drakon the Savage", 
                "Nyx the Deadly", "Kain the Brutal", "Sable the Vicious",
                "Cyrus the Cruel", "Morrigan the Fierce", "Vex the Relentless",
                "Azrael the Destroyer"]
    
    ai_name = random.choice(ai_names)
    ai_power = random.randint(80, 150)
    
    player_power = player_vampire["power_level"]
    
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
    
    # Battle narrative
    battle_actions = [
        "lunges forward with supernatural speed",
        "unleashes a torrent of dark magic",
        "transforms into mist to dodge an attack",
        "strikes with ancient fury",
        "summons shadows to bind their opponent",
        "moves with predatory grace",
        "channels centuries of bloodlust",
        "delivers a devastating blow"
    ]
    
    embed = discord.Embed(
        title="BATTLE OF THE DAMNED",
        color=0x8B0000
    )
    
    embed.add_field(
        name="Your Vampire",
        value=f"**{player_vampire['first_name']} {player_vampire['last_name']}**\nPower: {player_power}",
        inline=True
    )
    
    embed.add_field(
        name="Opponent",
        value=f"**{ai_name}**\nPower: {ai_power}",
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
        power_gain = random.randint(5, 15)
        player_vampire["power_level"] += power_gain
        player_vampire["wins"] = player_vampire.get("wins", 0) + 1
        
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
                "The Immortal King"
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
        value=f"Wins: {player_vampire.get('wins', 0)} | Losses: {player_vampire.get('losses', 0)}",
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
            
            # Check for earned titles
            earned_titles = vdata.get('earned_titles', [])
            title_display = f" - {earned_titles[0]}" if earned_titles else ""
            
            alive_list += f"``{vid}`` - **{name}**{title_display}\n"
            alive_list += f"Power: {power} | Record: {wins}W - {losses}L\n\n"
        
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
            
            # Check for earned titles
            earned_titles = vdata.get('earned_titles', [])
            title_display = f" - {earned_titles[0]}" if earned_titles else ""
            
            dead_list += f"``{vid}`` - **{name}**{title_display} [FALLEN]\n"
            dead_list += f"Final Record: {wins}W - {losses}L\n\n"
        
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
