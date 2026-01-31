import os
import aiohttp
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION_STRING")

API_URL = os.getenv("MUSIC_API_URL")
API_KEY = os.getenv("MUSIC_API_KEY")

user = Client(
    "vc-user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
)

pytg = PyTgCalls(user)


async def get_audio_url(query: str) -> str:
    """
    song name -> API -> direct audio url
    """
    headers = {"x-api-key": API_KEY}
    params = {"query": query}

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=headers, params=params) as r:
            if r.status != 200:
                raise Exception("API failed")

            data = await r.json()

            # ⚠️ IMPORTANT:
            # API response must contain audio stream url
            if "audio_url" not in data:
                raise Exception("API did not return audio_url")

            return data["audio_url"]


async def start_call(chat_id: int, query: str):
    await user.start()
    await pytg.start()

    audio_url = await get_audio_url(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(audio_url, HighQualityAudio()),
    )


async def stop_song(chat_id: int):
    await pytg.leave_group_call(chat_id)
