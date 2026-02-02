import os
import threading
import asyncio

from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

from call import play, stop

# ==============================
# ENV
# ==============================
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
STRING_SESSION = os.environ["STRING_SESSION"]

# ==============================
# BOT CLIENT (commands ke liye)
# ==============================
bot = Client(
    "music-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
)

# ==============================
# USER CLIENT (VC ke liye)
# ==============================
user = Client(
    "music-user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    in_memory=True,
)

# ==============================
# COMMANDS
# ==============================
@bot.on_message(filters.command("start"))
async def start_cmd(_, message: Message):
    await message.reply_text(
        "🎵 VC Music Bot Ready\n\n"
        "/play <song name>\n"
        "/stop",
        quote=True
    )

@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ Song name likho", quote=True)
        return

    query = " ".join(message.command[1:])
    await message.reply_text(f"⏬ Downloading: {query}", quote=True)

    try:
        await play(user, message.chat.id, query)
        await message.reply_text("▶️ Playing in VC", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error:\n{e}", quote=True)

@bot.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message: Message):
    try:
        await stop(message.chat.id)
        await message.reply_text("⏹ Stopped", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error:\n{e}", quote=True)

# ==============================
# FAKE HTTP SERVER (Render)
# ==============================
http_app = Flask(__name__)

@http_app.route("/")
def home():
    return "VC Music Bot Running"

def run_http():
    http_app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )

# ==============================
# MAIN
# ==============================
async def main():
    threading.Thread(target=run_http, daemon=True).start()
    print("✅ Fake HTTP server started")

    await user.start()
    print("✅ User client started")

    await bot.start()
    print("✅ Bot client started")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())