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
bot = commands.Bot(command_prefix='?', intents=intents)

# Files
VAMPIRES_FILE = 'vampires.json'
BATTLE_LOGS_FILE = 'battle_logs.json'
CREDITS_FILE = 'credits.json'

# Blocked channel ID
BLOCKED_CHANNEL_ID = 1470843481177198876

# Credit settings
MAX_CREDITS = 3
CREDIT_COST = 1
CREDIT_COOLDOWN_MINUTES = 30

# Load vampires
def load_vampires():
    if os.path.exists(VAMPIRES_FILE):
        with open(VAMPIRES_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save vampires
def save_vampires(vampires):
    with open(VAMPIRES_FILE, 'w') as f:
        json.dump(vampires, f, indent=4)

# Load battle logs
def load_battle_logs():
    if os.path.exists(BATTLE_LOGS_FILE):
        with open(BATTLE_LOGS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save battle logs
def save_battle_logs(logs):
    with open(BATTLE_LOGS_FILE, 'w') as f:
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

# Check and update credits
def check_credits(user_id):
    """Check if user has credits available or if cooldown has passed"""
    credits = load_credits()
    
    if user_id not in credits:
        # New user, give them max credits
        credits[user_id] = {
            "credits": MAX_CREDITS,
            "last_refill": datetime.now().isoformat()
        }
        save_credits(credits)
        return MAX_CREDITS, None
    
    user_data = credits[user_id]
    current_credits = user_data["credits"]
    
    # If they have credits, return them
    if current_credits > 0:
        return current_credits, None
    
    # Check if cooldown has passed
    last_refill = datetime.fromisoformat(user_data["last_refill"])
    time_passed = datetime.now() - last_refill
    cooldown_duration = timedelta(minutes=CREDIT_COOLDOWN_MINUTES)
    
    if time_passed >= cooldown_duration:
        # Cooldown passed, refill credits
        credits[user_id]["credits"] = MAX_CREDITS
        credits[user_id]["last_refill"] = datetime.now().isoformat()
        save_credits(credits)
        return MAX_CREDITS, None
    else:
        # Still on cooldown
        time_remaining = cooldown_duration - time_passed
        return 0, time_remaining

# Use a credit
def use_credit(user_id):
    """Deduct one credit from user"""
    credits = load_credits()
    
    if user_id not in credits:
        credits[user_id] = {
            "credits": MAX_CREDITS,
            "last_refill": datetime.now().isoformat()
        }
    
    credits[user_id]["credits"] -= CREDIT_COST
    
    # If credits hit 0, start the cooldown timer
    if credits[user_id]["credits"] == 0:
        credits[user_id]["last_refill"] = datetime.now().isoformat()
    
    save_credits(credits)

# Generate unique 6-digit ID
def generate_vampire_id(vampires):
    while True:
        vampire_id = str(random.randint(100000, 999999))
        if vampire_id not in vampires:
            return vampire_id

# Generate AI opponent based on player power (IMPROVED SCALING)
def generate_ai_opponent(player_power):
    """Generate an AI opponent that scales with player power - can go up to 100k"""
    
    # AI names pool (expanded)
    ai_names = [
        "Marcus the Merciless", "Elena the Ruthless", "Drakon the Savage", 
        "Nyx the Deadly", "Kain the Brutal", "Sable the Vicious",
        "Cyrus the Cruel", "Morrigan the Fierce", "Vex the Relentless",
        "Azrael the Destroyer", "Valeria the Bloodletter", "Theron the Merciless",
        "Ravenna the Shadow", "Darius the Ancient", "Lysandra the Wicked",
        "Cain the Accursed", "Octavia the Dread", "Grimwald the Eternal",
        "Seraphine the Void", "Lucien the Plague", "Morgath the Fallen",
        "Vesper the Nightbane", "Zephyr the Sinister", "Alaric the Cursed",
        "Belladonna the Profane", "Cassius the Corrupted", "Nero the Vile",
        "Isolde the Vengeful", "Draven the Malevolent", "Xander the Apostate"
    ]
    
    # Scale AI power based on player power with extended range
    # AI power range: player_power ± 20-30%
    min_variance = 0.70  # AI can be 30% weaker
    max_variance = 1.30  # AI can be 30% stronger
    
    # Calculate AI power range
    min_power = int(player_power * min_variance)
    max_power = int(player_power * max_variance)
    
    # Ensure minimum of 60 and maximum of 100,000
    min_power = max(60, min_power)
    max_power = min(100000, max_power)
    
    ai_power = random.randint(min_power, max_power)
    
    # Determine difficulty tier b
