from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION_STRING")

# ✅ USER CLIENT (VC JOIN करता है)
user = Client(
    name="vc-user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
)

pytg = PyTgCalls(user)

async def start_call(chat_id: int, audio_url: str):
    await user.start()
    await pytg.start()

    await pytg.join_group_call(
        chat_id,
        AudioPiped(
            audio_url,
            HighQualityAudio(),
        ),
    )

async def stop_song(chat_id: int):
    await pytg.leave_group_call(chat_id)
