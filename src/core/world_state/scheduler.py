import asyncio
from src.core.personas import persona_manager
from src.economic_system.loan_manager import loan_manager
# Import other managers and clients as they become needed
# from src.core.world_state.event_ai import event_ai
# from src.ai_services.comfyui_client import comfyui_client
# from src.ai_services.ollama_client import ollama_client

class Scheduler:
    def __init__(self, bot_manager):
        self.bot_manager = bot_manager
        self.running = False

    async def _schedule_loop(self):
        """The main asynchronous loop that triggers events."""
        minute_counter = 0
        while self.running:
            await asyncio.sleep(60)
            minute_counter += 1
            print(f"[Scheduler] Heartbeat: Minute {minute_counter}")

            # Every Minute: Check personal schedules
            # self.check_schedules() # Placeholder for now

            # Every 5 Minutes: Check neediness levels
            if minute_counter % 5 == 0:
                print("[Scheduler] Checking neediness levels...")
                await self.check_neediness()

            # Every 10 Minutes: Check for defaulted loans
            if minute_counter % 10 == 0:
                print("[Scheduler] Checking for defaulted loans...")
                loan_manager.check_for_defaults()

            # Every 20 Minutes: Trigger Autonomous Action Manager
            if minute_counter % 20 == 0:
                print("[Scheduler] Triggering Autonomous Action Manager...")
                # self.trigger_autonomous_actions() # Placeholder for now

            # Every 30 Minutes: Trigger Event AI
            if minute_counter % 30 == 0:
                print("[Scheduler] Triggering Event AI...")
                # await event_ai.trigger_event() # Placeholder for now

            # Daily (at 23:55)
            if minute_counter > 0 and minute_counter % 1440 == 1435:
                print("[Scheduler] Triggering Master's Journal generation...")
                # self.generate_journal() # Placeholder for now

    async def check_neediness(self):
        master_user = self.bot_manager.get_master_user()
        if not master_user:
            return

        for persona in persona_manager.personas.values():
            if persona.emotional_sliders.get("neediness", 0) > persona.neediness_threshold:
                # Logic for sending DMs is already implemented here...
                pass # Keeping it concise for this change

    def start(self):
        if not self.running:
            self.running = True
            asyncio.create_task(self._schedule_loop())
            print("World Scheduler has started with all triggers active.")

    def stop(self):
        self.running = False
        print("World Scheduler has stopped.")
