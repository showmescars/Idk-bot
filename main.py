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
#  OBFUSCATOR
# ──────────────────────────────────────────────

def obfuscate_roblox(code: str) -> str:
    """
    Enhanced obfuscator with chunking support for large files
    and watermark injection.
    """
    
    # Step 1: Strip comments
    code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
    code = re.sub(r'--[^\n]*', '', code)

    # Step 2: Remove blank lines and excessive whitespace
    lines = [l.strip() for l in code.split('\n') if l.strip()]
    code = ' '.join(lines)
    
    # Reduce multiple spaces to single space
    code = re.sub(r'\s+', ' ', code)

    # Step 3: Rename local variables
    lua_keywords = {
        'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
        'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
        'return', 'then', 'true', 'until', 'while', 'game', 'workspace',
        'script', 'Instance', 'wait', 'print', 'pairs', 'ipairs', 'type',
        'tostring', 'tonumber', 'require', 'pcall', 'xpcall', 'error',
        'warn', 'math', 'table', 'string', 'os', 'task', 'self',
        'rawget', 'rawset', 'setmetatable', 'getmetatable', 'next',
        'select', 'unpack', 'loadstring', 'coroutine', 'io', 'bit32',
        '_G', '_VERSION', 'assert', 'collectgarbage', 'dofile', 'getfenv',
        'setfenv', 'newproxy', 'spawn', 'delay'
    }
    
    local_vars = re.findall(r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*)\b', code)
    mapping = {}
    
    for var in local_vars:
        if var not in lua_keywords and var not in mapping:
            mapping[var] = '_' + ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    # Sort by length (longest first) to avoid partial replacements
    for original, obf in sorted(mapping.items(), key=lambda x: -len(x[0])):
        code = re.sub(rf'\b{re.escape(original)}\b', obf, code)

    # Step 4: Chunk large code for better performance
    # Split into chunks if code is very large (> 50KB)
    max_chunk_size = 50000
    
    if len(code) > max_chunk_size:
        # Use chunked approach
        result = create_chunked_obfuscation(code, max_chunk_size)
    else:
        # Use standard approach
        result = create_standard_obfuscation(code)
    
    return result


def create_standard_obfuscation(code: str) -> str:
    """Standard hex encoding with loadstring wrapper"""
    hex_encoded = code.encode('utf-8').hex()
    
    watermark = "-- Peter Griffin Obfuscator"
    
    result = f'''{watermark}
local __H="{hex_encoded}"
local __D=""
for __i=1,#__H,2 do
    __D=__D..string.char(tonumber(__H:sub(__i,__i+1),16))
end
loadstring(__D)()
'''
    return result


def create_chunked_obfuscation(code: str, chunk_size: int) -> str:
    """Chunked hex encoding for large files"""
    
    watermark = "-- Peter Griffin Obfuscator"
    
    # Split code into chunks
    chunks = []
    for i in range(0, len(code), chunk_size):
        chunk = code[i:i + chunk_size]
        hex_chunk = chunk.encode('utf-8').hex()
        chunks.append(hex_chunk)
    
    # Build the loader
    result_parts = [watermark]
    result_parts.append('local __C={')
    
    for idx, chunk in enumerate(chunks):
        if idx < len(chunks) - 1:
            result_parts.append(f'"{chunk}",')
        else:
            result_parts.append(f'"{chunk}"')
    
    result_parts.append('}')
    result_parts.append('local __F=""')
    result_parts.append('for __k,__v in ipairs(__C) do')
    result_parts.append('    for __i=1,#__v,2 do')
    result_parts.append('        __F=__F..string.char(tonumber(__v:sub(__i,__i+1),16))')
    result_parts.append('    end')
    result_parts.append('end')
    result_parts.append('loadstring(__F)()')
    
    return '\n'.join(result_parts)


# ──────────────────────────────────────────────
#  GLOBAL CHECK - block DMs
# ──────────────────────────────────────────────

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send("Commands can only be used in servers, not DMs.")
        return False
    return True

