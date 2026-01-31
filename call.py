import aiohttp, os, uuid
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pyrogram import Client

pytgcalls = None

API_ENDPOINT = "https://YOUR_API_ENDPOINT/download"  # ← वही API जो सुबह थी

async def get_audio_file(query: str) -> str:
    filename = f"/tmp/{uuid.uuid4()}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(API_ENDPOINT, params={"q": query}) as r:
            if r.status != 200:
                raise Exception("API failed")
            with open(filename, "wb") as f:
                f.write(await r.read())
    return filename

async def start_call(app: Client, message, query: str):
    global pytgcalls
    if not pytgcalls:
        pytgcalls = PyTgCalls(app)
        await pytgcalls.start()

    audio_file = await get_audio_file(query)

    await pytgcalls.join_group_call(
        message.chat.id,
        AudioPiped(audio_file),
    )
