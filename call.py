import os
import aiohttp

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

# ==========================
# 🔹 CONFIG
# ==========================
MUSIC_API_URL = os.environ.get(
    "MUSIC_API_URL",
    "https://oddus-audio.vercel.app/api/search"
)

pytg = None
ACTIVE_CHATS = set()

# ==========================
async def init_vc(app: Client):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()

# ==========================
async def get_stream_url(query: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            MUSIC_API_URL,
            params={"q": query}   # ✅ IMPORTANT FIX
        ) as resp:
            data = await resp.json()

    if not data or "audio" not in data:
        raise Exception("API did not return audio")

    return data["audio"]

# ==========================
async def play(app: Client, chat_id: int, query: str):
    await init_vc(app)

    stream_url = await get_stream_url(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(
            stream_url,
            HighQualityAudio(),
        ),
    )

    ACTIVE_CHATS.add(chat_id)

# ==========================
async def stop(chat_id: int):
    if pytg and chat_id in ACTIVE_CHATS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CHATS.remove(chat_id)
