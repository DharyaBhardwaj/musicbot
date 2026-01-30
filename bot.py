import os
import threading
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler

from dotenv import load_dotenv
from pyrogram import Client, filters

from assistant import assistant
from call import start_call, play_song

# ---------- Load ENV ----------
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------- Bot Client ----------
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


# ---------- Commands ----------

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("🎵 Music bot running!")

@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    chat_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply(
            "❗ Song name do.\nExample: /play Believer"
        )

    song = " ".join(message.command[1:])

    try:
        # assistant auto join group
        invite = await app.export_chat_invite_link(chat_id)
        await assistant.join_chat(invite)
    except Exception as e:
        print("Join error:", e)

    await message.reply(
        f"🎵 Requested: {song}\n\nJoining VC & starting music..."
    )

    try:
        # VC join + play song
        await play_song(chat_id, song)
    except Exception as e:
        print("Play error:", e)
        await message.reply("❌ VC join ya play failed.")


# ---------- Start Clients ----------
print("Starting assistant...")
assistant.start()

print("Starting call client...")
asyncio.get_event_loop().run_until_complete(start_call())

print("Starting bot...")
app.run()
