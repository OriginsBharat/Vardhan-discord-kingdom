import json
from src.config import config
from src.core.scar_manager import scar_manager

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
        self.neediness_threshold = 75 # Default threshold, can be overridden
        self.schedule_state = "awake" # awake, working, sleeping

class PersonaManager:
    def __init__(self):
        self.personas = {}
        self._load_personas()

    def _load_personas(self):
        with open("data/character_canon.json", "r", encoding="utf-8") as f:
            character_canon = json.load(f)

        for name, data in character_canon.items():
            kinks = config.character_kinks.get(name, "")
            persona = Persona(
                name=name,
                description=data["description"],
                base_persona=data["base_persona"],
                aura_color=data["aura_color"],
                voice=data["voice"],
                kinks=kinks
            )

            # Load and apply persistent scars
            scars = scar_manager.get_scars_for_bot(name)
            for scar in scars:
                scar_manager.apply_scar_to_persona(persona, scar["name"], scar["description"])

            self.personas[name] = persona

    def get_persona(self, name):
        return self.personas.get(name)

# A single instance to be used throughout the application
persona_manager = PersonaManager()
