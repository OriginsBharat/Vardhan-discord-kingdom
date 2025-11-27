"""
Comfort System - Bots check in on Master's wellbeing
"""
import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import random

class ComfortSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_checkin = None
        self.evening_checkin.start()

    def cog_unload(self):
        self.evening_checkin.cancel()

    @tasks.loop(time=time(hour=20, minute=0))  # 8 PM daily
    async def evening_checkin(self):
        """Once daily, a bot asks how the Master's day was."""
        from src.config import config
        from src.core.bot_manager import bot_manager

        # Only one bot should do this - randomly pick or use persona priority
        all_bots = list(bot_manager.bots.values())
        if not all_bots or self.bot != random.choice(all_bots):
            return

        master = bot_manager.get_master_user()
        if not master:
            return

        checkin_messages = [
            f"Master, how was your day today? I hope it treated you well.",
            f"The evening has arrived. Did you accomplish what you set out to do today, Master?",
            f"I've been thinking of you. How are you feeling this evening?",
            f"Another day draws to a close. Is there anything on your mind you'd like to share?",
        ]

        try:
            await master.send(random.choice(checkin_messages))
        except discord.Forbidden:
            pass  # Can't DM master

    @evening_checkin.before_loop
    async def before_checkin(self):
        await self.bot.wait_until_ready()

    @commands.command(name="mood")
    async def set_mood(self, ctx, *, mood: str):
        """Tell the bots how you're feeling."""
        from src.config import config

        if ctx.author.id != config.master_user_id:
            return

        mood_lower = mood.lower()

        if any(word in mood_lower for word in ["tired", "exhausted", "sleepy"]):
            response = f"You should rest, Master. {self.bot.persona.name} will watch over things while you sleep."
        elif any(word in mood_lower for word in ["sad", "down", "upset", "depressed"]):
            response = f"I'm sorry you're feeling that way, Master. I'm here for you, always. Would you like some quiet company, or shall I fetch something to lift your spirits?"
        elif any(word in mood_lower for word in ["happy", "good", "great", "wonderful"]):
            response = f"That brings me joy to hear, Master. Your happiness is the light that guides us all."
        elif any(word in mood_lower for word in ["stressed", "anxious", "worried"]):
            response = f"Take a deep breath, Master. Whatever troubles you, we will face it together. Perhaps some tea and a quiet moment?"
        elif any(word in mood_lower for word in ["angry", "frustrated", "annoyed"]):
            response = f"I understand, Master. Sometimes the world tests our patience. Shall I leave you in peace, or would you like to vent?"
        else:
            response = f"Thank you for sharing, Master. I've noted how you're feeling."

        await ctx.send(response)


class ReactiveListening(commands.Cog):
    """Bots react naturally to conversations."""

    def __init__(self, bot):
        self.bot = bot
        self.reaction_emojis = {
            "laugh": ["😄", "😂", "🤭"],
            "love": ["❤️", "💕", "🥰"],
            "think": ["🤔", "💭", "📚"],
            "agree": ["👍", "✨", "💫"],
            "sad": ["😢", "🥺", "💙"],
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        from src.config import config

        # Don't react to self or other bots
        if message.author.bot:
            return

        # Only react to Master's messages, and only sometimes
        if message.author.id != config.master_user_id:
            return

        # 15% chance to react
        if random.random() > 0.15:
            return

        content_lower = message.content.lower()

        # Determine reaction type based on content
        if any(word in content_lower for word in ["haha", "lol", "lmao", "funny"]):
            emoji = random.choice(self.reaction_emojis["laugh"])
        elif any(word in content_lower for word in ["love", "adore", "beautiful"]):
            emoji = random.choice(self.reaction_emojis["love"])
        elif any(word in content_lower for word in ["think", "wonder", "curious", "?"]):
            emoji = random.choice(self.reaction_emojis["think"])
        elif any(word in content_lower for word in ["sad", "sorry", "miss"]):
            emoji = random.choice(self.reaction_emojis["sad"])
        else:
            emoji = random.choice(self.reaction_emojis["agree"])

        try:
            await message.add_reaction(emoji)
        except:
            pass


async def setup(bot):
    await bot.add_cog(ComfortSystem(bot))
    await bot.add_cog(ReactiveListening(bot))
