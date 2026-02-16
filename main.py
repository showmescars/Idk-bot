import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# ──────────────────────────────────────────────
#  HUMAN GENERATOR
# ──────────────────────────────────────────────

class HumanGenerator:
    def __init__(self):
        self.first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
            "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
            "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
            "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
            "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White",
            "Harris", "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
            "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams"
        ]
        
        self.personality_traits = [
            "Adventurous", "Ambitious", "Analytical", "Artistic", "Assertive", "Calm",
            "Charismatic", "Compassionate", "Confident", "Creative", "Curious", "Determined",
            "Diplomatic", "Energetic", "Enthusiastic", "Friendly", "Generous", "Honest",
            "Humorous", "Imaginative", "Independent", "Intelligent", "Loyal", "Optimistic",
            "Patient", "Practical", "Reliable", "Resourceful", "Spontaneous", "Thoughtful"
        ]
        
        self.hobbies = [
            "Reading", "Gaming", "Cooking", "Photography", "Hiking", "Painting", "Music",
            "Sports", "Traveling", "Gardening", "Writing", "Dancing", "Fishing", "Cycling",
            "Swimming", "Yoga", "Martial Arts", "Chess", "Coding", "Baking", "Crafting",
            "Birdwatching", "Astronomy", "Collecting", "Volunteering", "Meditation"
        ]
        
        self.occupations = [
            "Software Engineer", "Teacher", "Nurse", "Artist", "Accountant", "Chef",
            "Lawyer", "Doctor", "Mechanic", "Writer", "Architect", "Scientist",
            "Marketing Manager", "Electrician", "Pharmacist", "Graphic Designer",
            "Police Officer", "Firefighter", "Pilot", "Entrepreneur", "Veterinarian",
            "Psychologist", "Engineer", "Consultant", "Photographer", "Musician"
        ]

    def generate_human(self):
        """Generate a random human with stats"""
        name = f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
        age = random.randint(18, 80)
        gender = random.choice(["Male", "Female", "Non-binary"])
        
        # Core stats (out of 100)
        strength = random.randint(1, 100)
        intelligence = random.randint(1, 100)
        charisma = random.randint(1, 100)
        agility = random.randint(1, 100)
        wisdom = random.randint(1, 100)
        luck = random.randint(1, 100)
        
        # Secondary stats
        health = random.randint(50, 100)
        stamina = random.randint(50, 100)
        
        # Personality & Life
        personality = random.sample(self.personality_traits, 3)
        hobbies = random.sample(self.hobbies, random.randint(2, 4))
        occupation = random.choice(self.occupations)
        
        return {
            "name": name,
            "age": age,
            "gender": gender,
            "occupation": occupation,
            "stats": {
                "strength": strength,
                "intelligence": intelligence,
                "charisma": charisma,
                "agility": agility,
                "wisdom": wisdom,
                "luck": luck,
                "health": health,
                "stamina": stamina
            },
            "personality": personality,
            "hobbies": hobbies
        }

# ──────────────────────────────────────────────
#  GLOBAL CHECK - block DMs
# ──────────────────────────────────────────────

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("❌ Commands can only be used in servers, not DMs.")
        return False
    return True

