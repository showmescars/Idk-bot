import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import re
import io
import random
import string

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# ──────────────────────────────────────────────
#  ENHANCED OBFUSCATOR (FIXED)
# ──────────────────────────────────────────────

class LuaObfuscator:
    def __init__(self):
        self.lua_keywords = {
            'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
            'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
            'return', 'then', 'true', 'until', 'while'
        }
        
        self.roblox_globals = {
            'game', 'workspace', 'script', 'Instance', 'wait', 'print', 
            'pairs', 'ipairs', 'type', 'tostring', 'tonumber', 'require', 
            'pcall', 'xpcall', 'error', 'warn', 'math', 'table', 'string', 
            'os', 'task', 'self', 'rawget', 'rawset', 'setmetatable', 
            'getmetatable', 'next', 'select', 'unpack', 'loadstring', 
            'coroutine', 'io', 'bit32', '_G', '_VERSION', 'assert', 
            'collectgarbage', 'dofile', 'getfenv', 'setfenv', 'newproxy', 
            'tick', 'typeof', 'spawn', 'delay', 'Workspace', 'Players', 
            'ReplicatedStorage', 'ServerStorage', 'StarterGui', 'StarterPack', 
            'StarterPlayer', 'Teams', 'SoundService', 'Lighting', 
            'MaterialService', 'BadgeService', 'InsertService', 
            'MarketplaceService', 'TeleportService', 'UserInputService', 
            'ContextActionService', 'RunService', 'HttpService', 
            'DataStoreService', 'AnalyticsService', 'LocalizationService', 
            'TextService', 'TweenService', 'Vector2', 'Vector3', 'CFrame',
            'Color3', 'UDim2', 'UDim', 'Enum', 'Ray', 'Region3', 'NumberRange',
            'NumberSequence', 'ColorSequence', 'DateTime', 'Random', 'utf8'
        }
        
        self.protected_names = self.lua_keywords | self.roblox_globals

    def generate_random_name(self, length=10):
        """Generate a random variable name"""
        chars = string.ascii_letters
        return '_' + ''.join(random.choices(chars, k=length))

    def strip_comments(self, code):
        """Remove all comments from code"""
        # Multi-line comments
        code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
        # Single-line comments
        code = re.sub(r'--[^\n]*', '', code)
        return code

    def extract_strings(self, code):
        """Extract and protect string literals"""
        strings = {}
        counter = [0]
        
        def replace_string(match):
            placeholder = f"__STRING_PLACEHOLDER_{counter[0]}__"
            strings[placeholder] = match.group(0)
            counter[0] += 1
            return placeholder
        
        # Match double quoted strings
        code = re.sub(r'"(?:[^"\\]|\\.)*"', replace_string, code)
        # Match single quoted strings
        code = re.sub(r"'(?:[^'\\]|\\.)*'", replace_string, code)
        # Match multi-line strings [[...]]
        code = re.sub(r'\[\[.*?\]\]', replace_string, code, flags=re.DOTALL)
        
        return code, strings

    def restore_strings(self, code, strings):
        """Restore string literals"""
        for placeholder, original in strings.items():
            code = code.replace(placeholder, original)
        return code

    def find_local_variables(self, code):
        """Find all local variable declarations"""
        variables = set()
        
        # Find: local var1, var2, var3 = ...
        matches = re.finditer(r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)', code)
        for match in matches:
            var_list = match.group(1)
            vars_found = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', var_list)
            variables.update(vars_found)
        
        # Find: function name(param1, param2)
        func_matches = re.finditer(r'\bfunction\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(([^)]*)\)', code)
        for match in func_matches:
            params = match.group(1)
            if params.strip():
                param_list = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', params)
                variables.update(param_list)
        
        # Find: function(param1, param2) -- anonymous functions
        anon_matches = re.finditer(r'\bfunction\s*\(([^)]*)\)', code)
        for match in anon_matches:
            params = match.group(1)
            if params.strip():
                param_list = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', params)
                variables.update(param_list)
        
        # Find: for var in/= ...
        for_matches = re.finditer(r'\bfor\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)\s+(?:in|=)', code)
        for match in for_matches:
            var_list = match.group(1)
            vars_found = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', var_list)
            variables.update(vars_found)
        
        return variables

    def rename_variables(self, code):
        """Rename local variables"""
        # Find all local variables
        local_vars = self.find_local_variables(code)
        
        # Create mapping for variables (exclude protected names)
        mapping = {}
        for var in local_vars:
            if var not in self.protected_names and var not in mapping:
                mapping[var] = self.generate_random_name()
        
        # Replace variables (longest first to avoid partial matches)
        for original, obfuscated in sorted(mapping.items(), key=lambda x: -len(x[0])):
            # Use word boundaries to match whole words only
            pattern = r'\b' + re.escape(original) + r'\b'
            code = re.sub(pattern, obfuscated, code)
        
        return code

    def encode_hex(self, code):
        """Hex encode and wrap in loadstring"""
        hex_encoded = code.encode('utf-8').hex()
        
        var_hex = self.generate_random_name(8)
        var_decoded = self.generate_random_name(8)
        var_index = self.generate_random_name(6)
        
        result = (
            f'local {var_hex}="{hex_encoded}"\n'
            f'local {var_decoded}=""\n'
            f'for {var_index}=1,#{var_hex},2 do\n'
            f'    {var_decoded}={var_decoded}..string.char(tonumber({var_hex}:sub({var_index},{var_index}+1),16))\n'
            f'end\n'
            f'loadstring({var_decoded})()\n'
        )
        return result

    def obfuscate(self, code, level='medium', encoding='hex'):
        """
        Main obfuscation method
        
        Levels:
        - basic: Only comments removal and encoding
        - medium: + variable renaming (default)
        - advanced: + variable renaming and minification
        """
        try:
            # Step 1: Always strip comments
            code = self.strip_comments(code)
            
            if level in ['medium', 'advanced']:
                # Step 2: Extract strings to protect them
                code, strings = self.extract_strings(code)
                
                # Step 3: Rename variables
                code = self.rename_variables(code)
                
                # Step 4: Restore strings
                code = self.restore_strings(code, strings)
            
            if level == 'advanced':
                # Step 5: Minify - remove extra whitespace
                lines = [line.strip() for line in code.split('\n') if line.strip()]
                code = '\n'.join(lines)
            
            # Step 6: Encode
            if encoding == 'hex':
                code = self.encode_hex(code)
            elif encoding == 'none':
                # No encoding, return as-is
                pass
            
            return code
            
        except Exception as e:
            raise Exception(f"Obfuscation error: {str(e)}")

