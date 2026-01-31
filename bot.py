from pyrogram import Client, filters
from call import start_call, stop_song
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@bot.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Song name do")

    query = message.text.split(None, 1)[1]

    # 👉 यहाँ API से audio URL लाओ
    audio_url = query  # फिलहाल test के लिए direct URL

    await start_call(message.chat.id, audio_url)
    await message.reply("🎶 Playing in VC")

@bot.on_message(filters.command("stop") & filters.group)
async def stop(_, message):
    await stop_song(message.chat.id)
    await message.reply("⏹ Stopped")

bot.run()
