import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
from keep_alive import keep_alive

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

balances = {}
shop_items = {}
inventories = {}  # user_id -> {item_id: quantity}
item_counter = 1

WORK_ACTIONS = [
    {"desc": "You helped a neighbor move furniture all day. Sweaty work but they paid up.", "flavor": "Manual labor hits different."},
    {"desc": "You washed cars outside the corner store for hours. People actually tipped.", "flavor": "Respect the grind."},
    {"desc": "You sold plates out the back of someone's kitchen. Food went fast.", "flavor": "Everyone eats when you cook."},
    {"desc": "You cut grass up and down the block with a borrowed mower.", "flavor": "Lawn game on point."},
    {"desc": "You did a delivery run across town on your bike. Legs are dead but the bread is real.", "flavor": "No days off."},
    {"desc": "You helped unload trucks at the warehouse from midnight to 6am.", "flavor": "While they slept, you worked."},
    {"desc": "You painted a fence for an OG down the street. He paid cash, no questions.", "flavor": "Honest money."},
    {"desc": "You bagged groceries at the market for a full shift.", "flavor": "Every dollar counts."},
    {"desc": "You cleaned out a garage and found some stuff worth keeping too.", "flavor": "Bonus score."},
    {"desc": "You fixed someone's phone screen in the parking lot. Word spread, did three more after.", "flavor": "Skills pay bills."},
    {"desc": "You flipped a pair of sneakers you copped early. Doubled up.", "flavor": "Buy low, sell high."},
    {"desc": "You sold homemade tamales outside the laundromat. Sold out in two hours.", "flavor": "Grandma's recipe never fails."},
    {"desc": "You ran a dice game in the alley and the math worked in your favor tonight.", "flavor": "Lucky or smart? Both."},
    {"desc": "You detailed a car for a guy who just needed it done same day.", "flavor": "Same day, same pay."},
    {"desc": "You sold mixtapes out of a backpack at the bus stop.", "flavor": "Supporting local artists."},
    {"desc": "You did hair in the kitchen all afternoon. Appointments back to back.", "flavor": "The chair stays full."},
    {"desc": "You fixed a busted exhaust for the neighbor's cousin. He paid in cash and referred two more.", "flavor": "Backyard mechanic money."},
    {"desc": "You resold some stuff from the swap meet online. Profit margin was clean.", "flavor": "Arbitrage, hood edition."},
    {"desc": "You cooked and sold plates out of the trunk at the park.", "flavor": "The park always eats."},
    {"desc": "You set up a table and sold phone cases and chargers downtown.", "flavor": "Accessories move fast."},
    {"desc": "You found a wallet. Returned it. They rewarded you and you kept it honest.", "flavor": "Good karma pays."},
    {"desc": "You won a bet on a pickup basketball game. Called the shot and hit it.", "flavor": "Confidence is currency."},
    {"desc": "You helped a lady carry groceries and she blessed you with more than expected.", "flavor": "Kindness came back around."},
    {"desc": "You entered a local rap battle at the rec center. Judges gave you the W.", "flavor": "The crowd don't lie."},
    {"desc": "You did a favor for someone who always pays back what he owes. Today was that day.", "flavor": "Old debt, new bread."},
]

# --- Helpers ---

def is_admin(message):
    return isinstance(message.author, discord.Member) and message.author.guild_permissions.administrator

def get_balance(user_id):
    return balances.get(user_id, 0)

def add_balance(user_id, amount):
    balances[user_id] = get_balance(user_id) + amount

def remove_balance(user_id, amount):
    balances[user_id] = max(0, get_balance(user_id) - amount)

def get_inventory(user_id):
    return inventories.get(user_id, {})

def add_to_inventory(user_id, item_id, quantity=1):
    if user_id not in inventories:
        inventories[user_id] = {}
    inventories[user_id][item_id] = inventories[user_id].get(item_id, 0) + quantity

def remove_from_inventory(user_id, item_id, quantity=1):
    if user_id not in inventories:
        return False
    current = inventories[user_id].get(item_id, 0)
    if current < quantity:
        return False
    inventories[user_id][item_id] = current - quantity
    if inventories[user_id][item_id] == 0:
        del inventories[user_id][item_id]
    return True

# --- Commands ---

async def handle_work(message, args):
    user_id = message.author.id
    amount = random.randint(1, 100)
    action = random.choice(WORK_ACTIONS)
    add_balance(user_id, amount)

    embed = discord.Embed(title="Work", description=action["desc"], color=discord.Color.green())
    embed.add_field(name="Earned", value=f"**${amount:,}**", inline=True)
    embed.add_field(name="Balance", value=f"**${get_balance(user_id):,}**", inline=True)
    embed.set_footer(text=action["flavor"])
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    await message.channel.send(embed=embed)


