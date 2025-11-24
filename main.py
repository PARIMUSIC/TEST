import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
OWNER_ID = int(os.getenv("OWNER_ID"))
AUDIO_FILE = "audio.mp3"

app = Client(
    name="vc-userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

calls = PyTgCalls(app)
current_volume = 100


# ---------- OWNER FILTER ----------
def is_owner(_, __, message):
    return message.from_user and message.from_user.id == OWNER_ID


owner_filter = filters.create(is_owner)


# ---------- JOIN VC ----------
@app.on_message(filters.command("joinvc") & owner_filter)
async def join_vc(client, message):
    global current_volume

    # /joinvc or /joinvc -1001234567
    if len(message.command) > 1:
        chat_id = int(message.command[1])
    else:
        chat_id = message.chat.id

    try:
        await calls.join_group_call(
            chat_id,
            AudioPiped(AUDIO_FILE, volume=current_volume)
        )
        await message.reply(f"✅ Joined VC in **{chat_id}** with volume {current_volume}%")
    except Exception as e:
        await message.reply(f"❌ Error joining VC:\n`{e}`")


# ---------- LEAVE VC ----------
@app.on_message(filters.command("leavevc") & owner_filter)
async def leave_vc(client, message):
    try:
        await calls.leave_group_call(message.chat.id)
        await message.reply("✅ Left VC")
    except Exception as e:
        await message.reply(f"❌ Error leaving VC:\n`{e}`")


# ---------- SET VOLUME ----------
@app.on_message(filters.command("volume") & owner_filter)
async def change_volume(client, message):
    global current_volume
    try:
        new_volume = int(message.command[1])
        if new_volume < 1:
            new_volume = 1
        if new_volume > 500:
            new_volume = 500

        current_volume = new_volume

        await calls.change_stream(
            message.chat.id,
            AudioPiped(AUDIO_FILE, volume=current_volume)
        )

        await message.reply(f"🔊 Volume set to {current_volume}%")
    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")


# ---------- START ----------
app.start()
calls.start()
print("Bot started!")
app.idle()
