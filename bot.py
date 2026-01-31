import os
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

from call import get_stream_url

# =====================
# Telegram credentials
# =====================
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

# =====================
# Telegram Bot
# =====================
app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Song ka naam ya link do")

    query = message.text.split(None, 1)[1]

    url = await get_stream_url(query)

    await message.reply(
        f"🎵 **DIRECT STREAM URL**\n\n{url}"
    )

# =====================
# Flask server (ONLY for Render port scan)
# =====================
web = Flask(__name__)

@web.route("/")
def home():
    return "Music bot is running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

# =====================
# Start both
# =====================
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("✅ Flask server started")
    print("✅ Telegram bot started (API STREAM MODE)")
    app.run()
