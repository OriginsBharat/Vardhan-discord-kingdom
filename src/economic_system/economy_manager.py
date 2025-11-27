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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS market_data (
                    item_type TEXT PRIMARY KEY,
                    transactions_last_cycle INTEGER NOT NULL,
                    base_price REAL NOT NULL
                )
            """)
            # Initialize some basic item types
            cursor.execute("INSERT OR IGNORE INTO market_data (item_type, transactions_last_cycle, base_price) VALUES ('artwork', 0, 500)")
            cursor.execute("INSERT OR IGNORE INTO market_data (item_type, transactions_last_cycle, base_price) VALUES ('healing_potion', 0, 50)")
            cursor.execute("INSERT OR IGNORE INTO market_data (item_type, transactions_last_cycle, base_price) VALUES ('custom_weapon', 0, 1500)")
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

    def get_market_price(self, item_type):
        """Calculates the current market price of an item based on recent transactions."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT transactions_last_cycle, base_price FROM market_data WHERE item_type=?", (item_type,))
            result = cursor.fetchone()
            if not result:
                return 100 # Default price for unknown items

            transactions, base_price = result

            # Simple supply/demand logic: price decreases as more items are sold
            # A transaction count of 0-5 is "scarce", > 20 is "saturated"
            demand_multiplier = 1.0
            if transactions > 20:
                demand_multiplier = 0.7 # Saturated market, price drops
            elif transactions > 10:
                demand_multiplier = 0.9 # Well-supplied
            elif transactions <= 5:
                demand_multiplier = 1.2 # Scarce, price increases

            return int(base_price * demand_multiplier)

    def record_transaction(self, item_type):
        """Records that a transaction for a given item type has occurred."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE market_data SET transactions_last_cycle = transactions_last_cycle + 1 WHERE item_type=?", (item_type,))
            conn.commit()

    def reset_market_cycles(self):
        """Resets the transaction counters for a new cycle (e.g., daily)."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE market_data SET transactions_last_cycle = 0")
            conn.commit()
        print("Market transaction cycles have been reset.")


economy_manager = EconomyManager()