async def handle_bal(message, args):
    # bal or bal @user
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author

    user_id = target.id
    balance = get_balance(user_id)
    inv = get_inventory(user_id)
    total_items = sum(inv.values())

    embed = discord.Embed(title="Balance", color=discord.Color.gold())
    embed.set_author(name=target.display_name, icon_url=target.display_avatar.url)
    embed.add_field(name="Wallet", value=f"**${balance:,}**", inline=True)
    embed.add_field(name="Items Owned", value=f"**{total_items}**", inline=True)
    embed.set_footer(text="Use `inv` to see your inventory.")
    await message.channel.send(embed=embed)


async def handle_inv(message, args):
    # inv or inv @user
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author

    user_id = target.id
    inv = get_inventory(user_id)

    if not inv:
        embed = discord.Embed(
            title=f"{target.display_name}'s Inventory",
            description="Nothing here yet. Buy something from the `shop`.",
            color=discord.Color.dark_grey()
        )
        await message.channel.send(embed=embed)
        return

    embed = discord.Embed(
        title=f"{target.display_name}'s Inventory",
        description="Use `use <id>` to use an item.",
        color=discord.Color.blurple()
    )
    embed.set_author(name=target.display_name, icon_url=target.display_avatar.url)

    for item_id, qty in inv.items():
        item = shop_items.get(item_id)
        if item:
            embed.add_field(
                name=f"[#{item_id}]  {item['name']}  x{qty}",
                value=item['description'],
                inline=False
            )
        else:
            # Item was removed from shop but user still owns it
            embed.add_field(
                name=f"[#{item_id}]  Unknown Item  x{qty}",
                value="This item no longer exists in the shop.",
                inline=False
            )

    total_items = sum(inv.values())
    embed.set_footer(text=f"{total_items} total item(s) in inventory.")
    await message.channel.send(embed=embed)


async def handle_shop(message, args):
    global item_counter

    sub = args[0].lower() if args else "view"

    # ── VIEW ──────────────────────────────────────────────
    if sub == "view" or not args:
        if not shop_items:
            embed = discord.Embed(
                title="🛒  Shop",
                description="The shop is empty right now. Check back later.",
                color=discord.Color.dark_grey()
            )
            await message.channel.send(embed=embed)
            return

        embed = discord.Embed(
            title="🛒  Shop",
            description="Browse the available items below. Use `buy <id>` to purchase.",
            color=discord.Color.gold()
        )
        for item_id, item in shop_items.items():
            embed.add_field(
                name=f"[#{item_id}]  {item['name']}  —  ${item['price']:,}",
                value=item['description'],
                inline=False
            )
        embed.set_footer(text=f"{len(shop_items)} item(s) available")
        await message.channel.send(embed=embed)

    # ── ADD (admin) ────────────────────────────────────────
    elif sub == "add":
        if not is_admin(message):
            await message.channel.send("You don't have permission to do that.")
            return

        if len(args) < 4:
            await message.channel.send(
                "Usage: `shop add <name> <price> <description>`\n"
                "Example: `shop add Sneakers 250 A clean pair of kicks.`"
            )
            return

        name = args[1]
        try:
            price = int(args[2])
        except ValueError:
            await message.channel.send("Price must be a whole number.")
            return

        if price < 1:
            await message.channel.send("Price must be at least $1.")
            return

        description = " ".join(args[3:])
        item_id = item_counter
        shop_items[item_id] = {"name": name, "price": price, "description": description}
        item_counter += 1

        embed = discord.Embed(title="Item Added", color=discord.Color.green())
        embed.add_field(name="ID", value=f"`#{item_id}`", inline=True)
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="Price", value=f"${price:,}", inline=True)
        embed.add_field(name="Description", value=description, inline=False)
        embed.set_footer(text=f"Shop now has {len(shop_items)} item(s).")
        await message.channel.send(embed=embed)

    # ── REMOVE (admin) ─────────────────────────────────────
    elif sub == "remove":
        if not is_admin(message):
            await message.channel.send("You don't have permission to do that.")
            return

        if len(args) < 2:
            await message.channel.send("Usage: `shop remove <id>`")
            return

        try:
            item_id = int(args[1])
        except ValueError:
            await message.channel.send("ID must be a number.")
            return

        if item_id not in shop_items:
            await message.channel.send(f"No item found with ID `#{item_id}`.")
            return

        removed = shop_items.pop(item_id)
        embed = discord.Embed(
            title="Item Removed",
            description=f"**{removed['name']}** (`#{item_id}`) has been removed from the shop.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Shop now has {len(shop_items)} item(s).")
        await message.channel.send(embed=embed)

    # ── EDIT (admin) ───────────────────────────────────────
    elif sub == "edit":
        if not is_admin(message):
            await message.channel.send("You don't have permission to do that.")
            return

        if len(args) < 5:
            await message.channel.send(
                "Usage: `shop edit <id> <name> <price> <description>`\n"
                "Example: `shop edit 1 Sneakers 300 Updated description here.`"
            )
            return

        try:
            item_id = int(args[1])
        except ValueError:
            await message.channel.send("ID must be a number.")
            return

        if item_id not in shop_items:
            await message.channel.send(f"No item found with ID `#{item_id}`.")
            return

        name = args[2]
        try:
            price = int(args[3])
        except ValueError:
            await message.channel.send("Price must be a whole number.")
            return

        if price < 1:
            await message.channel.send("Price must be at least $1.")
            return

        description = " ".join(args[4:])
        shop_items[item_id] = {"name": name, "price": price, "description": description}

        embed = discord.Embed(title="Item Updated", color=discord.Color.blue())
        embed.add_field(name="ID", value=f"`#{item_id}`", inline=True)
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="Price", value=f"${price:,}", inline=True)
        embed.add_field(name="Description", value=description, inline=False)
        await message.channel.send(embed=embed)

    else:
        await message.channel.send(
            "Unknown subcommand. Usage:\n"
            "`shop` — view the shop\n"
            "`shop add <name> <price> <description>` — admin only\n"
            "`shop remove <id>` — admin only\n"
            "`shop edit <id> <name> <price> <description>` — admin only"
        )


