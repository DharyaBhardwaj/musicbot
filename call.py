import os
import aiohttp
from pytgcalls import PyTgCalls
from pytgcalls.types.stream import AudioPiped

from youtube import search_youtube, is_youtube_url

ODDUS_API = "https://oddus-audio.vercel.app/api/download"
ODDUS_KEY = "oddus-wiz777"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

pytgcalls = None


async def start_call(client):
    global pytgcalls
    if pytgcalls is None:
        pytgcalls = PyTgCalls(client)
        await pytgcalls.start()


async def download_audio(youtube_url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            ODDUS_API,
            headers={"x-api-key": ODDUS_KEY},
            params={"url": youtube_url},
            timeout=60
        ) as resp:

            if resp.status != 200:
                raise Exception("Oddus API failed")

            filename = "audio.mp3"
            cd = resp.headers.get("Content-Disposition", "")
            if "filename=" in cd:
                filename = cd.split("filename=")[-1].replace('"', "")

            path = os.path.join(DOWNLOAD_DIR, filename)

            with open(path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    return path


async def play_song(client, chat_id: int, query: str):
    if is_youtube_url(query):
        youtube_url = query
    else:
        youtube_url = await search_youtube(query)

    audio_path = await download_audio(youtube_url)

    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(audio_path)
    )
