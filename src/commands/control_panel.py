from discord.ext import commands
from src.config import config
from src.core.bot_manager import bot_manager

class ControlPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # We will store the master's ID on the bot that is being possessed
        # bot.possessed_by_master = master_id

    @commands.command(name="possess")
    async def possess(self, ctx, bot_name: str):
        """Allows the Master to possess a bot, speaking as them."""
        if ctx.author.id != config.master_user_id:
            return

        target_bot = bot_manager.get_bot(bot_name)
        if not target_bot:
            await ctx.send(f"Bot '{bot_name}' not found or is not online.")
            return

        # Release any currently possessed bot
        for bot in bot_manager.bots.values():
            if hasattr(bot, 'possessed_in_channel') and bot.possessed_in_channel.get(ctx.channel.id) == ctx.author.id:
                del bot.possessed_in_channel[ctx.channel.id]

        # Possess the new bot in the current channel
        if not hasattr(target_bot, 'possessed_in_channel'):
            target_bot.possessed_in_channel = {}
        target_bot.possessed_in_channel[ctx.channel.id] = ctx.author.id

        await ctx.send(f"You have possessed **{bot_name}** in this channel. All your messages here will now be spoken by them. Use `!release` to stop.")

    @commands.command(name="release")
    async def release(self, ctx):
        """Releases the Master's control over a possessed bot in this channel."""
        if ctx.author.id != config.master_user_id:
            return

        released = False
        for bot in bot_manager.bots.values():
            if hasattr(bot, 'possessed_in_channel') and bot.possessed_in_channel.get(ctx.channel.id) == ctx.author.id:
                del bot.possessed_in_channel[ctx.channel.id]
                await ctx.send(f"You have released **{bot.persona.name}** in this channel.")
                released = True
                break

        if not released:
            await ctx.send("You are not currently possessing any bot in this channel.")

async def setup(bot):
    await bot.add_cog(ControlPanel(bot))
