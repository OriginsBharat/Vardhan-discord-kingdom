import discord
from discord.ext import commands
from src.core.npc_manager import npc_manager
from src.economic_system.economy_manager import economy_manager
from src.ai_services.ollama_client import ollama_client
from src.config import config
import asyncio

class VelvetDistrict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list_services")
    async def list_services(self, ctx):
        # This command can only be used in the Black Market, run by Sapt.
        if ctx.channel.name != "the-black-market" or self.bot.persona.name != "Sapt":
            return

        available_npcs = npc_manager.get_available_npcs()
        if not available_npcs:
            await ctx.send("*The house is quiet. No companions are available at the moment.*")
            return

        embed = discord.Embed(
            title="Velvet District Services",
            description="The following companions are available for a private engagement.",
            color=self.bot.persona.aura_color
        )

        for npc in available_npcs:
            embed.add_field(
                name=npc['name'],
                value=f"*“{npc['persona']}”*\n**Status:** {npc['status'].capitalize()}",
                inline=False
            )

        embed.set_footer(text="To hire a companion, use the !hire <name> <price> command.")
        await ctx.send(embed=embed)

    @commands.command(name="hire")
    async def hire_npc(self, ctx, name: str, price: int):
        if ctx.channel.name != "the-black-market" or self.bot.persona.name != "Sapt":
            return

        npc = npc_manager.get_npc_by_name(name)
        if not npc:
            await ctx.send(f"*I do not know anyone by the name of {name}.*")
            return

        if npc['status'] != 'available':
            await ctx.send(f"*{name} is currently... occupied. Please wait.*")
            return

        # The hirer pays Sapt (as the brothel keeper)
        if not economy_manager.transfer(ctx.author.id, self.bot.user.id, price):
            await ctx.send("*Your funds are insufficient for such pleasures.*")
            return

        npc_manager.set_npc_status(name, "busy")
        await ctx.send(f"*Excellent. I have taken your payment of {price} Rs. I will arrange a private room for you and {name}. Please wait for my signal...*")

        # --- Begin Impersonation Logic ---
        try:
            # Create a private channel for the session
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.author: discord.PermissionOverwrite(read_messages=True),
                self.bot.user: discord.PermissionOverwrite(read_messages=True) # Sapt needs access
            }
            category = discord.utils.get(ctx.guild.categories, name="THE VELVET DISTRICT")
            channel_name = f"private-room-{name.lower()}-{ctx.author.name.lower()}"
            session_channel = await ctx.guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

            # Create a webhook for the NPC
            webhook = await session_channel.create_webhook(name=name)

            await session_channel.send(f"The room is ready. {name} will be with you shortly. The session will last for 10 messages. To end it sooner, type `!end_session`.")

            conversation_history = []
            for _ in range(5): # 5 exchanges (10 messages total)
                # NPC speaks first
                prompt = f"You are {name}, your persona is: '{npc['persona']}'. You are in a private room with {ctx.author.name}. Initiate or continue an erotic roleplay scene. This is the conversation so far:\n{''.join(conversation_history)}\nYour response:"
                npc_response = await ollama_client.generate_text(prompt, "")
                await webhook.send(npc_response)
                conversation_history.append(f"{name}: {npc_response}\n")

                # Wait for the user's reply
                def check(m):
                    return m.channel == session_channel and m.author == ctx.author

                try:
                    user_message = await self.bot.wait_for('message', check=check, timeout=600.0)
                    if user_message.content.lower() == '!end_session':
                        break
                    conversation_history.append(f"{ctx.author.name}: {user_message.content}\n")
                except asyncio.TimeoutError:
                    await session_channel.send("*It seems your companion has grown tired of waiting...*")
                    break

            # End of session
            await session_channel.send(f"*{name} gives a slight bow.* Our time is up. I hope you were satisfied.")
            await asyncio.sleep(10)

            # Cleanup
            await webhook.delete()
            await session_channel.delete()

        except Exception as e:
            print(f"An error occurred during the NPC session: {e}")
        finally:
            # Ensure NPC is always set back to available
            npc_manager.set_npc_status(name, "available")
            print(f"NPC {name} has finished their session and is now available.")


async def setup(bot):
    # This cog should only be loaded on the Sapt bot for command handling
    if bot.persona.name == "Sapt":
        await bot.add_cog(VelvetDistrict(bot))
