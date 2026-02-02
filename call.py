import os
import aiohttp
import uuid
import subprocess

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

# =========================
# CONFIG
# =========================
DOWNLOAD_API = os.environ.get(
    "MUSIC_API_URL",
    "https://oddus-audio.vercel.app/api/download"
)

ODDUS_API_KEY = os.environ.get(
    "ODDUS_API_KEY",
    "oddus-wiz777"
)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

pytg = None
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
# DOWNLOAD + VERIFY
# =========================
async def download_song(query: str) -> str:
    raw_path = os.path.join(DOWNLOAD_DIR, f"{uuid.uuid4().hex}.raw")
    final_path = raw_path.replace(".raw", ".mp3")

    headers = {
        "x-api-key": ODDUS_API_KEY,
        "Accept": "*/*",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
            DOWNLOAD_API,
            params={"url": query},
            headers=headers,
        ) as resp:
            if resp.status != 200:
                raise Exception(f"Download API HTTP error: {resp.status}")

            with open(raw_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    # 🔥 FORCE CONVERT → REAL AUDIO
    cmd = [
        "ffmpeg",
        "-y",
        "-i", raw_path,
        "-vn",
        "-ac", "2",
        "-ar", "48000",
        "-f", "mp3",
        final_path
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(final_path) or os.path.getsize(final_path) < 5000:
        raise Exception("Downloaded file is not valid audio")

    return final_path


# =========================
# PLAY
# =========================
async def play(app: Client, chat_id: int, query: str):
    await init_vc(app)

    audio_path = await download_song(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(
            audio_path,
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