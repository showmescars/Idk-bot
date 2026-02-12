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
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)  # ← DISABLED DEFAULT HELP

# Files
KEYS_FILE = 'keys.json'
CONFIG_FILE = 'config.json'
BLACKLIST_FILE = 'blacklist.json'
CLAIMED_KEYS_FILE = 'claimed_keys.json'
COOLDOWNS_FILE = 'cooldowns.json'

# Spam detection settings - VERY STRICT
SPAM_THRESHOLD = 1  # Number of commands allowed (2 total uses = blacklist)
SPAM_TIMEFRAME = 3  # Timeframe in seconds
user_command_times = {}  # Track user command usage

# Key claim limits
MAX_KEYS_BEFORE_COOLDOWN = 3  # After 3 keys, user gets cooldown
COOLDOWN_DURATION = timedelta(hours=1)  # 1 hour cooldown

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

# Load blacklist
def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'r') as f:
            return json.load(f)
    return []

# Save blacklist
def save_blacklist(blacklist):
    with open(BLACKLIST_FILE, 'w') as f:
        json.dump(blacklist, f, indent=4)

blacklist = load_blacklist()

# Load claimed keys history
def load_claimed_keys():
    if os.path.exists(CLAIMED_KEYS_FILE):
        with open(CLAIMED_KEYS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save claimed keys history
def save_claimed_keys(claimed_keys):
    with open(CLAIMED_KEYS_FILE, 'w') as f:
        json.dump(claimed_keys, f, indent=4)

claimed_keys = load_claimed_keys()

# Load cooldowns
def load_cooldowns():
    if os.path.exists(COOLDOWNS_FILE):
        with open(COOLDOWNS_FILE, 'r') as f:
            data = json.load(f)
            # Convert string timestamps back to datetime objects
            for user_id in data:
                if 'cooldown_until' in data[user_id] and data[user_id]['cooldown_until']:
                    data[user_id]['cooldown_until'] = datetime.fromisoformat(data[user_id]['cooldown_until'])
            return data
    return {}

# Save cooldowns
def save_cooldowns(cooldowns_data):
    # Convert datetime objects to strings for JSON
    data_to_save = {}
    for user_id, info in cooldowns_data.items():
        data_to_save[user_id] = {
            'keys_claimed': info['keys_claimed'],
            'cooldown_until': info['cooldown_until'].isoformat() if info['cooldown_until'] else None,
            'cooldown_violations': info.get('cooldown_violations', 0)
        }
    
    with open(COOLDOWNS_FILE, 'w') as f:
        json.dump(data_to_save, f, indent=4)

cooldowns = load_cooldowns()

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

# Check if user is blacklisted
@bot.check
async def check_blacklist(ctx):
    # Admins bypass blacklist
    if ctx.author.guild_permissions.administrator:
        return True
    
    if ctx.author.id in blacklist:
        await ctx.send(f"{ctx.author.mention} You are blacklisted from using this bot.")
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

# Spam detection function
def check_spam(user_id):
    """Check if user is spamming and return True if they should be blacklisted"""
    current_time = datetime.now()
    
    # Initialize user's command times if not exists
    if user_id not in user_command_times:
        user_command_times[user_id] = []
    
    # Remove old timestamps outside the timeframe
    user_command_times[user_id] = [
        timestamp for timestamp in user_command_times[user_id]
        if current_time - timestamp < timedelta(seconds=SPAM_TIMEFRAME)
    ]
    
    # Add current timestamp
    user_command_times[user_id].append(current_time)
    
    # Check if spam threshold exceeded
    if len(user_command_times[user_id]) > SPAM_THRESHOLD:
        return True
    
    return False

# Check cooldown status
def check_cooldown(user_id):
    """Check if user is on cooldown. Returns (on_cooldown, time_remaining)"""
    user_id_str = str(user_id)
    
    if user_id_str not in cooldowns:
        cooldowns[user_id_str] = {
            'keys_claimed': 0,
            'cooldown_until': None,
            'cooldown_violations': 0
        }
        return False, None
    
    user_data = cooldowns[user_id_str]
    
    # Check if user is currently on cooldown
    if user_data['cooldown_until']:
        if datetime.now() < user_data['cooldown_until']:
            time_remaining = user_data['cooldown_until'] - datetime.now()
            return True, time_remaining
        else:
            # Cooldown expired, reset it
            user_data['cooldown_until'] = None
            user_data['keys_claimed'] = 0
            save_cooldowns(cooldowns)
    
    return False, None

# Update user key claim count
def update_key_claim(user_id):
    """Update user's key claim count and apply cooldown if needed. Returns status."""
    user_id_str = str(user_id)
    
    if user_id_str not in cooldowns:
        cooldowns[user_id_str] = {
            'keys_claimed': 0,
            'cooldown_until': None,
            'cooldown_violations': 0
        }
    
    user_data = cooldowns[user_id_str]
    user_data['keys_claimed'] += 1
    
    # If user has claimed 3 keys, apply cooldown
    if user_data['keys_claimed'] >= MAX_KEYS_BEFORE_COOLDOWN:
        user_data['cooldown_until'] = datetime.now() + COOLDOWN_DURATION
        user_data['keys_claimed'] = 0  # Reset count
        save_cooldowns(cooldowns)
        return 'cooldown_applied'
    
    save_cooldowns(cooldowns)
    return 'normal'

# Handle cooldown violation
def handle_cooldown_violation(user_id):
    """Handle when user tries to claim during cooldown. Returns True if should be blacklisted."""
    user_id_str = str(user_id)
    
    if user_id_str not in cooldowns:
        return False
    
    user_data = cooldowns[user_id_str]
    user_data['cooldown_violations'] = user_data.get('cooldown_violations', 0) + 1
    save_cooldowns(cooldowns)
    
    # If user violated cooldown, blacklist them
    if user_data['cooldown_violations'] >= 1:
        return True
    
    return False

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

# Blacklist a user
@bot.command(name='blacklist')
@commands.has_permissions(administrator=True)
async def blacklist_user(ctx, user_input: str = None):
    """Blacklist a user from using the bot - Usage: ?blacklist @user OR ?blacklist UserID"""
    if user_input is None:
        await ctx.send("Usage: ?blacklist @user OR ?blacklist UserID")
        return
    
    # Try to get user from mention or ID
    user = None
    
    # Check if it's a mention
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    else:
        # Try to treat it as a user ID
        try:
            user_id = int(user_input)
            user = await bot.fetch_user(user_id)
        except (ValueError, discord.NotFound):
            await ctx.send("Invalid user mention or ID! Use ?blacklist @user OR ?blacklist UserID")
            return
    
    # Check if user is an admin (in guild context)
    if ctx.guild and user.id in [m.id for m in ctx.guild.members]:
        member = ctx.guild.get_member(user.id)
        if member and member.guild_permissions.administrator:
            await ctx.send("Cannot blacklist administrators!")
            return
    
    if user.id in blacklist:
        await ctx.send(f"{user.name} (ID: {user.id}) is already blacklisted.")
        return
    
    blacklist.append(user.id)
    save_blacklist(blacklist)
    await ctx.send(f"**{user.name}** (ID: {user.id}) has been blacklisted from using the bot.")

# Unblacklist a user
@bot.command(name='unblacklist')
@commands.has_permissions(administrator=True)
async def unblacklist_user(ctx, user_input: str = None):
    """Remove a user from the blacklist - Usage: ?unblacklist @user OR ?unblacklist UserID"""
    if user_input is None:
        await ctx.send("Usage: ?unblacklist @user OR ?unblacklist UserID")
        return
    
    # Try to get user from mention or ID
    user = None
    
    # Check if it's a mention
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    else:
        # Try to treat it as a user ID
        try:
            user_id = int(user_input)
            user = await bot.fetch_user(user_id)
        except (ValueError, discord.NotFound):
            await ctx.send("Invalid user mention or ID! Use ?unblacklist @user OR ?unblacklist UserID")
            return
    
    if user.id not in blacklist:
        await ctx.send(f"**{user.name}** (ID: {user.id}) is not blacklisted.")
        return
    
    blacklist.remove(user.id)
    save_blacklist(blacklist)
    
    # Clear their spam tracking and cooldown data
    if user.id in user_command_times:
        del user_command_times[user.id]
    
    user_id_str = str(user.id)
    if user_id_str in cooldowns:
        del cooldowns[user_id_str]
        save_cooldowns(cooldowns)
    
    await ctx.send(f"**{user.name}** (ID: {user.id}) has been removed from the blacklist.")

# View blacklist
@bot.command(name='viewblacklist')
@commands.has_permissions(administrator=True)
async def view_blacklist(ctx):
    """View all blacklisted users"""
    if len(blacklist) == 0:
        await ctx.send("No users are blacklisted.")
        return
    
    blacklist_text = "**Blacklisted Users:**\n"
    for user_id in blacklist:
        user = bot.get_user(user_id)
        if user:
            blacklist_text += f"{user.name} (ID: {user_id})\n"
        else:
            blacklist_text += f"Unknown User (ID: {user_id})\n"
    
    await ctx.send(blacklist_text)

# View claimed keys history
@bot.command(name='claimed')
@commands.has_permissions(administrator=True)
async def view_claimed_keys(ctx):
    """View all users who claimed keys"""
    if len(claimed_keys) == 0:
        await ctx.send("No keys have been claimed yet.")
        return
    
    claimed_text = "**Claimed Keys History:**\n\n"
    
    for i, claim in enumerate(claimed_keys, 1):
        user_id = claim['user_id']
        username = claim['username']
        timestamp = claim['timestamp']
        key = claim['key']
        
        claimed_text += f"{i}. {username} (ID: {user_id})\n"
        claimed_text += f"   Key: ``{key}``\n"
        claimed_text += f"   Time: {timestamp}\n\n"
        
        # Discord has message limits, split if needed
        if len(claimed_text) > 1800:
            await ctx.send(claimed_text)
            claimed_text = ""
    
    if claimed_text:
        await ctx.send(claimed_text)

# Clear claimed keys history
@bot.command(name='clearclaimed')
@commands.has_permissions(administrator=True)
async def clear_claimed_history(ctx):
    """Clear all claimed keys history"""
    global claimed_keys
    count = len(claimed_keys)
    
    if count == 0:
        await ctx.send("No claimed keys history to clear.")
        return
    
    claimed_keys = []
    save_claimed_keys(claimed_keys)
    
    await ctx.send(f"✅ Successfully cleared **{count}** claimed keys from history!")

# View user cooldowns (admin)
@bot.command(name='cooldowns')
@commands.has_permissions(administrator=True)
async def view_cooldowns(ctx):
    """View all users on cooldown"""
    active_cooldowns = []
    
    for user_id_str, data in cooldowns.items():
        if data['cooldown_until'] and datetime.now() < data['cooldown_until']:
            user_id = int(user_id_str)
            user = bot.get_user(user_id)
            
            # Get username - try to fetch if not cached
            if user:
                username = user.name
                display_name = str(user)
            else:
                try:
                    user = await bot.fetch_user(user_id)
                    username = user.name
                    display_name = str(user)
                except:
                    username = "Unknown User"
                    display_name = "Unknown User"
            
            time_remaining = data['cooldown_until'] - datetime.now()
            
            # Format time remaining
            hours = int(time_remaining.total_seconds() // 3600)
            minutes = int((time_remaining.total_seconds() % 3600) // 60)
            
            active_cooldowns.append({
                'display_name': display_name,
                'user_id': user_id,
                'time_remaining': f"{hours}h {minutes}m",
                'violations': data.get('cooldown_violations', 0)
            })
    
    if len(active_cooldowns) == 0:
        await ctx.send("No users are currently on cooldown.")
        return
    
    cooldown_text = "**Active Cooldowns:**\n\n"
    for cd in active_cooldowns:
        cooldown_text += f"**{cd['display_name']}** (ID: {cd['user_id']})\n"
        cooldown_text += f"   ⏰ Time Remaining: {cd['time_remaining']}\n"
        cooldown_text += f"   ⚠️ Violations: {cd['violations']}\n\n"
    
    await ctx.send(cooldown_text)

# Reset user cooldown (admin)
@bot.command(name='resetcooldown')
@commands.has_permissions(administrator=True)
async def reset_cooldown(ctx, user_input: str = None):
    """Reset a user's cooldown - Usage: ?resetcooldown @user OR ?resetcooldown UserID"""
    if user_input is None:
        await ctx.send("Usage: ?resetcooldown @user OR ?resetcooldown UserID")
        return
    
    # Try to get user from mention or ID
    user = None
    
    # Check if it's a mention
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    else:
        # Try to treat it as a user ID
        try:
            user_id = int(user_input)
            user = await bot.fetch_user(user_id)
        except (ValueError, discord.NotFound):
            await ctx.send("Invalid user mention or ID! Use ?resetcooldown @user OR ?resetcooldown UserID")
            return
    
    user_id_str = str(user.id)
    
    if user_id_str not in cooldowns or not cooldowns[user_id_str]['cooldown_until']:
        await ctx.send(f"**{user.name}** (ID: {user.id}) is not on cooldown.")
        return
    
    cooldowns[user_id_str]['cooldown_until'] = None
    cooldowns[user_id_str]['keys_claimed'] = 0
    cooldowns[user_id_str]['cooldown_violations'] = 0
    save_cooldowns(cooldowns)
    
    await ctx.send(f"**{user.name}**'s (ID: {user.id}) cooldown has been reset.")

# Info/Help command - CUSTOM
@bot.command(name='info')
async def info_command(ctx):
    """Display all available commands"""
    is_admin = ctx.author.guild_permissions.administrator

    if is_admin:
        info_text = """KEY BOT - COMMANDS

USER COMMANDS:
?key - Generate and claim a key
?stock - Check available keys
?info - Display this command list

ADMIN COMMANDS:
?setchannel - Set current channel as bot channel
?restock - Upload .txt file to add keys
?clear - Clear all keys
?view - View all keys in stock
?announce - Announce restock to @everyone
?blacklist @user OR UserID - Blacklist a user
?unblacklist @user OR UserID - Remove from blacklist
?viewblacklist - View all blacklisted users
?claimed - View all users who claimed keys
?clearclaimed - Clear claimed keys history
?cooldowns - View all users on cooldown
?resetcooldown @user OR UserID - Reset a user's cooldown

NOTE: Users are limited to 3 keys. After 3 keys, 
a 1-hour cooldown is applied. Attempting to claim 
during cooldown results in automatic blacklist.
"""
    else:
        info_text = """KEY BOT - COMMANDS

?key - Generate and claim a key
?stock - Check available keys
?info - Display this command list

NOTE: You can claim up to 3 keys before a 
1-hour cooldown is applied.
"""

    await ctx.send(f"```{info_text}```")

# Add ?help as an alias to ?info
@bot.command(name='help')
async def help_command(ctx):
    """Display all available commands (alias for ?info)"""
    await info_command(ctx)

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
    # Skip spam check and cooldown for admins
    if not ctx.author.guild_permissions.administrator:
        # Check if user is on cooldown
        on_cooldown, time_remaining = check_cooldown(ctx.author.id)
        
        if on_cooldown:
            # User tried to claim during cooldown - handle violation
            should_blacklist = handle_cooldown_violation(ctx.author.id)
            
            if should_blacklist:
                # Auto-blacklist the user
                if ctx.author.id not in blacklist:
                    blacklist.append(ctx.author.id)
                    save_blacklist(blacklist)
                    await ctx.send(f"{ctx.author.mention} You have been automatically blacklisted for attempting to claim keys during cooldown.")
                    return
            
            # Format time remaining
            hours = int(time_remaining.total_seconds() // 3600)
            minutes = int((time_remaining.total_seconds() % 3600) // 60)
            
            await ctx.send(f"{ctx.author.mention} You are on cooldown! Time remaining: **{hours}h {minutes}m**\n⚠️ **WARNING:** Attempting to claim during cooldown will result in an automatic blacklist!")
            return
        
        # Check for spam
        if check_spam(ctx.author.id):
            # Auto-blacklist the user
            if ctx.author.id not in blacklist:
                blacklist.append(ctx.author.id)
                save_blacklist(blacklist)
                await ctx.send(f"{ctx.author.mention} You have been automatically blacklisted for spamming the ?key command.")
                return
    
    if len(keys) == 0:
        await ctx.send("No keys available in stock!")
        return
    
    # Get a random key
    claimed_key = random.choice(keys)
    keys.remove(claimed_key)
    save_keys(keys)

    # Record the claim
    claim_record = {
        'user_id': ctx.author.id,
        'username': str(ctx.author),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'key': claimed_key
    }
    claimed_keys.append(claim_record)
    save_claimed_keys(claimed_keys)

    # Update key claim count and check if cooldown should be applied (skip for admins)
    if not ctx.author.guild_permissions.administrator:
        status = update_key_claim(ctx.author.id)
        
        if status == 'cooldown_applied':
            # Notify user they're now on cooldown
            try:
                await ctx.author.send(f"``{claimed_key}``\n\n⏰ **COOLDOWN APPLIED**\nYou have claimed 3 keys and are now on a **1-hour cooldown**.\n⚠️ Attempting to claim more keys during this cooldown will result in an automatic blacklist!")
                await ctx.send(f"{ctx.author.mention} Check your DMs! ⏰ You've been placed on a 1-hour cooldown after claiming 3 keys.")
            except:
                await ctx.send(f"{ctx.author.mention} I couldn't DM you. Please enable DMs!\n⏰ **You are now on a 1-hour cooldown** after claiming 3 keys.")
            return

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
