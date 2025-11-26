import time
from src.core.personas import persona_manager

# This would store the last time the simulation was run.
# In a real implementation, this would be a persistent value in a database.
LAST_ONLINE_TIMESTAMP_FILE = "data/last_online.txt"

class Simulation:
    def __init__(self, economy_manager):
        self.economy_manager = economy_manager

    def run_offline_progression(self):
        """
        Calculates all world changes that occurred while the application was offline.
        """
        print("Running offline progression simulation...")

        try:
            with open(LAST_ONLINE_TIMESTAMP_FILE, "r") as f:
                last_online = float(f.read())
        except FileNotFoundError:
            print("First run. No offline progression to simulate.")
            self.save_current_timestamp()
            return

        current_time = time.time()
        hours_offline = (current_time - last_online) / 3600.0

        print(f"World has been offline for {hours_offline:.2f} hours. Simulating changes...")

        for persona in persona_manager.personas.values():
            # 1. Simulate Economic Changes (Jobs Worked, Rs Earned)
            # This is a placeholder. A real implementation would be much more complex.
            # It would check the bot's job, hourly rate, and work_ethic stat.
            work_ethic = 0.8 # Placeholder stat
            hourly_rate = 100 # Placeholder stat
            earnings = hours_offline * hourly_rate * work_ethic
            # self.economy_manager.deposit(persona.name, earnings)
            print(f"Simulated {earnings:.2f} Rs earned for {persona.name}.")

            # 2. Simulate Social/Emotional State Changes
            # Neediness increases based on a personality-driven growth rate.
            neediness_growth_rate = 5 # Placeholder stat (e.g., points per hour)
            neediness_increase = hours_offline * neediness_growth_rate
            persona.emotional_sliders["neediness"] = min(100, persona.emotional_sliders.get("neediness", 0) + neediness_increase)
            print(f"Simulated neediness increase for {persona.name}. New neediness: {persona.emotional_sliders['neediness']:.2f}")

        print("Offline progression simulation complete.")
        self.save_current_timestamp()

    def save_current_timestamp(self):
        """Saves the current timestamp to mark the last online time."""
        with open(LAST_ONLINE_TIMESTAMP_FILE, "w") as f:
            f.write(str(time.time()))

# This would be instantiated and run once in main.py before the bots connect.
# Example:
# simulation = Simulation(economy_manager)
# simulation.run_offline_progression()
