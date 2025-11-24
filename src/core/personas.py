import json
from src.config import config

class Persona:
    def __init__(self, name, description, base_persona, aura_color, voice, kinks):
        self.name = name
        self.description = description
        self.base_persona = base_persona
        self.aura_color = int(aura_color, 16)
        self.voice = voice
        self.kinks = kinks
        self.psychological_scars = []
        self.emotional_sliders = {
            "neediness": 0,
            "horny": 0,
            "dominance": 50,
            "submissiveness": 50,
        }
        self.power_level = 50  # Default power level, can be adjusted in canon if needed

class PersonaManager:
    def __init__(self):
        self.personas = {}
        self._load_personas()

    def _load_personas(self):
        with open("data/character_canon.json", "r", encoding="utf-8") as f:
            character_canon = json.load(f)

        for name, data in character_canon.items():
            kinks = config.character_kinks.get(name, "")
            self.personas[name] = Persona(
                name=name,
                description=data["description"],
                base_persona=data["base_persona"],
                aura_color=data["aura_color"],
                voice=data["voice"],
                kinks=kinks
            )

    def get_persona(self, name):
        return self.personas.get(name)

# A single instance to be used throughout the application
persona_manager = PersonaManager()
