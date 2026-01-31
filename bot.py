import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import asyncio

from dotenv import load_dotenv
from pyrogram import Client, filters

from assistant import assistant
from call import start_call, play_song

# ------------------ ENV ------------------
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ------------------ BOT CLIENT ------------------
app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ------------------ WEB SERVER (Render keep alive) ------------------
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Music Bot Running")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_web, daemon=True).start()

# ------------------ COMMANDS ------------------

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("🎵 Music bot running!")

@app.on_message(filters.command("play") & filters.group)
async def play(_, message):

    if len(message.command) < 2:
        return await message.reply("❌ YouTube link do")

    url = message.command[1]

    # assistant auto join group
    try:
        invite = await app.export_chat_invite_link(message.chat.id)
        await assistant.join_chat(invite)
    except:
        pass  # already joined

    await message.reply("🎵 Joining VC & playing...")

    ok = await play_song(message.chat.id, url)

    if not ok:
        await message.reply("❌ VC join ya play failed")

# ------------------ START ------------------

print("Starting assistant...")
assistant.start()

print("Starting call client...")
asyncio.get_event_loop().run_until_complete(start_call())

print("Starting bot...")
app.run()
