import random
from src.ai_services.ollama_client import ollama_client

class EventAI:
    def __init__(self, bot_manager):
        self.bot_manager = bot_manager
        self.announcement_channel_name = "announcements"
        self.event_types = [
            # ... (event types as before)
        ]
        print("EventAI (The Director) initialized.")

    async def trigger_event(self):
        """Selects a random event, generates a description, and announces it through Maya."""
        maya_bot = self.bot_manager.get_bot("Maya")
        if not maya_bot:
            print("Error: Maya bot instance not found. Cannot announce event.")
            return

        guild = maya_bot.guilds[0] if maya_bot.guilds else None
        if not guild:
            print("Error: Maya is not in any server. Cannot announce event.")
            return

        announcement_channel = discord.utils.get(guild.channels, name=self.announcement_channel_name)
        if not announcement_channel:
            print(f"Error: #{self.announcement_channel_name} channel not found.")
            return

        print("The Director is triggering a new world event...")
        event = random.choice(self.event_types)

        announcement_text = ollama_client.generate_text(
            persona_prompt="You are The Director, an omniscient narrator. Announce the following event to the world with a tone of grandiosity and mystery.",
            user_prompt=event["prompt"]
        )

        try:
            await announcement_channel.send(f"**--:--[ WORLD EVENT ]--:--**\n\n{announcement_text}")
            print(f"Announced Event: {event['name']}")
        except Exception as e:
            print(f"Failed to announce event: {e}")

# Re-add the event types
EventAI.event_types = [
    {
        "name": "Economic Boom",
        "prompt": "Generate an announcement for a sudden economic boom. A rare resource has been discovered, causing a specific industry (like alchemy or blacksmithing) to become highly profitable for a short time. Mention the resource and the industry."
    },
    {
        "name": "Grand Festival",
        "prompt": "Generate an announcement for a grand festival in the Master's honor. Describe the planned events, such as a grand feast, a tournament in the Coliseum, and a fireworks display."
    },
    {
        "name": "Whisper of Madness",
        "prompt": "Generate a subtle, ominous announcement. A strange, maddening whisper is spreading through the city, causing paranoia and distrust. The announcement should be phrased as a public safety warning, but with a hint of something supernatural and terrifying."
    }
]