# ──────────────────────────────────────────────
#  EVENTS
# ──────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is online and ready.')
    print(f'📊 Connected to {len(bot.guilds)} server(s)')
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="?make to create humans"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        pass
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        embed = discord.Embed(
            title="⚠️ Error Occurred",
            description=f"```{str(error)}```",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

# ──────────────────────────────────────────────
#  COMMANDS
# ──────────────────────────────────────────────

def get_stat_bar(value, max_value=100):
    """Create a visual bar for stats"""
    filled = int((value / max_value) * 10)
    bar = "█" * filled + "░" * (10 - filled)
    return f"{bar} {value}/{max_value}"

def get_stat_color(value):
    """Get color based on stat value"""
    if value >= 80:
        return "🟢"
    elif value >= 60:
        return "🟡"
    elif value >= 40:
        return "🟠"
    else:
        return "🔴"

@bot.command(name='make')
async def make(ctx):
    """Generate a random human with full stats"""
    
    generator = HumanGenerator()
    human = generator.generate_human()
    
    # Create embed
    embed = discord.Embed(
        title=f"👤 {human['name']}",
        description=f"*{human['occupation']}*",
        color=discord.Color.blue()
    )
    
    # Basic Info
    embed.add_field(
        name="📋 Basic Information",
        value=(
            f"**Age:** {human['age']}\n"
            f"**Gender:** {human['gender']}\n"
            f"**Occupation:** {human['occupation']}"
        ),
        inline=False
    )
    
    # Core Stats
    stats = human['stats']
    embed.add_field(
        name="⚔️ Core Stats",
        value=(
            f"{get_stat_color(stats['strength'])} **Strength:** {get_stat_bar(stats['strength'])}\n"
            f"{get_stat_color(stats['intelligence'])} **Intelligence:** {get_stat_bar(stats['intelligence'])}\n"
            f"{get_stat_color(stats['charisma'])} **Charisma:** {get_stat_bar(stats['charisma'])}\n"
            f"{get_stat_color(stats['agility'])} **Agility:** {get_stat_bar(stats['agility'])}\n"
            f"{get_stat_color(stats['wisdom'])} **Wisdom:** {get_stat_bar(stats['wisdom'])}\n"
            f"{get_stat_color(stats['luck'])} **Luck:** {get_stat_bar(stats['luck'])}"
        ),
        inline=False
    )
    
    # Secondary Stats
    embed.add_field(
        name="💚 Health & Stamina",
        value=(
            f"❤️ **Health:** {get_stat_bar(stats['health'])}\n"
            f"⚡ **Stamina:** {get_stat_bar(stats['stamina'])}"
        ),
        inline=False
    )
    
    # Personality
    embed.add_field(
        name="🎭 Personality Traits",
        value=", ".join(human['personality']),
        inline=False
    )
    
    # Hobbies
    embed.add_field(
        name="🎨 Hobbies & Interests",
        value=", ".join(human['hobbies']),
        inline=False
    )
    
    # Calculate overall rating
    avg_stats = sum(stats.values()) / len(stats)
    if avg_stats >= 75:
        rating = "S-Tier ⭐⭐⭐"
    elif avg_stats >= 60:
        rating = "A-Tier ⭐⭐"
    elif avg_stats >= 40:
        rating = "B-Tier ⭐"
    else:
        rating = "C-Tier"
    
    embed.set_footer(text=f"Overall Rating: {rating} | Requested by {ctx.author}")
    
    await ctx.send(embed=embed)


@bot.command(name='help')
async def help_command(ctx):
    """Show help information"""
    embed = discord.Embed(
        title="🤖 Human Generator Bot",
        description="Generate random humans with detailed stats and characteristics!",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="📝 Commands",
        value=(
            "`?make` - Generate a random human with full stats\n"
            "`?help` - Show this help message\n"
            "`?ping` - Check bot latency"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 Stats Explained",
        value=(
            "**Strength** - Physical power\n"
            "**Intelligence** - Mental capacity\n"
            "**Charisma** - Social skills\n"
            "**Agility** - Speed & reflexes\n"
            "**Wisdom** - Experience & judgment\n"
            "**Luck** - Fortune & chance\n"
            "**Health** - Physical wellbeing\n"
            "**Stamina** - Endurance"
        ),
        inline=False
    )
    
    embed.set_footer(text="Have fun creating random humans!")
    
    await ctx.send(embed=embed)


@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: `{latency}ms`",
        color=discord.Color.green() if latency < 100 else discord.Color.orange()
    )
    await ctx.send(embed=embed)


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("❌ ERROR: DISCORD_TOKEN not found in .env!")
        print("Please create a .env file with: DISCORD_TOKEN=your_token_here")
    else:
        print("✅ Token found! Starting bot...")
        try:
            bot.run(TOKEN)
        except discord.LoginFailure:
            print("❌ Invalid token! Please check your DISCORD_TOKEN in .env")
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
