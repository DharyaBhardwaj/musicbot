from pyrogram import Client, filters
from pyrogram.types import Message
import os

from call import start_call, play_song

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Song name ya YouTube link do")

    query = message.text.split(None, 1)[1]
    await start_call(app, message, query)

@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message: Message):
    await play_song.stop(message.chat.id)

print("✅ Bot started")

app.run()
