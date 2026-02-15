import discord
from discord.ext import commands
import json
import os
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# Files
CHARACTERS_FILE = 'characters.json'
GRAVEYARD_FILE = 'graveyard.json'

# Vampire abilities pool
SKILLS = [
    "Blood Manipulation", "Shadow Travel", "Hypnotic Gaze", "Supernatural Speed",
    "Enhanced Strength", "Regeneration", "Mist Form", "Bat Transformation",
    "Mind Control", "Night Vision", "Wall Crawling", "Blood Drain",
    "Immortality", "Shapeshifting", "Feral Claws", "Venomous Bite",
    "Telepathy", "Superhuman Agility", "Blood Sense", "Darkness Manipulation",
    "Charm", "Fear Inducement", "Enhanced Senses", "Undead Resilience",
    "Thrall Creation", "Blood Healing", "Vampiric Speed", "Death Touch",
    "Soul Drain", "Crimson Lightning", "Bloodlust Rage", "Eternal Youth",
    "Mesmerize", "Bloodfire", "Cursed Bite", "Nightmare Inducement",
    "Blood Wings", "Lunar Empowerment", "Corpse Animation", "Dark Pact"
]

# Vampire name pools
FIRST_NAMES = [
    "Dracula", "Vladislav", "Carmilla", "Lestat", "Akasha", "Armand", "Blade", "Selene",
    "Viktor", "Marcus", "Lucian", "Sonja", "Aro", "Caius", "Demetri", "Jane",
    "Alec", "Elijah", "Klaus", "Rebekah", "Kol", "Finn", "Alaric", "Damon",
    "Stefan", "Katherine", "Silas", "Qetsiyah", "Amara", "Niklaus", "Mikael", "Esther",
    "Freya", "Dahlia", "Lucien", "Tristan", "Aurora", "Rayna", "Julian", "Lily",
    "Valerie", "Nora", "Mary", "Beau", "Oscar", "Malcolm", "Sage", "Maddox",
    "Atticus", "Greta", "Antoinette"
]

LAST_NAMES = [
    "Tepes", "Drăculești", "Karnstein", "De Lioncourt", "Enkil", "Romanus", "Corvinus", "Nightshade",
    "Von Doom", "Bloodworth", "Blackthorn", "Darkmore", "Volturi", "Mikaelson", "Salvatore", "Pierce",
    "Bennett", "Forbes", "Lockwood", "Donovan", "Gilbert", "Fell", "Whitmore", "St. John",
    "Ashford", "Bloodmoon", "Crimson", "Ravencroft", "Shadowend", "Duskbane", "Nocturne", "Grave",
    "Morningstar", "Hellsing", "Alucard", "Belmont", "Castlevania", "Blackwood", "Von Carstein", "Draken",
    "Mourning", "Eclipse", "Eventide", "Twilight", "Sanguine", "Hemlock", "Mortis", "Grimwood",
    "Nightfall", "Darkholm"
]

# Transfer requests storage (temporary, in-memory)
transfer_requests = {}

