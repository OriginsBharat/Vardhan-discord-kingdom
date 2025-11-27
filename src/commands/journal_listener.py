import discord
from discord.ext import commands
from src.config import config
from src.core.personas import persona_manager
import json

class JournalListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Only listen to reactions from the Master
        if payload.user_id != config.master_user_id:
            return

        # Check if the reaction is on a journal entry from Maya
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if message.author.id != self.bot.user.id or not message.embeds:
            return

        embed = message.embeds[0]
        if "The Master's Journal" not in embed.title:
            return

        # The embed's description contains a hidden JSON payload with event metadata
        try:
            event_data = json.loads(embed.description.split("<!--")[1].split("-->")[0])
        except (json.JSONDecodeError, IndexError):
            return # Not a valid journal entry with metadata

        emoji = str(payload.emoji)

        # Determine the emotional impact
        adjustment = 0
        if emoji == '❤️': adjustment = 5
        elif emoji == '😂': adjustment = 3
        elif emoji == '😠': adjustment = -5
        elif emoji == '😢': adjustment = -3

        if adjustment == 0:
            return

        # Apply the emotional adjustment to the involved bots
        for event in event_data:
            bot_name = event.get("bot_name")
            emotion = event.get("emotion_to_affect")
            if bot_name and emotion:
                persona = persona_manager.get_persona(bot_name)
                if persona:
                    current_value = persona.emotional_sliders.get(emotion, 50)
                    persona.emotional_sliders[emotion] = max(0, min(100, current_value + adjustment))
                    print(f"Adjusted {emotion} for {bot_name} by {adjustment} due to Master's reaction.")

        await message.channel.send(f"*Your reaction has been noted and the world has shifted accordingly.*", delete_after=10)


async def setup(bot):
    # This cog should only be loaded on the Maya bot
    if bot.persona.name == "Maya":
        await bot.add_cog(JournalListener(bot))
