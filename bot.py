from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("Music bot running!")

app.run()
