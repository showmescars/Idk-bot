import discord
from discord.ext import commands
import json
import os
import random
from datetime import datetime
from dotenv import load_dotenv
import string

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Files
KEYS_FILE = 'keys.json'
LOGS_FILE = 'claim_logs.json'
CREDITS_FILE = 'credits.json'

# Blocked channel ID
BLOCKED_CHANNEL_ID = 1470843481177198876

# Credit settings
STARTING_CREDITS = 15
KEY_COST = 5

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

# Load keys
def load_keys():
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'r') as f:
            return json.load(f)
    return {"available": [], "claimed": {}}

# Save keys
def save_keys(keys_data):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys_data, f, indent=4)

# Generate random key
def generate_key(length=16):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

logs = load_logs()
credits = load_credits()
keys = load_keys()

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Key Generator Bot Ready')

# Check to block DM commands
@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
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

# Info command - lists all commands
@bot.command(name='i')
async def info_command(ctx):
    """Display all available commands"""

    # Check if user is admin
    is_admin = ctx.author.guild_permissions.administrator

    if is_admin:
        # Admin sees all commands
        info_text = """KEY GENERATOR BOT - ALL COMMANDS

USER COMMANDS:
!g - Generate/claim a key (costs 5 credits)
!c - Check your credit balance
!i - Display this command list

ADMIN COMMANDS:
!g [amount] - Generate keys (no credit cost, optional amount)
!gk [amount] - Create keys and add to stock (default: 1)
!stock - View how many keys are available
!vk - View all available keys
!ck - Clear all available keys
!l [limit] - View recent claims (default: 10)
!ac @user <amount> - Give credits to a user
!rc @user <amount> - Remove credits from a user
!vc - View all users and their credits
!ann - Announce key restock to @everyone
"""
    else:
        # Regular users see only user commands
        info_text = """KEY GENERATOR BOT - COMMANDS

!g - Generate/claim a key (costs 5 credits)
!c - Check your credit balance
!i - Display this command list

Note: Each key costs 5 credits. You start with 15 credits.
Contact an admin to get more credits!
"""

    await ctx.send(f"```{info_text}```")

# Check credits command
@bot.command(name='c')
async def check_credits(ctx):
    """Check your credit balance"""
    user_id = str(ctx.author.id)
    
    # Initialize credits if user doesn't exist
    if user_id not in credits:
        credits[user_id] = STARTING_CREDITS
        save_credits(credits)
    
    user_credits = credits[user_id]
    await ctx.send(f"You have **{user_credits}** credits")

# Add credits command (admin only)
@bot.command(name='ac')
@commands.has_permissions(administrator=True)
async def add_credits(ctx, member: discord.Member, amount: int = None):
    """Give credits to a user"""
    if amount is None:
        await ctx.send("Usage: !ac @user <amount>")
        return
    
    if amount <= 0:
        await ctx.send("Amount must be greater than 0")
        return
    
    user_id = str(member.id)
    
    # Initialize credits if user doesn't exist
    if user_id not in credits:
        credits[user_id] = STARTING_CREDITS
    
    credits[user_id] += amount
    save_credits(credits)
    
    await ctx.send(f"Added **{amount}** credits to **{member.name}**\nNew balance: **{credits[user_id]}** credits")

# Remove credits command (admin only)
@bot.command(name='rc')
@commands.has_permissions(administrator=True)
async def remove_credits(ctx, member: discord.Member, amount: int = None):
    """Remove credits from a user"""
    if amount is None:
        await ctx.send("Usage: !rc @user <amount>")
        return
    
    if amount <= 0:
        await ctx.send("Amount must be greater than 0")
        return
    
    user_id = str(member.id)
    
    # Initialize credits if user doesn't exist
    if user_id not in credits:
        credits[user_id] = STARTING_CREDITS
    
    credits[user_id] -= amount
    
    # Don't allow negative credits
    if credits[user_id] < 0:
        credits[user_id] = 0
    
    save_credits(credits)
    
    await ctx.send(f"Removed **{amount}** credits from **{member.name}**\nNew balance: **{credits[user_id]}** credits")

