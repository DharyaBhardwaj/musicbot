import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask

from call import start_call, stop_song

# =========================
# ENV
# =========================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# =========================
# Pyrogram Client
# =========================
app = Client(
    "vc_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# =========================
# Flask (Render keep-alive)
# =========================
web = Flask(__name__)

@web.route("/")
def home():
    return "VC Music Bot Running"

def run_web():
    web.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

# =========================
# Telegram Commands
# =========================
@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Song name do\n\nExample:\n/play kesariya"
        )

    query = message.text.split(None, 1)[1]

    try:
        await start_call(app, message, query)
    except Exception as e:
        await message.reply_text(f"⚠️ Error:\n`{e}`")


@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message: Message):
    try:
        await stop_song(message.chat.id)
        await message.reply_text("⏹ Stopped")
    except:
        await message.reply_text("❌ Nothing playing")


# =========================
# START
# =========================
async def main():
    await app.start()
    print("✅ API VC Music Bot Started")
    await app.idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    run_web()
