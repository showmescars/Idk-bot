import discord
from discord.ext import commands, tasks
import json
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import shutil

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

# Files
KEYS_FILE = 'keys.json'
CONFIG_FILE = 'config.json'
BLACKLIST_FILE = 'blacklist.json'
CLAIMED_KEYS_FILE = 'claimed_keys.json'
COOLDOWNS_FILE = 'cooldowns.json'
STATS_FILE = 'stats.json'
BACKUP_DIR = 'backups'

# Spam detection settings
SPAM_THRESHOLD = 1
SPAM_TIMEFRAME = 3
user_command_times = {}

# Auto-blacklist removal time (5 hours)
AUTO_BLACKLIST_REMOVAL_HOURS = 5

# Create backup directory if it doesn't exist
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

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

# Get key limit for server
def get_key_limit(guild_id):
    guild_id_str = str(guild_id)
    if guild_id_str in config and 'max_keys' in config[guild_id_str]:
        return config[guild_id_str]['max_keys']
    return 3  # Default

# Get cooldown duration for server (in hours)
def get_cooldown_hours(guild_id):
    guild_id_str = str(guild_id)
    if guild_id_str in config and 'cooldown_hours' in config[guild_id_str]:
        return config[guild_id_str]['cooldown_hours']
    return 1  # Default

# Load blacklist with timestamps
def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'r') as f:
            data = json.load(f)
            # Convert old format to new format if needed
            if isinstance(data, list):
                # Old format: just list of user IDs
                new_format = {}
                for user_id in data:
                    new_format[str(user_id)] = {
                        'blacklisted_at': datetime.now().isoformat(),
                        'auto_remove': True
                    }
                return new_format
            else:
                # New format: dict with timestamps
                for user_id in data:
                    if 'blacklisted_at' in data[user_id]:
                        data[user_id]['blacklisted_at'] = datetime.fromisoformat(data[user_id]['blacklisted_at'])
                return data
    return {}

# Save blacklist
def save_blacklist(blacklist_data):
    data_to_save = {}
    for user_id, info in blacklist_data.items():
        data_to_save[user_id] = {
            'blacklisted_at': info['blacklisted_at'].isoformat() if isinstance(info['blacklisted_at'], datetime) else info['blacklisted_at'],
            'auto_remove': info.get('auto_remove', True)
        }
    
    with open(BLACKLIST_FILE, 'w') as f:
        json.dump(data_to_save, f, indent=4)

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
            for user_id in data:
                if 'cooldown_until' in data[user_id] and data[user_id]['cooldown_until']:
                    data[user_id]['cooldown_until'] = datetime.fromisoformat(data[user_id]['cooldown_until'])
            return data
    return {}

# Save cooldowns
def save_cooldowns(cooldowns_data):
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

# Load stats
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {
        'total_keys_added': 0,
        'total_keys_claimed': 0,
        'total_restocks': 0,
        'total_blacklists': 0,
        'total_auto_unblacklists': 0,
        'most_active_claimer': {'user_id': None, 'count': 0},
        'first_restock_date': None,
        'last_restock_date': None
    }

# Save stats
def save_stats(stats_data):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats_data, f, indent=4)

stats = load_stats()

# Update stats
def update_stats(action, **kwargs):
    global stats
    
    if action == 'restock':
        stats['total_keys_added'] += kwargs.get('count', 0)
        stats['total_restocks'] += 1
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stats['last_restock_date'] = current_time
        if stats['first_restock_date'] is None:
            stats['first_restock_date'] = current_time
    
    elif action == 'claim':
        stats['total_keys_claimed'] += kwargs.get('count', 1)
        user_id = kwargs.get('user_id')
        
        # Update most active claimer
        user_claim_count = sum(1 for claim in claimed_keys if claim['user_id'] == user_id)
        if user_claim_count > stats['most_active_claimer']['count']:
            stats['most_active_claimer'] = {
                'user_id': user_id,
                'count': user_claim_count
            }
    
    elif action == 'blacklist':
        stats['total_blacklists'] += 1
    
    elif action == 'auto_unblacklist':
        stats['total_auto_unblacklists'] = stats.get('total_auto_unblacklists', 0) + 1
    
    save_stats(stats)

# Load keys
def load_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict) and any(isinstance(v, list) for v in data.values()):
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

# Create backup
def create_backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_subdir = os.path.join(BACKUP_DIR, f'backup_{timestamp}')
    
    if not os.path.exists(backup_subdir):
        os.makedirs(backup_subdir)
    
    files_to_backup = [
        KEYS_FILE,
        CONFIG_FILE,
        BLACKLIST_FILE,
        CLAIMED_KEYS_FILE,
        COOLDOWNS_FILE,
        STATS_FILE
    ]
    
    backed_up = []
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(backup_subdir, file))
            backed_up.append(file)
    
    return timestamp, backed_up

# List backups
def list_backups():
    if not os.path.exists(BACKUP_DIR):
        return []
    
    backups = []
    for item in os.listdir(BACKUP_DIR):
        if item.startswith('backup_'):
            backups.append(item)
    
    return sorted(backups, reverse=True)

