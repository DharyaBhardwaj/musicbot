import yt_dlp
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from assistant import assistant

pytgcalls = PyTgCalls(assistant)

async def start_call():
    await pytgcalls.start()

def get_stream_url(query):
    ydl_opts = {
        "format": "bestaudio",
        "noplaylist": True,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return info["entries"][0]["url"]

async def play_song(chat_id, query):
    stream_url = get_stream_url(query)

    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(stream_url)
    )
