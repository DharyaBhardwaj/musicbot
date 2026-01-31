import yt_dlp
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from pyrogram import Client

pytg = None

def yt_stream(query: str):
    ydl_opts = {
        "format": "bestaudio",
        "quiet": True,
        "default_search": "ytsearch",
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            info = info["entries"][0]
        return info["url"], info["title"]

async def play_song(app: Client, chat_id: int, query: str):
    global pytg

    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()

    stream_url, title = yt_stream(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(stream_url),
    )

    await app.send_message(chat_id, f"🎵 Playing: **{title}**")
