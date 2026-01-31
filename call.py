from pyrogram import Client
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.raw.functions.phone import JoinGroupCall
from pyrogram.raw.types import InputPeerChannel
from youtube import get_stream_url
import asyncio

active_calls = {}

async def start_call(app: Client, chat_id: int, song: str):
    if chat_id in active_calls:
        return

    url = await get_stream_url(song)

    peer = await app.resolve_peer(chat_id)

    call = await app.invoke(
        CreateGroupCall(
            peer=peer,
            random_id=app.rnd_id(),
        )
    )

    await app.invoke(
        JoinGroupCall(
            call=call.call,
            join_as=peer,
            muted=False,
            video_stopped=True,
            invite_hash=None,
        )
    )

    active_calls[chat_id] = url
