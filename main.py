
import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

# ---------------- CONFIG ----------------
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
SESSION_STRING = os.getenv("SESSION_STRING", "your_session_string")
AUDIO_FILE = os.getenv("AUDIO_FILE", "audio.mp3")
DEFAULT_VOLUME = int(os.getenv("DEFAULT_VOLUME", "100"))

# Validate audio file
if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")

# Init clients
app = Client(
    name="vc_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)
calls = PyTgCalls(app)
current_volume = DEFAULT_VOLUME


# ---------------- COMMANDS ----------------
@app.on_message(filters.command("joinvc") & filters.me)
async def join_voice(_, message):
    chat_id = message.chat.id
    try:
        await calls.join_group_call(
            chat_id,
            AudioPiped(AUDIO_FILE, volume=current_volume)
        )
        await message.reply(f"✅ Joined VC with volume {current_volume}%")
    except Exception as e:
        await message.reply(f"❌ Join failed: {e}")


@app.on_message(filters.command("leavevc") & filters.me)
async def leave_voice(_, message):
    chat_id = message.chat.id
    try:
        await calls.leave_group_call(chat_id)
        await message.reply("✅ Left VC")
    except Exception as e:
        await message.reply(f"❌ Leave failed: {e}")


@app.on_message(filters.command("volume") & filters.me)
async def set_volume(_, message):
    global current_volume
    try:
        new_volume = int(message.text.split()[1])
        new_volume = max(1, min(200, new_volume))  # clamp to 1–200
        current_volume = new_volume

        chat_id = message.chat.id
        await calls.change_stream(
            chat_id,
            AudioPiped(AUDIO_FILE, volume=current_volume)
        )
        await message.reply(f"🔊 Volume set to {current_volume}%")
    except IndexError:
        await message.reply("❌ Usage: /volume <1-200>")
    except Exception as e:
        await message.reply(f"❌ Volume error: {e}")


# ---------------- START ----------------
if name == "main":
    print("🚀 Starting VC Userbot...")
    app.start()
    calls.start()
    print("✅ Bot is running! Send /joinvc in any chat.")
    app.idle()
