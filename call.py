import os
import re
import aiohttp
import yt_dlp

from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream.audio_piped import AudioPiped



from assistant import assistant

API_URL = "https://oddus-audio.vercel.app/api/download"
API_KEY = "oddus-wiz777"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

pytgcalls = PyTgCalls(assistant)


async def start_call():
    await pytgcalls.start()


def search_youtube(query):
    ydl_opts = {"quiet": True, "noplaylist": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return info["entries"][0]["webpage_url"]


async def download_audio(video_url):
    headers = {"x-api-key": API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            API_URL,
            headers=headers,
            params={"url": video_url},
        ) as resp:

            cd = resp.headers.get("Content-Disposition", "")
            filename = "audio.mp3"

            m = re.search(r'filename="?([^"]+)"?', cd)
            if m:
                filename = m.group(1)

            file_path = os.path.join(DOWNLOAD_DIR, filename)

            with open(file_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    return file_path


async def play_song(chat_id, query):
    video_url = search_youtube(query)
    audio_file = await download_audio(video_url)

    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(audio_file)
    )
