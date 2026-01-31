import os
import re
import aiohttp
from youtubesearchpython.__future__ import VideosSearch

ODDUS_API = "https://oddus-audio.vercel.app/api/download"
API_KEY = "oddus-wiz777"
DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def search_song(query: str) -> str:
    search = VideosSearch(query, limit=1)
    result = await search.next()
    return result["result"][0]["link"]

async def download_audio(url: str) -> str:
    headers = {"x-api-key": API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            ODDUS_API,
            headers=headers,
            params={"url": url},
        ) as resp:

            if resp.status != 200:
                raise Exception("Oddus API download failed")

            filename = "audio.mp3"
            cd = resp.headers.get("Content-Disposition", "")
            m = re.search(r'filename="?([^"]+)"?', cd)
            if m:
                filename = m.group(1)

            path = os.path.join(DOWNLOAD_DIR, filename)
            with open(path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    return path
