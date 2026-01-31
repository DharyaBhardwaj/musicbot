from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.stream import AudioPiped
from pytgcalls.types.stream import StreamType

import os
import aiohttp

pytg = None

async def init_pytgcalls(app: Client):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()


async def fetch_stream_url(query: str) -> str:
    url = "https://oddus-audio.vercel.app/api/search"
    params = {"query": query}
    headers = {
        "x-api-key": os.getenv("MUSIC_API_KEY", "oddus-wiz777")
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            data = await resp.json()

    if "audio" not in data:
        raise Exception("API did not return audio")

    return data["audio"]


async def play(app: Client, chat_id: int, query: str):
    await init_pytgcalls(app)

    stream_url = await fetch_stream_url(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(
            stream_url,
        ),
        stream_type=StreamType().pulse_stream,
    )


async def stop(chat_id: int):
    if pytg:
        await pytg.leave_group_call(chat_id)
