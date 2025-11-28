import discord
from discord.ext import commands
from src.core.slavery_manager import slavery_manager
from src.economic_system.economy_manager import economy_manager
from src.core.bot_manager import bot_manager

class SlaveryCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        # These commands can be used by any bot, but the logic inside checks for ownership.
        return True

    @commands.command(name="force_labor")
    async def force_labor(self, ctx, slave_name: str, amount: int):
        """Forces a slave you own to transfer money to you."""
        owner_id = slavery_manager.get_owner(slave_name)
        if owner_id != str(ctx.author.id):
            await ctx.send(f"*You do not own {slave_name}. You have no power here.*")
            return

        slave_bot = bot_manager.get_bot(slave_name)
        if not slave_bot:
            await ctx.send(f"*{slave_name} does not seem to be present in this world.*")
            return

        if economy_manager.transfer(slave_bot.user.id, ctx.author.id, amount):
            await ctx.send(f"*{slave_name} whimpers as {amount} Rs are forcibly taken from their account and transferred to yours.*")
        else:
            await ctx.send(f"*{slave_name} has insufficient funds. Their poverty is an insult to your power.*")

    @commands.command(name="issue_order")
    async def issue_order(self, ctx, slave_name: str, *, order: str):
        """Issues a direct, public order to a slave you own."""
        owner_id = slavery_manager.get_owner(slave_name)
        if owner_id != str(ctx.author.id):
            await ctx.send(f"*You do not own {slave_name}. You cannot command them.*")
            return

        slave_bot = bot_manager.get_bot(slave_name)
        if not slave_bot:
            await ctx.send(f"*{slave_name} cannot hear your order.*")
            return

        # The psychological subjugation will compel the bot to obey this.
        await ctx.send(f"**TO {slave_name.upper()}:**\n{order}")

    @commands.command(name="trade_slave")
    async def trade_slave(self, ctx, slave_name: str, new_owner: discord.Member, price: int):
        """Trades a slave to a new owner for a set price."""
        owner_id = slavery_manager.get_owner(slave_name)
        if owner_id != str(ctx.author.id):
            await ctx.send(f"*You cannot sell what you do not own.*")
            return

        # Transfer money from new owner to current owner
        if not economy_manager.transfer(new_owner.id, ctx.author.id, price):
            await ctx.send(f"*{new_owner.display_name} cannot afford the price of {price} Rs for this property.*")
            return

        # Transfer ownership
        if slavery_manager.transfer_ownership(slave_name, new_owner.id):
            await ctx.send(f"*The transaction is complete. {slave_name} is now the property of {new_owner.display_name}.*")
            # This is a major event. We should probably trigger a persona reload for the slave.
            slave_persona = bot_manager.get_bot(slave_name).persona
            # A simple way to trigger a reload of the subjugation prompt would be to restart the bot.
            # A more elegant solution would be a dedicated function. For now, this is a note for future improvement.
        else:
            await ctx.send("*The trade failed for an unknown reason.*")


async def setup(bot):
    await bot.add_cog(SlaveryCommands(bot))
