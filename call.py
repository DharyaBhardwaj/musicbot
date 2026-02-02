import os
import aiohttp

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio


# ==============================
# 🔹 CONFIG
# ==============================
DOWNLOAD_API = os.environ.get(
    "MUSIC_API_URL",
    "https://oddus-audio.vercel.app/api/download"
)

pytg = None
ACTIVE_CHATS = set()


# ==============================
# 🔹 INIT VC
# ==============================
async def init_vc(app: Client):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()


# ==============================
# 🔹 DOWNLOAD SONG
# ==============================
async def download_song(song_name: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            DOWNLOAD_API,
            params={"title": song_name}  # 🔥 IMPORTANT
        ) as resp:

            if resp.status != 200:
                raise Exception(f"Download API HTTP error: {resp.status}")

            data = await resp.json()

    if "file" not in data:
        raise Exception("No audio source found")

    return data["file"]


# ==============================
# 🔹 PLAY
# ==============================
async def play(app: Client, chat_id: int, song_name: str):
    await init_vc(app)

    stream_url = await download_song(song_name)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(
            stream_url,
            HighQualityAudio(),
        ),
    )

    ACTIVE_CHATS.add(chat_id)


# ==============================
# 🔹 STOP
# ==============================
async def stop(chat_id: int):
    if pytg and chat_id in ACTIVE_CHATS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CHATS.remove(chat_id)