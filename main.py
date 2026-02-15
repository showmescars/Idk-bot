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
CHARACTERS_FILE = 'characters.json'

# Skills pool
SKILLS = [
    "Super Strength", "Speed Blitz", "Fire Manipulation", "Ice Control",
    "Lightning Strike", "Telekinesis", "Shadow Step", "Regeneration",
    "Energy Blast", "Force Field", "Mind Reading", "Invisibility",
    "Flight", "Time Slow", "Earth Manipulation", "Wind Control",
    "Laser Vision", "Berserker Rage", "Illusion Casting", "Poison Touch",
    "Gravity Control", "Weapon Mastery", "Martial Arts Expert", "Super Durability",
    "Sonic Scream", "Acid Spit", "Diamond Skin", "Shapeshifting",
    "Teleportation", "Blood Manipulation", "Bone Control", "Metal Bending",
    "Plant Growth", "Water Bending", "Explosion", "Petrification",
    "Curse", "Healing Touch", "Absorption", "Cloning"
]

# Load characters
def load_characters():
    if os.path.exists(CHARACTERS_FILE):
        with open(CHARACTERS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save characters
def save_characters(characters):
    with open(CHARACTERS_FILE, 'w') as f:
        json.dump(characters, f, indent=4)

characters = load_characters()

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Character Generator Ready')

# Check to block DM commands
@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True

# Make command - Creates a character
@bot.command(name='make')
async def make_character(ctx):
    """Generate a unique character with random skills and power level"""
    
    user_id = str(ctx.author.id)
    
    # Check if user already has a character
    if user_id in characters:
        char = characters[user_id]
        
        # Display existing character
        embed = discord.Embed(
            title=f"{ctx.author.name}'s Character",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Power Level", value=f"{char['power_level']}", inline=False)
        
        skills_text = "\n".join([f"- {skill}" for skill in char['skills']])
        embed.add_field(name="Skills", value=skills_text, inline=False)
        
        await ctx.send(embed=embed)
        return
    
    # Generate random power level (10 to 100)
    power_level = random.randint(10, 100)
    
    # Generate 3-5 random unique skills
    num_skills = random.randint(3, 5)
    selected_skills = random.sample(SKILLS, num_skills)
    
    # Create character data
    character_data = {
        "username": str(ctx.author),
        "user_id": user_id,
        "power_level": power_level,
        "skills": selected_skills,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save character
    characters[user_id] = character_data
    save_characters(characters)
    
    # Display new character
    embed = discord.Embed(
        title=f"{ctx.author.name}'s Character",
        color=discord.Color.green()
    )
    
    embed.add_field(name="Power Level", value=f"{power_level}", inline=False)
    
    skills_text = "\n".join([f"- {skill}" for skill in selected_skills])
    embed.add_field(name="Skills", value=skills_text, inline=False)
    
    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found!")
        print("For local: Create a .env file with DISCORD_TOKEN=your_token")
        print("For Railway: Add DISCORD_TOKEN in the Variables tab")
    else:
        print("Token found! Starting bot...")
        bot.run(TOKEN)
