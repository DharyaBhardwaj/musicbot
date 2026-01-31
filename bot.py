import os
from pyrogram import Client, filters
from call import play, stop

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message):
    if len(message.command) < 2:
        await message.reply("❌ Song name likho")
        return

    query = message.text.split(None, 1)[1]
    await play(app, message.chat.id, query)

@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message):
    await stop(message.chat.id)

print("✅ VC Music Bot Started (API MODE)")
app.run()