# Restore backup
def restore_backup(backup_name):
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    if not os.path.exists(backup_path):
        return False, "Backup not found"
    
    files_to_restore = [
        KEYS_FILE,
        CONFIG_FILE,
        BLACKLIST_FILE,
        CLAIMED_KEYS_FILE,
        COOLDOWNS_FILE,
        STATS_FILE
    ]
    
    restored = []
    for file in files_to_restore:
        backup_file = os.path.join(backup_path, file)
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, file)
            restored.append(file)
    
    return True, restored

# Background task to check and remove expired blacklists
@tasks.loop(minutes=5)  # Check every 5 minutes
async def check_blacklist_expiry():
    global blacklist
    current_time = datetime.now()
    users_to_remove = []
    
    for user_id_str, info in blacklist.items():
        if info.get('auto_remove', True):
            blacklist_time = info['blacklisted_at']
            if isinstance(blacklist_time, str):
                blacklist_time = datetime.fromisoformat(blacklist_time)
            
            time_elapsed = current_time - blacklist_time
            
            # Check if 5 hours have passed
            if time_elapsed >= timedelta(hours=AUTO_BLACKLIST_REMOVAL_HOURS):
                users_to_remove.append(user_id_str)
    
    # Remove expired blacklists
    for user_id_str in users_to_remove:
        user_id = int(user_id_str)
        del blacklist[user_id_str]
        
        # Clear cooldown data
        if user_id_str in cooldowns:
            del cooldowns[user_id_str]
            save_cooldowns(cooldowns)
        
        # Clear spam tracking
        if user_id in user_command_times:
            del user_command_times[user_id]
        
        # Update stats
        update_stats('auto_unblacklist')
        
        print(f"Auto-removed blacklist for user ID: {user_id}")
    
    if users_to_remove:
        save_blacklist(blacklist)

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Key Bot Ready')
    check_blacklist_expiry.start()  # Start the background task
    print('Auto-blacklist removal task started (checks every 5 minutes)')

