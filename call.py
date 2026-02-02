import os
import aiohttp
import asyncio

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

# ==============================
# ENV
# ==============================
MUSIC_API_URL = os.environ.get(
    "MUSIC_API_URL",
    "https://oddus-audio.vercel.app/api/download"
)
ODDUS_API_KEY = os.environ["ODDUS_API_KEY"]

# ==============================
pytg = None
ACTIVE_CHATS = set()

async def init_vc(user: Client):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(user)
        await pytg.start()

async def download_audio(query: str) -> str:
    headers = {
        "x-api-key": ODDUS_API_KEY,
        "Accept": "*/*",
    }
    params = {"query": query}

    async with aiohttp.ClientSession() as session:
        async with session.get(MUSIC_API_URL, headers=headers, params=params) as resp:
            if resp.status != 200:
                raise Exception(f"Download API HTTP error: {resp.status}")

            file_path = f"/tmp/{hash(query)}.mp3"
            with open(file_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    return file_path

async def play(user: Client, chat_id: int, query: str):
    await init_vc(user)

    audio_file = await download_audio(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(
            audio_file,
            HighQualityAudio(),
        ),
    )

    ACTIVE_CHATS.add(chat_id)

async def stop(chat_id: int):
    if pytg and chat_id in ACTIVE_CHATS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CHATS.remove(chat_id)