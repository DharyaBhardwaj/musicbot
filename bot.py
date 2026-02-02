import os
import threading

from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

from call import play, stop

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = Client(
    "music-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
)

@bot.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply_text(
        "🎵 VC Music Bot Ready\n\n"
        "/play <song name>\n"
        "/stop"
    )

@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(client: Client, m: Message):
    if len(m.command) < 2:
        await m.reply_text("❌ Song name likho")
        return

    query = " ".join(m.command[1:])
    await m.reply_text(f"⏬ Downloading: {query}")

    try:
        await play(m.chat.id, query)
        await m.reply_text("▶️ Playing in VC")
    except Exception as e:
        await m.reply_text(f"❌ Error:\n{e}")

@bot.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, m: Message):
    try:
        await stop(m.chat.id)
        await m.reply_text("⏹ Stopped")
    except Exception as e:
        await m.reply_text(f"❌ Error:\n{e}")

# ---- fake HTTP for Render ----
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot running"

def run_http():
    app.run("0.0.0.0", int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    threading.Thread(target=run_http, daemon=True).start()
    bot.run()