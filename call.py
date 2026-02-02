import os
import aiohttp
import asyncio

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio


# ======================
# CONFIG
# ======================
MUSIC_API_URL = os.environ["MUSIC_API_URL"]

pytg: PyTgCalls | None = None
ACTIVE_CHATS = set()


# ======================
async def init_vc(app: Client):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()


# ======================
async def download_audio(query: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            MUSIC_API_URL,
            json={"query": query}   # ❗ DOWNLOAD ONLY
        ) as resp:

            if resp.status != 200:
                raise Exception(f"Download API HTTP error: {resp.status}")

            data = await resp.json()

    if "audio" not in data:
        raise Exception("Download API did not return audio")

    return data["audio"]


# ======================
async def play(app: Client, chat_id: int, query: str):
    await init_vc(app)

    audio_source = await download_audio(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(
            audio_source,
            HighQualityAudio()
        )
    )

    ACTIVE_CHATS.add(chat_id)


# ======================
async def stop(chat_id: int):
    if pytg and chat_id in ACTIVE_CHATS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CHATS.remove(chat_id)