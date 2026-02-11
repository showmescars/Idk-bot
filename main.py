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
            data = json.load(f)
            # Handle old format with types
            if isinstance(data, dict) and any(isinstance(v, list) for v in data.values()):
                # Flatten all keys into one list
                all_keys = []
                for key_list in data.values():
                    all_keys.extend(key_list)
                return all_keys
            return data if isinstance(data, list) else []
    return []

# Save keys
def save_keys(keys_list):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys_list, f, indent=4)

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

# Check to only allow specific channel per server (except for admins)
@bot.check
async def only_allowed_channel(ctx):
    # Admins can use commands anywhere
    if ctx.author.guild_permissions.administrator:
        return True
    
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
    
    await ctx.send(f"This channel is now set as the bot command channel!\nChannel ID: {ctx.channel.id}")

# Info command
@bot.command(name='i')
async def info_command(ctx):
    """Display all available commands"""
    is_admin = ctx.author.guild_permissions.administrator

    if is_admin:
        info_text = """KEY BOT - COMMANDS

USER COMMANDS:
?key - Generate and claim a key
?stock - Check available keys
?i - Display this command list

ADMIN COMMANDS:
?setchannel - Set current channel as bot channel
?restock - Upload .txt file to add keys
?clear - Clear all keys
?view - View all keys in stock
?announce - Announce restock to @everyone
"""
    else:
        info_text = """KEY BOT - COMMANDS

?key - Generate and claim a key
?stock - Check available keys
?i - Display this command list
"""

    await ctx.send(f"```{info_text}```")

# Restock from file
@bot.command(name='restock')
@commands.has_permissions(administrator=True)
async def restock_from_file(ctx):
    """Restock from a txt file - attach the file when using this command"""
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

    # Add keys to existing stock
    keys.extend(keys_list)
    save_keys(keys)

    await ctx.send(f"Successfully added {len(keys_list)} keys!\nTotal stock: {len(keys)}")

# Clear keys
@bot.command(name='clear')
@commands.has_permissions(administrator=True)
async def clear_keys(ctx):
    """Clear all keys"""
    global keys
    count = len(keys)
    keys = []
    save_keys(keys)

    await ctx.send(f"Cleared {count} keys from stock")

# View stock
@bot.command(name='view')
@commands.has_permissions(administrator=True)
async def view_stock(ctx):
    """View all keys in stock"""
    if len(keys) == 0:
        await ctx.send("No keys in stock")
        return

    stock_list = "\n".join(keys)

    # Discord has a 2000 character limit, so split if needed
    if len(stock_list) > 1900:
        await ctx.send(f"**Current Stock** ({len(keys)} keys):")
        for i in range(0, len(stock_list), 1900):
            await ctx.send(f"```{stock_list[i:i+1900]}```")
    else:
        await ctx.send(f"**Current Stock** ({len(keys)} keys):\n```{stock_list}```")

# Check stock
@bot.command(name='stock')
async def check_stock(ctx):
    """Check available stock"""
    await ctx.send(f"**CURRENT STOCK:** {len(keys)} keys available")

# Generate/Claim a key
@bot.command(name='key')
async def generate_key(ctx):
    """Generate and claim a key"""
    if len(keys) == 0:
        await ctx.send("No keys available in stock!")
        return
    
    # Get a random key
    claimed_key = random.choice(keys)
    keys.remove(claimed_key)
    save_keys(keys)

    # Send key via DM
    try:
        await ctx.author.send(f"``{claimed_key}``")
        await ctx.send(f"{ctx.author.mention} Check your DMs!")
    except:
        await ctx.send(f"{ctx.author.mention} I couldn't DM you. Please enable DMs and try again!")

# Announce restock
@bot.command(name='announce')
@commands.has_permissions(administrator=True)
async def announce_restock(ctx):
    """Announce a restock"""
    if len(keys) == 0:
        await ctx.send("No stock available to announce")
        return

    stock_count = len(keys)

    announcement = f"@everyone\n\n**RESTOCK ALERT**\n\nKeys are now available!\n\nStock: {stock_count} keys\n\nUse `?key` to get yours!"

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
