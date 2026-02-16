import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import string
import re
import io

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────

def random_var(length=12):
    """l/I/O/0 mix — visually indistinguishable like Prometheus."""
    pool = ['l', 'I', 'O', '0', 'l', 'I', 'l', 'I']
    return '_' + ''.join(random.choices(pool, k=length))

def random_short_var():
    return '__' + ''.join(random.choices('abcdef0123456789', k=6))

def garbage_code() -> str:
    """Dead/unreachable code blocks to confuse deobfuscators."""
    v1 = random_short_var()
    v2 = random_short_var()
    n1 = random.randint(1, 999)
    snippets = [
        f"local {v1} = {n1}; if {v1} > 99999 then error() end\n",
        f"local {v1} = {n1}; local {v2} = {n1 + 1}; {v1} = {v1} + {v2};\n",
        f"local {v1} = (function() return {n1} end)()\n",
        f"do local {v1} = nil; if {v1} then return end end\n",
        f"local {v1} = math.floor(math.abs({n1}))\n",
    ]
    return random.choice(snippets)

# ──────────────────────────────────────────────
#  PIPELINE STEPS
# ──────────────────────────────────────────────

def step_strip_comments(code: str) -> str:
    code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
    code = re.sub(r'--[^\n]*', '', code)
    return code

def step_rename_variables(code: str) -> str:
    """Rename all local variables to l/I/O/0 style names."""
    lua_keywords = {
        'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
        'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
        'return', 'then', 'true', 'until', 'while', 'game', 'workspace',
        'script', 'Instance', 'wait', 'print', 'pairs', 'ipairs', 'type',
        'tostring', 'tonumber', 'require', 'pcall', 'xpcall', 'error',
        'warn', 'math', 'table', 'string', 'os', 'task', 'self',
        'rawget', 'rawset', 'setmetatable', 'getmetatable', 'next',
        'select', 'unpack', 'loadstring', 'coroutine', 'io', 'bit32'
    }
    local_vars = re.findall(r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*)\b', code)
    mapping = {}
    for var in local_vars:
        if var not in lua_keywords and var not in mapping:
            mapping[var] = random_var()

    # Sort by length descending to avoid partial replacements
    for original, obf in sorted(mapping.items(), key=lambda x: -len(x[0])):
        code = re.sub(rf'\b{re.escape(original)}\b', obf, code)

    return code

def step_inject_garbage(code: str, density: int = 4) -> str:
    """Inject dead code at random positions."""
    lines = code.split('\n')
    if len(lines) < 2:
        return code

    positions = random.sample(range(len(lines)), min(density, len(lines)))
    positions.sort(reverse=True)

    for pos in positions:
        lines.insert(pos, garbage_code())

    return '\n'.join(lines)

def step_wrap_closure(code: str) -> str:
    """Wrap in anonymous self-calling function for scope isolation."""
    return f"(function()\n{code}\nend)()\n"

def step_hex_loadstring(code: str) -> str:
    """
    Final layer: hex encode the entire processed script and wrap
    in a native Roblox loadstring decoder.
    This is the only encoding layer — applied LAST so the output
    stays compact and clean.
    """
    hex_encoded = code.encode('utf-8').hex()
    wrapper = (
        'local __H="' + hex_encoded + '"\n'
        'local __D=""\n'
        'for __i=1,#__H,2 do\n'
        '    __D=__D..string.char(tonumber(__H:sub(__i,__i+1),16))\n'
        'end\n'
        'loadstring(__D)()\n'
    )
    return wrapper

# ──────────────────────────────────────────────
#  FULL PIPELINE
# ──────────────────────────────────────────────

def obfuscate_roblox(code: str) -> str:
    """
    Pipeline (Prometheus-inspired):
    1. Strip comments
    2. Rename locals to l/I/O/0 names
    3. Inject garbage/dead code
    4. Wrap in anonymous closure
    5. Hex encode + loadstring (single clean final layer)
    """
    code = step_strip_comments(code)
    code = step_rename_variables(code)
    code = step_inject_garbage(code, density=5)
    code = step_wrap_closure(code)
    code = step_hex_loadstring(code)
    return code

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Missing argument!\n"
            "Attach a .lua or .txt file and run ?obf\n"
            "Or inline: ?obf <your lua code>"
        )
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        await ctx.send(f"An error occurred: {error}")

# ──────────────────────────────────────────────
#  COMMANDS
# ──────────────────────────────────────────────

@bot.command(name='obf')
async def obf(ctx, *, code: str = None):
    """
    Obfuscate Roblox Lua code.

    File mode:   attach a .lua or .txt file and run ?obf
    Inline mode: ?obf <your lua code here>
    """

    # -- FILE MODE --
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        filename = attachment.filename.lower()

        if not filename.endswith(('.lua', '.txt')):
            await ctx.send(
                "Only .lua and .txt files are supported.\n"
                "Please attach a valid file."
            )
            return

        try:
            file_bytes = await attachment.read()
            source_code = file_bytes.decode('utf-8')
        except Exception as e:
            await ctx.send(f"Could not read file: {e}")
            return

        input_filename = attachment.filename.rsplit('.', 1)[0]

    # -- INLINE TEXT MODE --
    elif code is not None:
        source_code = re.sub(r'^```[a-zA-Z]*\n?', '', code)
        source_code = re.sub(r'```$', '', source_code).strip()
        input_filename = 'obfuscated'

    else:
        await ctx.send(
            "Usage:\n"
            "Inline: ?obf <your lua code>\n"
            "File:   attach a .lua or .txt file and run ?obf"
        )
        return

    # -- OBFUSCATE --
    try:
        result = obfuscate_roblox(source_code)
    except Exception as e:
        await ctx.send(f"Obfuscation failed: {e}")
        return

    # -- SEND RESULT AS FILE --
    out_filename = f"{input_filename}_obfuscated.lua"

    file_obj = discord.File(
        fp=io.BytesIO(result.encode('utf-8')),
        filename=out_filename
    )

    await ctx.send(
        "Roblox Lua obfuscation complete. Here is your file:",
        file=file_obj
    )


@bot.command(name='obfhelp')
async def obfhelp(ctx):
    await ctx.send(
        "Obfuscation Bot Help\n\n"
        "Inline code:\n"
        "?obf local x = game.Players.LocalPlayer\n\n"
        "File upload:\n"
        "Attach a .lua or .txt file and run ?obf\n"
        "Result is sent back as a downloadable .lua file.\n\n"
        "Pipeline steps:\n"
        "1. Comment stripping\n"
        "2. Variable renaming (l/I/O/0 style)\n"
        "3. Garbage dead code injection\n"
        "4. Anonymous closure wrapping\n"
        "5. Hex encode + loadstring final layer"
    )


@bot.command(name='start')
async def start(ctx):
    await ctx.send("Bot is running. Use ?obfhelp to see available commands.")


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN not found in .env!")
    else:
        print("Token found! Starting bot...")
        bot.run(TOKEN)
