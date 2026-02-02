import os
import aiohttp
import uuid

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio


# ======================
# ENV
# ======================
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
STRING_SESSION = os.environ["STRING_SESSION"]

MUSIC_API_URL = os.environ.get(
    "MUSIC_API_URL",
    "https://oddus-audio.vercel.app/api/download"
)
ODDUS_API_KEY = os.environ["ODDUS_API_KEY"]


# ======================
# USER CLIENT (VC)
# ======================
user = Client(
    "user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    in_memory=True,
    no_updates=True
)

pytg = PyTgCalls(user)
ACTIVE = set()


# ======================
async def start_vc():
    if not user.is_connected:
        await user.start()
    if not pytg.is_connected:
        await pytg.start()


# ======================
async def download_audio(query: str) -> str:
    params = {
        "query": query,
        "key": ODDUS_API_KEY
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(MUSIC_API_URL, params=params) as resp:
            if resp.status != 200:
                raise Exception(f"Download API HTTP error: {resp.status}")
            data = await resp.json()

    if "audio" not in data:
        raise Exception("Download API did not return audio")

    return data["audio"]


# ======================
async def play(chat_id: int, query: str):
    await start_vc()

    audio_url = await download_audio(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(audio_url, HighQualityAudio())
    )

    ACTIVE.add(chat_id)


# ======================
async def stop(chat_id: int):
    if chat_id in ACTIVE:
        await pytg.leave_group_call(chat_id)
        ACTIVE.remove(chat_id)