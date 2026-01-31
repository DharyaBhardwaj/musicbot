from pyrogram import Client, filters
from call import start_call
import os

app = Client(
    "music",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("SESSION_STRING"),
)

@app.on_message(filters.command("play") & filters.group)
async def play(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("❌ song name do")

    song = msg.text.split(None, 1)[1]
    await start_call(app, msg.chat.id, song)
    await msg.reply(f"▶️ Playing **{song}**")

app.run()
