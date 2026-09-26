
import sqlite3

from app.config import DATABASE_PATH, MAX_HISTORY


class Memory:

    def __init__(self):
        self.path = DATABASE_PATH
        self.initialize()

    def connect(self):
        return sqlite3.connect(self.path)

    def initialize(self):
        with self.connect() as db:

            db.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            db.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save_exchange(self, user_message, ai_response):
        with self.connect() as db:

            db.execute(
                "INSERT INTO conversations (role, content) VALUES (?, ?)",
                ("user", user_message)
            )

            db.execute(
                "INSERT INTO conversations (role, content) VALUES (?, ?)",
                ("assistant", ai_response)
            )

    def get_history(self):
        with self.connect() as db:

            rows = db.execute("""
                SELECT role, content
                FROM conversations
                ORDER BY id DESC
                LIMIT ?
            """, (MAX_HISTORY,)).fetchall()

        rows.reverse()

        return [
            {"role": role, "content": content}
            for role, content in rows
        ]

    def remember(self, fact):
        fact = fact.strip()

        if not fact:
            return

        with self.connect() as db:
            db.execute(
                "INSERT INTO facts (content) VALUES (?)",
                (fact,)
            )

    def get_facts(self):
        with self.connect() as db:

            rows = db.execute("""
                SELECT content
                FROM facts
                ORDER BY id DESC
                LIMIT 20
            """).fetchall()

        return [row[0] for row in rows]
