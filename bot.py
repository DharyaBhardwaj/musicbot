import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from pyrogram import Client, filters
from pyrogram.types import Message

from call import start_call

# =========================
# 🔹 FAKE HTTP SERVER (Render ke liye)
# =========================
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start_http_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), HealthHandler).serve_forever()

threading.Thread(target=start_http_server, daemon=True).start()

print("✅ Fake HTTP server started")

# =========================
# 🔹 TELEGRAM BOT CONFIG
# =========================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# =========================
# 🔹 COMMANDS
# =========================
@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Song name do")

    query = message.text.split(None, 1)[1]
    await start_call(app, message, query)

@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message: Message):
    await message.reply("⏹ Stop command received")

print("✅ Telegram bot started")
app.run()
