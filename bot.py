from pyrogram import Client, filters
from pyrogram.types import Message
import os

from call import start_call

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
async def play(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Song name likho")

    query = message.text.split(None, 1)[1]
    await start_call(app, message.chat.id, query)

print("✅ API VC Music Bot Started")
app.run()
