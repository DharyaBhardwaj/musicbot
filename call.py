import aiohttp
from youtube import search_youtube

ODDUS_API = "https://oddus-audio.vercel.app/api/download"

async def get_stream_url(song_name: str):
    yt_url = await search_youtube(song_name)

    async with aiohttp.ClientSession() as session:
        async with session.get(ODDUS_API, params={"url": yt_url}) as r:
            if r.status != 200:
                raise Exception("Oddus failed")

            # Oddus returns audio stream directly
            return str(r.url)
