import aiohttp
import re

YOUTUBE_SEARCH_API = "https://ytsearch-api.vercel.app/api/search"

async def search_youtube(query: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            YOUTUBE_SEARCH_API,
            params={"query": query, "limit": 1},
            timeout=15
        ) as resp:
            data = await resp.json()

    if not data or "results" not in data or not data["results"]:
        raise Exception("No results found")

    return data["results"][0]["url"]


def is_youtube_url(text: str) -> bool:
    return bool(re.search(r"(youtube\.com|youtu\.be)", text))
