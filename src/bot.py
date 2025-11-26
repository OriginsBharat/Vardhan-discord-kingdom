import discord
from discord.ext import commands
import os
import time
from src.core.personas import persona_manager
from src.config import config
from src.core.bot_manager import bot_manager

class MyAIWorldBot(commands.Bot):
    def __init__(self, persona_name, **kwargs):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), **kwargs)
        self.persona = persona_manager.get_persona(persona_name)
        self.master_ping_timestamps = []

    async def setup_hook(self):
        """Load all command cogs."""
        for filename in os.listdir("./src/commands"):
            if filename.endswith(".py") and filename != "__init__.py":
                await self.load_extension(f"src.commands.{filename[:-3]}")
                print(f"Loaded command cog: {filename}")

    async def on_ready(self):
        bot_manager.register_bot(self)
        print(f"{self.persona.name} has connected to Discord!")
        await self.change_presence(activity=discord.Game(name=f"Serving the Master"))

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Puppet Master Interception
        if hasattr(self, 'possessed_in_channel') and self.possessed_in_channel.get(message.channel.id) == message.author.id:
            try:
                await message.delete()
                await message.channel.send(message.content)
            except Exception as e:
                print(f"Error during possession message handling: {e}")
            return # Stop further processing

        # The Master's Call (Ping-based Summoning)
        if config.master_user_id and self.user.mentioned_in(message) and message.author.id == config.master_user_id:
            current_time = time.time()

            # If bot is awake, respond immediately
            if self.persona.schedule_state in ["awake", "working"]:
                await message.channel.send(f"I am here, Master. {self.persona.name} answers your call.")

            # If bot is sleeping, check for multiple pings
            elif self.persona.schedule_state == "sleeping":
                # Clean up old pings (older than 2 minutes)
                self.master_ping_timestamps = [t for t in self.master_ping_timestamps if current_time - t < 120]

                self.master_ping_timestamps.append(current_time)

                if len(self.master_ping_timestamps) >= 3:
                    self.persona.schedule_state = "awake" # Wake the bot up
                    self.master_ping_timestamps.clear() # Reset pings
                    await message.channel.send(f"*Stirring from a deep slumber...* I was sleeping, but your insistent call has awakened me, Master. How may {self.persona.name} serve you?")

        await self.process_commands(message)
