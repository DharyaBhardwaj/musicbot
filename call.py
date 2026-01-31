import aiohttp
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

ODDUS_API = "https://oddus-audio.vercel.app"
ODDUS_KEY = "oddus-wiz777"

pytg = None


async def init(app):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()


async def fetch_audio(query: str) -> str:
    async with aiohttp.ClientSession() as s:
        async with s.get(
            f"{ODDUS_API}/api/search",
            params={"query": query},
            headers={"x-api-key": ODDUS_KEY},
        ) as r:
            data = await r.json()

    if "url" not in data:
        raise Exception("Song not found")

    yt = data["url"]

    async with aiohttp.ClientSession() as s:
        async with s.get(
            f"{ODDUS_API}/api/download",
            params={"url": yt},
            headers={"x-api-key": ODDUS_KEY},
        ) as r:
            with open("song.mp3", "wb") as f:
                async for c in r.content.iter_chunked(65536):
                    f.write(c)

    return "song.mp3"


async def play(app, chat_id: int, query: str):
    await init(app)
    audio = await fetch_audio(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(audio, HighQualityAudio()),
    )


async def stop(chat_id: int):
    if pytg:
        await pytg.leave_group_call(chat_id)
