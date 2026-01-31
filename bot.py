from pyrogram import Client, filters
from pyrogram.types import Message
import os
from call import start_call

app = Client(
    "musicbot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
)

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Song name ya link do")

    query = message.text.split(None, 1)[1]
    await start_call(app, message, query)

print("✅ Bot started (API → TEMP → VC)")
app.run()