# View all credits command (admin only)
@bot.command(name='vc')
@commands.has_permissions(administrator=True)
async def view_credits(ctx):
    """View all users and their credits"""
    if not credits:
        await ctx.send("No users have credits yet")
        return

    msg = "ALL USER CREDITS:\n\n"
    
    # Sort by credits (highest first)
    sorted_credits = sorted(credits.items(), key=lambda x: x[1], reverse=True)
    
    for user_id, user_credits in sorted_credits:
        try:
            user = await bot.fetch_user(int(user_id))
            msg += f"{user.name} ({user.id}) - {user_credits} credits\n"
        except:
            msg += f"Unknown User ({user_id}) - {user_credits} credits\n"

    # Discord has a 2000 character limit, so split if needed
    if len(msg) > 1900:
        await ctx.send("**ALL USER CREDITS:**")
        # Send in chunks
        for i in range(0, len(msg), 1900):
            await ctx.send(f"```{msg[i:i+1900]}```")
    else:
        await ctx.send(f"```{msg}```")

# Generate keys and add to stock (admin only)
@bot.command(name='gk')
@commands.has_permissions(administrator=True)
async def generate_keys_stock(ctx, amount: int = 1):
    """Generate keys and add them to stock"""
    
    if amount < 1:
        await ctx.send("Amount must be at least 1")
        return
    
    if amount > 50:
        await ctx.send("Maximum 50 keys per command")
        return
    
    generated_keys = []
    for i in range(amount):
        new_key = generate_key()
        # Make sure key is unique
        while new_key in keys["available"]:
            new_key = generate_key()
        
        keys["available"].append(new_key)
        generated_keys.append(new_key)
    
    save_keys(keys)
    
    # Send keys in DM to admin
    try:
        if amount == 1:
            await ctx.author.send(f"**Generated Key:**\n``{generated_keys[0]}``")
        else:
            dm_message = f"**Generated {amount} Keys:**\n"
            for idx, key in enumerate(generated_keys, 1):
                dm_message += f"{idx}. ``{key}``\n"
            await ctx.author.send(dm_message)
        
        await ctx.send(f"Generated **{amount}** key(s) and added to stock! Check your DMs.\nTotal stock: **{len(keys['available'])}** keys")
    except:
        await ctx.send(f"I couldn't DM you the keys. Please enable DMs!")

# Check stock
@bot.command(name='stock')
async def check_stock(ctx):
    """Check how many keys are available"""
    stock_count = len(keys["available"])
    await ctx.send(f"**Available Keys:** {stock_count}")

# View all available keys (admin only)
@bot.command(name='vk')
@commands.has_permissions(administrator=True)
async def view_keys(ctx):
    """View all available keys"""
    
    if len(keys["available"]) == 0:
        await ctx.send("No keys in stock")
        return
    
    keys_list = "\n".join([f"``{key}``" for key in keys["available"]])
    
    # Discord has a 2000 character limit
    if len(keys_list) > 1900:
        await ctx.send(f"**Available Keys ({len(keys['available'])}):**")
        for i in range(0, len(keys_list), 1900):
            await ctx.send(keys_list[i:i+1900])
    else:
        await ctx.send(f"**Available Keys ({len(keys['available'])}):**\n{keys_list}")

# Clear all keys (admin only)
@bot.command(name='ck')
@commands.has_permissions(administrator=True)
async def clear_keys(ctx):
    """Clear all available keys"""
    
    count = len(keys["available"])
    keys["available"] = []
    save_keys(keys)
    
    await ctx.send(f"Cleared **{count}** keys from stock")

