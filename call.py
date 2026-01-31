from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

from youtube import download_audio

pytg = PyTgCalls(None)

ACTIVE_CALLS = {}

async def play_song(app, message: Message, query: str):
    chat_id = message.chat.id

    if chat_id not in ACTIVE_CALLS:
        await pytg.start(app)
        ACTIVE_CALLS[chat_id] = True

    await message.reply("🔎 Searching & downloading...")

    audio_path, title = await download_audio(query)

    if not audio_path:
        return await message.reply("❌ Song nahi mila")

    try:
        await pytg.join_group_call(
            chat_id,
            AudioPiped(audio_path),
        )
        await message.reply(f"🎶 Playing: **{title}**")
    except Exception as e:
        await message.reply(f"❌ VC Error: {e}")

async def stop_song(chat_id: int):
    if chat_id in ACTIVE_CALLS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CALLS.pop(chat_id, None)