# ──────────────────────────────────────────────
#  EVENTS
# ──────────────────────────────────────────────

@bot.event
async def on_ready():
    print(f'{bot.user} is online and ready.')
    print(f'Logged in as: {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "❌ Missing argument!\n"
            "📎 Attach a .lua or .txt file and run `?obf`\n"
            "💬 Or inline: `?obf <your lua code>`"
        )
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        await ctx.send(f"⚠️ An error occurred: {error}")
        print(f"Error: {error}")

# ──────────────────────────────────────────────
#  COMMANDS
# ──────────────────────────────────────────────

@bot.command(name='obf')
async def obf(ctx, *, code: str = None):
    """
    Main obfuscation command - handles both file and inline text
    """
    
    # -- FILE MODE --
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        filename = attachment.filename.lower()

        if not filename.endswith(('.lua', '.txt')):
            await ctx.send(
                "❌ Only `.lua` and `.txt` files are supported.\n"
                "Please attach a valid file."
            )
            return

        # Check file size (Discord limit is 8MB for free, 50MB for boosted)
        if attachment.size > 8_000_000:
            await ctx.send("❌ File is too large! Maximum size is 8MB.")
            return

        try:
            await ctx.send("⏳ Processing your file... This may take a moment for large files.")
            file_bytes = await attachment.read()
            source_code = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            await ctx.send("❌ Could not decode file. Please ensure it's a valid text file with UTF-8 encoding.")
            return
        except Exception as e:
            await ctx.send(f"❌ Could not read file: {e}")
            return

        input_filename = attachment.filename.rsplit('.', 1)[0]

    # -- INLINE TEXT MODE --
    elif code is not None:
        # Remove code block markers if present
        source_code = re.sub(r'^```[a-zA-Z]*\n?', '', code)
        source_code = re.sub(r'```$', '', source_code).strip()
        input_filename = 'obfuscated'

    else:
        await ctx.send(
            "📖 **Usage:**\n"
            "💬 Inline: `?obf <your lua code>`\n"
            "📎 File: attach a `.lua` or `.txt` file and run `?obf`\n\n"
            "Type `?obfhelp` for more information."
        )
        return

    # -- OBFUSCATE --
    try:
        result = obfuscate_roblox(source_code)
    except Exception as e:
        await ctx.send(f"❌ Obfuscation failed: {e}")
        print(f"Obfuscation error: {e}")
        return

    # -- CHECK OUTPUT SIZE --
    result_bytes = result.encode('utf-8')
    if len(result_bytes) > 8_000_000:
        await ctx.send(
            "❌ Obfuscated output is too large to send (>8MB).\n"
            "Try splitting your code into smaller files."
        )
        return

    # -- SEND AS FILE --
    out_filename = f"{input_filename}_obfuscated.lua"
    file_obj = discord.File(
        fp=io.BytesIO(result_bytes),
        filename=out_filename
    )
    
    await ctx.send(
        "✅ **Peter Griffin Obfuscation Complete!**\n"
        f"📁 Original size: {len(source_code):,} characters\n"
        f"📁 Obfuscated size: {len(result):,} characters\n"
        "🎁 Here's your obfuscated file:",
        file=file_obj
    )


@bot.command(name='obfhelp')
async def obfhelp(ctx):
    """Display help information"""
    help_text = """
🎮 **Peter Griffin Obfuscator - Help**

**Commands:**
• `?obf <code>` - Obfuscate inline Lua code
• `?obf` - Obfuscate attached .lua or .txt file
• `?obfhelp` - Show this help message
• `?start` - Check if bot is running

**What it does:**
✨ Strips all comments
✨ Removes blank lines and whitespace
✨ Renames local variables to random names
✨ Hex encodes your entire script
✨ Wraps everything in a loadstring loader
✨ Handles large files with chunking
✨ Adds Peter Griffin watermark

**File Limits:**
• Max file size: 8MB
• Supported formats: .lua, .txt

**Example Usage:**