# Generate/claim key
@bot.command(name='g')
async def generate_key_command(ctx, amount: int = 1):
    """Claim a key (costs 5 credits per key, admins get unlimited free)"""

    user_id = str(ctx.author.id)
    is_admin = ctx.author.guild_permissions.administrator

    # Regular users can only claim 1 key
    if not is_admin and amount > 1:
        await ctx.send("Only admins can claim multiple keys at once")
        return

    # Validate amount
    if amount < 1:
        await ctx.send("Amount must be at least 1")
        return

    if amount > 10:
        await ctx.send("Maximum 10 keys per command")
        return

    # Check credits (only for non-admins)
    if not is_admin:
        # Initialize credits if user doesn't exist
        if user_id not in credits:
            credits[user_id] = STARTING_CREDITS
            save_credits(credits)
        
        total_cost = KEY_COST * amount
        
        if credits[user_id] < total_cost:
            await ctx.send(f"Not enough credits! You have **{credits[user_id]}** credits but need **{total_cost}** credits ({KEY_COST} per key)")
            return

    # Check if keys are available
    if len(keys["available"]) == 0:
        await ctx.send(f"❌ No keys available in stock! Contact an admin.")
        return

    # Check if enough stock
    if len(keys["available"]) < amount:
        await ctx.send(f"Not enough stock! Only **{len(keys['available'])}** keys available")
        return

    # Get random keys
    claimed_keys = []
    for i in range(amount):
        key = random.choice(keys["available"])
        keys["available"].remove(key)
        claimed_keys.append(key)

        # Add to claimed
        keys["claimed"][key] = {
            "user": str(ctx.author),
            "user_id": user_id,
            "claimed_at": datetime.now().isoformat(),
            "is_admin": is_admin
        }

    save_keys(keys)

    # Deduct credits (only for non-admins)
    if not is_admin:
        total_cost = KEY_COST * amount
        credits[user_id] -= total_cost
        save_credits(credits)

    # Log the claims
    for key in claimed_keys:
        log_entry = {
            "user": str(ctx.author),
            "user_id": user_id,
            "key": key,
            "timestamp": datetime.now().isoformat(),
            "is_admin": is_admin,
            "credits_spent": 0 if is_admin else KEY_COST
        }
        logs.append(log_entry)
    save_logs(logs)

    # Send keys via DM
    try:
        if amount == 1:
            await ctx.author.send(f"**Your Key:**\n``{claimed_keys[0]}``")
        else:
            dm_message = f"**Your {amount} Keys:**\n"
            for idx, key in enumerate(claimed_keys, 1):
                dm_message += f"{idx}. ``{key}``\n"
            await ctx.author.send(dm_message)

        # Success message with credit info
        if is_admin:
            await ctx.send(f"✅ Check your DMs!")
        else:
            remaining_credits = credits[user_id]
            await ctx.send(f"✅ Check your DMs! Credits remaining: **{remaining_credits}**")
    except:
        await ctx.send(f"❌ I couldn't DM you. Please enable DMs and try again!")

# View logs
@bot.command(name='l')
@commands.has_permissions(administrator=True)
async def view_logs(ctx, limit: int = 10):
    """View recent key claims"""

    if not logs:
        await ctx.send("No logs available")
        return

    recent_logs = logs[-limit:]
    recent_logs.reverse()

    log_msg = f"**RECENT KEY CLAIMS (Last {len(recent_logs)}):**\n"
    for log in recent_logs:
        timestamp = datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        admin_badge = " [ADMIN]" if log.get('is_admin', False) else ""
        credits_info = f" (-{log.get('credits_spent', 0)} credits)" if log.get('credits_spent', 0) > 0 else ""
        log_msg += f"\n`{timestamp}` - {log['user']}{admin_badge} claimed key{credits_info}"

    await ctx.send(log_msg)

# Announce restock
@bot.command(name='ann')
@commands.has_permissions(administrator=True)
async def announce_restock(ctx):
    """Announce a key restock"""

    stock_count = len(keys["available"])

    if stock_count == 0:
        await ctx.send("No keys in stock to announce")
        return

    announcement = f"@everyone\n\n🎉 **KEY RESTOCK ALERT** 🎉\n\nKeys are now available!\n\nStock: **{stock_count}** keys\n\nUse `!g` to claim yours!\n(Costs {KEY_COST} credits per key)"

    await ctx.send(announcement)

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
