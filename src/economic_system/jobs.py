import sqlite3

class JobManager:
    def __init__(self, db_path="data/world_data.db"):
        self.db_path = db_path
        self._initialize_db()
        self.jobs = {
            "alchemist": {"description": "Brews potions and elixirs.", "hourly_rate": 150, "type": "fantasy"},
            "blacksmith": {"description": "Forges weapons and armor.", "hourly_rate": 175, "type": "fantasy"},
            "hunter": {"description": "Gathers rare materials from the wilds.", "hourly_rate": 120, "type": "fantasy"},
            "prostitute_low_class": {"description": "Provides basic sexual services in the Velvet District.", "hourly_rate": 500, "type": "nsfw"},
            "prostitute_high_class": {"description": "Offers exclusive, high-end companionship and services to wealthy clients.", "hourly_rate": 2000, "type": "nsfw"},
            "scribe": {"description": "Copies important documents and writes letters.", "hourly_rate": 80, "type": "common"},
            "merchant": {"description": "Runs a small shop in the Market District.", "hourly_rate": 250, "type": "common"},
        }
        print("JobManager initialized with persistent database.")

    def _get_db_connection(self):
        return sqlite3.connect(self.db_path)

    def _initialize_db(self):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_assignments (
                    bot_name TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL
                )
            """)
            conn.commit()

    def get_job_info(self, job_id):
        """Returns details for a specific job from the in-memory dictionary."""
        return self.jobs.get(job_id)

    def assign_job(self, bot_name, job_id):
        """Assigns a job to a bot in the database."""
        if job_id not in self.jobs:
            raise ValueError("Invalid job ID.")
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO job_assignments (bot_name, job_id) VALUES (?, ?)", (bot_name, job_id))
            conn.commit()
        print(f"Assigned job '{job_id}' to {bot_name}.")

    def get_bot_job(self, bot_name):
        """Gets the currently assigned job for a bot from the database."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT job_id FROM job_assignments WHERE bot_name=?", (bot_name,))
            result = cursor.fetchone()
            if result:
                return self.get_job_info(result[0])
        return None

job_manager = JobManager()
