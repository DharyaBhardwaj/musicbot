# ==============================
# Render keep-alive (IMPORTANT)
# ==============================
from flask import Flask
import threading

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "API VC Music Bot Running"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask, daemon=True).start()

# ==============================
# Telegram Bot
# ==============================
import os
from pyrogram import Client, filters
from pyrogram.types import Message

from call import play_song, stop_song   # <-- call.py se aayega

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# ==============================
# Commands
# ==============================
@app.on_message(filters.command("start"))
async def start_cmd(_, message: Message):
    await message.reply_text(
        "🎵 **API VC Music Bot Running**\n\n"
        "Use:\n"
        "`/play song name`\n"
        "`/stop`",
        quote=True,
    )

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Song name do")

    query = message.text.split(None, 1)[1]

    await message.reply_text("🎶 Searching & Playing...")
    try:
        await play_song(app, message.chat.id, query)
    except Exception as e:
        await message.reply_text(f"❌ Error:\n`{e}`")

@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message: Message):
    await stop_song(message.chat.id)
    await message.reply_text("⏹️ Stopped")

# ==============================
# Run Bot
# ==============================
print("✅ API VC Music Bot Started")
app.run()
