import aiohttp
import asyncio
import os

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

# =========================
# ODDUS API CONFIG
# =========================
ODDUS_API = "https://oddus-audio.vercel.app/api/play"
ODDUS_KEY = os.getenv("ODDUS_API_KEY", "oddus-wiz777")

# =========================
# Pyrogram + PyTgCalls
# =========================
pytg = PyTgCalls(None)
started = False


async def get_stream_url(query: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            ODDUS_API,
            params={"query": query},
            headers={"x-api-key": ODDUS_KEY},
        ) as resp:
            if resp.status != 200:
                raise Exception("API error")

            data = await resp.json()

            if "stream_url" not in data:
                raise Exception("API did not return stream_url")

            return data["stream_url"]


async def start_call(app: Client, message, query: str):
    global started

    if not started:
        pytg._app = app
        await pytg.start()
        started = True

    chat_id = message.chat.id

    stream_url = await get_stream_url(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(stream_url),
    )

    await message.reply_text(
        f"🎵 **Now Playing**\n`{query}`",
        disable_web_page_preview=True,
    )


async def stop_song(chat_id: int):
    await pytg.leave_group_call(chat_id)