# Check to block DM commands
@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        embed = discord.Embed(
            title="DMs Not Allowed",
            description="Commands can only be used in servers, not DMs",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return False
    return True

# Check if user is blacklisted
@bot.check
async def check_blacklist_check(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    
    user_id_str = str(ctx.author.id)
    if user_id_str in blacklist:
        info = blacklist[user_id_str]
        blacklist_time = info['blacklisted_at']
        if isinstance(blacklist_time, str):
            blacklist_time = datetime.fromisoformat(blacklist_time)
        
        time_elapsed = datetime.now() - blacklist_time
        time_remaining = timedelta(hours=AUTO_BLACKLIST_REMOVAL_HOURS) - time_elapsed
        
        hours = int(time_remaining.total_seconds() // 3600)
        minutes = int((time_remaining.total_seconds() % 3600) // 60)
        
        embed = discord.Embed(
            title="Access Denied",
            description=f"{ctx.author.mention} You are blacklisted from using this bot.\n\n**Auto-removal in:** {hours}h {minutes}m",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return False
    return True

# Check to only allow specific channel per server
@bot.check
async def only_allowed_channel(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    
    guild_id = str(ctx.guild.id)
    
    if guild_id not in config or 'allowed_channel' not in config[guild_id]:
        return True
    
    allowed_channel = config[guild_id]['allowed_channel']
    if ctx.channel.id != allowed_channel:
        return False
    return True

# Spam detection
def check_spam(user_id):
    current_time = datetime.now()
    
    if user_id not in user_command_times:
        user_command_times[user_id] = []
    
    user_command_times[user_id] = [
        timestamp for timestamp in user_command_times[user_id]
        if current_time - timestamp < timedelta(seconds=SPAM_TIMEFRAME)
    ]
    
    user_command_times[user_id].append(current_time)
    
    if len(user_command_times[user_id]) > SPAM_THRESHOLD:
        return True
    
    return False

# Check cooldown
def check_cooldown(user_id):
    user_id_str = str(user_id)
    
    if user_id_str not in cooldowns:
        cooldowns[user_id_str] = {
            'keys_claimed': 0,
            'cooldown_until': None,
            'cooldown_violations': 0
        }
        return False, None, 0
    
    user_data = cooldowns[user_id_str]
    
    if user_data['cooldown_until']:
        if datetime.now() < user_data['cooldown_until']:
            time_remaining = user_data['cooldown_until'] - datetime.now()
            return True, time_remaining, user_data['keys_claimed']
        else:
            user_data['cooldown_until'] = None
            user_data['keys_claimed'] = 0
            save_cooldowns(cooldowns)
    
    return False, None, user_data['keys_claimed']

# Get keys remaining for user
def get_keys_remaining(user_id, guild_id):
    max_keys = get_key_limit(guild_id)
    user_id_str = str(user_id)
    
    if user_id_str not in cooldowns:
        return max_keys
    
    user_data = cooldowns[user_id_str]
    
    # If on cooldown, no keys available
    if user_data['cooldown_until'] and datetime.now() < user_data['cooldown_until']:
        return 0
    
    return max_keys - user_data['keys_claimed']

# Update key claim with multiple keys
def update_key_claim(user_id, num_keys, guild_id):
    max_keys = get_key_limit(guild_id)
    cooldown_hours = get_cooldown_hours(guild_id)
    user_id_str = str(user_id)
    
    if user_id_str not in cooldowns:
        cooldowns[user_id_str] = {
            'keys_claimed': 0,
            'cooldown_until': None,
            'cooldown_violations': 0
        }
    
    user_data = cooldowns[user_id_str]
    user_data['keys_claimed'] += num_keys
    
    # If user has claimed max keys or more, apply cooldown
    if user_data['keys_claimed'] >= max_keys:
        user_data['cooldown_until'] = datetime.now() + timedelta(hours=cooldown_hours)
        user_data['keys_claimed'] = 0
        save_cooldowns(cooldowns)
        return 'cooldown_applied'
    
    save_cooldowns(cooldowns)
    return 'normal'

# Handle cooldown violation
def handle_cooldown_violation(user_id):
    user_id_str = str(user_id)
    
    if user_id_str not in cooldowns:
        return False
    
    user_data = cooldowns[user_id_str]
    user_data['cooldown_violations'] = user_data.get('cooldown_violations', 0) + 1
    save_cooldowns(cooldowns)
    
    if user_data['cooldown_violations'] >= 1:
        return True
    
    return False

# NEW COMMAND: Set key limit
@bot.command(name='setkeylimit')
@commands.has_permissions(administrator=True)
async def set_key_limit(ctx, max_keys: int = None):
    if max_keys is None:
        # Show current settings
        current_max = get_key_limit(ctx.guild.id)
        
        embed = discord.Embed(
            title="Current Key Limit Settings",
            color=discord.Color.blue()
        )
        embed.add_field(name="Max Keys Per User", value=f"{current_max} keys", inline=True)
        embed.add_field(
            name="Usage",
            value="?setkeylimit <number>\nExample: ?setkeylimit 5\n(Allows users to claim up to 5 keys)",
            inline=False
        )
        await ctx.send(embed=embed)
        return
    
    if max_keys < 1 or max_keys > 20:
        embed = discord.Embed(
            title="Invalid Value",
            description="Max keys must be between 1 and 20",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    guild_id_str = str(ctx.guild.id)
    
    if guild_id_str not in config:
        config[guild_id_str] = {}
    
    config[guild_id_str]['max_keys'] = max_keys
    save_config(config)
    
    embed = discord.Embed(
        title="Key Limit Updated",
        color=discord.Color.green()
    )
    embed.add_field(name="Max Keys Per User", value=f"{max_keys} keys", inline=True)
    embed.add_field(
        name="Note",
        value=f"Users can now claim 1-{max_keys} keys before cooldown is applied.",
        inline=False
    )
    
    await ctx.send(embed=embed)

# NEW COMMAND: Set cooldown duration
@bot.command(name='setcooldown')
@commands.has_permissions(administrator=True)
async def set_cooldown_duration(ctx, hours: int = None):
    if hours is None:
        # Show current settings
        current_cooldown = get_cooldown_hours(ctx.guild.id)
        
        embed = discord.Embed(
            title="Current Cooldown Settings",
            color=discord.Color.blue()
        )
        embed.add_field(name="Cooldown Duration", value=f"{current_cooldown} hour(s)", inline=True)
        embed.add_field(
            name="Usage",
            value="?setcooldown <hours>\nExample: ?setcooldown 2\n(Sets 2 hour cooldown after max keys claimed)",
            inline=False
        )
        await ctx.send(embed=embed)
        return
    
    if hours < 1 or hours > 48:
        embed = discord.Embed(
            title="Invalid Value",
            description="Cooldown hours must be between 1 and 48",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    guild_id_str = str(ctx.guild.id)
    
    if guild_id_str not in config:
        config[guild_id_str] = {}
    
    config[guild_id_str]['cooldown_hours'] = hours
    save_config(config)
    
    embed = discord.Embed(
        title="Cooldown Duration Updated",
        color=discord.Color.green()
    )
    embed.add_field(name="Cooldown Duration", value=f"{hours} hour(s)", inline=True)
    embed.add_field(
        name="Note",
        value=f"Users will be on cooldown for {hours} hour(s) after claiming max keys.",
        inline=False
    )
    
    await ctx.send(embed=embed)

# Set allowed channel
@bot.command(name='setchannel')
@commands.has_permissions(administrator=True)
async def set_channel(ctx):
    guild_id = str(ctx.guild.id)
    
    if guild_id not in config:
        config[guild_id] = {}
    
    config[guild_id]['allowed_channel'] = ctx.channel.id
    save_config(config)
    
    embed = discord.Embed(
        title="Channel Set",
        description=f"This channel is now set as the bot command channel\nChannel ID: {ctx.channel.id}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# Blacklist a user
@bot.command(name='blacklist')
@commands.has_permissions(administrator=True)
async def blacklist_user(ctx, user_input: str = None, permanent: str = None):
    if user_input is None:
        embed = discord.Embed(
            title="Usage",
            description="?blacklist @user OR ?blacklist UserID [permanent]\n\nAdd 'permanent' to prevent auto-removal after 5 hours\nExample: ?blacklist @user permanent",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    user = None
    
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    else:
        try:
            user_id = int(user_input)
            user = await bot.fetch_user(user_id)
        except (ValueError, discord.NotFound):
            embed = discord.Embed(
                title="Error",
                description="Invalid user mention or ID! Use ?blacklist @user OR ?blacklist UserID",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
    
    if ctx.guild and user.id in [m.id for m in ctx.guild.members]:
        member = ctx.guild.get_member(user.id)
        if member and member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error",
                description="Cannot blacklist administrators!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
    
    user_id_str = str(user.id)
    if user_id_str in blacklist:
        embed = discord.Embed(
            title="Already Blacklisted",
            description=f"{user.name} (ID: {user.id}) is already blacklisted.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    is_permanent = permanent and permanent.lower() == 'permanent'
    
    blacklist[user_id_str] = {
        'blacklisted_at': datetime.now(),
        'auto_remove': not is_permanent
    }
    save_blacklist(blacklist)
    update_stats('blacklist')
    
    blacklist_type = "permanently" if is_permanent else f"for {AUTO_BLACKLIST_REMOVAL_HOURS} hours (auto-removal enabled)"
    
    embed = discord.Embed(
        title="User Blacklisted",
        description=f"**{user.name}** (ID: {user.id}) has been blacklisted {blacklist_type}.",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

# Unblacklist a user
@bot.command(name='unblacklist')
@commands.has_permissions(administrator=True)
async def unblacklist_user(ctx, user_input: str = None):
    if user_input is None:
        embed = discord.Embed(
            title="Usage",
            description="?unblacklist @user OR ?unblacklist UserID",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    user = None
    
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    else:
        try:
            user_id = int(user_input)
            user = await bot.fetch_user(user_id)
        except (ValueError, discord.NotFound):
            embed = discord.Embed(
                title="Error",
                description="Invalid user mention or ID! Use ?unblacklist @user OR ?unblacklist UserID",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
    
    user_id_str = str(user.id)
    if user_id_str not in blacklist:
        embed = discord.Embed(
            title="Not Blacklisted",
            description=f"**{user.name}** (ID: {user.id}) is not blacklisted.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    del blacklist[user_id_str]
    save_blacklist(blacklist)
    
    if user.id in user_command_times:
        del user_command_times[user.id]
    
    if user_id_str in cooldowns:
        del cooldowns[user_id_str]
        save_cooldowns(cooldowns)
    
    embed = discord.Embed(
        title="User Unblacklisted",
        description=f"**{user.name}** (ID: {user.id}) has been removed from the blacklist.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# View blacklist
@bot.command(name='viewblacklist')
@commands.has_permissions(administrator=True)
async def view_blacklist(ctx):
    if len(blacklist) == 0:
        embed = discord.Embed(
            title="Blacklist",
            description="No users are blacklisted.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        return
    
    blacklist_text = ""
    
    for user_id_str, info in blacklist.items():
        user_id = int(user_id_str)
        user = bot.get_user(user_id)
        
        if user:
            display_name = str(user)
        else:
            try:
                user = await bot.fetch_user(user_id)
                display_name = str(user)
            except:
                display_name = "Unknown User"
        
        blacklist_time = info['blacklisted_at']
        if isinstance(blacklist_time, str):
            blacklist_time = datetime.fromisoformat(blacklist_time)
        
        time_elapsed = datetime.now() - blacklist_time
        
        if info.get('auto_remove', True):
            time_remaining = timedelta(hours=AUTO_BLACKLIST_REMOVAL_HOURS) - time_elapsed
            hours = int(time_remaining.total_seconds() // 3600)
            minutes = int((time_remaining.total_seconds() % 3600) // 60)
            status = f"Auto-removes in: {hours}h {minutes}m"
        else:
            status = "Permanent"
        
        blacklist_text += f"**{display_name}** (ID: {user_id})\n"
        blacklist_text += f"   {status}\n\n"
    
    embed = discord.Embed(
        title="Blacklisted Users",
        description=blacklist_text,
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Auto-removal occurs after {AUTO_BLACKLIST_REMOVAL_HOURS} hours (unless permanent)")
    await ctx.send(embed=embed)

# View claimed keys
@bot.command(name='claimed')
@commands.has_permissions(administrator=True)
async def view_claimed_keys(ctx):
    if len(claimed_keys) == 0:
        embed = discord.Embed(
            title="Claimed Keys History",
            description="No keys have been claimed yet.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        return
    
    claimed_text = ""
    
    for i, claim in enumerate(claimed_keys, 1):
        user_id = claim['user_id']
        username = claim['username']
        timestamp = claim['timestamp']
        key = claim['key']
        
        claimed_text += f"{i}. {username} (ID: {user_id})\n"
        claimed_text += f"   Key: ``{key}``\n"
        claimed_text += f"   Time: {timestamp}\n\n"
        
        if len(claimed_text) > 1800:
            embed = discord.Embed(
                title="Claimed Keys History",
                description=claimed_text,
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            claimed_text = ""
    
    if claimed_text:
        embed = discord.Embed(
            title="Claimed Keys History",
            description=claimed_text,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

# Clear claimed keys
@bot.command(name='clearclaimed')
@commands.has_permissions(administrator=True)
async def clear_claimed_history(ctx):
    global claimed_keys
    count = len(claimed_keys)
    
    if count == 0:
        embed = discord.Embed(
            title="No History",
            description="No claimed keys history to clear.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    claimed_keys = []
    save_claimed_keys(claimed_keys)
    
    embed = discord.Embed(
        title="History Cleared",
        description=f"Successfully cleared **{count}** claimed keys from history!",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# View cooldowns
@bot.command(name='cooldowns')
@commands.has_permissions(administrator=True)
async def view_cooldowns(ctx):
    active_cooldowns = []
    
    for user_id_str, data in cooldowns.items():
        if data['cooldown_until'] and datetime.now() < data['cooldown_until']:
            user_id = int(user_id_str)
            user = bot.get_user(user_id)
            
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
            
            hours = int(time_remaining.total_seconds() // 3600)
            minutes = int((time_remaining.total_seconds() % 3600) // 60)
            
            active_cooldowns.append({
                'display_name': display_name,
                'user_id': user_id,
                'time_remaining': f"{hours}h {minutes}m",
                'violations': data.get('cooldown_violations', 0)
            })
    
    if len(active_cooldowns) == 0:
        embed = discord.Embed(
            title="Active Cooldowns",
            description="No users are currently on cooldown.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        return
    
    cooldown_text = ""
    for cd in active_cooldowns:
        cooldown_text += f"**{cd['display_name']}** (ID: {cd['user_id']})\n"
        cooldown_text += f"Time Remaining: {cd['time_remaining']}\n"
        cooldown_text += f"Violations: {cd['violations']}\n\n"
    
    embed = discord.Embed(
        title="Active Cooldowns",
        description=cooldown_text,
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)

# Reset cooldown
@bot.command(name='resetcooldown')
@commands.has_permissions(administrator=True)
async def reset_cooldown(ctx, user_input: str = None):
    if user_input is None:
        embed = discord.Embed(
            title="Usage",
            description="?resetcooldown @user OR ?resetcooldown UserID",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    user = None
    
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    else:
        try:
            user_id = int(user_input)
            user = await bot.fetch_user(user_id)
        except (ValueError, discord.NotFound):
            embed = discord.Embed(
                title="Error",
                description="Invalid user mention or ID! Use ?resetcooldown @user OR ?resetcooldown UserID",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
    
    user_id_str = str(user.id)
    
    if user_id_str not in cooldowns or not cooldowns[user_id_str]['cooldown_until']:
        embed = discord.Embed(
            title="Not On Cooldown",
            description=f"**{user.name}** (ID: {user.id}) is not on cooldown.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    cooldowns[user_id_str]['cooldown_until'] = None
    cooldowns[user_id_str]['keys_claimed'] = 0
    cooldowns[user_id_str]['cooldown_violations'] = 0
    save_cooldowns(cooldowns)
    
    embed = discord.Embed(
        title="Cooldown Reset",
        description=f"**{user.name}**'s (ID: {user.id}) cooldown has been reset.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# Stats dashboard
@bot.command(name='stats')
@commands.has_permissions(administrator=True)
async def view_stats(ctx):
    embed = discord.Embed(
        title="Bot Statistics Dashboard",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Keys",
        value=f"Total Added: {stats['total_keys_added']}\nTotal Claimed: {stats['total_keys_claimed']}\nCurrent Stock: {len(keys)}",
        inline=True
    )
    
    embed.add_field(
        name="Restocks",
        value=f"Total Restocks: {stats['total_restocks']}\nFirst: {stats['first_restock_date'] or 'N/A'}\nLast: {stats['last_restock_date'] or 'N/A'}",
        inline=True
    )
    
    embed.add_field(
        name="Users",
        value=f"Total Blacklists: {stats['total_blacklists']}\nAuto-Removals: {stats.get('total_auto_unblacklists', 0)}\nActive Blacklists: {len(blacklist)}\nUnique Claimers: {len(set(c['user_id'] for c in claimed_keys))}",
        inline=True
    )
    
    # Most active claimer
    if stats['most_active_claimer']['user_id']:
        user = bot.get_user(stats['most_active_claimer']['user_id'])
        if not user:
            try:
                user = await bot.fetch_user(stats['most_active_claimer']['user_id'])
            except:
                user = None
        
        claimer_name = str(user) if user else "Unknown User"
        embed.add_field(
            name="Most Active Claimer",
            value=f"{claimer_name}\nKeys Claimed: {stats['most_active_claimer']['count']}",
            inline=False
        )
    
    # Server settings
    max_keys = get_key_limit(ctx.guild.id)
    cooldown_hours = get_cooldown_hours(ctx.guild.id)
    embed.add_field(
        name="Server Settings",
        value=f"Max Keys: {max_keys}\nCooldown: {cooldown_hours}h\nAuto-Unblacklist: {AUTO_BLACKLIST_REMOVAL_HOURS}h",
        inline=False
    )
    
    embed.set_footer(text=f"Stats as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    await ctx.send(embed=embed)

# Create backup
@bot.command(name='backup')
@commands.has_permissions(administrator=True)
async def backup_data(ctx):
    timestamp, backed_up = create_backup()
    
    embed = discord.Embed(
        title="Backup Created",
        description=f"Backup created successfully!\n\nBackup ID: backup_{timestamp}\nFiles backed up: {len(backed_up)}",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="Backed Up Files",
        value="\n".join(backed_up),
        inline=False
    )
    
    await ctx.send(embed=embed)

# List backups
@bot.command(name='backups')
@commands.has_permissions(administrator=True)
async def list_all_backups(ctx):
    backups = list_backups()
    
    if len(backups) == 0:
        embed = discord.Embed(
            title="Backups",
            description="No backups found.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    backup_list = "\n".join([f"{i+1}. {backup}" for i, backup in enumerate(backups)])
    
    embed = discord.Embed(
        title="Available Backups",
        description=backup_list,
        color=discord.Color.blue()
    )
    
    embed.set_footer(text=f"Use ?restore <backup_name> to restore a backup")
    
    await ctx.send(embed=embed)

# Restore backup
@bot.command(name='restore')
@commands.has_permissions(administrator=True)
async def restore_data(ctx, backup_name: str = None):
    if backup_name is None:
        embed = discord.Embed(
            title="Usage",
            description="?restore <backup_name>\n\nUse ?backups to see available backups",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        return
    
    success, result = restore_backup(backup_name)
    
    if not success:
        embed = discord.Embed(
            title="Restore Failed",
            description=result,
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Reload data
    global keys, config, blacklist, claimed_keys, cooldowns, stats
    keys = load_keys()
    config = load_config()
    blacklist = load_blacklist()
    claimed_keys = load_claimed_keys()
    cooldowns = load_cooldowns()
    stats = load_stats()
    
    embed = discord.Embed(
        title="Backup Restored",
        description=f"Backup restored successfully!\n\nBackup: {backup_name}\nFiles restored: {len(result)}",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="Restored Files",
        value="\n".join(result),
        inline=False
    )
    
    await ctx.send(embed=embed)

# Info/Help command
@bot.command(name='info')
async def info_command(ctx):
    is_admin = ctx.author.guild_permissions.administrator
    max_keys = get_key_limit(ctx.guild.id)
    cooldown_hours = get_cooldown_hours(ctx.guild.id)

    if is_admin:
        embed = discord.Embed(
            title="Key Bot - Commands",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="User Commands",
            value=f"?key [amount] - Generate and claim keys (1-{max_keys})\n?stock - Check available keys\n?remaining - Check your remaining claims\n?info - Display this command list",
            inline=False
        )
        
        embed.add_field(
            name="Admin Commands - Setup",
            value="?setchannel - Set current channel as bot channel\n?setkeylimit <number> - Set max keys per user (1-20)\n?setcooldown <hours> - Set cooldown duration (1-48h)\n?restock - Upload .txt file to add keys\n?clear - Clear all keys\n?view - View all keys in stock\n?announce - Announce restock to @everyone",
            inline=False
        )
        
        embed.add_field(
            name="Admin Commands - User Management",
            value="?blacklist @user OR UserID [permanent] - Blacklist a user\n?unblacklist @user OR UserID - Remove from blacklist\n?viewblacklist - View all blacklisted users\n?resetcooldown @user OR UserID - Reset a user's cooldown\n?cooldowns - View all users on cooldown",
            inline=False
        )
        
        embed.add_field(
            name="Admin Commands - Data & Stats",
            value="?claimed - View all users who claimed keys\n?clearclaimed - Clear claimed keys history\n?stats - View bot statistics dashboard\n?backup - Create a backup\n?backups - List all backups\n?restore <backup_name> - Restore a backup",
            inline=False
        )
        
        embed.set_footer(text=f"Server: {max_keys} keys max, {cooldown_hours}h cooldown | Blacklist auto-removes after {AUTO_BLACKLIST_REMOVAL_HOURS}h")
    else:
        embed = discord.Embed(
            title="Key Bot - Commands",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Available Commands",
            value=f"?key [amount] - Generate and claim keys (1-{max_keys})\nExample: ?key 2 (claims 2 keys)\n?stock - Check available keys\n?remaining - Check your remaining claims\n?info - Display this command list",
            inline=False
        )
        
        embed.set_footer(text=f"Note: You can claim up to {max_keys} keys total before {cooldown_hours}h cooldown")

    await ctx.send(embed=embed)

# Help alias
@bot.command(name='help')
async def help_command(ctx):
    await info_command(ctx)

# Check remaining keys command
@bot.command(name='remaining')
async def check_remaining(ctx):
    max_keys = get_key_limit(ctx.guild.id)
    cooldown_hours = get_cooldown_hours(ctx.guild.id)
    keys_left = get_keys_remaining(ctx.author.id, ctx.guild.id)
    on_cooldown, time_remaining, _ = check_cooldown(ctx.author.id)
    
    embed = discord.Embed(
        title="Your Key Status",
        color=discord.Color.blue()
    )
    
    if on_cooldown:
        hours = int(time_remaining.total_seconds() // 3600)
        minutes = int((time_remaining.total_seconds() % 3600) // 60)
        
        embed.add_field(
            name="Status",
            value="On Cooldown",
            inline=True
        )
        embed.add_field(
            name="Time Remaining",
            value=f"{hours}h {minutes}m",
            inline=True
        )
        embed.add_field(
            name="Keys Available",
            value="0",
            inline=True
        )
    else:
        embed.add_field(
            name="Status",
            value="Active",
            inline=True
        )
        embed.add_field(
            name="Keys Remaining",
            value=f"{keys_left}/{max_keys}",
            inline=True
        )
        embed.add_field(
            name="Can Claim",
            value=f"1-{keys_left} keys",
            inline=True
        )
    
    embed.set_footer(text=f"Cooldown: {cooldown_hours}h after claiming {max_keys} keys")
    
    await ctx.send(embed=embed)

# Restock from file
@bot.command(name='restock')
@commands.has_permissions(administrator=True)
async def restock_from_file(ctx):
    if len(ctx.message.attachments) == 0:
        embed = discord.Embed(
            title="Error",
            description="Please attach a .txt file with keys",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    attachment = ctx.message.attachments[0]

    if not attachment.filename.endswith('.txt'):
        embed = discord.Embed(
            title="Error",
            description="File must be a .txt file",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    file_content = await attachment.read()
    keys_list = file_content.decode('utf-8').strip().split('\n')

    keys_list = [key.strip() for key in keys_list if key.strip()]

    original_count = len(keys_list)
    keys_list_unique = list(set(keys_list))
    duplicates_in_file = original_count - len(keys_list_unique)

    existing_keys_set = set(keys)
    new_keys = [key for key in keys_list_unique if key not in existing_keys_set]
    duplicates_in_stock = len(keys_list_unique) - len(new_keys)

    keys.extend(new_keys)
    save_keys(keys)
    
    # Update stats
    update_stats('restock', count=len(new_keys))

    embed = discord.Embed(
        title="Restock Complete",
        color=discord.Color.green()
    )
    
    embed.add_field(name="Added", value=f"{len(new_keys)} new keys", inline=True)
    embed.add_field(name="Total Stock", value=f"{len(keys)} keys", inline=True)
    embed.add_field(name="Duplicates", value=f"{duplicates_in_file + duplicates_in_stock}", inline=True)
    
    if duplicates_in_file > 0:
        embed.add_field(name="Duplicates in File", value=f"{duplicates_in_file} (removed)", inline=False)
    
    if duplicates_in_stock > 0:
        embed.add_field(name="Already in Stock", value=f"{duplicates_in_stock} (skipped)", inline=False)

    await ctx.send(embed=embed)

# Clear keys
@bot.command(name='clear')
@commands.has_permissions(administrator=True)
async def clear_keys(ctx):
    global keys
    count = len(keys)
    keys = []
    save_keys(keys)

    embed = discord.Embed(
        title="Keys Cleared",
        description=f"Cleared {count} keys from stock",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)

# View stock
@bot.command(name='view')
@commands.has_permissions(administrator=True)
async def view_stock(ctx):
    if len(keys) == 0:
        embed = discord.Embed(
            title="Current Stock",
            description="No keys in stock",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    stock_list = "\n".join(keys)

    if len(stock_list) > 1900:
        embed = discord.Embed(
            title=f"Current Stock ({len(keys)} keys)",
            description="Stock is too large. Sending in chunks...",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        
        for i in range(0, len(stock_list), 1900):
            await ctx.send(f"```{stock_list[i:i+1900]}```")
    else:
        embed = discord.Embed(
            title=f"Current Stock ({len(keys)} keys)",
            description=f"```{stock_list}```",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

# Check stock
@bot.command(name='stock')
async def check_stock(ctx):
    embed = discord.Embed(
        title="Current Stock",
        description=f"{len(keys)} keys available",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Generate/Claim keys - NO EMBEDS IN DM
@bot.command(name='key')
async def generate_key(ctx, amount: int = 1):
    max_keys = get_key_limit(ctx.guild.id)
    cooldown_hours = get_cooldown_hours(ctx.guild.id)
    
    # Validate amount
    if amount < 1 or amount > max_keys:
        embed = discord.Embed(
            title="Invalid Amount",
            description=f"You can only claim between 1-{max_keys} keys at a time.\nUsage: ?key [1-{max_keys}]\nExample: ?key 2",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Skip checks for admins
    if not ctx.author.guild_permissions.administrator:
        on_cooldown, time_remaining, _ = check_cooldown(ctx.author.id)
        
        if on_cooldown:
            should_blacklist = handle_cooldown_violation(ctx.author.id)
            
            if should_blacklist:
                user_id_str = str(ctx.author.id)
                if user_id_str not in blacklist:
                    blacklist[user_id_str] = {
                        'blacklisted_at': datetime.now(),
                        'auto_remove': True
                    }
                    save_blacklist(blacklist)
                    update_stats('blacklist')
                    
                    embed = discord.Embed(
                        title="Auto-Blacklisted",
                        description=f"{ctx.author.mention} You have been automatically blacklisted for attempting to claim keys during cooldown.\n\n**Auto-removal in:** {AUTO_BLACKLIST_REMOVAL_HOURS} hours",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
                    return
            
            hours = int(time_remaining.total_seconds() // 3600)
            minutes = int((time_remaining.total_seconds() % 3600) // 60)
            
            embed = discord.Embed(
                title="Cooldown Active",
                description=f"{ctx.author.mention} You are on cooldown!\n\nTime remaining: **{hours}h {minutes}m**\n\nWARNING: Attempting to claim during cooldown will result in an automatic blacklist!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Check if user has enough keys remaining
        keys_remaining = get_keys_remaining(ctx.author.id, ctx.guild.id)
        if amount > keys_remaining:
            embed = discord.Embed(
                title="Not Enough Claims Available",
                description=f"You only have **{keys_remaining}** claim(s) remaining before cooldown.\nYou requested **{amount}** key(s).\n\nUse ?remaining to check your status.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Check for spam
        if check_spam(ctx.author.id):
            user_id_str = str(ctx.author.id)
            if user_id_str not in blacklist:
                blacklist[user_id_str] = {
                    'blacklisted_at': datetime.now(),
                    'auto_remove': True
                }
                save_blacklist(blacklist)
                update_stats('blacklist')
                
                embed = discord.Embed(
                    title="Auto-Blacklisted",
                    description=f"{ctx.author.mention} You have been automatically blacklisted for spamming the ?key command.\n\n**Auto-removal in:** {AUTO_BLACKLIST_REMOVAL_HOURS} hours",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
    
    # Check stock
    if len(keys) == 0:
        embed = discord.Embed(
            title="Out of Stock",
            description="No keys available in stock!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Check if enough keys in stock
    if len(keys) < amount:
        embed = discord.Embed(
            title="Insufficient Stock",
            description=f"Only **{len(keys)}** key(s) available in stock.\nYou requested **{amount}** key(s).",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    # Claim the keys
    claimed_keys_list = []
    for _ in range(amount):
        claimed_key = random.choice(keys)
        keys.remove(claimed_key)
        claimed_keys_list.append(claimed_key)
        
        # Record each claim
        claim_record = {
            'user_id': ctx.author.id,
            'username': str(ctx.author),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'key': claimed_key
        }
        claimed_keys.append(claim_record)
    
    save_keys(keys)
    save_claimed_keys(claimed_keys)
    
    # Update stats
    update_stats('claim', user_id=ctx.author.id, count=amount)

    # Update user's claim count and check cooldown (skip for admins)
    if not ctx.author.guild_permissions.administrator:
        status = update_key_claim(ctx.author.id, amount, ctx.guild.id)
        
        # Format keys for DM (PLAIN TEXT - NO EMBED)
        keys_text = "\n".join([f"``{key}``" for key in claimed_keys_list])
        
        if status == 'cooldown_applied':
            try:
                dm_message = f"**Your {amount} Key(s):**\n\n{keys_text}\n\n"
                dm_message += "──────────────────────\n"
                dm_message += "**COOLDOWN APPLIED**\n"
                dm_message += f"You have claimed {max_keys} keys total and are now on a **{cooldown_hours}-hour cooldown**.\n\n"
                dm_message += "WARNING: Attempting to claim more keys during this cooldown will result in an automatic blacklist!"
                
                await ctx.author.send(dm_message)
                
                embed = discord.Embed(
                    title="Keys Claimed",
                    description=f"{ctx.author.mention} Check your DMs!\n\nYou've been placed on a {cooldown_hours}-hour cooldown after claiming {max_keys} total keys.",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="DM Failed",
                    description=f"{ctx.author.mention} I couldn't DM you. Please enable DMs!\n\nYou are now on a {cooldown_hours}-hour cooldown after claiming {max_keys} total keys.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
            return
        else:
            # Calculate remaining keys after this claim
            keys_left_after = get_keys_remaining(ctx.author.id, ctx.guild.id)
            
            try:
                dm_message = f"**Your {amount} Key(s):**\n\n{keys_text}\n\n"
                dm_message += "──────────────────────\n"
                dm_message += f"**Remaining Claims:** {keys_left_after}\n"
                dm_message += f"You have **{keys_left_after}** claim(s) remaining before cooldown."
                
                await ctx.author.send(dm_message)
                
                embed = discord.Embed(
                    title="Keys Claimed",
                    description=f"{ctx.author.mention} Check your DMs!\n\nYou have **{keys_left_after}** claim(s) remaining.",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="DM Failed",
                    description=f"{ctx.author.mention} I couldn't DM you. Please enable DMs and try again!",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
    else:
        # Admin claiming - no cooldown tracking (PLAIN TEXT - NO EMBED)
        keys_text = "\n".join([f"``{key}``" for key in claimed_keys_list])
        
        try:
            dm_message = f"**Your {amount} Key(s):**\n\n{keys_text}\n\n"
            dm_message += "──────────────────────\n"
            dm_message += "**Admin** - No cooldown applied"
            
            await ctx.author.send(dm_message)
            
            embed = discord.Embed(
                title="Keys Claimed",
                description=f"{ctx.author.mention} Check your DMs!",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title="DM Failed",
                description=f"{ctx.author.mention} I couldn't DM you. Please enable DMs and try again!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

# Announce restock
@bot.command(name='announce')
@commands.has_permissions(administrator=True)
async def announce_restock(ctx):
    max_keys = get_key_limit(ctx.guild.id)
    
    if len(keys) == 0:
        embed = discord.Embed(
            title="Error",
            description="No stock available to announce",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    stock_count = len(keys)

    embed = discord.Embed(
        title="🔑 RESTOCK ALERT 🔑",
        description=f"Keys are now available!\n\nStock: **{stock_count}** keys\n\nUse `?key [1-{max_keys}]` to claim yours!\nExample: `?key 2` to claim 2 keys at once",
        color=discord.Color.gold()
    )
    
    await ctx.send("@everyone", embed=embed)

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
