from collections import defaultdict

# queue per group
queues = defaultdict(list)

def add_song(chat_id, song):
    queues[chat_id].append(song)

def get_next(chat_id):
    if queues[chat_id]:
        return queues[chat_id].pop(0)
    return None

def clear_queue(chat_id):
    queues[chat_id] = []
