import sqlite3
from src.config import config

class EconomyManager:
    def __init__(self, db_path="data/world_data.db"):
        self.db_path = db_path
        self._initialize_db()
        print("EconomyManager initialized with persistent database.")

    def _get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    user_id TEXT PRIMARY KEY,
                    balance REAL NOT NULL
                )
            """)
            conn.commit()

    def get_balance(self, user_id):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE user_id=?", (str(user_id),))
            result = cursor.fetchone()
            return result[0] if result else 0

    def _set_balance(self, user_id, balance):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO accounts (user_id, balance) VALUES (?, ?)", (str(user_id), balance))
            conn.commit()

    def deposit(self, user_id, amount):
        if amount < 0:
            raise ValueError("Cannot deposit a negative amount.")
        current_balance = self.get_balance(user_id)
        self._set_balance(user_id, current_balance + amount)
        print(f"Deposited {amount} Rs into account {user_id}.")

    def withdraw(self, user_id, amount):
        if user_id == config.master_user_id:
            return True

        if amount < 0:
            raise ValueError("Cannot withdraw a negative amount.")
        current_balance = self.get_balance(user_id)
        if current_balance < amount:
            return False
        self._set_balance(user_id, current_balance - amount)
        print(f"Withdrew {amount} Rs from account {user_id}.")
        return True

    def transfer(self, from_user_id, to_user_id, amount):
        if str(from_user_id) == str(config.master_user_id):
            self.deposit(to_user_id, amount)
            print(f"Master transferred {amount} Rs to {to_user_id}.")
            return True

        # Use a transaction for safety
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                from_balance = self.get_balance(from_user_id)
                if from_balance < amount:
                    return False

                to_balance = self.get_balance(to_user_id)

                cursor.execute("UPDATE accounts SET balance=? WHERE user_id=?", (from_balance - amount, str(from_user_id)))
                cursor.execute("UPDATE accounts SET balance=? WHERE user_id=?", (to_balance + amount, str(to_user_id)))

                conn.commit()
                print(f"Transferred {amount} Rs from {from_user_id} to {to_user_id}.")
                return True
            except Exception as e:
                conn.rollback()
                print(f"Transaction failed: {e}")
                return False

economy_manager = EconomyManager()
