import os
import re
import aiohttp

from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio

from assistant import assistant

# ================= CONFIG =================
ODDUS_API_URL = "https://oddus-audio.vercel.app/api/download"
ODDUS_API_KEY = "oddus-wiz777"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
# =========================================

pytgcalls = PyTgCalls(assistant)


async def start_call():
    await pytgcalls.start()


async def download_from_oddus(youtube_url: str) -> str:
    headers = {"x-api-key": ODDUS_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            ODDUS_API_URL,
            headers=headers,
            params={"url": youtube_url},
        ) as resp:

            if resp.status != 200:
                raise Exception("Oddus API failed")

            cd = resp.headers.get("Content-Disposition", "")
            filename = "song.mp3"

            match = re.search(r'filename="?([^"]+)"?', cd)
            if match:
                filename = match.group(1)

            path = os.path.join(DOWNLOAD_DIR, filename)

            with open(path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    return path


async def play_song(chat_id: int, youtube_url: str):
    try:
        audio_path = await download_from_oddus(youtube_url)

        await pytgcalls.join_group_call(
            chat_id,
            InputAudioStream(
                audio_path,
                HighQualityAudio()
            ),
        )

        return True

    except Exception as e:
        print("VC PLAY ERROR:", e)
        return False
