import os
import threading
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler

from dotenv import load_dotenv
from pyrogram import Client, filters
from assistant import assistant

from call import (
    start_call,
    play_song,
    skip,
    stop,
    pause,
    resume,
)

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Render keep-alive
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Running")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_web, daemon=True).start()

# ---------------- COMMANDS ----------------

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("🎵 Music bot active!")

@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Song link do")

    url = message.command[1]
    await message.reply("🎵 Adding to queue...")

    await play_song(message.chat.id, url)

@app.on_message(filters.command("skip") & filters.group)
async def cmd_skip(_, message):
    await skip(message.chat.id)
    await message.reply("⏭ Skipped")

@app.on_message(filters.command("stop") & filters.group)
async def cmd_stop(_, message):
    await stop(message.chat.id)
    await message.reply("⏹ Stopped")

@app.on_message(filters.command("pause") & filters.group)
async def cmd_pause(_, message):
    await pause(message.chat.id)
    await message.reply("⏸ Paused")

@app.on_message(filters.command("resume") & filters.group)
async def cmd_resume(_, message):
    await resume(message.chat.id)
    await message.reply("▶ Resumed")

# ---------------- START ----------------

print("Starting assistant...")
assistant.start()

print("Starting call client...")
asyncio.get_event_loop().run_until_complete(start_call())

print("Starting bot...")
app.run()
