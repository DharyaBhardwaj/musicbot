import aiohttp
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

pytg = None

ODDUS_API = "https://oddus-audio.vercel.app/api/stream"

async def get_stream_url(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(ODDUS_API, params={"q": query}) as r:
            data = await r.json()

            # API returns direct audio URL
            if "audio" not in data:
                raise Exception("API did not return audio stream")

            return data["audio"], data.get("title", query)


async def start_call(app, chat_id: int, query: str):
    global pytg

    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()

    stream_url, title = await get_stream_url(query)

    await pytg.join_group_call(
        chat_id,
        AudioPiped(stream_url),
    )

    await app.send_message(chat_id, f"🎵 Playing: **{title}**")
