import os
from pyrogram import Client, filters
from call import play, stop

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION_STRING")

app = Client(
    "vcbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
)

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, m):
    if len(m.command) < 2:
        return await m.reply("❌ Song name do")

    await m.reply("🎵 VC joining...")
    await play(app, m.chat.id, m.text.split(None, 1)[1])


@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, m):
    await stop(m.chat.id)
    await m.reply("⏹ Stopped")

print("✅ VC Music Bot Running")
app.run()
