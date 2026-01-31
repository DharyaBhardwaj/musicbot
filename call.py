import aiohttp
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

pytgcalls = None

ODDUS_API = "https://oddus-audio.vercel.app/api/stream"
ODDUS_KEY = "oddus-wiz777"


async def init_call(app):
    global pytgcalls
    if not pytgcalls:
        pytgcalls = PyTgCalls(app)
        await pytgcalls.start()


async def play_song(chat_id: int, youtube_url: str):
    api_url = f"{ODDUS_API}?url={youtube_url}&api_key={ODDUS_KEY}"

    stream = AudioPiped(
        api_url,
        HighQualityAudio(),
    )

    await pytgcalls.join_group_call(
        chat_id,
        stream,
    )


async def stop_song(chat_id: int):
    await pytgcalls.leave_group_call(chat_id)
