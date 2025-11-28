import discord
from discord.ext import commands
import asyncio
import os
from src.config import config
from src.ai_services.chatterbox_client import chatterbox_client

class ParrotMode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore self, other bots, and non-master messages
        if message.author.id != config.master_user_id or message.author.bot:
            return

        # Check if the Master is in a voice channel
        if not message.author.voice or not message.author.voice.channel:
            return

        voice_channel = message.author.voice.channel

        # Check if the message was sent in the text channel associated with that voice channel
        if not hasattr(voice_channel, 'text_channel') or message.channel.id != voice_channel.text_channel.id:
            # Fallback for category-based association if direct text_channel is not available
            if message.channel.category_id != voice_channel.category_id:
                return

        # Check if the bot is in that same voice channel
        vc = discord.utils.get(self.bot.voice_clients, channel=voice_channel)
        if not vc or not vc.is_connected():
            return

        # Check if the voice engine is available
        if not chatterbox_client.is_available():
            await message.channel.send("*The voice engine is currently offline, Master. I cannot speak your words.*", delete_after=10)
            return

        # Generate the audio for the Master's message
        try:
            output_filename = f"temp_parrot_{message.id}.wav"

            voice_file = await chatterbox_client.generate_voice(
                text=message.content,
                output_filename=output_filename,
                voice_name=self.bot.persona.name
            )

            if voice_file:
                while vc.is_playing():
                    await asyncio.sleep(0.1)

                vc.play(discord.FFmpegPCMAudio(voice_file), after=lambda e: os.remove(voice_file) if e is None and os.path.exists(voice_file) else None)

        except Exception as e:
            print(f"Error in Parrot Mode for {self.bot.persona.name}: {e}")

    @commands.command(name="join")
    async def join(self, ctx):
        """Commands the bot to join your current voice channel."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client:
                await ctx.voice_client.move_to(channel)
            else:
                await channel.connect()
            await ctx.send(f"`{self.bot.persona.name} has joined the voice channel. I am listening.`")
        else:
            await ctx.send("`You are not in a voice channel, Master.`")

    @commands.command(name="leave")
    async def leave(self, ctx):
        """Commands the bot to leave its current voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send(f"`{self.bot.persona.name} has left the voice channel.`")
        else:
            await ctx.send("`I am not in a voice channel, Master.`")


async def setup(bot):
    await bot.add_cog(ParrotMode(bot))
