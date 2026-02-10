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
bot = commands.Bot(command_prefix='!', intents=intents)

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
    print('Account Generator Ready')

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
        info_text = """ACCOUNT GENERATOR BOT - ALL COMMANDS

USER COMMANDS:
!g <type> - Claim an account (costs 5 credits, whitelist required)
!s - Check stock for all types
!c - Check your credit balance
!i - Display this command list

ADMIN COMMANDS:
!g <type> [amount] - Generate accounts (no credit cost, optional amount)
!rs <type> - Upload .txt file to add accounts
!cl <type> - Clear all accounts of a specific type
!vs <type> - View all accounts in stock for a type
!l [limit] - View recent claims (default: 10)
!ac @user <amount> - Give credits to a user
!rc @user <amount> - Remove credits from a user
!vc - View all users and their credits
!ann <type> - Announce restock to @everyone
!aw @user - Add user to whitelist
!rw @user - Remove user from whitelist
!vw - View all whitelisted users
"""
    else:
        # Regular users see only user commands
        info_text = """ACCOUNT GENERATOR BOT - COMMANDS

!g <type> - Claim an account (costs 5 credits, whitelist required)
!s - Check stock for all types
!c - Check your credit balance
!i - Display this command list

Note: You must be whitelisted to use !g
Each generation costs 5 credits. You start with 15 credits.
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
            whitelist_status = " [WHITELISTED]" if user_id in whitelist else ""
            msg += f"{user.name} ({user.id}){whitelist_status} - {user_credits} credits\n"
        except:
            whitelist_status = " [WHITELISTED]" if user_id in whitelist else ""
            msg += f"Unknown User ({user_id}){whitelist_status} - {user_credits} credits\n"

    # Discord has a 2000 character limit, so split if needed
    if len(msg) > 1900:
        await ctx.send("**ALL USER CREDITS:**")
        # Send in chunks
        for i in range(0, len(msg), 1900):
            await ctx.send(f"```{msg[i:i+1900]}```")
    else:
        await ctx.send(f"```{msg}```")

# Add user to whitelist
@bot.command(name='aw')
@commands.has_permissions(administrator=True)
async def add_whitelist(ctx, member: discord.Member):
    """Add a user to the whitelist"""
    user_id = str(member.id)

    if user_id in whitelist:
        await ctx.send(f"**{member.name}** is already whitelisted")
        return

    whitelist.append(user_id)
    save_whitelist(whitelist)
    
    # Initialize credits for new whitelisted user
    if user_id not in credits:
        credits[user_id] = STARTING_CREDITS
        save_credits(credits)
    
    await ctx.send(f"Added **{member.name}** to whitelist with **{STARTING_CREDITS}** starting credits")

# Remove user from whitelist
@bot.command(name='rw')
@commands.has_permissions(administrator=True)
async def remove_whitelist(ctx, member: discord.Member):
    """Remove a user from the whitelist"""
    user_id = str(member.id)

    if user_id not in whitelist:
        await ctx.send(f"**{member.name}** is not whitelisted")
        return

    whitelist.remove(user_id)
    save_whitelist(whitelist)
    await ctx.send(f"Removed **{member.name}** from whitelist")

# View whitelist
@bot.command(name='vw')
@commands.has_permissions(administrator=True)
async def view_whitelist(ctx):
    """View all whitelisted users"""
    if not whitelist:
        await ctx.send("Whitelist is empty")
        return

    msg = "WHITELISTED USERS:\n\n"
    for user_id in whitelist:
        try:
            user = await bot.fetch_user(int(user_id))
            user_credits = credits.get(user_id, STARTING_CREDITS)
            msg += f"{user.name} ({user.id}) - {user_credits} credits\n"
        except:
            user_credits = credits.get(user_id, STARTING_CREDITS)
            msg += f"Unknown User ({user_id}) - {user_credits} credits\n"

    await ctx.send(f"```{msg}```")

# Restock from file
@bot.command(name='rs')
@commands.has_permissions(administrator=True)
async def restock_from_file(ctx, account_type: str = None):
    """Restock from a txt file - attach the file when using this command"""

    if account_type is None:
        await ctx.send("Usage: !rs <type> (and attach a .txt file)")
        return

    account_type = account_type.lower()

    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach a .txt file with accounts")
        return

    attachment = ctx.message.attachments[0]

    if not attachment.filename.endswith('.txt'):
        await ctx.send("File must be a .txt file")
        return

    # Download and read file
    file_content = await attachment.read()
    accounts_list = file_content.decode('utf-8').strip().split('\n')

    # Remove empty lines
    accounts_list = [acc.strip() for acc in accounts_list if acc.strip()]

    if account_type not in accounts:
        accounts[account_type] = []

    # Add accounts
    accounts[account_type].extend(accounts_list)
    save_accounts(accounts)

    await ctx.send(f"Successfully added {len(accounts_list)} accounts to **{account_type}**\nTotal stock: {len(accounts[account_type])}")

# Clear accounts
@bot.command(name='cl')
@commands.has_permissions(administrator=True)
async def clear_accounts(ctx, account_type: str = None):
    """Clear all accounts of a specific type"""

    if account_type is None:
        await ctx.send("Usage: !cl <type>")
        return

    account_type = account_type.lower()

    if account_type not in accounts:
        await ctx.send(f"No accounts found for type: **{account_type}**")
        return

    count = len(accounts[account_type])
    accounts[account_type] = []
    save_accounts(accounts)

    await ctx.send(f"Cleared {count} accounts from **{account_type}**")

# View stock for specific type
@bot.command(name='vs')
@commands.has_permissions(administrator=True)
async def view_stock(ctx, account_type: str = None):
    """View all accounts in stock for a type"""

    if account_type is None:
        await ctx.send("Usage: !vs <type>")
        return

    account_type = account_type.lower()

    if account_type not in accounts or len(accounts[account_type]) == 0:
        await ctx.send(f"No accounts in stock for **{account_type}**")
        return

    stock_list = "\n".join(accounts[account_type])

    # Discord has a 2000 character limit, so split if needed
    if len(stock_list) > 1900:
        await ctx.send(f"**{account_type}** stock ({len(accounts[account_type])} accounts):")
        # Send in chunks
        for i in range(0, len(stock_list), 1900):
            await ctx.send(f"```{stock_list[i:i+1900]}```")
    else:
        await ctx.send(f"**{account_type}** stock ({len(accounts[account_type])} accounts):\n```{stock_list}```")

# Check stock
@bot.command(name='s')
async def check_stock(ctx):
    """Check available stock for all account types"""

    if not accounts or all(len(accs) == 0 for accs in accounts.values()):
        await ctx.send("No accounts in stock")
        return

    stock_msg = "**CURRENT STOCK:**\n"
    for acc_type, acc_list in accounts.items():
        stock_msg += f"{acc_type}: {len(acc_list)} available\n"

    await ctx.send(stock_msg)

# Generate/claim account
@bot.command(name='g')
async def generate_account(ctx, account_type: str = None, amount: int = 1):
    """Claim an account (costs 5 credits per account, whitelist required, admins get unlimited free gens)"""

    user_id = str(ctx.author.id)
    is_admin = ctx.author.guild_permissions.administrator

    # Check whitelist (admins bypass this)
    if not is_admin and user_id not in whitelist:
        await ctx.send("You are not whitelisted to use this command")
        return

    if account_type is None:
        await ctx.send("Usage: !g <type> [amount] (amount is optional, admins only)")
        return

    account_type = account_type.lower()

    # Regular users can only claim 1 account
    if not is_admin and amount > 1:
        await ctx.send("Only admins can claim multiple accounts at once")
        return

    # Validate amount
    if amount < 1:
        await ctx.send("Amount must be at least 1")
        return

    if amount > 10:
        await ctx.send("Maximum 10 accounts per command")
        return

    # Check credits (only for non-admins)
    if not is_admin:
        # Initialize credits if user doesn't exist
        if user_id not in credits:
            credits[user_id] = STARTING_CREDITS
            save_credits(credits)
        
        total_cost = GEN_COST * amount
        
        if credits[user_id] < total_cost:
            await ctx.send(f"Not enough credits! You have **{credits[user_id]}** credits but need **{total_cost}** credits ({GEN_COST} per account)")
            return

    # Check if type exists
    if account_type not in accounts or len(accounts[account_type]) == 0:
        await ctx.send(f"No accounts available for **{account_type}**")
        return

    # Check if enough stock
    if len(accounts[account_type]) < amount:
        await ctx.send(f"Not enough stock! Only {len(accounts[account_type])} accounts available for **{account_type}**")
        return

    # Get random accounts
    claimed_accounts = []
    for i in range(amount):
        account = random.choice(accounts[account_type])
        accounts[account_type].remove(account)
        claimed_accounts.append(account)

    save_accounts(accounts)

    # Deduct credits (only for non-admins)
    if not is_admin:
        total_cost = GEN_COST * amount
        credits[user_id] -= total_cost
        save_credits(credits)

    # Log the claims
    for account in claimed_accounts:
        log_entry = {
            "user": str(ctx.author),
            "user_id": user_id,
            "type": account_type,
            "account": account,
            "timestamp": datetime.now().isoformat(),
            "is_admin": is_admin,
            "credits_spent": 0 if is_admin else GEN_COST
        }
        logs.append(log_entry)
    save_logs(logs)

    # Send accounts via DM with double backtick formatting
    try:
        if amount == 1:
            await ctx.author.send(f"**Your {account_type} account:**\n``{claimed_accounts[0]}``")
        else:
            dm_message = f"**Your {amount} {account_type} accounts:**\n"
            for idx, account in enumerate(claimed_accounts, 1):
                dm_message += f"{idx}. ``{account}``\n"
            await ctx.author.send(dm_message)

        # Success message with credit info (NO MENTION)
        if is_admin:
            await ctx.send(f"Check your DMs!")
        else:
            remaining_credits = credits[user_id]
            await ctx.send(f"Check your DMs! Credits remaining: **{remaining_credits}**")
    except:
        await ctx.send(f"I couldn't DM you. Please enable DMs and try again!")

# View logs
@bot.command(name='l')
@commands.has_permissions(administrator=True)
async def view_logs(ctx, limit: int = 10):
    """View recent claim logs"""

    if not logs:
        await ctx.send("No logs available")
        return

    recent_logs = logs[-limit:]
    recent_logs.reverse()

    log_msg = f"**RECENT CLAIMS (Last {len(recent_logs)}):**\n"
    for log in recent_logs:
        timestamp = datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        admin_badge = " [ADMIN]" if log.get('is_admin', False) else ""
        credits_info = f" (-{log.get('credits_spent', 0)} credits)" if log.get('credits_spent', 0) > 0 else ""
        log_msg += f"\n`{timestamp}` - {log['user']}{admin_badge} claimed **{log['type']}**{credits_info}"

    await ctx.send(log_msg)

# Announce restock
@bot.command(name='ann')
@commands.has_permissions(administrator=True)
async def announce_restock(ctx, account_type: str = None):
    """Announce a restock"""

    if account_type is None:
        await ctx.send("Usage: !ann <type>")
        return

    account_type = account_type.lower()

    if account_type not in accounts or len(accounts[account_type]) == 0:
        await ctx.send(f"No stock available for **{account_type}**")
        return

    stock_count = len(accounts[account_type])

    announcement = f"@everyone\n\n🎉 **RESTOCK ALERT** 🎉\n\n**{account_type.upper()}** accounts are now available!\n\nStock: {stock_count} accounts\n\nUse `!g {account_type}` to claim yours!\n(Costs {GEN_COST} credits per account)"

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
