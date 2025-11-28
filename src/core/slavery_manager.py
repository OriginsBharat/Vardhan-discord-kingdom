import sqlite3

class SlaveryManager:
    def __init__(self, db_path="data/world_data.db"):
        self.db_path = db_path
        self._initialize_db()
        print("SlaveryManager initialized.")

    def _get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS slavery_records (
                    slave_name TEXT PRIMARY KEY,
                    owner_id TEXT NOT NULL
                )
            """)
            conn.commit()

    def enslave_bot(self, slave_name, owner_id):
        """Creates a permanent record of a bot's enslavement."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO slavery_records (slave_name, owner_id) VALUES (?, ?)",
                (slave_name, str(owner_id))
            )
            conn.commit()
        print(f"Slavery record created: {slave_name} is now owned by {owner_id}.")

    def free_bot(self, slave_name):
        """Removes a bot's enslavement record."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM slavery_records WHERE slave_name = ?", (slave_name,))
            conn.commit()
        print(f"Slavery record removed: {slave_name} is now free.")

    def get_owner(self, slave_name):
        """Finds the owner of a specific slave."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT owner_id FROM slavery_records WHERE slave_name = ?", (slave_name,))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_slaves(self, owner_id):
        """Finds all slaves owned by a specific user."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT slave_name FROM slavery_records WHERE owner_id = ?", (str(owner_id),))
            return [row[0] for row in cursor.fetchall()]

    def is_enslaved(self, bot_name):
        """Checks if a bot is currently enslaved."""
        return self.get_owner(bot_name) is not None

    def transfer_ownership(self, slave_name, new_owner_id):
        """Transfers a slave from one owner to another."""
        if not self.is_enslaved(slave_name):
            return False
        self.enslave_bot(slave_name, new_owner_id)
        print(f"Ownership of {slave_name} transferred to {new_owner_id}.")
        return True

# Singleton instance
slavery_manager = SlaveryManager()
