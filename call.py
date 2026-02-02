import os
import aiohttp
import uuid

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio


# ======================
# CONFIG
# ======================
DOWNLOAD_API = os.environ.get(
    "MUSIC_API_URL",
    "https://oddus-audio.vercel.app/api/download"
)

API_KEY = os.environ.get("ODDUS_API_KEY")


pytg = None
ACTIVE_CHATS = set()


# ======================
# INIT VC
# ======================
async def init_vc(app: Client):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()


# ======================
# DOWNLOAD AUDIO
# ======================
async def download_audio(query: str) -> str:
    file_name = f"/tmp/{uuid.uuid4()}.mp3"

    params = {
        "query": query,
        "key": API_KEY
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(DOWNLOAD_API, params=params) as resp:
            if resp.status != 200:
                raise Exception(f"Download API HTTP error: {resp.status}")

            with open(file_name, "wb") as f:
                f.write(await resp.read())

    return file_name


# ======================
# PLAY
# ======================
async def play(app: Client, chat_id: int, query: str):
    await init_vc(app)

    audio = await download_audio(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(audio, HighQualityAudio())
    )

    ACTIVE_CHATS.add(chat_id)


# ======================
# STOP
# ======================
async def stop(chat_id: int):
    if pytg and chat_id in ACTIVE_CHATS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CHATS.remove(chat_id)