async def handle_buy(message, args):
    if not args:
        await message.channel.send("Usage: `buy <id>`  —  Example: `buy 1`")
        return

    try:
        item_id = int(args[0])
    except ValueError:
        await message.channel.send("ID must be a number. Example: `buy 1`")
        return

    item = shop_items.get(item_id)
    if not item:
        await message.channel.send(f"No item found with ID `#{item_id}`. Use `shop` to browse.")
        return

    user_id = message.author.id
    balance = get_balance(user_id)

    if balance < item['price']:
        shortage = item['price'] - balance
        embed = discord.Embed(
            title="Insufficient Funds",
            description=f"**{item['name']}** costs **${item['price']:,}** but you only have **${balance:,}**.\nYou're **${shortage:,}** short. Get back to `work`.",
            color=discord.Color.red()
        )
        await message.channel.send(embed=embed)
        return

    remove_balance(user_id, item['price'])
    add_to_inventory(user_id, item_id)

    embed = discord.Embed(
        title="Purchase Successful",
        description=f"You bought **{item['name']}**.",
        color=discord.Color.green()
    )
    embed.add_field(name="Item", value=item['name'], inline=True)
    embed.add_field(name="Cost", value=f"${item['price']:,}", inline=True)
    embed.add_field(name="Remaining Balance", value=f"${get_balance(user_id):,}", inline=True)
    embed.add_field(name="Description", value=item['description'], inline=False)
    embed.set_footer(text="Use `inv` to see your inventory. Use `use <id>` to use it.")
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    await message.channel.send(embed=embed)


async def handle_use(message, args):
    if not args:
        await message.channel.send("Usage: `use <id>`  —  Example: `use 1`")
        return

    try:
        item_id = int(args[0])
    except ValueError:
        await message.channel.send("ID must be a number. Example: `use 1`")
        return

    user_id = message.author.id
    inv = get_inventory(user_id)

    if item_id not in inv or inv[item_id] < 1:
        await message.channel.send(f"You don't have item `#{item_id}` in your inventory. Use `inv` to check what you own.")
        return

    item = shop_items.get(item_id)
    item_name = item['name'] if item else f"Item #{item_id}"
    item_desc = item['description'] if item else "No description available."

    remove_from_inventory(user_id, item_id)

    embed = discord.Embed(
        title=f"Used — {item_name}",
        description=f"You used **{item_name}**.\n\n{item_desc}",
        color=discord.Color.purple()
    )
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)

    remaining = get_inventory(user_id).get(item_id, 0)
    if remaining > 0:
        embed.set_footer(text=f"You have {remaining}x {item_name} left.")
    else:
        embed.set_footer(text=f"That was your last {item_name}.")

    await message.channel.send(embed=embed)


# --- Bot plumbing ---

COMMANDS = {
    "work": handle_work,
    "bal": handle_bal,
    "balance": handle_bal,
    "inv": handle_inv,
    "inventory": handle_inv,
    "shop": handle_shop,
    "buy": handle_buy,
    "use": handle_use,
}

@bot.event
async def on_ready():
    print(f'{bot.user} is online and ready.')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.guild is None:
        await message.channel.send("Commands only work in servers, not DMs.")
        return

    parts = message.content.strip().split()
    if not parts:
        return

    cmd = parts[0].lower()
    args = parts[1:]

    if cmd in COMMANDS:
        try:
            await COMMANDS[cmd](message, args)
        except discord.HTTPException as e:
            print(f"HTTP error in {cmd}: {e}")
            try:
                await message.channel.send("Something went wrong. Try again.")
            except:
                pass
        except Exception as e:
            import traceback
            print(f"Error in {cmd}: {e}")
            traceback.print_exc()
            try:
                await message.channel.send("An error occurred. Check the logs.")
            except:
                pass

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env")
    else:
        keep_alive()
        bot.run(TOKEN)
