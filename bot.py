from youtubesearchpython.__future__ import VideosSearch


@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Song name ya YouTube link do")

    query = " ".join(message.command[1:])

    # If not a URL → search YouTube
    if "youtube.com" not in query and "youtu.be" not in query:
        await message.reply("🔎 Searching song...")
        search = await VideosSearch(query, limit=1).next()
        results = search.get("result", [])

        if not results:
            return await message.reply("❌ Song nahi mila")

        url = results[0]["link"]
    else:
        url = query

    await message.reply("🎵 Joining VC & playing...")

    ok = await play_song(message.chat.id, url)

    if not ok:
        await message.reply("❌ VC play failed")
