import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from dotenv import load_dotenv
from pyrogram import Client, filters
from assistant import assistant

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

# ---------- Render Web Server ----------
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
# ----------------------------------------

# Start command
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("🎵 Music bot running!")

# Play command
@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    chat_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply("❗ Song name do.\nExample: /play Believer")

    song = " ".join(message.command[1:])

    try:
        # assistant auto join group
        await assistant.join_chat(chat_id)
    except Exception:
        pass

    await message.reply(
        f"🎵 Requested: {song}\n\nAssistant joining voice chat..."
    )

print("Starting assistant...")
assistant.start()

print("Starting bot...")
app.run()
