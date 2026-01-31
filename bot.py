from pyrogram import Client, filters
from pyrogram.types import Message
import os
from dotenv import load_dotenv

from call import play_song, stop_song

load_dotenv()

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
        return await message.reply("❌ Song name do")

    query = message.text.split(None, 1)[1]
    await play_song(app, message, query)

@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message: Message):
    await stop_song(message.chat.id)
    await message.reply("⏹️ Stopped")

print("✅ VC Music Bot Started")

app.run()
