import os
import aiohttp
import asyncio

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch

API_URL = "https://oddus-audio.vercel.app/api/download"
API_KEY = "oddus-wiz777"

pytg = None
ACTIVE_CALLS = {}

async def init_vc(app: Client):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()

async def song_to_youtube(song):
    res = await VideosSearch(song, limit=1).next()
    return res["result"][0]["link"]

async def download_from_api(yt_url, chat_id):
    os.makedirs("downloads", exist_ok=True)
    path = f"downloads/{chat_id}.mp3"

    async with aiohttp.ClientSession() as s:
        async with s.get(
            API_URL,
            params={"url": yt_url},
            headers={"x-api-key": API_KEY}
        ) as r:
            if r.status != 200:
                raise Exception("API did not return audio")
            with open(path, "wb") as f:
                f.write(await r.read())

    return path

async def play_song(app: Client, chat_id: int, song_name: str):
    await app.get_chat(chat_id)   # 🔥 Peer fix
    await init_vc(app)

    yt = await song_to_youtube(song_name)
    audio = await download_from_api(yt, chat_id)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(audio)
    )

    ACTIVE_CALLS[chat_id] = audio

async def stop_song(chat_id: int):
    if chat_id in ACTIVE_CALLS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CALLS.pop(chat_id, None)
