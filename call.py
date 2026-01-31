import aiohttp
import os
from pyrogram.types import Message

ODDUS_API = "https://oddus-audio.vercel.app/api/download"
ODDUS_KEY = "oddus-wiz777"

class Player:
    async def stop(self, chat_id: int):
        # simple placeholder (no vc state handling)
        return

play_song = Player()

async def start_call(app, message: Message, query: str):
    await message.reply("🔎 Searching & downloading...")

    params = {"url": query}
    headers = {"x-api-key": ODDUS_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(ODDUS_API, params=params, headers=headers) as resp:
            if resp.status != 200:
                return await message.reply("❌ API error")

            file_path = "song.mp3"
            with open(file_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 64):
                    f.write(chunk)

    await app.send_audio(
        chat_id=message.chat.id,
        audio=file_path,
        caption="▶️ Playing via API",
    )

    try:
        os.remove(file_path)
    except:
        pass
