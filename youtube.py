from youtubesearchpython import VideosSearch

async def search_youtube(query: str):
    search = VideosSearch(query, limit=1)
    result = search.result()

    if not result["result"]:
        raise Exception("Song not found")

    return result["result"][0]["link"]
