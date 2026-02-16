import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import re
import io

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# ──────────────────────────────────────────────
#  OBFUSCATOR
# ──────────────────────────────────────────────

def obfuscate_roblox(code: str) -> str:
    # Step 1: Strip comments
    code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
    code = re.sub(r'--[^\n]*', '', code)

    # Step 2: Remove blank lines
    lines = [l for l in code.split('\n') if l.strip()]
    code = ' '.join(lines)

    # Step 3: Rename local variables
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
    import random, string
    for var in local_vars:
        if var not in lua_keywords and var not in mapping:
            mapping[var] = '_' + ''.join(random.choices(string.ascii_letters, k=10))

    for original, obf in sorted(mapping.items(), key=lambda x: -len(x[0])):
        code = re.sub(rf'\b{re.escape(original)}\b', obf, code)

    # Step 4: Hex encode and wrap in loadstring
    hex_encoded = code.encode('utf-8').hex()
    result = (
        'local __H="' + hex_encoded + '"\n'
        'local __D=""\n'
        'for __i=1,#__H,2 do\n'
        '    __D=__D..string.char(tonumber(__H:sub(__i,__i+1),16))\n'
        'end\n'
        'loadstring(__D)()\n'
    )
    return result

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

    # -- SEND AS FILE --
    out_filename = f"{input_filename}_obfuscated.lua"
    file_obj = discord.File(
        fp=io.BytesIO(result.encode('utf-8')),
        filename=out_filename
    )
    await ctx.send("Roblox Lua obfuscation complete. Here is your file:", file=file_obj)


@bot.command(name='obfhelp')
async def obfhelp(ctx):
    await ctx.send(
        "Obfuscation Bot Help\n\n"
        "Inline: ?obf <your lua code>\n"
        "File:   attach a .lua or .txt file and run ?obf\n\n"
        "What it does:\n"
        "- Strips comments\n"
        "- Renames local variables\n"
        "- Hex encodes and wraps in loadstring"
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
