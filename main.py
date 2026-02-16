import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import string
import base64
import re
import io

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────

def random_var(length=8):
    chars = string.ascii_letters
    return ''.join(random.choices(chars, k=length))

def random_hex_var():
    return '_0x' + ''.join(random.choices('0123456789abcdef', k=6))

# ──────────────────────────────────────────────
#  PYTHON OBFUSCATOR
# ──────────────────────────────────────────────

def obfuscate_python(code: str) -> str:
    lines = code.split('\n')
    cleaned = []
    for line in lines:
        stripped = re.sub(r'#.*', '', line).rstrip()
        if stripped.strip():
            cleaned.append(stripped)
    code = '\n'.join(cleaned)

    encoded = base64.b64encode(code.encode()).decode()

    obfuscated = (
        "import base64 as _b\n"
        f"_c = '{encoded}'\n"
        "exec(compile(_b.b64decode(_c.encode()), '<string>', 'exec'))\n"
    )
    return obfuscated

# ──────────────────────────────────────────────
#  JAVASCRIPT OBFUSCATOR
# ──────────────────────────────────────────────

def obfuscate_js(code: str) -> str:
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    identifiers = re.findall(r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\b', code)
    keywords = {
        'var', 'let', 'const', 'function', 'return', 'if', 'else',
        'for', 'while', 'do', 'break', 'continue', 'new', 'this',
        'true', 'false', 'null', 'undefined', 'typeof', 'instanceof',
        'class', 'extends', 'import', 'export', 'default', 'switch',
        'case', 'try', 'catch', 'finally', 'throw', 'delete', 'in',
        'of', 'async', 'await', 'yield', 'console', 'log'
    }
    mapping = {}
    for ident in identifiers:
        if ident not in keywords and ident not in mapping:
            mapping[ident] = random_hex_var()

    for original, obf in mapping.items():
        code = re.sub(rf'\b{re.escape(original)}\b', obf, code)

    encoded = base64.b64encode(code.encode()).decode()
    result = f"eval(atob('{encoded}'));"
    return result

# ──────────────────────────────────────────────
#  ROBLOX LUA OBFUSCATOR
# ──────────────────────────────────────────────

def obfuscate_roblox(code: str) -> str:
    code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
    code = re.sub(r'--[^\n]*', '', code)

    lines = [l for l in code.split('\n') if l.strip()]
    code = ' '.join(lines)

    local_vars = re.findall(r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*)\b', code)
    lua_keywords = {
        'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
        'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
        'return', 'then', 'true', 'until', 'while', 'game', 'workspace',
        'script', 'Instance', 'wait', 'print', 'pairs', 'ipairs', 'type',
        'tostring', 'tonumber', 'require', 'pcall', 'xpcall', 'error',
        'warn', 'math', 'table', 'string', 'os', 'task'
    }
    mapping = {}
    for var in local_vars:
        if var not in lua_keywords and var not in mapping:
            mapping[var] = random_var(10)

    for original, obf in mapping.items():
        code = re.sub(rf'\b{re.escape(original)}\b', obf, code)

    hex_encoded = code.encode().hex()

    obfuscated = (
        'local __H = "' + hex_encoded + '"\n'
        'local __D = ""\n'
        'for i = 1, #__H, 2 do\n'
        '    __D = __D .. string.char(tonumber(__H:sub(i, i+1), 16))\n'
        'end\n'
        'loadstring(__D)()\n'
    )
    return obfuscated

# ──────────────────────────────────────────────
#  FILE EXTENSION → LANGUAGE DETECTOR
# ──────────────────────────────────────────────

def detect_language(filename: str) -> str | None:
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    mapping = {
        'py':   'python',
        'js':   'js',
        'lua':  'roblox',
        'rbx':  'roblox',
        'txt':  None,   # needs explicit lang arg
    }
    return mapping.get(ext)

# ──────────────────────────────────────────────
#  GLOBAL CHECK — block DMs
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
            "**Missing argument!**\n"
            "Usage: `?obf <type> <code>` or attach a `.py`, `.js`, `.lua` file.\n"
            "For `.txt` files, do: `?obf <python|js|roblox>` with attachment.\n"
            "Types: `python`, `js`, `roblox`"
        )
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        await ctx.send(f"An error occurred: `{error}`")

# ──────────────────────────────────────────────
#  COMMANDS
# ──────────────────────────────────────────────

