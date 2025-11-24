from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import os

# ---------------- CONFIG ----------------
API_ID = 38516298              # your Telegram API ID
API_HASH = "2d660c3eab3f16d6a01534448fc850e7"
SESSION_STRING = "BAJLtkoAokJ3WolO8t7af4HpwVe3-Wf9eLJbAwrNFG1qYc_U_uMK9xZu8MMu_wPsUBiXV88GY1ZrDchBkSQgTd_o7xMwe38tSLkBudkjfkIN1voQjJNEkFZkbUFqgXMb1KV70q_It-STisF5mCPd1YxWZDXRPqWM2nIWSYbM3kMrwo1GJrCk8Da3sCFXdTujN30EV-FgVZX002Bj3wlI9bnHgjLugbMI_LOXuI6DmG-uRWM88C7Bwcg1bqWDnuyV2c_PkK86j3tsbaT9WDPIfSvfB4YTjq8bYoYdaGHRGqvWmM9wZo5fuJNp0H_geG4ZLoEMAs1EiC1lcn58ja0r7jy6Dd8mmAAAAAHV6rIfAA"

ALLOWED_USER = 6836129142    # only this user can send audio & control
AUDIO_FILE = "last_audio.ogg"
DEFAULT_VOLUME = 100
current_volume = DEFAULT_VOLUME

# ---------------- INIT ----------------
app = Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
call = PyTgCalls(app)

def allowed(msg: Message):
    return msg.from_user and msg.from_user.id == ALLOWED_USER

# -------- AUTO-DOWNLOAD AUDIO FROM SPECIFIC USER --------
@app.on_message(filters.private & filters.voice)
async def download_audio(client, message):
    if not allowed(message):
        return

    await message.download(AUDIO_FILE)
    await message.reply("🎵 Voice saved. Use /joinvc to play.")

# ---------------- JOIN VC ----------------
@app.on_message(filters.command("joinvc") & filters.private)
async def joinvc(client, message):
    if not allowed(message):
        return

    chat_id = message.chat.id

    if not os.path.exists(AUDIO_FILE):
        return await message.reply("❌ No audio. Send a voice note first.")

    try:
        await call.join_group_call(
            chat_id,
            AudioPiped(AUDIO_FILE, volume=current_volume)
        )
        await message.reply(f"✅ Playing audio\n🔊 Volume: {current_volume}%")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# ---------------- LEAVE VC ----------------
@app.on_message(filters.command("leavevc") & filters.private)
async def leavevc(client, message):
    if not allowed(message):
        return

    chat_id = message.chat.id
    try:
        await call.leave_group_call(chat_id)
        await message.reply("👋 Left VC")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# ---------------- CHANGE VOLUME ----------------
@app.on_message(filters.command("volume") & filters.private)
async def change_volume(client, message):
    if not allowed(message):
        return

    global current_volume
    chat_id = message.chat.id

    try:
        new_volume = int(message.text.split()[1])
        new_volume = max(1, min(500, new_volume))

        current_volume = new_volume

        await call.change_stream(
            chat_id,
            AudioPiped(AUDIO_FILE, volume=current_volume)
        )
        await message.reply(f"🔊 Volume: {current_volume}%")
    except:
        await message.reply("❌ Use: /volume 1-500")

# ------------- START BOT -------------
app.start()
call.start()
print("Userbot started. Allowed User:", ALLOWED_USER)
app.idle()
