import os
import re
import aiohttp
import yt_dlp

from pytgcalls import PyTgCalls

# Compatible import for different versions
try:
    from pytgcalls.types.input_stream import AudioPiped
except Exception:
    try:
        from pytgcalls.types.stream import AudioPiped
    except Exception:
        from pytgcalls.types import AudioPiped

from assistant import assistant

# ---------- CONFIG ----------
API_URL = "https://oddus-audio.vercel.app/api/download"
API_KEY = "oddus-wiz777"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
# ----------------------------

pytgcalls = PyTgCalls(assistant)


# Start call client
async def start_call():
    await pytgcalls.start()


# Search song on YouTube
def search_youtube(query):
    ydl_opts = {
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return info["entries"][0]["webpage_url"]


# Download audio using your Oddus API
async def download_audio(video_url):
    headers = {"x-api-key": API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            API_URL,
            headers=headers,
            params={"url": video_url},
        ) as resp:

            if resp.status != 200:
                raise RuntimeError("API download failed")

            cd = resp.headers.get("Content-Disposition", "")
            filename = "audio.mp3"

            match = re.search(r'filename="?([^"]+)"?', cd)
            if match:
                filename = match.group(1)

            file_path = os.path.join(DOWNLOAD_DIR, filename)

            with open(file_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    return file_path


# Join VC & play music
async def play_song(chat_id, query):
    video_url = search_youtube(query)
    audio_file = await download_audio(video_url)

    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(audio_file),
    )
