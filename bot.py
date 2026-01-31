import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from pyrogram import Client, filters
from call import play, stop

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.environ["SESSION_STRING"]

# --------------------
# 🔹 Dummy HTTP Server
# --------------------
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# --------------------
# 🔹 Telegram Client
# --------------------
app = Client(
    "vc-music-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
)

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message):
    if len(message.command) < 2:
        return await message.reply("Song name likho")
    query = " ".join(message.command[1:])
    await play(app, message.chat.id, query)
    await message.reply(f"🎵 Playing: {query}")

@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message):
    await stop(message.chat.id)
    await message.reply("⏹ Stopped")

print("✅ Bot started")
app.run()
