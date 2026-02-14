import discord
from discord.ext import commands, tasks
import json
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import shutil
Load environment variables
load_dotenv()
Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=’?’, intents=intents, help_command=None)
Files
KEYS_FILE = ‘keys.json’
CONFIG_FILE = ‘config.json’
BLACKLIST_FILE = ‘blacklist.json’
CLAIMED_KEYS_FILE = ‘claimed_keys.json’
COOLDOWNS_FILE = ‘cooldowns.json’
STATS_FILE = ‘stats.json’
BACKUP_DIR = ‘backups’
Spam detection settings
SPAM_THRESHOLD = 1
SPAM_TIMEFRAME = 3
user_command_times = {}
Auto-blacklist removal time (5 hours)
AUTO_BLACKLIST_REMOVAL_HOURS = 5
Create backup directory if it doesn’t exist
if not os.path.exists(BACKUP_DIR):
os.makedirs(BACKUP_DIR)
Load config
def load_config():
if os.path.exists(CONFIG_FILE):
with open(CONFIG_FILE, ‘r’) as f:
return json.load(f)
return {}
Save config
def save_config(config):
with open(CONFIG_FILE, ‘w’) as f:
json.dump(config, f, indent=4)
config = load_config()
Get key limit for server
def get_key_limit(guild_id):
guild_id_str = str(guild_id)
if guild_id_str in config and ‘max_keys’ in config[guild_id_str]:
return config[guild_id_str][‘max_keys’]
return 3  # Default
Get cooldown duration for server (in hours)
def get_cooldown_hours(guild_id):
guild_id_str = str(guild_id)
if guild_id_str in config and ‘cooldown_hours’ in config[guild_id_str]:
return config[guild_id_str][‘cooldown_hours’]
return 1  # Default
Load blacklist with timestamps
def load_blacklist():
if os.path.exists(BLACKLIST_FILE):
with open(BLACKLIST_FILE, ‘r’) as f:
data = json.load(f)
Convert old format to new format if needed
if isinstance(data, list):
Old format: just list of user IDs
new_format = {}
for user_id in data:
new_format[str(user_id)] = {
‘blacklisted_at’: datetime.now().isoformat(),
‘auto_remove’: True
}
return new_format
else:
New format: dict with timestamps
for user_id in data:
if ‘blacklisted_at’ in data[user_id]:
data[user_id][‘blacklisted_at’] = datetime.fromisoformat(data[user_id][‘blacklisted_at’])
return data
return {}
Save blacklist
def save_blacklist(blacklist_data):
data_to_save = {}
for user_id, info in blacklist_data.items():
data_to_save[user_id] = {
‘blacklisted_at’: info[‘blacklisted_at’].isoformat() if isinstance(info[‘blacklisted_at’], datetime) else info[‘blacklisted_at’],
‘auto_remove’: info.get(‘auto_remove’, True)
}
with open(BLACKLIST_FILE, ‘w’) as f:
json.dump(data_to_save, f, indent=4)
blacklist = load_blacklist()
Load claimed keys history
def load_claimed_keys():
if os.path.exists(CLAIMED_KEYS_FILE):
with open(CLAIMED_KEYS_FILE, ‘r’) as f:
return json.load(f)
return []
Save claimed keys history
def save_claimed_keys(claimed_keys):
with open(CLAIMED_KEYS_FILE, ‘w’) as f:
json.dump(claimed_keys, f, indent=4)
claimed_keys = load_claimed_keys()
Load cooldowns
def load_cooldowns():
if os.path.exists(COOLDOWNS_FILE):
with open(COOLDOWNS_FILE, ‘r’) as f:
data = json.load(f)
for user_id in data:
if ‘cooldown_until’ in data[user_id] and data[user_id][‘cooldown_until’]:
data[user_id][‘cooldown_until’] = datetime.fromisoformat(data[user_id][‘cooldown_until’])
return data
return {}
Save cooldowns
def save_cooldowns(cooldowns_data):
data_to_save = {}
for user_id, info in cooldowns_data.items():
data_to_save[user_id] = {
‘keys_claimed’: info[‘keys_claimed’],
‘cooldown_until’: info[‘cooldown_until’].isoformat() if info[‘cooldown_until’] else None,
‘cooldown_violations’: info.get(‘cooldown_violations’, 0)
}
with open(COOLDOWNS_FILE, ‘w’) as f:
json.dump(data_to_save, f, indent=4)
cooldowns = load_cooldowns()
Load stats
def load_stats():
if os.path.exists(STATS_FILE):
with open(STATS_FILE, ‘r’) as f:
return json.load(f)
return {
‘total_keys_added’: 0,
‘total_keys_claimed’: 0,
‘total_restocks’: 0,
‘total_blacklists’: 0,
‘total_auto_unblacklists’: 0,
‘most_active_claimer’: {‘user_id’: None, ‘count’: 0},
‘first_restock_date’: None,
‘last_restock_date’: None
}
Save stats
def save_stats(stats_data):
with open(STATS_FILE, ‘w’) as f:
json.dump(stats_data, f, indent=4)
stats = load_stats()
Update stats
def update_stats(action, **kwargs):
global stats
if action == ‘restock’:
stats[‘total_keys_added’] += kwargs.get(‘count’, 0)
stats[‘total_restocks’] += 1
current_time = datetime.now().strftime(’%Y-%m-%d %H:%M:%S’)
stats[‘last_restock_date’] = current_time
if stats[‘first_restock_date’] is None:
stats[‘first_restock_date’] = current_time
elif action == ‘claim’:
stats[‘total_keys_claimed’] += kwargs.get(‘count’, 1)
user_id = kwargs.get(‘user_id’)

# Update most active claimer
user_claim_count = sum(1 for claim in claimed_keys if claim['user_id'] == user_id)
if user_claim_count > stats['most_active_claimer']['count']:
    stats['most_active_claimer'] = {
        'user_id': user_id,
        'count': user_claim_count
    }


eli
