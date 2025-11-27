import sqlite3
from src.core.personas import persona_manager

class RelationshipManager:
    def __init__(self, db_path="data/world_data.db"):
        self.db_path = db_path
        self._initialize_db()

    def _get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bot_relationships (
                    source_bot TEXT NOT NULL,
                    target_bot TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    PRIMARY KEY (source_bot, target_bot)
                )
            """)
            # Initialize relationships for all bot pairs
            all_bots = list(persona_manager.personas.keys())
            for source_bot in all_bots:
                for target_bot in all_bots:
                    if source_bot != target_bot:
                        cursor.execute(
                            "INSERT OR IGNORE INTO bot_relationships (source_bot, target_bot, score) VALUES (?, ?, 0)",
                            (source_bot, target_bot)
                        )
            conn.commit()
        print("RelationshipManager initialized and database is ready.")

    def get_relationship_score(self, source_bot, target_bot):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT score FROM bot_relationships WHERE source_bot = ? AND target_bot = ?",
                (source_bot, target_bot)
            )
            result = cursor.fetchone()
            return result[0] if result else 0

    def adjust_relationship_score(self, source_bot, target_bot, adjustment):
        current_score = self.get_relationship_score(source_bot, target_bot)
        new_score = max(-100, min(100, current_score + adjustment))
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE bot_relationships SET score = ? WHERE source_bot = ? AND target_bot = ?",
                (new_score, source_bot, target_bot)
            )
            conn.commit()
        print(f"Relationship from {source_bot} to {target_bot} adjusted to {new_score}.")

# Singleton instance
relationship_manager = RelationshipManager()
