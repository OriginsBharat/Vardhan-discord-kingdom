import asyncio
import discord
import os
import signal
from src.bot import MyAIWorldBot
from src.config import config
from src.core.world_state.scheduler import Scheduler
from src.core.world_state.simulation import Simulation
from src.economic_system.economy_manager import economy_manager
from src.core.bot_manager import bot_manager

# Event to signal that all bots are ready
all_bots_ready = asyncio.Event()

async def run_bot(bot_token, persona_name):
    bot = MyAIWorldBot(persona_name)

    @bot.event
    async def on_ready():
        bot_manager.register_bot(bot)
        print(f"{bot.persona.name} has connected and is ready.")
        # Check if all bots have registered
        if len(bot_manager.bots) == len(config.discord_tokens):
            all_bots_ready.set()

    @bot.event
    async def on_guild_join(guild):
        # Only the primary bot (Maya) should be the architect
        if bot.persona.name == "Maya":
            flag_path = "data/world_created.flag"
            if not os.path.exists(flag_path):
                print("World creation flag not found. Beginning server construction.")
                # We use the function defined at the bottom of the file
                await create_server_structure(guild)
            else:
                print("World already created. Skipping server construction.")

    await bot.start(bot_token)


async def main():
    simulation = Simulation(economy_manager)
    simulation.run_offline_progression()

    scheduler = None # Initialize scheduler as None

    def handle_shutdown(signum, frame):
        print("Shutting down gracefully...")
        if scheduler:
            scheduler.stop()
        simulation.save_current_timestamp()

        # Close all bot connections
        for bot in bot_manager.bots.values():
            asyncio.create_task(bot.close())

    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    tasks = []
    for bot_name, token in config.discord_tokens.items():
        if token:
            tasks.append(asyncio.create_task(run_bot(token, bot_name)))

    if not tasks:
        print("Error: No bot tokens found. The world cannot awaken.")
        return

    print("Waiting for all bots to connect and report ready...")
    await all_bots_ready.wait()
    print("All bots are ready. Initializing core systems.")

    await bot_manager.initialize_master_user()

    scheduler = Scheduler(bot_manager)
    scheduler.start()

    print("--- My AI World is now fully operational. ---")
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    async def create_server_structure(guild):
        print(f"Entering World Architect Mode for server: {guild.name}")
        for channel in await guild.fetch_channels(): await channel.delete()
        for category in guild.categories: await category.delete()
        citadel = await guild.create_category("THE CITADEL")
        await guild.create_text_channel("announcements", category=citadel)
        await guild.create_text_channel("lore", category=citadel)
        sfw_chat = await guild.create_text_channel("sfw-chat", category=citadel)
        await guild.create_text_channel("sfw-art", category=citadel)
        await guild.create_voice_channel("The Town Square", category=citadel)
        await guild.create_text_channel("bot-commands-list", category=citadel)
        market = await guild.create_category("THE MARKET DISTRICT")
        await guild.create_text_channel("jobs", category=market)
        await guild.create_text_channel("bot-owned-shops", category=market)
        await guild.create_text_channel("auction-house", category=market)
        await guild.create_text_channel("bank-of-vardhan", category=market)
        sapt_overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_member(config.master_user_id): discord.PermissionOverwrite(read_messages=True)}
        await guild.create_text_channel("the-black-market", category=market, overwrites=sapt_overwrites)
        await guild.create_voice_channel("The Trading Floor", category=market)
        homes = await guild.create_category("CHARACTER HOMES")
        for char_name in config.character_names: await guild.create_text_channel(f"{char_name.lower()}-s-playroom", category=homes)
        await guild.create_voice_channel("The Living Quarters", category=homes)
        velvet = await guild.create_category("THE VELVET DISTRICT")
        await guild.create_text_channel("public-nsfw-roleplay", category=velvet)
        await guild.create_text_channel("erotica", category=velvet)
        await guild.create_text_channel("nsfw-art", category=velvet)
        await guild.create_voice_channel("The Whispering Suite", category=velvet)
        await guild.create_voice_channel("Private Room 1", category=velvet)
        judgement = await guild.create_category("THE HALL OF JUDGEMENT")
        await guild.create_text_channel("the-courthouse", category=judgement)
        await guild.create_text_channel("the-jail", category=judgement)
        await guild.create_voice_channel("The Deliberation Chamber", category=judgement)
        arena = await guild.create_category("THE ARENA OF SOULS")
        await guild.create_text_channel("the-coliseum", category=arena)
        await guild.create_voice_channel("The Arena", category=arena)
        master_overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), guild.get_member(config.master_user_id): discord.PermissionOverwrite(read_messages=True)}
        chambers = await guild.create_category("MASTER'S PRIVATE CHAMBERS", overwrites=master_overwrites)
        master_control_channel = await guild.create_text_channel("master-control", category=chambers)
        await guild.create_text_channel("mayas-journal", category=chambers)
        await master_control_channel.send("**World Architecture Complete.**\nMaster, a final manual step is required for security.\nPlease grant the 'Sapt' bot access to the `#the-black-market` channel and deny access to all other users.")
        print("World Architect Mode finished.")
        with open("data/world_created.flag", "w") as f: f.write("True")

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("The world is shutting down...")
