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
ACCOUNTS_FILE = 'accounts.json'
LOGS_FILE = 'claim_logs.json'
CREDITS_FILE = 'credits.json'
WHITELIST_FILE = 'whitelist.json'

# Blocked channel ID
BLOCKED_CHANNEL_ID = 1470843481177198876

# Credit settings
STARTING_CREDITS = 15
GEN_COST = 5

# Load accounts
def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save accounts
def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=4)

# Load logs
def load_logs():
    if os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save logs
def save_logs(logs):
    with open(LOGS_FILE, 'w') as f:
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

# Load whitelist
def load_whitelist():
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, 'r') as f:
            return json.load(f)
    return []

# Save whitelist
def save_whitelist(whitelist):
    with open(WHITELIST_FILE, 'w') as f:
        json.dump(whitelist, f, indent=4)

accounts = load_accounts()
logs = load_logs()
credits = load_credits()
whitelist = load_whitelist()

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Vampire Character Bot Ready')

# Check to block DM commands
@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("🦇 Commands can only be used in servers, not in the shadows of DMs...")
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
    
    # Create embed
    embed = discord.Embed(
        title=f"🦇 {first_name} {last_name} 🦇",
        description=f"*{title}*",
        color=0x8B0000  # Dark red/blood color
    )
    
    embed.add_field(
        name="⚰️ Age",
        value=f"{age} years old",
        inline=True
    )
    
    embed.add_field(
        name="🌙 Origin",
        value=f"Born from {origin}",
        inline=False
    )
    
    embed.add_field(
        name="💀 Dark Gift",
        value=f"Possesses {power}",
        inline=False
    )
    
    embed.add_field(
        name="✝️ Fatal Flaw",
        value=f"However, {weakness}",
        inline=False
    )
    
    embed.add_field(
        name="🎭 Nature",
        value=personality.capitalize(),
        inline=False
    )
    
    # Add atmospheric footer
    embed.set_footer(text="🩸 The night is eternal, and so are we... 🩸")
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
