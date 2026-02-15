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

# Name pools
FIRST_NAMES = [
    "Axel", "Blaze", "Drake", "Ember", "Frost", "Gale", "Hunter", "Iron",
    "Jade", "Kane", "Luna", "Magnus", "Nova", "Onyx", "Phoenix", "Raven",
    "Shadow", "Storm", "Titan", "Vex", "Wolf", "Zane", "Ash", "Blade",
    "Crimson", "Dante", "Echo", "Flint", "Hawk", "Iris", "Jett", "Kai",
    "Lyra", "Maximus", "Nyx", "Orion", "Pierce", "Quinn", "Rex", "Sage",
    "Thorn", "Viper", "Zara", "Atlas", "Celeste", "Dusk", "Elektra", "Fang",
    "Glacier", "Havoc", "Inferno", "Jinx"
]

LAST_NAMES = [
    "Blackwood", "Stormborn", "Ironheart", "Shadowfang", "Firebrand", "Frostbane",
    "Thunderstrike", "Nightshade", "Bloodmoon", "Steelheart", "Darkblade", "Windwalker",
    "Stormbringer", "Flamekeeper", "Icebreaker", "Thunderfist", "Shadowclaw", "Ironfist",
    "Nightwing", "Bloodstone", "Stormrider", "Fireborn", "Frostforge", "Thunderbolt",
    "Darkheart", "Windstorm", "Stormguard", "Flameheart", "Icestorm", "Nightbringer",
    "Bloodfang", "Steelborn", "Darkstorm", "Windblade", "Stormcaller", "Firewalker",
    "Frostheart", "Thunderborn", "Shadowborn", "Ironborn", "Nightfall", "Bloodreaper",
    "Stormforge", "Firestorm", "Iceborn", "Thunderclaw", "Darkfire", "Windborne",
    "Stormbreaker", "Flamebringer"
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

# Generate unique 6-digit ID
def generate_unique_id():
    characters = load_characters()
    existing_ids = [char.get('character_id') for char in characters.values() if 'character_id' in char]
    
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing_ids:
            return new_id

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
    """Generate a unique character with random name, skills and power level"""
    
    user_id = str(ctx.author.id)
    
    # Check if user already has a character
    if user_id in characters:
        char = characters[user_id]
        
        # Display existing character
        embed = discord.Embed(
            title=char['name'],
            description=f"Owner: {ctx.author.name}\nID: `{char['character_id']}`",
            color=discord.Color.red()
        )
        
        embed.add_field(name="Power Level", value=f"{char['power_level']}", inline=False)
        
        skills_text = "\n".join([f"- {skill}" for skill in char['skills']])
        embed.add_field(name="Skills", value=skills_text, inline=False)
        
        await ctx.send(embed=embed)
        return
    
    # Generate random character name
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    character_name = f"{first_name} {last_name}"
    
    # Generate unique character ID
    character_id = generate_unique_id()
    
    # Generate random power level (10 to 100)
    power_level = random.randint(10, 100)
    
    # Generate 3-5 random unique skills
    num_skills = random.randint(3, 5)
    selected_skills = random.sample(SKILLS, num_skills)
    
    # Create character data
    character_data = {
        "character_id": character_id,
        "name": character_name,
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
        title=character_name,
        description=f"Owner: {ctx.author.name}\nID: `{character_id}`",
        color=discord.Color.green()
    )
    
    embed.add_field(name="Power Level", value=f"{power_level}", inline=False)
    
    skills_text = "\n".join([f"- {skill}" for skill in selected_skills])
    embed.add_field(name="Skills", value=skills_text, inline=False)
    
    await ctx.send(embed=embed)

# Show command - Shows your character
@bot.command(name='show')
async def show_character(ctx):
    """Show your character"""
    
    user_id = str(ctx.author.id)
    
    # Check if user has a character
    if user_id not in characters:
        await ctx.send("You don't have a character yet! Use `?make` to create one.")
        return
    
    char = characters[user_id]
    
    # Display character
    embed = discord.Embed(
        title=char['name'],
        description=f"Owner: {ctx.author.name}\nID: `{char['character_id']}`",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="Power Level", value=f"{char['power_level']}", inline=False)
    
    skills_text = "\n".join([f"- {skill}" for skill in char['skills']])
    embed.add_field(name="Skills", value=skills_text, inline=False)
    
    await ctx.send(embed=embed)

# Fight command - Fight random AI characters
@bot.command(name='fight')
async def fight_character(ctx):
    """Fight a random AI character - you can win or lose!"""
    
    user_id = str(ctx.author.id)
    
    # Check if user has a character
    if user_id not in characters:
        await ctx.send("You don't have a character yet! Use `?make` to create one.")
        return
    
    player_char = characters[user_id]
    
    # Generate random AI opponent
    ai_first_name = random.choice(FIRST_NAMES)
    ai_last_name = random.choice(LAST_NAMES)
    ai_name = f"{ai_first_name} {ai_last_name}"
    ai_power_level = random.randint(10, 100)
    ai_num_skills = random.randint(3, 5)
    ai_skills = random.sample(SKILLS, ai_num_skills)
    
    # Battle embed - show both fighters
    battle_embed = discord.Embed(
        title="BATTLE START",
        description="The fight is about to begin!",
        color=discord.Color.orange()
    )
    
    battle_embed.add_field(
        name=f"{player_char['name']} (YOU)",
        value=f"Power Level: {player_char['power_level']}\nSkills: {', '.join(player_char['skills'][:2])}...",
        inline=True
    )
    
    battle_embed.add_field(
        name=f"{ai_name} (AI)",
        value=f"Power Level: {ai_power_level}\nSkills: {', '.join(ai_skills[:2])}...",
        inline=True
    )
    
    await ctx.send(embed=battle_embed)
    
    # Calculate win chance based on power levels
    player_power = player_char['power_level']
    total_power = player_power + ai_power_level
    player_win_chance = (player_power / total_power) * 100
    
    # Add some randomness (30% random factor)
    random_factor = random.randint(-15, 15)
    final_win_chance = max(10, min(90, player_win_chance + random_factor))
    
    # Determine winner
    roll = random.randint(1, 100)
    player_wins = roll <= final_win_chance
    
    # Result embed
    if player_wins:
        result_embed = discord.Embed(
            title="VICTORY",
            description=f"{player_char['name']} has defeated {ai_name}!",
            color=discord.Color.green()
        )
        
        result_embed.add_field(name="Your Power Level", value=f"{player_power}", inline=True)
        result_embed.add_field(name="Enemy Power Level", value=f"{ai_power_level}", inline=True)
        result_embed.add_field(name="Win Chance", value=f"{final_win_chance:.1f}%", inline=True)
        result_embed.add_field(
            name="Battle Summary",
            value=f"{player_char['name']} emerged victorious and lives to fight another day!",
            inline=False
        )
        
        await ctx.send(embed=result_embed)
    else:
        result_embed = discord.Embed(
            title="DEFEAT",
            description=f"{player_char['name']} has been defeated by {ai_name}!",
            color=discord.Color.red()
        )
        
        result_embed.add_field(name="Your Power Level", value=f"{player_power}", inline=True)
        result_embed.add_field(name="Enemy Power Level", value=f"{ai_power_level}", inline=True)
        result_embed.add_field(name="Win Chance", value=f"{final_win_chance:.1f}%", inline=True)
        result_embed.add_field(
            name="Battle Summary",
            value=f"{player_char['name']} has fallen in battle and is no more...\n\nYour character has been deleted. Use `?make` to create a new one.",
            inline=False
        )
        
        await ctx.send(embed=result_embed)
        
        # Delete the character
        del characters[user_id]
        save_characters(characters)

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
