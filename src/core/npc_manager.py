import sqlite3
import json

class NPCManager:
    def __init__(self, db_path="data/world_data.db"):
        self.db_path = db_path
        self._initialize_db()
        self._load_initial_npcs()
        print("NPCManager initialized.")

    def _get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS npcs (
                    npc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    persona TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'available' -- available, busy
                )
            """)
            conn.commit()

    def _load_initial_npcs(self):
        # In a real scenario, these would be more dynamic.
        # For now, we define a few NPCs to populate the brothel.
        initial_npcs = {
            "Liliana": "A shy, innocent-looking girl with a surprising wild side. She craves gentle praise and affection.",
            "Seraphina": "A proud, fiery woman with a sharp tongue. She respects those who can match her wit and dominate her spirit.",
            "Isolde": "A melancholic and beautiful soul who seems distant. She is drawn to deep, philosophical conversations and a sense of emotional connection.",
        }
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            for name, persona in initial_npcs.items():
                cursor.execute(
                    "INSERT OR IGNORE INTO npcs (name, persona) VALUES (?, ?)",
                    (name, persona)
                )
            conn.commit()

    def get_available_npcs(self):
        with self._get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM npcs WHERE status = 'available'")
            return [dict(row) for row in cursor.fetchall()]

    def get_npc_by_name(self, name):
        with self._get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM npcs WHERE name = ?", (name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def set_npc_status(self, name, status):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE npcs SET status = ? WHERE name = ?",
                (status, name)
            )
            conn.commit()

# Singleton instance
npc_manager = NPCManager()
