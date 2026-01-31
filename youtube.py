import aiohttp

API = "https://oddus-audio.vercel.app/api/search"

async def get_stream_url(song_name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(API, params={"q": song_name}) as r:
            data = await r.json()

    if not data or "stream" not in data:
        raise Exception("Song not found")

    return data["stream"]  # direct audio stream url
