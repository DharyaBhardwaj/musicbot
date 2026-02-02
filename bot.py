import os
import threading
import asyncio

from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

from call import play, stop


# ======================
# ENV
# ======================
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]


# ======================
# BOT CLIENT (COMMANDS)
# ======================
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
    no_memory=True
)


@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text(
        "🎵 VC Music Bot Ready\n\n"
        "/play <song name>\n"
        "/stop"
    )


@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ Song name likho")
        return

    song = " ".join(message.command[1:])
    await message.reply_text(f"⏬ Downloading: {song}")

    try:
        await play(message.chat.id, song)
        await message.reply_text("▶️ Playing in VC")
    except Exception as e:
        await message.reply_text(f"❌ Error:\n{e}")


@bot.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message: Message):
    try:
        await stop(message.chat.id)
        await message.reply_text("⏹ Stopped")
    except Exception as e:
        await message.reply_text(f"❌ Error:\n{e}")


# ======================
# FAKE HTTP (RENDER)
# ======================
http_app = Flask(__name__)

@http_app.route("/")
def home():
    return "VC Music Bot Running"


def run_http():
    http_app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    threading.Thread(target=run_http, daemon=True).start()
    print("✅ HTTP server started")
    bot.run()