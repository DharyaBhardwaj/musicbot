import aiohttp
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

# ==========================
# CONFIG
# ==========================
MUSIC_API_URL = "https://oddus-audio.vercel.app/api/download"

pytg: PyTgCalls | None = None
ACTIVE_CHATS = set()


# ==========================
# INIT VC
# ==========================
async def init_vc(app: Client):
    global pytg
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()


# ==========================
# GET AUDIO URL (DOWNLOAD API)
# ==========================
async def get_stream_url(query: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            MUSIC_API_URL,
            params={"query": query},
            timeout=aiohttp.ClientTimeout(total=30),
        ) as resp:
            if resp.status != 200:
                raise Exception("Download API HTTP error")

            data = await resp.json()

    # 🔥 REAL RESPONSE CHECK
    if not data.get("success"):
        raise Exception("Download API failed")

    audio_url = data.get("data", {}).get("download")

    if not audio_url:
        raise Exception("Download API did not return audio")

    return audio_url


# ==========================
# PLAY
# ==========================
async def play(app: Client, chat_id: int, query: str):
    await init_vc(app)

    audio_url = await get_stream_url(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(audio_url, HighQualityAudio()),
    )

    ACTIVE_CHATS.add(chat_id)


# ==========================
# STOP
# ==========================
async def stop(chat_id: int):
    if pytg and chat_id in ACTIVE_CHATS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CHATS.remove(chat_id)