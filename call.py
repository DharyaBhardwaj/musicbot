import aiohttp

# 👇 TUMHARI WORKING API
API_BASE = "https://oddus-audio.vercel.app/api/stream"
API_KEY = "oddus-wiz777"

async def get_stream_url(query: str) -> str:
    params = {
        "q": query,
        "key": API_KEY
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(API_BASE, params=params) as r:
            data = await r.json()
            return data["url"]   # <-- direct audio stream URL
