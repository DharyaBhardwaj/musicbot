import yt_dlp
import uuid
import os

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def download_audio(query: str):
    filename = f"{uuid.uuid4()}.mp3"
    path = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": path,
        "quiet": True,
        "noplaylist": True,
        "default_search": "ytsearch",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            title = info.get("title", "Unknown")
        return path, title
    except Exception:
        return None, None