# ──────────────────────────────────────────────
#  GLOBAL CHECK - block DMs
# ──────────────────────────────────────────────

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("❌ Commands can only be used in servers, not DMs.")
        return False
    return True

# ──────────────────────────────────────────────
#  EVENTS
# ──────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is online and ready.')
    print(f'📊 Connected to {len(bot.guilds)} server(s)')
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="?obfhelp for commands"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Missing Argument",
            description=(
                "**Usage:**\n"
                "📎 Attach a `.lua` or `.txt` file and run `?obf`\n"
                "💬 Inline: `?obf <your lua code>`\n\n"
                "Use `?obfhelp` for more information."
            ),
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CheckFailure):
        pass
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        embed = discord.Embed(
            title="⚠️ Error Occurred",
            description=f"```{str(error)}```",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

# ──────────────────────────────────────────────
#  COMMANDS
# ──────────────────────────────────────────────

@bot.command(name='obf')
async def obf(ctx, *, args: str = None):
    """Obfuscate Roblox Lua code"""
    
    # Parse arguments
    level = 'medium'
    encoding = 'hex'
    code = None
    
    if args:
        parts = args.split(None, 2)
        
        # Check if first part is a level
        if len(parts) > 0 and parts[0] in ['basic', 'medium', 'advanced']:
            level = parts[0]
            parts = parts[1:]
        
        # Check if first part is an encoding
        if len(parts) > 0 and parts[0] in ['hex', 'none']:
            encoding = parts[0]
            parts = parts[1:]
        
        # Rest is code
        if parts:
            code = ' '.join(parts)
    
    # Show processing message
    processing_msg = await ctx.send("🔄 Processing your code...")
    
    # -- FILE MODE --
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        filename = attachment.filename.lower()

        if not filename.endswith(('.lua', '.txt')):
            await processing_msg.edit(content="❌ Only `.lua` and `.txt` files are supported.")
            return

        if attachment.size > 1_000_000:
            await processing_msg.edit(content="❌ File too large! Maximum size is 1MB.")
            return

        try:
            file_bytes = await attachment.read()
            source_code = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            await processing_msg.edit(content="❌ Could not decode file. Ensure it's UTF-8 encoded.")
            return
        except Exception as e:
            await processing_msg.edit(content=f"❌ Could not read file: {e}")
            return

        input_filename = attachment.filename.rsplit('.', 1)[0]

    # -- INLINE TEXT MODE --
    elif code is not None:
        source_code = re.sub(r'^```[a-zA-Z]*\n?', '', code)
        source_code = re.sub(r'```$', '', source_code).strip()
        input_filename = 'obfuscated'

    else:
        embed = discord.Embed(
            title="📖 Obfuscator Usage",
            description=(
                "**Methods:**\n"
                "💬 Inline: `?obf [level] [encoding] <code>`\n"
                "📎 File: Attach a `.lua` or `.txt` file and run `?obf [level] [encoding]`\n\n"
                "**Levels:** `basic`, `medium` (default), `advanced`\n"
                "**Encoding:** `hex` (default), `none`\n\n"
                "**Examples:**\n"
                "`?obf print('Hello')`\n"
                "`?obf advanced hex print('Hello')`\n"
                "`?obf medium none` (with file)"
            ),
            color=discord.Color.blue()
        )
        await processing_msg.delete()
        await ctx.send(embed=embed)
        return

    if len(source_code) > 100_000:
        await processing_msg.edit(content="❌ Code too large! Maximum size is 100,000 characters.")
        return

    # -- OBFUSCATE --
    try:
        obfuscator = LuaObfuscator()
        result = obfuscator.obfuscate(source_code, level=level, encoding=encoding)
        
        original_size = len(source_code)
        obfuscated_size = len(result)
        size_increase = ((obfuscated_size - original_size) / original_size) * 100
        
    except Exception as e:
        await processing_msg.edit(content=f"❌ Obfuscation failed: {e}")
        return

    # -- SEND AS FILE --
    out_filename = f"{input_filename}_obfuscated.lua"
    file_obj = discord.File(
        fp=io.BytesIO(result.encode('utf-8')),
        filename=out_filename
    )
    
    embed = discord.Embed(
        title="✅ Obfuscation Complete",
        description=f"Your code has been obfuscated successfully!",
        color=discord.Color.green()
    )
    embed.add_field(name="📊 Level", value=f"`{level}`", inline=True)
    embed.add_field(name="🔐 Encoding", value=f"`{encoding}`", inline=True)
    embed.add_field(name="📏 Size Change", value=f"`{size_increase:+.1f}%`", inline=True)
    embed.add_field(
        name="📝 Stats",
        value=f"Original: `{original_size:,}` chars\nObfuscated: `{obfuscated_size:,}` chars",
        inline=False
    )
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    await processing_msg.delete()
    await ctx.send(embed=embed, file=file_obj)


@bot.command(name='obfhelp')
async def obfhelp(ctx):
    """Show detailed help information"""
    embed = discord.Embed(
        title="🔧 Roblox Lua Obfuscator Bot",
        description="A powerful tool to obfuscate your Roblox Lua scripts.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📝 Basic Usage",
        value=(
            "**Inline Code:**\n"
            "`?obf <your lua code>`\n\n"
            "**File Upload:**\n"
            "Attach a `.lua` or `.txt` file and run `?obf`"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Advanced Usage",
        value=(
            "`?obf [level] [encoding] <code>`\n\n"
            "**Levels:**\n"
            "• `basic` - Only removes comments\n"
            "• `medium` - + Variable renaming (default)\n"
            "• `advanced` - + Minification\n\n"
            "**Encoding:**\n"
            "• `hex` - Hex encoding (default)\n"
            "• `none` - No encoding"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎯 Features",
        value=(
            "✓ Comment removal\n"
            "✓ Variable renaming\n"
            "✓ String protection\n"
            "✓ Hex encoding\n"
            "✓ Code minification\n"
            "✓ Preserves functionality"
        ),
        inline=True
    )
    
    embed.add_field(
        name="📌 Examples",
        value=(
            "`?obf print('test')`\n"
            "`?obf advanced hex print('test')`\n"
            "`?obf basic none` (with file)\n"
            "`?obf medium hex` (with file)"
        ),
        inline=True
    )
    
    embed.add_field(
        name="⚠️ Limits",
        value=(
            "Max file size: 1MB\n"
            "Max code length: 100K chars"
        ),
        inline=False
    )
    
    embed.set_footer(text="Made for Roblox Lua scripting")
    
    await ctx.send(embed=embed)


@bot.command(name='start')
async def start(ctx):
    """Welcome message"""
    embed = discord.Embed(
        title="👋 Welcome to Roblox Lua Obfuscator!",
        description=(
            "I'm online and ready to obfuscate your Lua code.\n\n"
            "Use `?obfhelp` to see all available commands and features."
        ),
        color=discord.Color.green()
    )
    embed.add_field(
        name="Quick Start",
        value="`?obf <your code>` or attach a file with `?obf`",
        inline=False
    )
    await ctx.send(embed=embed)


@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: `{latency}ms`",
        color=discord.Color.green() if latency < 100 else discord.Color.orange()
    )
    await ctx.send(embed=embed)


@bot.command(name='stats')
@commands.has_permissions(administrator=True)
async def stats(ctx):
    """Show bot statistics (Admin only)"""
    embed = discord.Embed(
        title="📊 Bot Statistics",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(bot.users), inline=True)
    embed.add_field(name="Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)
    
    await ctx.send(embed=embed)


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("❌ ERROR: DISCORD_TOKEN not found in .env!")
        print("Please create a .env file with: DISCORD_TOKEN=your_token_here")
    else:
        print("✅ Token found! Starting bot...")
        try:
            bot.run(TOKEN)
        except discord.LoginFailure:
            print("❌ Invalid token! Please check your DISCORD_TOKEN in .env")
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
