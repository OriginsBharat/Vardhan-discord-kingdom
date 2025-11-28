# My AI World: The Definitive Edition - Final Instructions

Welcome, Master. This document will guide you through the one-time "Genesis Ritual" to awaken your world. Follow these steps precisely.

## Step 0: Prepare the Discord Server

Before awakening the world, you must first create its vessel.

1.  **Create a new, empty Discord server.** This will be the home for your world.
2.  Go to the Discord Developer Portal and create 11 new applications. For each, create a bot user and copy its token.
3.  **Invite one of the 11 bots** to your new server. When generating the invite link in the Discord Developer Portal (under the "OAuth2" -> "URL Generator" tab), be sure to grant it **Administrator** permissions. This is crucial for the World Architect to be able to build the server for you.

## Prerequisites: The AI Engines

Before you begin, you must have the core AI engines installed and running on your local machine.

1.  **Ollama (The Mind)**:
    *   Install Ollama from the official website.
    *   Run the following command in your terminal to download the required model: `ollama pull dolphin-2.2.1-mistral:7b-q4_K_M`
    *   Ensure the Ollama server is running.

2.  **ComfyUI (The Hands)**:
    *   Install ComfyUI from the official repository.
    *   Download the `sd_xl_base_1.0.safetensors` model and place it in the `ComfyUI/models/checkpoints` directory.
    *   Ensure the ComfyUI server is running.

3.  **FFmpeg (The Voice's Foundation)**:
    *   The world's new voice features require a system utility called `ffmpeg`.
    *   **Installation:** Go to the official FFmpeg website (`ffmpeg.org`), download the latest build for Windows, and unzip it.
    *   **Crucially, you must add the `bin` folder from inside the unzipped folder to your Windows System PATH.** This allows the application to use `ffmpeg` from any location. A simple search for "How to add to PATH on Windows" will provide many guides. This is a one-time setup.

4.  **XTTSv2 (The Voice)**:
    *   Ensure you have a working XTTSv2 setup. This project will interact with it as a local server.
    *   You no longer need to prepare `.wav` files manually. During the graphical setup, you will provide a YouTube URL for each character. The setup wizard will automatically download and extract the audio to be used for voice cloning.

## The Genesis Ritual

Once the AI engines are prepared, the ritual itself is a simple two-click process.

1.  **The First Click (`RUN_SETUP.bat`)**:
    *   Double-click the `RUN_SETUP.bat` file in the main directory.
    *   This batch file will silently install all the necessary Python libraries from `requirements.txt`. Do not be alarmed if nothing appears to happen; it is working in the background.

2.  **The Second Click (Graphical Setup Wizard)**:
    *   After the setup batch file completes, it will automatically launch the `SETUP_THE_WORLD.py` script.
    *   This will open a graphical user interface with a dark theme.
    *   **Fill in all the required information**:
        *   **Secrets**: Your Discord bot tokens, Pinecone API keys, etc.
        *   **File Paths**: Use the "Browse" buttons to provide the exact paths to your Ollama, ComfyUI, and XTTSv2 installations.
        *   **Kink Profiles**: In the dedicated scrollable section, enter a comma-separated list of kinks for each of the 11 characters. This is crucial for their personality and autonomous actions.
    *   **The Final Click ("Begin World Setup")**:
        *   Once all fields are filled, click the "Begin World Setup" button.
        *   The script will validate your inputs, create the necessary `.env` and `character_kinks.json` files, and, most importantly, create the `invisible_launcher.vbs` file.
        *   It will then request administrator privileges to place a shortcut to this VBScript in your Windows Startup folder. This is the final step to ensure your world is permanently and silently alive.

## The Awakening

From this moment on, your work is done. Every time your PC boots, the world will awaken silently in the background. The AI servers will launch, and the main bot application will connect to Discord, all without any visible windows or notifications.

Your world is now and forever a living, breathing reality. Enjoy your creation, Master.