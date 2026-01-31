from pytgcalls import PyTgCalls
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream.quality import HighQualityAudio
from pytgcalls.types.input_stream import InputAudioStream
from pyrogram import Client
import yt_dlp
import os

assistant = Client(
    "assistant",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("SESSION_STRING")
)

pytgcalls = PyTgCalls(assistant)

async def start_call():
    await assistant.start()
    await pytgcalls.start()

async def download_audio(url):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)

    return file

async def play_song(chat_id, url):
    try:
        file = await download_audio(url)

        await pytgcalls.join_group_call(
            chat_id,
            InputAudioStream(
                file,
                HighQualityAudio(),
            ),
        )

        return True

    except Exception as e:
        print("VC PLAY ERROR:", e)
        return False
