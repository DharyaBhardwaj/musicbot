from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

from youtube import download_audio

pytg = None
ACTIVE_CALLS = set()

async def play_song(app, message: Message, query: str):
    global pytg

    chat_id = message.chat.id

    # 🔹 Init PyTgCalls ONLY when needed
    if pytg is None:
        pytg = PyTgCalls(app)
        await pytg.start()

    if chat_id in ACTIVE_CALLS:
        return await message.reply("⚠️ VC already playing here")

    await message.reply("🔎 Searching song...")

    audio_path, title = await download_audio(query)

    if not audio_path:
        return await message.reply("❌ Song nahi mila")

    try:
        await pytg.join_group_call(
            chat_id,
            AudioPiped(audio_path),
        )
        ACTIVE_CALLS.add(chat_id)
        await message.reply(f"🎶 Playing: **{title}**")
    except Exception as e:
        await message.reply(f"❌ VC Error:\n`{e}`")

async def stop_song(chat_id: int):
    if pytg and chat_id in ACTIVE_CALLS:
        await pytg.leave_group_call(chat_id)
        ACTIVE_CALLS.remove(chat_id)
