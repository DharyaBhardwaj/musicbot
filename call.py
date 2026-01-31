import os
import asyncio
import aiohttp
import re
from collections import defaultdict, deque

from pytgcalls import PyTgCalls
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream import AudioPiped

from assistant import assistant

API_URL = "https://oddus-audio.vercel.app/api/download"
API_KEY = "oddus-wiz777"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

pytgcalls = PyTgCalls(assistant)

# group queues
queues = defaultdict(deque)
playing = {}

async def start_call():
    await pytgcalls.start()

# ---------------------------
# Download audio via API
# ---------------------------
async def download_audio(url):
    headers = {"x-api-key": API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=headers, params={"url": url}) as r:
            cd = r.headers.get("Content-Disposition", "")
            filename = "song.mp3"

            m = re.search(r'filename="?([^"]+)"?', cd)
            if m:
                filename = m.group(1)

            path = os.path.join(DOWNLOAD_DIR, filename)

            with open(path, "wb") as f:
                async for chunk in r.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    return path

# ---------------------------
# Queue Player
# ---------------------------
async def play_next(chat_id):
    if not queues[chat_id]:
        await pytgcalls.leave_group_call(chat_id)
        playing.pop(chat_id, None)
        return

    url = queues[chat_id].popleft()
    file_path = await download_audio(url)

    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(file_path)
    )

    playing[chat_id] = file_path

# ---------------------------
# Main play function
# ---------------------------
async def play_song(chat_id, url):
    queues[chat_id].append(url)

    if chat_id not in playing:
        await play_next(chat_id)

    return True

# ---------------------------
# Controls
# ---------------------------
async def skip(chat_id):
    if chat_id in playing:
        await play_next(chat_id)

async def stop(chat_id):
    queues[chat_id].clear()
    await pytgcalls.leave_group_call(chat_id)
    playing.pop(chat_id, None)

async def pause(chat_id):
    await pytgcalls.pause_stream(chat_id)

async def resume(chat_id):
    await pytgcalls.resume_stream(chat_id)

# ---------------------------
# Auto next when song ends
# ---------------------------
@pytgcalls.on_stream_end()
async def on_stream_end(_, update: StreamAudioEnded):
    await play_next(update.chat_id)
