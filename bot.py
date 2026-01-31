from pyrogram import Client, filters
from pyrogram.types import Message
import os
import asyncio

from call import get_stream_url

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Song ka naam ya link do")

    query = message.text.split(None, 1)[1]

    url = await get_stream_url(query)

    # 👇 Telegram VC direct stream
    await app.send_message(
        message.chat.id,
        f"🎵 STREAM URL READY\n{url}"
    )

print("✅ BOT RUNNING (API STREAM MODE)")
app.run()
