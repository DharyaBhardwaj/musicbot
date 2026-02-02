import os
import aiohttp
import uuid

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

# =========================
# CONFIG
# =========================
MUSIC_API_URL = os.environ.get(
    "MUSIC_API_URL",
    "https://oddus-audio.vercel.app/api/download"
)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

pytg: PyTgCalls | None = None
ACTIVE_CHATS = set()


# =========================
# INIT VC
# =========================
async def init_vc(app: Client):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()


# =========================
# DOWNLOAD AUDIO
# =========================
async def download_song(query: str) -> str:
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(
            MUSIC_API_URL,
            params={"url": query},
        ) as resp:
            if resp.status != 200:
                raise Exception(f"Download API HTTP error: {resp.status}")

            with open(filepath, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    return filepath


# =========================
# PLAY
# =========================
async def play(app: Client, chat_id: int, query: str):
    await init_vc(app)

    file_path = await download_song(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(
            file_path,
            HighQualityAudio(),
        ),
    )

    ACTIVE_CHATS.add(chat_id)


# =========================
# STOP
# =========================
async def stop(chat_id: int):
    if pytg and chat_id in ACTIVE_CHATS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CHATS.remove(chat_id)