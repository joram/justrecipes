import os
import sqlite3

_queue_manager = None


def get_queue_manager():
    global _queue_manager
    if _queue_manager is None:
        _queue_manager = QueueManager()
    return _queue_manager


class QueueManager:

    def __init__(self):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        self.conn = sqlite3.connect(f"{curr_dir}/queue.db")
        # self.conn = sqlite3.connect("queue.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS queue (url TEXT PRIMARY KEY, visited INT DEFAULT 0)")
        self.conn.commit()

    def add_urls_to_visit(self, urls):
        for url in urls:
            url = url.split("?")[0]
            # verify that url is not already in the queue
            self.cursor.execute("SELECT * FROM queue WHERE url=?", (url,))
            if self.cursor.fetchone() is None:
                self.cursor.execute("INSERT INTO queue VALUES (?, 0)", (url,))
        self.conn.commit()

    def get_urls_to_visit(self, n):
        self.cursor.execute("SELECT * FROM queue WHERE visited=0  LIMIT ? ", (n,))
        return [row[0] for row in self.cursor.fetchall()]

    def mark_url_visited(self, url):
        self.cursor.execute("UPDATE queue SET visited=1 WHERE url=?", (url,))
        self.conn.commit()