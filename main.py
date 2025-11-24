# Minimal Telegram Music/Userbot
import os
import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types import StreamType

# Load environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER_ID = int(os.getenv("OWNER_ID"))
DEFAULT_VOLUME = int(os.getenv("DEFAULT_VOLUME", 50))

# Initialize Pyrogram client
app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

# Initialize PyTgCalls client
pytgcalls = PyTgCalls(app)


# Function to join VC and play audio
async def play_audio(chat_id: int, file_path: str):
    try:
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(file_path, stream_type=StreamType().local_stream),
        )
        print(f"✅ Playing audio in chat {chat_id}")
    except Exception as e:
        print(f"❌ Error joining VC: {e}")


# Command listener example
@app.on_message()
async def handler(client: Client, message: Message):
    if message.from_user and message.from_user.id == OWNER_ID:
        if message.text and message.text.startswith("/play "):
            file_path = message.text.split("/play ", 1)[1]
            chat_id = message.chat.id
            await play_audio(chat_id, file_path)


async def main():
    await app.start()
    await pytgcalls.start()
    print("✅ Bot is online and ready...")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
