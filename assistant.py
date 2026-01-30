from pyrogram import Client
from config import API_ID, API_HASH, SESSION

assistant = Client(
    "assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)
