import os
import aiohttp
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.stream import AudioPiped

pytg = None

async def init_vc(app: Client):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()


async def get_stream_url(song_name: str) -> str:
    url = "https://oddus-audio.vercel.app/api/search"
    params = {"query": song_name}
    headers = {
        "x-api-key": os.getenv("MUSIC_API_KEY", "oddus-wiz777")
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            data = await resp.json()

    # 👇 यही सुबह वाले bot का behaviour है
    if "audio" not in data:
        raise Exception("API did not return audio")

    return data["audio"]


async def play(app: Client, chat_id: int, song_name: str):
    await init_vc(app)
    stream_url = await get_stream_url(song_name)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(stream_url),
    )


async def stop(chat_id: int):
    if pytg:
        await pytg.leave_group_call(chat_id)
