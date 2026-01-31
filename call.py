import os
import requests
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from assistant import assistant

API_URL = "https://oddus-audio.vercel.app/api/download"
API_KEY = "oddus-wiz777"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

pytgcalls = PyTgCalls(assistant)


async def start_call():
    await pytgcalls.start()


def download_audio(url):
    headers = {"x-api-key": API_KEY}
    params = {"url": url}

    r = requests.get(API_URL, headers=headers, params=params)

    if r.status_code != 200:
        raise Exception("Audio download failed")

    file_path = os.path.join(DOWNLOAD_DIR, "song.mp3")

    with open(file_path, "wb") as f:
        f.write(r.content)

    return file_path


async def play_song(chat_id, url):
    try:
        audio_file = download_audio(url)

        await pytgcalls.join_group_call(
            chat_id,
            InputAudioStream(audio_file),
        )

        return True

    except Exception as e:
        print("VC PLAY ERROR:", e)
        return False
