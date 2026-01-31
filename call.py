import os
import asyncio
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from pyrogram.types import Message
from pyrogram import Client
import aiohttp

ODDUS_API = "https://oddus-audio.vercel.app/api/search"

pytg = None
active_calls = {}

async def start_call(app: Client, message: Message, query: str):
    global pytg

    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()

    chat_id = message.chat.id

    await message.reply("🎵 Searching & playing...")

    audio_url = await search_song(query)
    if not audio_url:
        return await message.reply("❌ Song nahi mila")

    stream = MediaStream(audio_url)

    await pytg.join_group_call(chat_id, stream)
    active_calls[chat_id] = True

async def search_song(query: str) -> str | None:
    params = {"q": query}
    async with aiohttp.ClientSession() as session:
        async with session.get(ODDUS_API, params=params) as r:
            if r.status != 200:
                return None
            data = await r.json()
            return data.get("audio")
