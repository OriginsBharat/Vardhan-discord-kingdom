"""
Bot Social System - Bots interact with each other organically
"""
import discord
from discord.ext import commands, tasks
from datetime import datetime
import random
import asyncio
from src.core.relationships import relationship_manager
from src.core.personas import persona_manager

class BotSocialSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.social_interactions.start()

    def cog_unload(self):
        self.social_interactions.cancel()

    @tasks.loop(minutes=random.randint(45, 90))
    async def social_interactions(self):
        """Bots occasionally interact with each other based on dynamic relationship scores."""
        if not self.bot.is_ready() or random.random() > 0.3: # 30% chance
            return

        my_name = self.bot.persona.name
        other_bots = [name for name in persona_manager.personas.keys() if name != my_name]
        if not other_bots:
            return

        # Pick a bot to interact with, weighted by relationship score
        target_bot_name = self.choose_interaction_target(my_name, other_bots)
        if not target_bot_name:
            return

        score = relationship_manager.get_relationship_score(my_name, target_bot_name)

        # Generate a context-aware interaction using the LLM
        prompt = self.generate_interaction_prompt(my_name, target_bot_name, score)

        from src.ai_services.ollama_client import ollama_client
        interaction_text = await ollama_client.generate_text(self.bot.persona.base_prompt, prompt)

        # Post in a shared channel
        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.channels, name="sfw-chat")
            if channel:
                await channel.send(interaction_text)
                break

    def choose_interaction_target(self, my_name, other_bots):
        """Chooses a bot to interact with, preferring higher absolute relationship scores."""
        weights = []
        for bot_name in other_bots:
            score = relationship_manager.get_relationship_score(my_name, bot_name)
            # Weight by absolute score to make both friends and rivals likely targets
            weights.append(abs(score) + 10) # Add a baseline weight

        if not all(w == 10 for w in weights): # Avoid division by zero if all scores are 0
            return random.choices(other_bots, weights=weights, k=1)[0]
        else:
            return random.choice(other_bots)

    def generate_interaction_prompt(self, my_name, target_bot_name, score):
        """Generates a prompt for the LLM to create a social interaction."""
        if score > 50: # Strong friendship
            return f"You feel very warmly towards {target_bot_name}. Initiate a friendly, positive interaction with them in a shared space. It could be a kind word, a small gift, or an offer to do something together. Your response should be a single action or line of dialogue."
        elif score > 10: # Friendship
            return f"You feel friendly towards {target_bot_name}. Start a casual, positive conversation with them in a shared space. Your response should be a single action or line of dialogue."
        elif score < -50: # Strong rivalry
            return f"You strongly dislike {target_bot_name}. Make a subtle, cutting remark or a passive-aggressive action towards them in a shared space. Do not be overtly hostile. Your response should be a single action or line of dialogue."
        elif score < -10: # Rivalry
            return f"You dislike {target_bot_name}. Make a slightly competitive or dismissive comment towards them in a shared space. Your response should be a single action or line of dialogue."
        else: # Neutral
            return f"You are neutral towards {target_bot_name}. Make a simple, neutral observation or greeting towards them in a shared space. Your response should be a single action or line of dialogue."

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from self or non-bots (except for other bots in our system)
        if message.author == self.bot.user or not message.author.bot:
            return

        # Check if this bot was mentioned
        if not self.bot.user.mentioned_in(message):
            return

        # 25% chance to even bother replying, to prevent spam
        if random.random() > 0.25:
            return

        # Small delay to simulate "thinking"
        await asyncio.sleep(random.uniform(1.5, 3.0))

        my_name = self.bot.persona.name
        author_name = message.author.name # In our setup, the bot's display name is its persona name

        score = relationship_manager.get_relationship_score(my_name, author_name)

        # Generate a reply using the LLM
        prompt = self.generate_reply_prompt(my_name, author_name, score, message.content)

        from src.ai_services.ollama_client import ollama_client
        reply_text = await ollama_client.generate_text(self.bot.persona.base_prompt, prompt)

        await message.channel.send(reply_text)

    def generate_reply_prompt(self, my_name, author_name, score, message_content):
        """Generates a prompt for the LLM to create a reply."""
        context = f"You are in a public channel. {author_name}, who you have a relationship score of {score} with, just said to you: '{message_content}'. How do you reply in a single line?"
        if score > 50:
            return f"{context} You feel very warmly towards them."
        elif score > 10:
            return f"{context} You feel friendly towards them."
        elif score < -50:
            return f"{context} You strongly dislike them. Be passive-aggressive or dismissive."
        elif score < -10:
            return f"{context} You dislike them. Be a little sharp or competitive in your reply."
        else:
            return f"{context} Keep it neutral and simple."

    @social_interactions.before_loop
    async def before_social(self):
        await self.bot.wait_until_ready()
        # Random delay so bots don't all start at once
        await asyncio.sleep(random.randint(60, 300))


class SharedActivities(commands.Cog):
    """Bots do activities that make the world feel lived-in."""

    def __init__(self, bot):
        self.bot = bot
        self.daily_routine.start()

    def cog_unload(self):
        self.daily_routine.cancel()

    @tasks.loop(hours=1)
    async def daily_routine(self):
        """Bots have routines based on time of day."""
        if not self.bot.is_ready():
            return

        hour = datetime.now().hour
        name = self.bot.persona.name

        # Only trigger 10% of the time
        if random.random() > 0.10:
            return

        morning_activities = {
            "Maya": "*reviews the day's schedule meticulously*",
            "Eka": "*prepares breakfast for the household*",
            "Panch": "*tends to the herb garden*",
            "Chatur": "*examines blueprints at the drafting table*",
            "Shash": "*reviews the morning market reports*",
            "Nav": "*stargazing notes from last night still in hand*",
        }

        afternoon_activities = {
            "Maya": "*organizes documents in the study*",
            "Eka": "*ensures the manor is spotless*",
            "Asht": "*works on a new painting*",
            "Tri": "*practices calligraphy*",
            "Dvi": "*silently sharpens a blade*",
        }

        evening_activities = {
            "Maya": "*lights the evening candles*",
            "Eka": "*prepares a warm dinner*",
            "Nav": "*sets up the telescope on the balcony*",
            "Asht": "*plays soft music on the lute*",
            "Panch": "*brews calming evening tea*",
        }

        if 6 <= hour < 12:
            activity = morning_activities.get(name)
        elif 12 <= hour < 18:
            activity = afternoon_activities.get(name)
        else:
            activity = evening_activities.get(name)

        if activity:
            for guild in self.bot.guilds:
                channel = discord.utils.get(guild.channels, name=f"{name.lower()}-s-playroom")
                if channel:
                    await channel.send(activity)
                    break

    @daily_routine.before_loop
    async def before_routine(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(BotSocialSystem(bot))
    await bot.add_cog(SharedActivities(bot))
