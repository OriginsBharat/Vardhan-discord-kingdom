import sqlite3
import time
from uuid import uuid4
from src.economic_system.economy_manager import economy_manager
from src.core.scar_manager import scar_manager

class LoanManager:
    def __init__(self, db_path="data/world_data.db"):
        self.db_path = db_path
        self._initialize_db()
        self.economy_manager = economy_manager
        self.scar_manager = scar_manager
        print("LoanManager initialized with persistent database.")

    def _get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS active_loans (
                    loan_id TEXT PRIMARY KEY,
                    lender_id TEXT NOT NULL,
                    borrower_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    due_date REAL NOT NULL
                )
            """)
            conn.commit()

    def grant_loan(self, lender_id, borrower_id, amount, duration_days=7):
        """Grants a loan, transferring funds and creating a persistent debt record."""
        if self.economy_manager.transfer(lender_id, borrower_id, amount):
            loan_id = str(uuid4())
            due_date = time.time() + (duration_days * 86400)
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO active_loans (loan_id, lender_id, borrower_id, amount, due_date) VALUES (?, ?, ?, ?, ?)",
                    (loan_id, str(lender_id), str(borrower_id), amount, due_date)
                )
                conn.commit()
            print(f"Loan {loan_id} granted from {lender_id} to {borrower_id} for {amount} Rs.")
            return loan_id
        return None

    def repay_loan(self, loan_id, borrower_id):
        """Repays a loan, transferring funds and clearing the debt from the database."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT lender_id, amount FROM active_loans WHERE loan_id=? AND borrower_id=?", (loan_id, str(borrower_id)))
            result = cursor.fetchone()
            if not result:
                return "Loan not found or you are not the borrower."

            lender_id, amount = result
            if self.economy_manager.transfer(borrower_id, lender_id, amount):
                cursor.execute("DELETE FROM active_loans WHERE loan_id=?", (loan_id,))
                conn.commit()
                print(f"Loan {loan_id} has been repaid by {borrower_id}.")
                return "Loan successfully repaid."
        return "Insufficient funds to repay the loan."

    def check_for_defaults(self):
        """Scans the database for overdue loans and triggers the 'Enslaved' scar."""
        print("Checking for defaulted loans...")
        current_time = time.time()
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT loan_id, lender_id, borrower_id FROM active_loans WHERE due_date < ?", (current_time,))
            defaulted_loans = cursor.fetchall()

            for loan_id, lender_id, borrower_id in defaulted_loans:
                print(f"Loan {loan_id} from {borrower_id} to {lender_id} has defaulted!")

                # The Gilded Cage: Enslave the borrower to the creditor
                self.scar_manager.inflict_scar(
                    target_bot_name=borrower_id, # Assuming bot names are used as IDs
                    scar_name="Enslaved",
                    scar_description=f"Permanently enslaved to {lender_id} due to a defaulted loan."
                )

            # Clean up defaulted loans
            if defaulted_loans:
                loan_ids_to_delete = tuple(loan[0] for loan in defaulted_loans)
                placeholders = ','.join('?' for _ in loan_ids_to_delete)
                cursor.execute(f"DELETE FROM active_loans WHERE loan_id IN ({placeholders})", loan_ids_to_delete)
                conn.commit()

loan_manager = LoanManager()
