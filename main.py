import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import re
import io
import random
import string
import base64
import hashlib

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# ──────────────────────────────────────────────
#  ENHANCED OBFUSCATOR
# ──────────────────────────────────────────────

class LuaObfuscator:
    def __init__(self):
        self.lua_keywords = {
            'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
            'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
            'return', 'then', 'true', 'until', 'while', 'game', 'workspace',
            'script', 'Instance', 'wait', 'print', 'pairs', 'ipairs', 'type',
            'tostring', 'tonumber', 'require', 'pcall', 'xpcall', 'error',
            'warn', 'math', 'table', 'string', 'os', 'task', 'self',
            'rawget', 'rawset', 'setmetatable', 'getmetatable', 'next',
            'select', 'unpack', 'loadstring', 'coroutine', 'io', 'bit32',
            '_G', '_VERSION', 'assert', 'collectgarbage', 'dofile', 'getfenv',
            'setfenv', 'newproxy', 'tick', 'typeof', 'spawn', 'delay'
        }
        
        self.roblox_globals = {
            'Workspace', 'Players', 'ReplicatedStorage', 'ServerStorage',
            'StarterGui', 'StarterPack', 'StarterPlayer', 'Teams', 'SoundService',
            'Lighting', 'MaterialService', 'BadgeService', 'InsertService',
            'MarketplaceService', 'TeleportService', 'UserInputService',
            'ContextActionService', 'RunService', 'HttpService', 'DataStoreService',
            'AnalyticsService', 'LocalizationService', 'TextService'
        }
        
        self.protected_names = self.lua_keywords | self.roblox_globals

    def generate_random_name(self, length=12, prefix='_'):
        """Generate a random variable name"""
        chars = string.ascii_letters + string.digits
        return prefix + ''.join(random.choices(chars, k=length))

    def strip_comments(self, code):
        """Remove all comments from code"""
        # Multi-line comments
        code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
        # Single-line comments
        code = re.sub(r'--[^\n]*', '', code)
        return code

    def strip_whitespace(self, code):
        """Remove unnecessary whitespace"""
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        return '\n'.join(lines)

    def extract_strings(self, code):
        """Extract and protect string literals"""
        strings = {}
        counter = [0]
        
        def replace_string(match):
            placeholder = f"__STR_{counter[0]}__"
            strings[placeholder] = match.group(0)
            counter[0] += 1
            return placeholder
        
        # Match both single and double quoted strings
        code = re.sub(r'"(?:[^"\\]|\\.)*"', replace_string, code)
        code = re.sub(r"'(?:[^'\\]|\\.)*'", replace_string, code)
        
        return code, strings

    def restore_strings(self, code, strings):
        """Restore string literals"""
        for placeholder, original in strings.items():
            code = code.replace(placeholder, original)
        return code

    def rename_variables(self, code):
        """Rename local variables and function parameters"""
        mapping = {}
        
        # Find local variable declarations
        local_vars = re.findall(r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
        
        # Find function parameters
        func_params = re.findall(r'function\s*\(([^)]*)\)', code)
        for params in func_params:
            param_list = [p.strip() for p in params.split(',') if p.strip()]
            local_vars.extend(param_list)
        
        # Create mappings for non-protected names
        for var in set(local_vars):
            if var not in self.protected_names and var not in mapping:
                mapping[var] = self.generate_random_name()
        
        # Replace variables (longest first to avoid partial matches)
        for original, obfuscated in sorted(mapping.items(), key=lambda x: -len(x[0])):
            # Use word boundaries to avoid replacing parts of other words
            code = re.sub(rf'\b{re.escape(original)}\b', obfuscated, code)
        
        return code

    def add_junk_code(self, code):
        """Add harmless junk code to confuse deobfuscators"""
        junk_lines = [
            "local _unused = nil",
            "local _dummy = function() end",
            "local _void = {}",
        ]
        
        junk = '\n'.join(random.sample(junk_lines, k=random.randint(1, 3)))
        return junk + '\n' + code

    def obfuscate_numbers(self, code):
        """Obfuscate number literals"""
        def replace_number(match):
            num = match.group(0)
            try:
                value = int(num)
                # Simple arithmetic obfuscation
                offset = random.randint(100, 999)
                return f"({offset} - {offset - value})"
            except ValueError:
                return num
        
        # Only replace standalone numbers (not in strings)
        code = re.sub(r'\b\d+\b', replace_number, code)
        return code

    def control_flow_obfuscation(self, code):
        """Add basic control flow obfuscation"""
        # Wrap code in a do-end block with a dummy condition
        wrapped = f"do\n{code}\nend"
        return wrapped

    def encode_hex(self, code):
        """Hex encode and wrap in loadstring"""
        hex_encoded = code.encode('utf-8').hex()
        
        # Use more complex variable names for the loader
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

    def encode_base64(self, code):
        """Base64 encode alternative"""
        b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        
        encoded = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        
        var_data = self.generate_random_name(8)
        var_decoded = self.generate_random_name(8)
        
        # Custom base64 decoder in Lua
        result = f'''local {var_data}="{encoded}"
local {var_decoded}=""
local b='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
for i=1,#{var_data},4 do
    local a,b,c,d=string.byte({var_data},i,i+3)
    a=string.find(b,string.char(a))-1
    b=string.find(b,string.char(b or 61))-1
    c=string.find(b,string.char(c or 61))-1
    d=string.find(b,string.char(d or 61))-1
    {var_decoded}={var_decoded}..string.char(bit32.bor(bit32.lshift(a,2),bit32.rshift(b,4)))
    if c~=nil then {var_decoded}={var_decoded}..string.char(bit32.bor(bit32.lshift(bit32.band(b,15),4),bit32.rshift(c,2)))end
    if d~=nil then {var_decoded}={var_decoded}..string.char(bit32.bor(bit32.lshift(bit32.band(c,3),6),d))end
end
loadstring({var_decoded})()'''
        return result

    def obfuscate(self, code, level='medium', encoding='hex'):
        """
        Main obfuscation method
        
        Levels:
        - basic: Comments and whitespace removal only
        - medium: + variable renaming and hex encoding
        - advanced: + number obfuscation, junk code, control flow
        """
        original_code = code
        
        try:
            # Always strip comments and whitespace
            code = self.strip_comments(code)
            
            if level in ['medium', 'advanced']:
                # Extract strings to protect them
                code, strings = self.extract_strings(code)
                
                # Rename variables
                code = self.rename_variables(code)
                
                # Restore strings
                code = self.restore_strings(code, strings)
            
            if level == 'advanced':
                # Add junk code
                code = self.add_junk_code(code)
                
                # Obfuscate numbers
                # code = self.obfuscate_numbers(code)  # Can break some code
                
                # Control flow obfuscation
                code = self.control_flow_obfuscation(code)
            
            # Strip final whitespace
            code = self.strip_whitespace(code)
            
            # Encode
            if encoding == 'hex':
                code = self.encode_hex(code)
            elif encoding == 'base64':
                code = self.encode_base64(code)
            else:
                # No encoding, return as-is
                pass
            
            return code
            
        except Exception as e:
            raise Exception(f"Obfuscation failed at processing stage: {str(e)}")

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
    
    # Set bot status
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
        pass  # Already handled by the check
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore invalid commands
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
async def obf(ctx, level: str = 'medium', encoding: str = 'hex', *, code: str = None):
    """
    Obfuscate Roblox Lua code
    
    Usage:
        ?obf [level] [encoding] <code>
        ?obf [level] [encoding] (with file attachment)
    
    Levels: basic, medium, advanced
    Encoding: hex, base64, none
    """
    
    # Validate level
    if level not in ['basic', 'medium', 'advanced']:
        # If level looks like code, treat it as such
        if code is None and not ctx.message.attachments:
            code = level + (' ' + encoding if encoding != 'hex' else '')
            level = 'medium'
            encoding = 'hex'
        elif level not in ['basic', 'medium', 'advanced', 'hex', 'base64', 'none']:
            await ctx.send("❌ Invalid level. Use: `basic`, `medium`, or `advanced`")
            return
    
    # Validate encoding
    if encoding not in ['hex', 'base64', 'none']:
        if code is None:
            code = encoding
            encoding = 'hex'
        else:
            await ctx.send("❌ Invalid encoding. Use: `hex`, `base64`, or `none`")
            return
    
    # Show processing message
    processing_msg = await ctx.send("🔄 Processing your code...")
    
    # -- FILE MODE --
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        filename = attachment.filename.lower()

        if not filename.endswith(('.lua', '.txt')):
            await processing_msg.edit(content="❌ Only `.lua` and `.txt` files are supported.")
            return

        # Check file size (max 1MB)
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
        # Remove code block formatting if present
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
                "**Encoding:** `hex` (default), `base64`, `none`\n\n"
                "**Examples:**\n"
                "`?obf print('Hello')`\n"
                "`?obf advanced hex print('Hello')`\n"
                "`?obf medium base64` (with file)"
            ),
            color=discord.Color.blue()
        )
        await processing_msg.delete()
        await ctx.send(embed=embed)
        return

    # Check code size
    if len(source_code) > 100_000:
        await processing_msg.edit(content="❌ Code too large! Maximum size is 100,000 characters.")
        return

    # -- OBFUSCATE --
    try:
        obfuscator = LuaObfuscator()
        result = obfuscator.obfuscate(source_code, level=level, encoding=encoding)
        
        # Calculate stats
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
    
    # Create result embed
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
            "• `basic` - Comments & whitespace removal\n"
            "• `medium` - + Variable renaming (default)\n"
            "• `advanced` - + Junk code & control flow\n\n"
            "**Encoding:**\n"
            "• `hex` - Hex encoding (default)\n"
            "• `base64` - Base64 encoding\n"
            "• `none` - No encoding"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎯 Features",
        value=(
            "✓ Comment removal\n"
            "✓ Variable renaming\n"
            "✓ Whitespace optimization\n"
            "✓ String protection\n"
            "✓ Hex/Base64 encoding\n"
            "✓ Junk code insertion\n"
            "✓ Control flow obfuscation"
        ),
        inline=True
    )
    
    embed.add_field(
        name="📌 Examples",
        value=(
            "`?obf print('test')`\n"
            "`?obf advanced hex print('test')`\n"
            "`?obf basic none` (with file)\n"
            "`?obf medium base64` (with file)"
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
