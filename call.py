import aiohttp

ODDUS_SEARCH = "https://oddus-audio.vercel.app/api/search"

async def start_call(message, query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(ODDUS_SEARCH, params={"q": query}) as resp:
            if resp.status != 200:
                return await message.reply_text("❌ API error")

            data = await resp.json()

    # API response safety
    if not data or "audio" not in data:
        return await message.reply_text("❌ Song nahi mila")

    audio_url = data["audio"]

    # Telegram VC streaming requires pytgcalls/node
    # BUT since you explicitly want API stream only,
    # we send playable stream link for VC-compatible bots
    await message.reply_text(
        f"🎵 **Found:** {query}\n\n"
        f"🔊 Stream URL:\n{audio_url}"
    )
