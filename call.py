import os
import re
import aiohttp

from pytgcalls import PyTgCalls
from pytgcalls.types.stream import AudioPiped

from assistant import assistant

API_URL = "https://oddus-audio.vercel.app/api/download"
API_KEY = "oddus-wiz777"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

pytgcalls = PyTgCalls(assistant)


async def start_call():
    await pytgcalls.start()


async def download_audio(video_url):
    headers = {"x-api-key": API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            API_URL,
            headers=headers,
            params={"url": video_url},
        ) as resp:

            if resp.status != 200:
                raise Exception("Download failed")

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


async def play_song(chat_id, url):
    try:
        file_path = await download_audio(url)

        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(file_path)
        )

        return True

    except Exception as e:
        print("VC PLAY ERROR:", e)
        return False
