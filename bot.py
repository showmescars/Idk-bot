import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import asyncio
from keep_alive import keep_alive

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

balances = {}

WORK_ACTIONS = [
    # Hustle / odd jobs
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
    # Side hustle
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
    # Random luck / found money
    {"desc": "You found a wallet. Returned it. They rewarded you and you kept it honest.", "flavor": "Good karma pays."},
    {"desc": "You won a bet on a pickup basketball game. Called the shot and hit it.", "flavor": "Confidence is currency."},
    {"desc": "You helped a lady carry groceries and she blessed you with more than expected.", "flavor": "Kindness came back around."},
    {"desc": "You entered a local rap battle at the rec center. Judges gave you the W.", "flavor": "The crowd don't lie."},
    {"desc": "You did a favor for someone who always pays back what he owes. Today was that day.", "flavor": "Old debt, new bread."},
]

def get_balance(user_id):
    return balances.get(user_id, 0)

def add_balance(user_id, amount):
    balances[user_id] = get_balance(user_id) + amount

async def handle_work(message, args):
    user_id = message.author.id
    amount = random.randint(1, 100)
    action = random.choice(WORK_ACTIONS)
    add_balance(user_id, amount)

    embed = discord.Embed(
        title="Work",
        description=action["desc"],
        color=discord.Color.green()
    )
    embed.add_field(name="Earned", value=f"**${amount:,}**", inline=True)
    embed.add_field(name="Balance", value=f"**${get_balance(user_id):,}**", inline=True)
    embed.set_footer(text=action["flavor"])
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)

    await message.channel.send(embed=embed)

COMMANDS = {
    "work": handle_work,
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