# Load characters
def load_characters():
    if os.path.exists(CHARACTERS_FILE):
        with open(CHARACTERS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save characters
def save_characters(characters):
    with open(CHARACTERS_FILE, 'w') as f:
        json.dump(characters, f, indent=4)

# Load graveyard
def load_graveyard():
    if os.path.exists(GRAVEYARD_FILE):
        with open(GRAVEYARD_FILE, 'r') as f:
            return json.load(f)
    return []

# Save graveyard
def save_graveyard(graveyard):
    with open(GRAVEYARD_FILE, 'w') as f:
        json.dump(graveyard, f, indent=4)

# Generate unique 6-digit ID
def generate_unique_id():
    characters = load_characters()
    graveyard = load_graveyard()
    existing_ids = [char.get('character_id') for char in characters.values() if 'character_id' in char]
    existing_ids += [char.get('character_id') for char in graveyard if 'character_id' in char]
    
    while True:
        new_id = str(random.randint(100000, 999999))
        if new_id not in existing_ids:
            return new_id

characters = load_characters()
graveyard = load_graveyard()

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    print('Vampire Generator Ready')

# Check to block DM commands
@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs")
        return False
    return True

# Make command - Creates a vampire
@bot.command(name='make')
async def make_character(ctx):
    """Generate a unique vampire with random abilities and power level"""
    
    user_id = str(ctx.author.id)
    
    # Check if user already has a vampire
    if user_id in characters:
        char = characters[user_id]
        
        # Display existing vampire
        embed = discord.Embed(
            title=char['name'],
            description=f"Owner: {ctx.author.name}\nID: `{char['character_id']}`\nRace: Vampire",
            color=discord.Color.dark_red()
        )
        
        embed.add_field(name="Blood Power", value=f"{char['power_level']}", inline=False)
        
        skills_text = "\n".join([f"- {skill}" for skill in char['skills']])
        embed.add_field(name="Vampiric Abilities", value=skills_text, inline=False)
        
        # Show record
        wins = char.get('wins', 0)
        losses = char.get('losses', 0)
        embed.add_field(name="Battle Record", value=f"{wins}W - {losses}L", inline=False)
        
        await ctx.send(embed=embed)
        return
    
    # Generate random vampire name
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    character_name = f"{first_name} {last_name}"
    
    # Generate unique character ID
    character_id = generate_unique_id()
    
    # Generate random power level (10 to 100)
    power_level = random.randint(10, 100)
    
    # Generate 3-5 random unique vampiric abilities
    num_skills = random.randint(3, 5)
    selected_skills = random.sample(SKILLS, num_skills)
    
    # Create vampire data
    character_data = {
        "character_id": character_id,
        "name": character_name,
        "username": str(ctx.author),
        "user_id": user_id,
        "power_level": power_level,
        "skills": selected_skills,
        "wins": 0,
        "losses": 0,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save vampire
    characters[user_id] = character_data
    save_characters(characters)
    
    # Display new vampire
    embed = discord.Embed(
        title=character_name,
        description=f"Owner: {ctx.author.name}\nID: `{character_id}`\nRace: Vampire",
        color=discord.Color.dark_red()
    )
    
    embed.add_field(name="Blood Power", value=f"{power_level}", inline=False)
    
    skills_text = "\n".join([f"- {skill}" for skill in selected_skills])
    embed.add_field(name="Vampiric Abilities", value=skills_text, inline=False)
    
    # Show initial record
    embed.add_field(name="Battle Record", value="0W - 0L", inline=False)
    
    await ctx.send(embed=embed)

# Show command - Shows your vampire
@bot.command(name='show')
async def show_character(ctx):
    """Show your vampire"""
    
    user_id = str(ctx.author.id)
    
    # Check if user has a vampire
    if user_id not in characters:
        await ctx.send("You don't have a vampire yet! Use `?make` to create one.")
        return
    
    char = characters[user_id]
    
    # Display vampire
    embed = discord.Embed(
        title=char['name'],
        description=f"Owner: {ctx.author.name}\nID: `{char['character_id']}`\nRace: Vampire",
        color=discord.Color.dark_red()
    )
    
    embed.add_field(name="Blood Power", value=f"{char['power_level']}", inline=False)
    
    skills_text = "\n".join([f"- {skill}" for skill in char['skills']])
    embed.add_field(name="Vampiric Abilities", value=skills_text, inline=False)
    
    # Show record
    wins = char.get('wins', 0)
    losses = char.get('losses', 0)
    embed.add_field(name="Battle Record", value=f"{wins}W - {losses}L", inline=False)
    
    await ctx.send(embed=embed)

# Train command - Train your vampire to become more powerful
@bot.command(name='train')
async def train_vampire(ctx, character_id: str = None):
    """Train your vampire to increase their power! Usage: ?train <character_id>"""
    
    # Check if character ID was provided
    if character_id is None:
        await ctx.send("Usage: `?train <character_id>`\nExample: `?train 123456`\n\nUse `?show` to see your vampire ID.")
        return
    
    user_id = str(ctx.author.id)
    
    # Check if user has a vampire
    if user_id not in characters:
        await ctx.send("You don't have a vampire yet! Use `?make` to create one.")
        return
    
    player_char = characters[user_id]
    
    # Verify the character ID matches
    if player_char['character_id'] != character_id:
        await ctx.send(f"Invalid vampire ID! Your vampire ID is `{player_char['character_id']}`")
        return
    
    # Training embed
    training_embed = discord.Embed(
        title="TRAINING SESSION",
        description=f"{player_char['name']} begins intense training in the shadows...",
        color=discord.Color.blue()
    )
    
    await ctx.send(embed=training_embed)
    
    # 3 second delay for training
    await asyncio.sleep(3)
    
    # Random power increase (1 to 10)
    power_gain = random.randint(1, 10)
    old_power = player_char['power_level']
    new_power = old_power + power_gain
    
    # Cap at 200
    if new_power > 200:
        new_power = 200
        power_gain = 200 - old_power
    
    player_char['power_level'] = new_power
    
    # Random chance to learn a new skill (20% chance)
    learned_new_skill = False
    new_skill = None
    
    if random.randint(1, 100) <= 20 and len(player_char['skills']) < 10:
        # Get skills the vampire doesn't have yet
        available_skills = [skill for skill in SKILLS if skill not in player_char['skills']]
        if available_skills:
            new_skill = random.choice(available_skills)
            player_char['skills'].append(new_skill)
            learned_new_skill = True
    
    # If hybrid, update both users
    if player_char.get('is_hybrid', False):
        shared_user_id = player_char.get('shared_user_id')
        if shared_user_id and shared_user_id in characters:
            characters[shared_user_id]['power_level'] = new_power
            characters[shared_user_id]['skills'] = player_char['skills']
    
    # Save updated vampire
    characters[user_id] = player_char
    save_characters(characters)
    
    # Results embed
    result_embed = discord.Embed(
        title="TRAINING COMPLETE",
        description=f"{player_char['name']} has grown stronger!",
        color=discord.Color.gold()
    )
    
    result_embed.add_field(
        name="Power Increase",
        value=f"{old_power} → {new_power} (+{power_gain})",
        inline=False
    )
    
    if learned_new_skill:
        result_embed.add_field(
            name="New Ability Learned!",
            value=f"{new_skill}",
            inline=False
        )
    
    result_embed.add_field(
        name="Total Abilities",
        value=f"{len(player_char['skills'])} abilities",
        inline=False
    )
    
    await ctx.send(embed=result_embed)

# Transfer command - Blood transfer ritual between two vampires
@bot.command(name='transfer')
async def blood_transfer(ctx, member: discord.Member = None):
    """Initiate a blood transfer ritual with another vampire. Both vampires die and create a powerful hybrid! Usage: ?transfer @user"""
    
    if member is None:
        await ctx.send("Usage: `?transfer @user`\nExample: `?transfer @JohnDoe`\n\nBoth vampires will be sacrificed to create a powerful hybrid vampire that both users can control!")
        return
    
    # Can't transfer with yourself
    if member.id == ctx.author.id:
        await ctx.send("You cannot perform a blood transfer ritual with yourself!")
        return
    
    initiator_id = str(ctx.author.id)
    target_id = str(member.id)
    
    # Check if both users have vampires
    if initiator_id not in characters:
        await ctx.send("You don't have a vampire yet! Use `?make` to create one.")
        return
    
    if target_id not in characters:
        await ctx.send(f"{member.name} doesn't have a vampire yet!")
        return
    
    initiator_char = characters[initiator_id]
    target_char = characters[target_id]
    
    # Create transfer request
    request_key = f"{initiator_id}_{target_id}"
    
    # Check if there's already a pending request FROM the target TO the initiator
    reverse_key = f"{target_id}_{initiator_id}"
    
    if reverse_key in transfer_requests:
        # Both agreed! Perform the transfer
        await ctx.send(f"{ctx.author.mention} and {member.mention} - Both vampires have agreed to the blood transfer ritual!")
        
        # Ritual embed
        ritual_embed = discord.Embed(
            title="BLOOD TRANSFER RITUAL",
            description=f"{initiator_char['name']} and {target_char['name']} begin the ancient blood ritual...\n\nTheir essences merge in darkness...",
            color=discord.Color.dark_purple()
        )
        
        ritual_embed.add_field(
            name=f"{initiator_char['name']}",
            value=f"Power: {initiator_char['power_level']} | Skills: {len(initiator_char['skills'])}",
            inline=True
        )
        
        ritual_embed.add_field(
            name=f"{target_char['name']}",
            value=f"Power: {target_char['power_level']} | Skills: {len(target_char['skills'])}",
            inline=True
        )
        
        await ctx.send(embed=ritual_embed)
        
        # 5 second ritual delay
        await asyncio.sleep(5)
        
        # Create new hybrid vampire
        # Generate new name
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        hybrid_name = f"{first_name} {last_name}"
        
        # Generate new ID (SINGLE ID for both users)
        hybrid_id = generate_unique_id()
        
        # Combine powers (average + bonus)
        combined_power = initiator_char['power_level'] + target_char['power_level']
        bonus = random.randint(10, 30)
        hybrid_power = combined_power + bonus
        
        # Combine skills (all unique skills from both)
        all_skills = list(set(initiator_char['skills'] + target_char['skills']))
        
        # Add 1-3 random new skills
        available_skills = [skill for skill in SKILLS if skill not in all_skills]
        if available_skills:
            num_new_skills = min(random.randint(1, 3), len(available_skills))
            new_skills = random.sample(available_skills, num_new_skills)
            all_skills.extend(new_skills)
        
        # Combine wins
        total_wins = initiator_char.get('wins', 0) + target_char.get('wins', 0)
        
        # Create SINGLE hybrid vampire data
        hybrid_data = {
            "character_id": hybrid_id,
            "name": hybrid_name,
            "username": f"{ctx.author.name} & {member.name}",
            "user_id": initiator_id,
            "shared_user_id": target_id,
            "power_level": hybrid_power,
            "skills": all_skills,
            "wins": total_wins,
            "losses": 0,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "is_hybrid": True
        }
        
        # Add old vampires to graveyard
        old_vamp1 = initiator_char.copy()
        old_vamp1['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        old_vamp1['killed_by'] = "Blood Transfer Ritual"
        
        old_vamp2 = target_char.copy()
        old_vamp2['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        old_vamp2['killed_by'] = "Blood Transfer Ritual"
        
        graveyard.append(old_vamp1)
        graveyard.append(old_vamp2)
        save_graveyard(graveyard)
        
        # Delete old vampires
        del characters[initiator_id]
        del characters[target_id]
        
        # Save THE SAME hybrid vampire for both users (exact copy with swapped IDs)
        characters[initiator_id] = hybrid_data
        characters[target_id] = hybrid_data.copy()
        characters[target_id]['user_id'] = target_id
        characters[target_id]['shared_user_id'] = initiator_id
        
        save_characters(characters)
        
        # Clear the request
        del transfer_requests[reverse_key]
        
        # Result embed
        result_embed = discord.Embed(
            title="HYBRID VAMPIRE BORN",
            description=f"The ritual is complete! {hybrid_name} emerges from the darkness!\n\nBoth {ctx.author.mention} and {member.mention} can now use this vampire with ID: `{hybrid_id}`",
            color=discord.Color.gold()
        )
        
        result_embed.add_field(name="Hybrid Name", value=hybrid_name, inline=False)
        result_embed.add_field(name="Blood Power", value=f"{hybrid_power} (+{bonus} ritual bonus)", inline=False)
        result_embed.add_field(name="Total Abilities", value=f"{len(all_skills)} abilities", inline=False)
        result_embed.add_field(name="Battle Record", value=f"{total_wins}W - 0L", inline=False)
        result_embed.add_field(
            name="Shared Ownership",
            value=f"{ctx.author.name} and {member.name} both control this vampire",
            inline=False
        )
        
        await ctx.send(embed=result_embed)
        
    else:
        # Create new request
        transfer_requests[request_key] = {
            "initiator": ctx.author.id,
            "target": member.id,
            "timestamp": datetime.now()
        }
        
        # Request embed
        request_embed = discord.Embed(
            title="BLOOD TRANSFER REQUEST",
            description=f"{ctx.author.mention} has initiated a blood transfer ritual with {member.mention}!",
            color=discord.Color.orange()
        )
        
        request_embed.add_field(
            name="Warning",
            value="Both vampires will be sacrificed to create a powerful hybrid vampire that both users can control!",
            inline=False
        )
        
        request_embed.add_field(
            name=f"{ctx.author.name}'s Vampire",
            value=f"{initiator_char['name']} - Power: {initiator_char['power_level']}",
            inline=True
        )
        
        request_embed.add_field(
            name=f"{member.name}'s Vampire",
            value=f"{target_char['name']} - Power: {target_char['power_level']}",
            inline=True
        )
        
        request_embed.add_field(
            name="To Accept",
            value=f"{member.mention} use `?transfer {ctx.author.mention}` to accept and complete the ritual!",
            inline=False
        )
        
        await ctx.send(embed=request_embed)

# Fight command - Fight random vampire opponents
@bot.command(name='fight')
async def fight_character(ctx, character_id: str = None):
    """Fight a random vampire - you can win or lose! Usage: ?fight <character_id>"""
    
    # Check if character ID was provided
    if character_id is None:
        await ctx.send("Usage: `?fight <character_id>`\nExample: `?fight 123456`\n\nUse `?show` to see your vampire ID.")
        return
    
    user_id = str(ctx.author.id)
    
    # Check if user has a vampire
    if user_id not in characters:
        await ctx.send("You don't have a vampire yet! Use `?make` to create one.")
        return
    
    player_char = characters[user_id]
    
    # Verify the character ID matches
    if player_char['character_id'] != character_id:
        await ctx.send(f"Invalid vampire ID! Your vampire ID is `{player_char['character_id']}`")
        return
    
    # Generate random AI vampire opponent
    ai_first_name = random.choice(FIRST_NAMES)
    ai_last_name = random.choice(LAST_NAMES)
    ai_name = f"{ai_first_name} {ai_last_name}"
    ai_power_level = random.randint(10, 100)
    ai_num_skills = random.randint(3, 5)
    ai_skills = random.sample(SKILLS, ai_num_skills)
    
    # Battle embed - show both vampires
    battle_embed = discord.Embed(
        title="BLOOD BATTLE",
        description="Two vampires clash in the darkness!",
        color=discord.Color.purple()
    )
    
    battle_embed.add_field(
        name=f"{player_char['name']} (YOU)",
        value=f"Blood Power: {player_char['power_level']}\nAbilities: {', '.join(player_char['skills'][:2])}...",
        inline=True
    )
    
    battle_embed.add_field(
        name=f"{ai_name} (ENEMY VAMPIRE)",
        value=f"Blood Power: {ai_power_level}\nAbilities: {', '.join(ai_skills[:2])}...",
        inline=True
    )
    
    await ctx.send(embed=battle_embed)
    
    # 4 second delay before showing results
    await asyncio.sleep(4)
    
    # Calculate win chance based on power levels
    player_power = player_char['power_level']
    total_power = player_power + ai_power_level
    player_win_chance = (player_power / total_power) * 100
    
    # Add some randomness (30% random factor)
    random_factor = random.randint(-15, 15)
    final_win_chance = max(10, min(90, player_win_chance + random_factor))
    
    # Determine winner
    roll = random.randint(1, 100)
    player_wins = roll <= final_win_chance
    
    # Result embed
    if player_wins:
        # Update wins
        if 'wins' not in player_char:
            player_char['wins'] = 0
        player_char['wins'] += 1
        
        # If hybrid, update both users
        if player_char.get('is_hybrid', False):
            shared_user_id = player_char.get('shared_user_id')
            if shared_user_id and shared_user_id in characters:
                characters[shared_user_id]['wins'] = player_char['wins']
        
        characters[user_id] = player_char
        save_characters(characters)
        
        result_embed = discord.Embed(
            title="VICTORY",
            description=f"{player_char['name']} has drained {ai_name} of their blood!",
            color=discord.Color.green()
        )
        
        result_embed.add_field(name="Your Blood Power", value=f"{player_power}", inline=True)
        result_embed.add_field(name="Enemy Blood Power", value=f"{ai_power_level}", inline=True)
        result_embed.add_field(name="Win Chance", value=f"{final_win_chance:.1f}%", inline=True)
        result_embed.add_field(
            name="Battle Summary",
            value=f"{player_char['name']} emerged victorious from the blood battle and survives to hunt another night!",
            inline=False
        )
        
        # Show updated record
        wins = player_char.get('wins', 0)
        losses = player_char.get('losses', 0)
        result_embed.add_field(name="New Record", value=f"{wins}W - {losses}L", inline=False)
        
        await ctx.send(embed=result_embed)
    else:
        result_embed = discord.Embed(
            title="DEFEAT",
            description=f"{player_char['name']} has been destroyed by {ai_name}!",
            color=discord.Color.red()
        )
        
        result_embed.add_field(name="Your Blood Power", value=f"{player_power}", inline=True)
        result_embed.add_field(name="Enemy Blood Power", value=f"{ai_power_level}", inline=True)
        result_embed.add_field(name="Win Chance", value=f"{final_win_chance:.1f}%", inline=True)
        
        # Show final record before deletion
        wins = player_char.get('wins', 0)
        losses = player_char.get('losses', 0)
        result_embed.add_field(name="Final Record", value=f"{wins}W - {losses}L", inline=False)
        
        result_embed.add_field(
            name="Battle Summary",
            value=f"{player_char['name']} has been staked through the heart and turned to ash...\n\nYour vampire has been destroyed. Use `?make` to create a new one.",
            inline=False
        )
        
        await ctx.send(embed=result_embed)
        
        # Add to graveyard before deleting
        dead_vampire = player_char.copy()
        dead_vampire['death_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dead_vampire['killed_by'] = ai_name
        graveyard.append(dead_vampire)
        save_graveyard(graveyard)
        
        # If hybrid, delete from both users
        if player_char.get('is_hybrid', False):
            shared_user_id = player_char.get('shared_user_id')
            if shared_user_id and shared_user_id in characters:
                del characters[shared_user_id]
        
        # Delete the vampire
        del characters[user_id]
        save_characters(characters)

# Stats command - Shows world statistics
@bot.command(name='stats')
async def world_stats(ctx):
    """View world statistics of all vampires alive and dead"""
    
    # Load current data
    alive_vampires = load_characters()
    dead_vampires = load_graveyard()
    
    # Calculate stats
    total_alive = len(alive_vampires)
    total_dead = len(dead_vampires)
    total_vampires = total_alive + total_dead
    
    # Calculate total wins and losses
    total_wins = sum(char.get('wins', 0) for char in alive_vampires.values())
    total_losses = sum(char.get('wins', 0) for char in dead_vampires)
    
    # Main stats embed
    stats_embed = discord.Embed(
        title="VAMPIRE WORLD STATISTICS",
        description="Global vampire data across all realms",
        color=discord.Color.dark_purple()
    )
    
    stats_embed.add_field(name="Total Vampires Created", value=f"{total_vampires}", inline=True)
    stats_embed.add_field(name="Vampires Alive", value=f"{total_alive}", inline=True)
    stats_embed.add_field(name="Vampires Destroyed", value=f"{total_dead}", inline=True)
    stats_embed.add_field(name="Total Victories", value=f"{total_wins}", inline=True)
    stats_embed.add_field(name="Total Defeats", value=f"{total_losses}", inline=True)
    stats_embed.add_field(name="Total Battles", value=f"{total_wins + total_losses}", inline=True)
    
    await ctx.send(embed=stats_embed)
    
    # Show top 5 alive vampires by wins (remove duplicates for hybrids)
    if alive_vampires:
        # Use character_id to deduplicate hybrids
        seen_ids = set()
        unique_vampires = []
        
        for vamp in alive_vampires.values():
            char_id = vamp.get('character_id')
            if char_id not in seen_ids:
                seen_ids.add(char_id)
                unique_vampires.append(vamp)
        
        alive_list = sorted(unique_vampires, key=lambda x: x.get('wins', 0), reverse=True)[:5]
        
        alive_embed = discord.Embed(
            title="TOP LIVING VAMPIRES",
            description="The strongest vampires still walking the earth",
            color=discord.Color.green()
        )
        
        for idx, vamp in enumerate(alive_list, 1):
            wins = vamp.get('wins', 0)
            losses = vamp.get('losses', 0)
            hybrid_tag = " [HYBRID]" if vamp.get('is_hybrid', False) else ""
            alive_embed.add_field(
                name=f"{idx}. {vamp['name']}{hybrid_tag}",
                value=f"ID: `{vamp['character_id']}` | Power: {vamp['power_level']} | Record: {wins}W-{losses}L",
                inline=False
            )
        
        await ctx.send(embed=alive_embed)
    
    # Show last 5 fallen vampires
    if dead_vampires:
        recent_dead = dead_vampires[-5:]
        recent_dead.reverse()
        
        dead_embed = discord.Embed(
            title="RECENTLY FALLEN VAMPIRES",
            description="Those who met their end in battle",
            color=discord.Color.dark_red()
        )
        
        for vamp in recent_dead:
            wins = vamp.get('wins', 0)
            losses = vamp.get('losses', 0)
            dead_embed.add_field(
                name=f"{vamp['name']}",
                value=f"ID: `{vamp['character_id']}` | Power: {vamp['power_level']} | Record: {wins}W-{losses}L\nKilled by: {vamp.get('killed_by', 'Unknown')}",
                inline=False
            )
        
        await ctx.send(embed=dead_embed)

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
