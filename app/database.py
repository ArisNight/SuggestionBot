import sqlite3
from pathlib import Path
import os
from app.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'data' / 'suggestions.db'

class Database:
    def __init__(self):
        os.makedirs(BASE_DIR / 'data', exist_ok=True)
        self.conn = self._create_connection()
        self._init_db()

    def _create_connection(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            logger.error(f"DB connection error: {e}")
            raise

    def _init_db(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suggestions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_msg_id INTEGER NOT NULL,
                    moderated_msg_id INTEGER NOT NULL UNIQUE,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    text TEXT NOT NULL,
                    media_type TEXT DEFAULT 'text',
                    media_id TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except Exception as e:
            logger.error(f"DB init error: {e}")
            raise

    def add_suggestion(self, original_msg_id, moderated_msg_id, user_id, username, text, media_type='text', media_id=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO suggestions 
                (original_msg_id, moderated_msg_id, user_id, username, text, media_type, media_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (original_msg_id, moderated_msg_id, user_id, username, text, media_type, media_id))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Add suggestion error: {e}")
            return None

    def get_suggestion(self, moderated_msg_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM suggestions WHERE moderated_msg_id = ?", (moderated_msg_id,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Get suggestion error: {e}")
            return None

    def update_status(self, moderated_msg_id, status):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE suggestions 
                SET status = ? 
                WHERE moderated_msg_id = ? AND status = 'pending'
            """, (status, moderated_msg_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Update status error: {e}")
            return False

    def close(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.error(f"DB close error: {e}")

db = Database()