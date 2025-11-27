"""
Presence System - Makes the world feel alive and responsive
"""
import discord
from discord.ext import commands, tasks
from datetime import datetime
import random

class PresenceSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.master_last_seen = None
        self.ambient_chatter.start()

    def cog_unload(self):
        self.ambient_chatter.cancel()

    def get_time_greeting(self):
        """Returns appropriate greeting based on time of day."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return random.choice([
                "Good morning, Master.",
                "The morning sun greets you, Master.",
                "A fresh day awaits your command.",
            ])
        elif 12 <= hour < 17:
            return random.choice([
                "Good afternoon, Master.",
                "The day is still young, Master.",
            ])
        elif 17 <= hour < 21:
            return random.choice([
                "Good evening, Master.",
                "The evening welcomes your presence.",
            ])
        else:
            return random.choice([
                "The night grows deep, Master.",
                "Burning the midnight oil, Master?",
                "The world sleeps, but I remain vigilant.",
            ])

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        """Detect when Master comes online."""
        from src.config import config

        if after.id != config.master_user_id:
            return

        # Master came online
        if before.status == discord.Status.offline and after.status != discord.Status.offline:
            # Only greet if it's been more than 30 minutes
            if self.master_last_seen:
                time_away = (datetime.now() - self.master_last_seen).total_seconds()
                if time_away < 1800:  # 30 minutes
                    return

            self.master_last_seen = datetime.now()

            # Find a general channel to greet in
            for guild in self.bot.guilds:
                channel = discord.utils.get(guild.channels, name="sfw-chat")
                if channel:
                    greeting = self.get_time_greeting()
                    await channel.send(f"*{self.bot.persona.name} notices your presence.* {greeting}")
                    break

    @commands.Cog.listener()
    async def on_presence_update_offline(self, before, after):
        """Track when Master goes offline."""
        from src.config import config

        if after.id != config.master_user_id:
            return

        if after.status == discord.Status.offline:
            self.master_last_seen = datetime.now()

    @tasks.loop(minutes=random.randint(45, 90))
    async def ambient_chatter(self):
        """Bots occasionally say things to feel alive."""
        if not self.bot.is_ready():
            return

        # Only trigger 20% of the time to keep it sparse
        if random.random() > 0.20:
            return

        ambient_actions = [
            "*stretches and yawns softly*",
            "*hums a quiet melody*",
            "*gazes out the window thoughtfully*",
            "*organizes some papers on the desk*",
            "*sips tea quietly*",
            "*flips through an old book*",
        ]

        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.channels, name=f"{self.bot.persona.name.lower()}-s-playroom")
            if channel:
                action = random.choice(ambient_actions)
                await channel.send(action)
                break

    @ambient_chatter.before_loop
    async def before_ambient(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(PresenceSystem(bot))
