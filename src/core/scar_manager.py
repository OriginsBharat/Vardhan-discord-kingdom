import sqlite3
from src.core.personas import persona_manager

class ScarManager:
    def __init__(self, db_path="data/world_data.db"):
        self.db_path = db_path
        self._initialize_db()
        print("ScarManager initialized with persistent database.")

    def _get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS psychological_scars (
                    bot_name TEXT NOT NULL,
                    scar_name TEXT NOT NULL,
                    scar_description TEXT NOT NULL,
                    PRIMARY KEY (bot_name, scar_name)
                )
            """)
            conn.commit()

    def inflict_scar(self, target_bot_name, scar_name, scar_description):
        """Inflicts a permanent psychological scar on a bot by saving it to the database."""
        persona = persona_manager.get_persona(target_bot_name)
        if not persona:
            print(f"Error: Could not find persona for {target_bot_name} to inflict scar.")
            return

        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO psychological_scars (bot_name, scar_name, scar_description) VALUES (?, ?, ?)",
                (target_bot_name, scar_name, scar_description)
            )
            conn.commit()

        # Also update the in-memory persona immediately
        self.apply_scar_to_persona(persona, scar_name, scar_description)
        print(f"Persistently inflicted scar '{scar_name}' on {target_bot_name}.")

    def get_scars_for_bot(self, bot_name):
        """Retrieves all scars for a specific bot from the database."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT scar_name, scar_description FROM psychological_scars WHERE bot_name=?", (bot_name,))
            return [{"name": name, "description": desc} for name, desc in cursor.fetchall()]

    def apply_scar_to_persona(self, persona, scar_name, scar_description):
        """Applies a scar to the in-memory persona object."""
        scar = {"name": scar_name, "description": scar_description}
        # Avoid duplicate application on hot-reload or initial load
        if not any(s['name'] == scar_name for s in persona.psychological_scars):
            persona.psychological_scars.append(scar)
            persona.base_persona += f"\\n\\n**Psychological Scar: {scar_name}** - {scar_description}"
            print(f"Applied scar '{scar_name}' to {persona.name}'s in-memory persona.")

# A single instance for the application
scar_manager = ScarManager()
