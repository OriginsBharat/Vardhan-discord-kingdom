import asyncio
import discord
import os
from src.bot import MyAIWorldBot
from src.config import config

async def create_server_structure(guild):
    """
    Creates the full Discord server structure based on the blueprint.
    This function should be called only once when the bot joins a new server.
    """
    print(f"Entering World Architect Mode for server: {guild.name}")

    # Clear existing channels and categories
    for channel in await guild.fetch_channels():
        await channel.delete()
    for category in guild.categories:
        await category.delete()

    # THE CITADEL
    citadel = await guild.create_category("THE CITADEL")
    await guild.create_text_channel("announcements", category=citadel)
    await guild.create_text_channel("lore", category=citadel)
    await guild.create_text_channel("sfw-chat", category=citadel)
    await guild.create_text_channel("sfw-art", category=citadel)
    await guild.create_voice_channel("The Town Square", category=citadel)
    await guild.create_text_channel("bot-commands-list", category=citadel)

    # THE MARKET DISTRICT
    market = await guild.create_category("THE MARKET DISTRICT")
    await guild.create_text_channel("jobs", category=market)
    await guild.create_text_channel("bot-owned-shops", category=market)
    await guild.create_text_channel("auction-house", category=market)
    await guild.create_text_channel("bank-of-vardhan", category=market)
    # Hidden channel for Sapt
    sapt_overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.get_member(config.master_user_id): discord.PermissionOverwrite(read_messages=True)
    }
    await guild.create_text_channel("the-black-market", category=market, overwrites=sapt_overwrites)
    await guild.create_voice_channel("The Trading Floor", category=market)

    # CHARACTER HOMES
    homes = await guild.create_category("CHARACTER HOMES")
    for char_name in config.character_names:
        await guild.create_text_channel(f"{char_name.lower()}-s-playroom", category=homes)
    await guild.create_voice_channel("The Living Quarters", category=homes)

    # THE VELVET DISTRICT
    velvet = await guild.create_category("THE VELVET DISTRICT")
    await guild.create_text_channel("public-nsfw-roleplay", category=velvet)
    await guild.create_text_channel("erotica", category=velvet)
    await guild.create_text_channel("nsfw-art", category=velvet)
    await guild.create_voice_channel("The Whispering Suite", category=velvet)
    await guild.create_voice_channel("Private Room 1", category=velvet)

    # THE HALL OF JUDGEMENT
    judgement = await guild.create_category("THE HALL OF JUDGEMENT")
    await guild.create_text_channel("the-courthouse", category=judgement)
    await guild.create_text_channel("the-jail", category=judgement)
    await guild.create_voice_channel("The Deliberation Chamber", category=judgement)

    # THE ARENA OF SOULS
    arena = await guild.create_category("THE ARENA OF SOULS")
    await guild.create_text_channel("the-coliseum", category=arena)
    await guild.create_voice_channel("The Arena", category=arena)

    # MASTER'S PRIVATE CHAMBERS
    master_overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.get_member(config.master_user_id): discord.PermissionOverwrite(read_messages=True)
    }
    chambers = await guild.create_category("MASTER'S PRIVATE CHAMBERS", overwrites=master_overwrites)
    master_control_channel = await guild.create_text_channel("master-control", category=chambers)
    await guild.create_text_channel("mayas-journal", category=chambers)

    # Post-setup instructions for the Master
    await master_control_channel.send(
        "**World Architecture Complete.**\n"
        "Master, a final manual step is required for security.\n"
        "Please grant the 'Sapt' bot access to the `#the-black-market` channel and deny access to all other users."
    )

    print("World Architect Mode finished.")
    # Create the flag file to prevent this from running again
    with open("data/world_created.flag", "w") as f:
        f.write("True")


async def run_bot(bot_token, persona_name):
    bot = MyAIWorldBot(persona_name)

    @bot.event
    async def on_guild_join(guild):
        # Only the primary bot (Maya) should be the architect
        if persona_name == "Maya":
            flag_path = "data/world_created.flag"
            if not os.path.exists(flag_path):
                print("World creation flag not found. Beginning server construction.")
                await create_server_structure(guild)
            else:
                print("World already created. Skipping server construction.")

    await bot.start(bot_token)


async def main():
    tasks = []
    for bot_name, token in config.discord_tokens.items():
        if token:
            tasks.append(run_bot(token, bot_name))
        else:
            print(f"Warning: No token found for {bot_name}. This bot will not be started.")

    if not tasks:
        print("Error: No bot tokens found in .env file. The world cannot awaken.")
        return

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("The world is shutting down...")
