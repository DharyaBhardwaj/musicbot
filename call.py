import os
import re
import aiohttp
import requests

from pytgcalls import PyTgCalls
from pytgcalls.types.stream import AudioPiped

from assistant import assistant

# ===== API CONFIG =====
API_URL = "https://oddus-audio.vercel.app/api/download"
API_KEY = "oddus-wiz777"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# PyTgCalls client
pytgcalls = PyTgCalls(assistant)


# ===== START VC CLIENT =====
async def start_call():
    await pytgcalls.start()


# ===== YOUTUBE SEARCH (NO YT-DLP) =====
def search_youtube(query):
    r = requests.get(
        "https://ytsearch-api.vercel.app/search",
        params={"query": query},
        timeout=15,
    )

    data = r.json()
    return data["videos"][0]["url"]


# ===== DOWNLOAD AUDIO USING ODDUS API =====
async def download_audio(video_url):
    headers = {"x-api-key": API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            API_URL,
            headers=headers,
            params={"url": video_url},
        ) as resp:

            if resp.status != 200:
                raise Exception("Download API error")

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


# ===== PLAY SONG =====
async def play_song(chat_id, query):
    try:
        video_url = search_youtube(query)
        audio_file = await download_audio(video_url)

        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(audio_file),
        )

        return True

    except Exception as e:
        print("Play error:", e)
        return False
