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

# Generate unique 6-digit ID
def generate_vampire_id(vampires):
    while True:
        vampire_id = str(random.randint(100000, 999999))
        if vampire_id not in vampires:
            return vampire_id

vampires = load_vampires()

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
        "created_at": datetime.now().isoformat()
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
