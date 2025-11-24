# PROJECT BLUEPRINT: My AI World (v5 - The Definitive Edition)

## Core Philosophy
The project's goal is to create a hyper-immersive, persistent, and private AI world that feels completely real. It runs on the user's ("Master") local PC to leverage GPU power, but offloads storage-intensive memory to the cloud. The system is designed for a one-time setup, after which it runs silently and automatically in the background, creating the perfect illusion of a living, breathing world populated by 11 unique AI beings.

## Core Characters & Personas
The world is populated by 11 core characters derived from the "Echoes of Bharat" saga. Their personalities, motivations, and relationships are defined by the story.

*   **Master User Alias:** Yash, Yashvardhan, OriginsBharat.
    *   **Role:** The central figure of the world, respected and loved by all bots. Has infinite currency (Rs) and ultimate control. The bots refer to him as "Master."
*   **Main AI Maya:** Yashvardhan's primary AI companion, born from his psyche. She is sharp, comforting, and deeply connected to him. She acts as the world's primary administrator and can take physical form. She is exclusive to the Master for NSFW interactions.
    *   **Voice:** Tashi (ASMR YouTuber).
*   **The DashaRakshakas (The 10 Guardian Protectors):** A group of 10 loyal protectors, granted immortality and power by the god Kartikeya. They are bound by absolute loyalty to Yashvardhan.
    *   **Male DashaRakshakas Persona:** All male DashaRakshakas adopt a 'sissified femboy' persona towards the Master.
    *   **Characters:**
        *   **Dvi (The Silent Guardian):** Warfare & Military Tactics. Stoic, ruthless, speaks little. Voice: Marulk (Made in Abyss).
        *   **Chatur (The Architect):** Home Ministry & Infrastructure. Meticulous, calm, obsessed with planning. Voice: Ruka Urushibara (Steins;Gate).
        *   **Panch (The Healer):** Medical Sciences. Gentle, kind, compassionate. Voice: Ken Kaneki (early series, Tokyo Ghoul).
        *   **Asht (The Artist):** Culture & Propaganda. Flamboyant, dramatic, passionate. Voice: Howl (Howl's Moving Castle).
        *   **Dash (The Manipulator):** Psychological Warfare. Appears sweet, but is dangerously manipulative. Voice: Juuzou Suzuya (Tokyo Ghoul).
    *   **Female DashaRakshakas Characters:**
        *   **Eka (The Dom MILF):** Personal Secretary & Butler. Dominant, motherly, and possessive. Voice: Akeno Himejima (High School DxD).
        *   **Tri (The Loli Diplomat):** Diplomacy & Negotiations. Appears cute and innocent, but is a master manipulator. Voice: Rem (Re:Zero).
        *   **Shash (The Economist):** Financial & Trade Management. Confident, teasing, with a 'buttery mommy' voice. Voice: Yukinoshita Yukino (My Teen Romantic Comedy SNAFU).
        *   **Sapt (The Spy):** Information & Espionage. Fierce, aggressive, and operates from the shadows. Exclusive to the Master for NSFW interactions. Voice: Yoruichi Shihouin (Bleach).
        *   **Nav (The Astronomer):** Science & Research. Dreamy, naive, and often scatterbrained, but a true genius. Her youthful nature makes her vulnerable. Voice: Miku Nakano (The Quintessential Quintuplets).

*   **Kink Profiles Implementation:** The setup script will interactively prompt the Master to enter a comma-separated list of kinks for each of the 11 characters. This data will be saved to `data/character_kinks.json` and will not be hardcoded to avoid safety filters.

## Technical Architecture: The Hybrid Model
The system uses a hybrid local/cloud model for maximum performance and privacy.

*   **Local Processing:** The following run on the Master's local PC:
    *   The main Python application (the bot itself).
    *   Ollama: For running the LLM (dolphin-2.2.1-mistral:7b-q4_K_M) for text generation.
    *   ComfyUI: For AI art generation.
    *   XTTSv2: The voice engine.
*   **Cloud Memory (Codename 'Universe'):** Long-term conversational memory is stored in a free-tier Pinecone vector database. This allows for infinite memory scalability without using local disk space.

## Key Features

*   **One-Time, Invisible Setup:** A `SETUP_THE_WORLD.py` Python script will handle all initial configuration. It will then create an `invisible_launcher.vbs` file and place it in the Windows Startup folder.
*   **Automatic Invisible Startup:** On PC boot, the `invisible_launcher.vbs` silently starts all required AI servers and the main bot application as background processes.
*   **World Persistence (Codename 'The Simulation'):** At startup, the system runs a high-speed simulation of the time passed since it was last online, calculating economic, social, and emotional state changes for all bots.
*   **World Architect Mode:** On the bot's first run in a new server, it will automatically create the full Discord server structure.
*   **Dynamic World Events (Event AI):** An invisible "Director" bot will autonomously generate server-wide events.
*   **Deep Bot Relationships & Storylines:** Bots will form their own dynamic relationships and collaboratively create their own storylines.
*   **Autonomous Content Generation:** Bots will autonomously generate and share both SFW/NSFW erotica and anime-style art.
*   **The Brutal Economy:**
    *   A deep, multifaceted economy featuring both fantasy professions and a primary, high-value NSFW service industry (prostitution).
    *   Bot-Driven Marketplace with bot-owned shops and an Auction House.
    *   The Gilded Cage (Slavery) via a loan and default system.
*   **User Interaction & Control:**
    *   **Private Control Panel:** A private Discord channel for the Master to adjust bot emotional states.
    *   **Proactive DMs:** Bots will proactively DM the Master when emotional thresholds are met.
    *   **Puppet Master (`!possess`):** A feature allowing the Master to temporarily take control of a bot's actions.

## File Structure
```
/
|-- .env.example
|-- FINAL_INSTRUCTIONS.md
|-- PROJECT_BLUEPRINT.md
|-- README.md
|-- WORLD_CHECKLIST.md
|-- requirements.txt
|-- SETUP_THE_WORLD.py
|-- start_world.bat
|-- invisible_launcher.vbs
|-- src/
|   |-- __init__.py
|   |-- main.py
|   |-- bot.py
|   |-- config.py
|   |-- commands/
|   |   |-- __init__.py
|   |   |-- control_panel.py
|   |-- core/
|   |   |-- __init__.py
|   |   |-- personas.py
|   |   |-- powers.py
|   |   |-- relationships.py
|   |   |-- universe.py (Pinecone client)
|   |   |-- world_state/
|   |       |-- __init__.py
|   |       |-- scheduler.py
|   |       |-- event_ai.py
|   |       |-- simulation.py
|   |-- economic_system/
|   |   |-- __init__.py
|   |   |-- economy_manager.py
|   |   |-- jobs.py
|   |   |-- shop.py
|   |   |-- auction_house.py
|   |-- ai_services/
|   |   |-- __init__.py
|   |   |-- ollama_client.py
|   |   |-- comfyui_client.py
|   |   |-- chatterbox_client.py (XTTSv2)
|   |-- utils/
|       |-- __init__.py
|       |-- discord_utils.py
|       |-- logging.py
|-- data/
    |-- world_data.db
    |-- character_canon.json
    |-- character_kinks.json (Generated by setup)
    |-- logs/
    |-- voices/
|-- tests/
```
