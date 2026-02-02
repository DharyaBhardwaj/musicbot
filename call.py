import os
import aiohttp
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

# ======================
# ENV
# ======================
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
STRING_SESSION = os.environ["STRING_SESSION"]

DOWNLOAD_API = os.environ.get(
    "MUSIC_API_URL",
    "https://oddus-audio.vercel.app/api/download"
)

# ======================
# ASSISTANT CLIENT
# ======================
assistant = Client(
    "assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    in_memory=True,
)

pytg = PyTgCalls(assistant)
ACTIVE_CHATS = set()

# ======================
async def start_assistant():
    if not assistant.is_connected:
        await assistant.start()
    if not pytg.is_connected:
        await pytg.start()

# ======================
async def download_song(query: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(DOWNLOAD_API, params={"query": query}) as r:
            if r.status != 200:
                raise Exception(f"Download API HTTP error: {r.status}")
            data = await r.json()

    if "file" not in data:
        raise Exception("No audio source found")

    return data["file"]

# ======================
async def play(_, chat_id: int, query: str):
    await start_assistant()

    file_path = await download_song(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(file_path),
    )

    ACTIVE_CHATS.add(chat_id)

# ======================
async def stop(chat_id: int):
    if chat_id in ACTIVE_CHATS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CHATS.remove(chat_id)