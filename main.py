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
            "Just attach a .lua or .txt file and run ?obf\n"
            "For .txt files run: ?obf with your file attached."
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

        # Only accept .lua and .txt files
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
        # Strip markdown code blocks if user wraps code in them
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
    result = obfuscate_roblox(source_code)

    # -- SEND RESULT AS FILE --
    out_filename = f"{input_filename}_obfuscated.lua"

    file_obj = discord.File(
        fp=io.BytesIO(result.encode('utf-8')),
        filename=out_filename
    )

    await ctx.send(
        f"Roblox Lua obfuscation complete. Here is your file:",
        file=file_obj
    )


@bot.command(name='obfhelp')
async def obfhelp(ctx):
    help_text = (
        "Obfuscation Bot Help\n\n"
        "Inline code:\n"
        "?obf local x = game.Players.LocalPlayer\n\n"
        "File upload:\n"
        "Attach a .lua or .txt file and run ?obf\n"
        "The result will be sent back as a downloadable .lua file.\n\n"
        "Output file will be named: yourfile_obfuscated.lua"
    )
    await ctx.send(help_text)


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
