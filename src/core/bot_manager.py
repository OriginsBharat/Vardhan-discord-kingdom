from src.config import config

class BotManager:
    def __init__(self):
        self.bots = {} # { "Maya": bot_instance, ... }
        self.master_user = None
        self.primary_bot = None # Will be Maya
        print("BotManager initialized.")

    def register_bot(self, bot):
        """Adds a running bot instance to the manager."""
        self.bots[bot.persona.name] = bot
        if bot.persona.name == "Maya":
            self.primary_bot = bot
        print(f"Registered bot: {bot.persona.name}")

    def get_bot(self, name):
        """Retrieves a bot instance by name."""
        return self.bots.get(name)

    async def initialize_master_user(self):
        """Fetches and stores the Master's user object for DMs."""
        if not self.primary_bot:
            print("Error: Primary bot (Maya) is not registered. Cannot fetch Master user.")
            return

        if config.master_user_id:
            self.master_user = await self.primary_bot.fetch_user(config.master_user_id)
            if self.master_user:
                print(f"Successfully fetched Master user object: {self.master_user.name}")
            else:
                print(f"Error: Could not fetch Master user with ID {config.master_user_id}.")

    def get_master_user(self):
        return self.master_user

    def get_persona_name_by_user_id(self, user_id):
        """Finds the persona name associated with a given Discord user ID."""
        for bot in self.bots.values():
            if bot.user.id == user_id:
                return bot.persona.name
        return None

# A single instance for the application
bot_manager = BotManager()
