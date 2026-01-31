import asyncio

from pytgcalls import PyTgCalls

# 🔁 version-safe import
try:
    from pytgcalls.types.stream import AudioPiped
except Exception:
    from pytgcalls.types.input_stream import AudioPiped

pytgcalls = None

async def start_call(app, message, query):
    global pytgcalls

    if pytgcalls is None:
        pytgcalls = PyTgCalls(app)
        await pytgcalls.start()

    chat_id = message.chat.id

    try:
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(query),
        )
        await message.reply(f"▶️ Playing: {query}")

    except Exception as e:
        await message.reply(f"❌ VC ERROR:\n{e}")

class play_song:
    @staticmethod
    async def stop(chat_id: int):
        try:
            await pytgcalls.leave_group_call(chat_id)
        except:
            pass