@bot.command(name='obf')
async def obf(ctx, lang: str = None, *, code: str = None):
    """
    Obfuscate code from inline text OR an attached file.

    Inline:      ?obf python print('hi')
    File auto:   ?obf          (attach a .py / .js / .lua file)
    File txt:    ?obf python   (attach a .txt file, specify lang)
    """

    # ── FILE MODE ──────────────────────────────
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        filename = attachment.filename.lower()

        # Read file bytes
        try:
            file_bytes = await attachment.read()
            file_code = file_bytes.decode('utf-8')
        except Exception as e:
            await ctx.send(f"Could not read file: `{e}`")
            return

        # Determine language
        auto_lang = detect_language(filename)

        if auto_lang is not None:
            # .py / .js / .lua — language auto-detected
            resolved_lang = auto_lang
        elif lang is not None:
            # .txt or unknown ext — user must supply lang
            resolved_lang = lang.lower()
            if resolved_lang in ('lua', 'rbx'):
                resolved_lang = 'roblox'
            elif resolved_lang == 'javascript':
                resolved_lang = 'js'
        else:
            await ctx.send(
                "Could not detect language from file extension.\n"
                "For `.txt` files please specify the language:\n"
                "`?obf <python|js|roblox>` with your file attached."
            )
            return

        source_code = file_code
        input_filename = filename

    # ── INLINE TEXT MODE ───────────────────────
    elif code is not None and lang is not None:
        resolved_lang = lang.lower()
        if resolved_lang in ('lua', 'rbx'):
            resolved_lang = 'roblox'
        elif resolved_lang == 'javascript':
            resolved_lang = 'js'

        # Strip markdown code blocks
        source_code = re.sub(r'^```[a-zA-Z]*\n?', '', code)
        source_code = re.sub(r'```$', '', source_code).strip()
        input_filename = None

    else:
        await ctx.send(
            "**Usage:**\n"
            "Inline: `?obf <python|js|roblox> <code>`\n"
            "File:   attach a `.py`, `.js`, or `.lua` file and run `?obf`\n"
            "TXT:    attach a `.txt` file and run `?obf <python|js|roblox>`"
        )
        return

    # ── OBFUSCATE ──────────────────────────────
    if resolved_lang == 'python':
        result = obfuscate_python(source_code)
        out_ext = 'py'
        label = 'Python'
    elif resolved_lang == 'js':
        result = obfuscate_js(source_code)
        out_ext = 'js'
        label = 'JavaScript'
    elif resolved_lang == 'roblox':
        result = obfuscate_roblox(source_code)
        out_ext = 'lua'
        label = 'Roblox Lua'
    else:
        await ctx.send(
            f"Unknown language `{resolved_lang}`.\n"
            "Supported: `python`, `js`, `roblox`"
        )
        return

    # ── SEND RESULT ────────────────────────────
    # Always send as a .txt file so Discord doesn't struggle with large outputs
    out_filename = (
        input_filename.rsplit('.', 1)[0] + f'_obfuscated.{out_ext}'
        if input_filename else f'obfuscated.{out_ext}'
    )

    file_obj = discord.File(
        fp=io.BytesIO(result.encode('utf-8')),
        filename=out_filename
    )

    await ctx.send(
        f"✅ **{label} obfuscation complete!**\nHere is your obfuscated file:",
        file=file_obj
    )


@bot.command(name='obfhelp')
async def obfhelp(ctx):
    help_text = (
        "**🔒 Obfuscation Bot Help**\n\n"
        "**Inline code:**\n"
        "`?obf python print('hello')`\n"
        "`?obf js function greet() { console.log('hi') }`\n"
        "`?obf roblox local x = game.Players.LocalPlayer`\n\n"
        "**File upload (auto-detect language):**\n"
        "Attach a `.py`, `.js`, or `.lua` file and just type `?obf`\n\n"
        "**TXT file (specify language):**\n"
        "Attach a `.txt` file and type `?obf python` (or js / roblox)\n\n"
        "**Output:** always returned as a downloadable file.\n\n"
        "**Supported languages:** `python`, `js`, `roblox` / `lua`"
    )
    await ctx.send(help_text)


@bot.command(name='start')
async def start(ctx):
    await ctx.send("Bot is running! Use `?obfhelp` to see available commands.")


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
