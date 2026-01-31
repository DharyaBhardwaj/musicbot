import os
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv

from call import start_call, play_song

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
async def play_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Song name ya YouTube link do")

    query = message.text.split(None, 1)[1]

    await message.reply("🎵 Joining VC & playing...")
    await start_call(client)
    await play_song(client, message.chat.id, query)


@app.on_message(filters.command("stop") & filters.group)
async def stop_handler(_, message: Message):
    from call import pytgcalls
    if pytgcalls:
        await pytgcalls.leave_group_call(message.chat.id)
        await message.reply("🛑 Stopped")


print("✅ Music bot started")
app.run()
