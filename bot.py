import os
import asyncio
from pyrogram import Client, filters
from call import play_song, stop_song

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("STRING_SESSION")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    session_string=SESSION
)

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Song name do")

    query = " ".join(message.command[1:])
    await play_song(app, message.chat.id, query)
    await message.reply(f"▶️ Playing: **{query}**")

@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message):
    await stop_song(message.chat.id)
    await message.reply("⏹ Stopped")

async def main():
    await app.start()
    print("✅ Bot started")
    await asyncio.Event().wait()

asyncio.run(main())
