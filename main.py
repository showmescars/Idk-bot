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
KEYS_FILE = 'keys.json'
CONFIG_FILE = 'config.json'

# Load config
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save config
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

config = load_config()

# Load keys
def load_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save keys
def save_keys(keys):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

keys = load_keys()

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Key Bot Ready')

# Check to block DM commands
@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True

# Check to only allow specific channel per server
@bot.check
async def only_allowed_channel(ctx):
    guild_id = str(ctx.guild.id)
    
    # If server not configured, allow all channels
    if guild_id not in config or 'allowed_channel' not in config[guild_id]:
        return True
    
    allowed_channel = config[guild_id]['allowed_channel']
    if ctx.channel.id != allowed_channel:
        return False
    return True

# Set allowed channel (admin only)
@bot.command(name='setchannel')
@commands.has_permissions(administrator=True)
async def set_channel(ctx):
    """Set this channel as the allowed channel for bot commands"""
    guild_id = str(ctx.guild.id)
    
    if guild_id not in config:
        config[guild_id] = {}
    
    config[guild_id]['allowed_channel'] = ctx.channel.id
    save_config(config)
    
    await ctx.send(f"✅ This channel is now set as the bot command channel!\nChannel ID: {ctx.channel.id}")

# Info command
@bot.command(name='i')
async def info_command(ctx):
    """Display all available commands"""
    is_admin = ctx.author.guild_permissions.administrator

    if is_admin:
        info_text = """KEY BOT - COMMANDS

USER COMMANDS:
?key - Generate and claim a random key
?stock - Check available keys
?i - Display this command list

ADMIN COMMANDS:
?setchannel - Set current channel as bot channel
?restock <type> - Upload .txt file to add keys
?clear <type> - Clear all keys of a specific type
?view <type> - View all keys in stock for a type
?announce <type> - Announce restock to @everyone
"""
    else:
        info_text = """KEY BOT - COMMANDS

?key - Generate and claim a random key
?stock - Check available keys
?i - Display this command list
"""

    await ctx.send(f"```{info_text}```")

# Restock from file
@bot.command(name='restock')
@commands.has_permissions(administrator=True)
async def restock_from_file(ctx, key_type: str = None):
    """Restock from a txt file - attach the file when using this command"""
    if key_type is None:
        await ctx.send("Usage: ?restock <type> (and attach a .txt file)")
        return

    key_type = key_type.lower()

    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach a .txt file with keys")
        return

    attachment = ctx.message.attachments[0]

    if not attachment.filename.endswith('.txt'):
        await ctx.send("File must be a .txt file")
        return

    # Download and read file
    file_content = await attachment.read()
    keys_list = file_content.decode('utf-8').strip().split('\n')

    # Remove empty lines
    keys_list = [key.strip() for key in keys_list if key.strip()]

    if key_type not in keys:
        keys[key_type] = []

    # Add keys
    keys[key_type].extend(keys_list)
    save_keys(keys)

    await ctx.send(f"Successfully added {len(keys_list)} keys to **{key_type}**\nTotal stock: {len(keys[key_type])}")

# Clear keys
@bot.command(name='clear')
@commands.has_permissions(administrator=True)
async def clear_keys(ctx, key_type: str = None):
    """Clear all keys of a specific type"""
    if key_type is None:
        await ctx.send("Usage: ?clear <type>")
        return

    key_type = key_type.lower()

    if key_type not in keys:
        await ctx.send(f"No keys found for type: **{key_type}**")
        return

    count = len(keys[key_type])
    keys[key_type] = []
    save_keys(keys)

    await ctx.send(f"Cleared {count} keys from **{key_type}**")

# View stock for specific type
@bot.command(name='view')
@commands.has_permissions(administrator=True)
async def view_stock(ctx, key_type: str = None):
    """View all keys in stock for a type"""
    if key_type is None:
        await ctx.send("Usage: ?view <type>")
        return

    key_type = key_type.lower()

    if key_type not in keys or len(keys[key_type]) == 0:
        await ctx.send(f"No keys in stock for **{key_type}**")
        return

    stock_list = "\n".join(keys[key_type])

    # Discord has a 2000 character limit, so split if needed
    if len(stock_list) > 1900:
        await ctx.send(f"**{key_type}** stock ({len(keys[key_type])} keys):")
        for i in range(0, len(stock_list), 1900):
            await ctx.send(f"```{stock_list[i:i+1900]}```")
    else:
        await ctx.send(f"**{key_type}** stock ({len(keys[key_type])} keys):\n```{stock_list}```")

# Check stock
@bot.command(name='stock')
async def check_stock(ctx):
    """Check available stock for all key types"""
    if not keys or all(len(k) == 0 for k in keys.values()):
        await ctx.send("No keys in stock")
        return

    stock_msg = "**CURRENT STOCK:**\n"
    for key_type, key_list in keys.items():
        stock_msg += f"{key_type}: {len(key_list)} available\n"

    await ctx.send(stock_msg)

# Generate/Claim a random key from any available type
@bot.command(name='key')
async def generate_key(ctx):
    """Generate and claim a random key from available stock"""
    # Get all key types that have stock
    available_types = [key_type for key_type, key_list in keys.items() if len(key_list) > 0]
    
    if not available_types:
        await ctx.send("❌ No keys available in stock!")
        return
    
    # Pick a random type
    chosen_type = random.choice(available_types)
    
    # Get a random key from that type
    claimed_key = random.choice(keys[chosen_type])
    keys[chosen_type].remove(claimed_key)
    save_keys(keys)

    # Send key via DM
    try:
        await ctx.author.send(f"**Your {chosen_type} key:**\n```{claimed_key}```")
        await ctx.send(f"{ctx.author.mention} ✅ Check your DMs! You received a **{chosen_type}** key!")
    except:
        await ctx.send(f"{ctx.author.mention} ❌ I couldn't DM you. Please enable DMs and try again!")

# Announce restock
@bot.command(name='announce')
@commands.has_permissions(administrator=True)
async def announce_restock(ctx, key_type: str = None):
    """Announce a restock"""
    if key_type is None:
        await ctx.send("Usage: ?announce <type>")
        return

    key_type = key_type.lower()

    if key_type not in keys or len(keys[key_type]) == 0:
        await ctx.send(f"No stock available for **{key_type}**")
        return

    stock_count = len(keys[key_type])

    announcement = f"@everyone\n\n🎉 **RESTOCK ALERT** 🎉\n\n**{key_type.upper()}** keys are now available!\n\nStock: {stock_count} keys\n\nUse `?key` to get yours!"

    await ctx.send(announcement)

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
