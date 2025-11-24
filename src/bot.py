import discord
from discord.ext import commands
from src.core.personas import persona_manager

class MyAIWorldBot(commands.Bot):
    def __init__(self, persona_name, **kwargs):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), **kwargs)
        self.persona = persona_manager.get_persona(persona_name)

    async def on_ready(self):
        print(f"{self.persona.name} has connected to Discord!")
        await self.change_presence(activity=discord.Game(name=f"Serving the Master"))

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Simple reply for testing
        if self.user.mentioned_in(message):
            await message.channel.send(f"Yes, Master? {self.persona.name} is here.")

        await self.process_commands(message)
