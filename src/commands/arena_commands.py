from discord.ext import commands
import discord
from src.config import config
from src.core.scar_manager import scar_manager
from src.core.bot_manager import bot_manager

class ArenaCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_duels = {} # {channel_id: (challenger, challenged)}

    @commands.command(name="challenge")
    async def challenge(self, ctx, member: discord.Member):
        """Challenges another user to a duel in the Coliseum."""
        if ctx.channel.name != "the-coliseum":
            await ctx.send("Duels can only be declared in `#the-coliseum`.")
            return

        challenger = ctx.author
        challenged = member

        if challenger == challenged:
            await ctx.send("You cannot challenge yourself, warrior.")
            return

        self.active_duels[ctx.channel.id] = (challenger, challenged)
        await ctx.send(f"**A duel is declared!** {challenger.mention} has challenged {challenged.mention} in the Arena of Souls! The Master will declare the winner.")

    @commands.command(name="declare_winner")
    async def declare_winner(self, ctx, winner: discord.Member):
        """(Master-only) Declares the winner of a duel and scars the loser."""
        if ctx.author.id != config.master_user_id:
            await ctx.send("Only the Master can declare a winner.")
            return

        if ctx.channel.id not in self.active_duels:
            await ctx.send("No active duel in this channel.")
            return

        challenger, challenged = self.active_duels.pop(ctx.channel.id)

        if winner not in [challenger, challenged]:
            await ctx.send("The declared winner was not part of the duel.")
            return

        loser = challenged if winner == challenger else challenger

        # Inflict the 'Humiliated' scar on the loser
        loser_persona_name = bot_manager.get_persona_name_by_user_id(loser.id)

        if loser_persona_name:
            scar_manager.inflict_scar(
                target_bot_name=loser_persona_name,
                scar_name="Humiliated",
                scar_description=f"Was defeated in a duel by {winner.name} in the Coliseum."
            )
            await ctx.send(f"**The duel is over!** The Master has declared {winner.mention} the victor. {loser.mention} has been humiliated and will forever carry the scar of this defeat.")
        else:
            await ctx.send(f"**The duel is over!** The Master has declared {winner.mention} the victor. Could not identify the loser's persona to inflict a scar.")

async def setup(bot):
    await bot.add_cog(ArenaCommands(bot))
