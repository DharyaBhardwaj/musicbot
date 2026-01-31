import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from dotenv import load_dotenv
from pyrogram import Client, filters

from assistant import assistant
from call import start_call, play_song
from queue import add_song

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

# -----------------------------
# Render keep-alive web server
# -----------------------------
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_web).start()

# -----------------------------
# PLAY COMMAND
# -----------------------------
@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Song name ya YouTube link do")

    query = " ".join(message.command[1:])
    chat_id = message.chat.id

    add_song(chat_id, query)

    await message.reply(
        f"➕ Added to queue:\n{query}\n\n🎵 Playing..."
    )

    ok = await play_song(chat_id, query)

    if not ok:
        await message.reply("❌ VC play failed")

# -----------------------------
# START BOT
# -----------------------------
async def main():
    print("Starting assistant...")
    await assistant.start()

    print("Starting call client...")
    await start_call()

    print("Starting bot...")
    await app.start()

    await idle()

from pyrogram import idle

asyncio.get_event_loop().run_until_complete(main())
