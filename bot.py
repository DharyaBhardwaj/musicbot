from pyrogram import Client, filters
from pyrogram.types import Message
import os
from dotenv import load_dotenv

from call import init_call, play_song, stop_song

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
        return await message.reply("❌ YouTube link do")

    link = message.text.split(None, 1)[1]

    await init_call(app)
    await play_song(message.chat.id, link)

    await message.reply("▶️ Playing via API")


@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message: Message):
    await stop_song(message.chat.id)
    await message.reply("⏹ Stopped")


print("✅ Music Bot Started")
app.run()
