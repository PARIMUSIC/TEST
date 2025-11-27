# Install requirements:
# pip install pyrogram tgcrypto pytgcalls

from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import os

# ---------------- CONFIG ----------------
API_ID = 123456          # your Telegram API ID
API_HASH = "your_api_hash"  # your Telegram API hash
SESSION_STRING = "your_session_string"  # generated from Pyrogram
AUDIO_FILE = "audio.mp3"  # path to your audio file
DEFAULT_VOLUME = 100      # 100 = normal (valid range: 1–200)

# Validate audio file
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")

# -------------- INIT -------------------
app = Client(
    name="vc_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)
calls = PyTgCalls(app)

current_volume = DEFAULT_VOLUME

# -------------- COMMANDS ----------------
@app.on_message(filters.command("joinvc") & filters.me)
async def join_voice(client, message):
    chat_id = message.chat.id
    try:
        await calls.join_group_call(
            chat_id,
            AudioPiped(AUDIO_FILE, volume=current_volume)
        )
        await message.reply(f"✅ Joined VC with volume {current_volume}%")
    except Exception as e:
        await message.reply(f"❌ Error joining VC: {e}")

@app.on_message(filters.command("leavevc") & filters.me)
async def leave_voice(client, message):
    chat_id = message.chat.id
    try:
        await calls.leave_group_call(chat_id)
        await message.reply("✅ Left VC")
    except Exception as e:
        await message.reply(f"❌ Error leaving VC: {e}")

@app.on_message(filters.command("volume") & filters.me)
async def set_volume(client, message):
    global current_volume
    try:
        new_volume = int(message.text.split()[1])
        if new_volume < 1:
            new_volume = 1
        elif new_volume > 200:  # PyTgCalls safe max
            new_volume = 200

        current_volume = new_volume
        chat_id = message.chat.id
        await calls.change_stream(
            chat_id,
            AudioPiped(AUDIO_FILE, volume=current_volume)
        )
        await message.reply(f"🔊 Volume set to {current_volume}%")
    except IndexError:
        await message.reply("❌ Usage: /volume <number> (1–200)")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# -------------- START BOT ----------------
print("Starting userbot...")
app.start()
calls.start()
print("✅ Userbot started. Use /joinvc, /leavevc, /volume commands.")
app.idle()
