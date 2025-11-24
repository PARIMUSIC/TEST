import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))
DEFAULT_VOLUME = int(os.environ.get("DEFAULT_VOLUME", 100))

# Pyrogram client
app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
)

# PyTgCalls client
pytgcall = PyTgCalls(app)

async def start_call(chat_id, audio_file):
    await pytgcall.join_group_call(
        chat_id,
        AudioPiped(audio_file),
    )
    await pytgcall.set_stream_volume(chat_id, DEFAULT_VOLUME)

# Command to play audio
@app.on_message(filters.user(OWNER_ID) & filters.command("play"))
async def play_audio(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /play <audio_file_path>")
        return
    audio_file = message.command[1]
    chat_id = message.chat.id
    await start_call(chat_id, audio_file)
    await message.reply_text(f"🎵 Playing {audio_file} in VC!")

print("Userbot started...")
app.run()
