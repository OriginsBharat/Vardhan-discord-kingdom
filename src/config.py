import os
from dotenv import load_dotenv
import json

load_dotenv()

class Config:
    def __init__(self):
        # Load character canon to get names
        with open("data/character_canon.json", "r", encoding="utf-8") as f:
            self.character_names = list(json.load(f).keys())

        # Load tokens for all bots
        self.discord_tokens = {
            name: os.getenv(f"{name.upper()}_TOKEN") for name in self.character_names
        }

        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
        self.master_user_id = int(os.getenv("MASTER_USER_ID")) if os.getenv("MASTER_USER_ID") else None

        self.ollama_path = os.getenv("OLLAMA_PATH")
        self.comfyui_path = os.getenv("COMFYUI_PATH")

        # Load kinks
        try:
            with open("data/character_kinks.json", "r", encoding="utf-8") as f:
                self.character_kinks = json.load(f)
        except FileNotFoundError:
            self.character_kinks = {name: "" for name in self.character_names}

config = Config()
