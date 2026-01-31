import asyncio

class QueueManager:
    def __init__(self):
        # chat_id -> song queue
        self.queues = {}

        # chat_id -> currently playing
        self.current = {}

    def add_song(self, chat_id, song):
        if chat_id not in self.queues:
            self.queues[chat_id] = []

        self.queues[chat_id].append(song)

    def get_next(self, chat_id):
        if chat_id not in self.queues:
            return None

        if not self.queues[chat_id]:
            return None

        song = self.queues[chat_id].pop(0)
        self.current[chat_id] = song
        return song

    def get_queue(self, chat_id):
        return self.queues.get(chat_id, [])

    def clear(self, chat_id):
        self.queues[chat_id] = []
        self.current.pop(chat_id, None)

    def has_queue(self, chat_id):
        return bool(self.queues.get(chat_id))
        

queue_manager = QueueManager()
