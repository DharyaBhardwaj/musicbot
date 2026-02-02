import os
import aiohttp
import uuid

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
STRING_SESSION = os.environ["STRING_SESSION"]

ODDUS_API_KEY = os.environ["ODDUS_API_KEY"]
DOWNLOAD_API = os.environ["MUSIC_API_URL"]

assistant = Client(
    STRING_SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    in_memory=True,
)

pytg = PyTgCalls(assistant)
ACTIVE = set()

async def init():
    if not assistant.is_connected:
        await assistant.start()
    if not pytg.is_connected:
        await pytg.start()

async def download_song(query: str) -> str:
    params = {"query": query}
    headers = {"x-api-key": ODDUS_API_KEY}

    async with aiohttp.ClientSession() as s:
        async with s.get(DOWNLOAD_API, params=params, headers=headers) as r:
            if r.status != 200:
                raise Exception(f"Download API HTTP error: {r.status}")

            path = f"downloads/{uuid.uuid4().hex}.mp3"
            os.makedirs("downloads", exist_ok=True)

            with open(path, "wb") as f:
                async for chunk in r.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    if os.path.getsize(path) < 100_000:
        raise Exception("Downloaded file is not valid audio")

    return path

async def play(chat_id: int, query: str):
    await init()

    audio = await download_song(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(audio, HighQualityAudio()),
    )
    ACTIVE.add(chat_id)

async def stop(chat_id: int):
    if chat_id in ACTIVE:
        await pytg.leave_group_call(chat_id)
        ACTIVE.remove(chat_id)