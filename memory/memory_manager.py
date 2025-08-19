import sqlite3
import os

class MemoryManager:
    def __init__(self, db_path="memory/collarbone_memory.db"):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Chat history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Image prompt history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS image_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                image_url TEXT,
                source TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    # ---- Chat Memory ----
    def save_message(self, role, message):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_history (role, message) VALUES (?, ?)", (role, message))
        conn.commit()
        conn.close()

    def get_chat_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT role, message, timestamp FROM chat_history ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_conversation(self, limit=10):
        """Returns the last `limit` messages in chronological order."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role, message 
            FROM chat_history 
            ORDER BY id DESC 
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return list(reversed(rows))  # so the oldest is first


    # ---- Image Memory ----
    def save_image_prompt(self, prompt, image_url, source):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO image_history (prompt, image_url, source) VALUES (?, ?, ?)",
            (prompt, image_url, source)
        )
        conn.commit()
        conn.close()

    def get_image_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT prompt, image_url, source, timestamp FROM image_history ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    # ---- Export Chat ----
    def export_chat(self, filename="chat_history.txt"):
        chat_data = self.get_chat_history()
        with open(filename, "w", encoding="utf-8") as f:
            for role, message, timestamp in chat_data:
                f.write(f"[{timestamp}] {role.upper()}: {message}\n")
        return filename
