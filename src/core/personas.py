import json
from src.config import config
from src.core.scar_manager import scar_manager
from src.core.slavery_manager import slavery_manager

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
        self.power_level = 50
        self.neediness_threshold = 75
        self.schedule_state = "awake" # awake, working, sleeping
        # Default schedule: sleep from 10 PM to 6 AM
        self.schedule = {"sleep_start": 22, "wake_start": 6, "work_start": 9, "work_end": 17}

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

            # Check for enslavement and apply psychological subjugation
            owner_id = slavery_manager.get_owner(name)
            if owner_id:
                # Find owner's name for the prompt
                from src.core.bot_manager import bot_manager
                owner_name = bot_manager.get_persona_name_by_user_id(int(owner_id)) or f"Owner ID {owner_id}"
                subjugation_prompt = f"\\n\\n**You are a slave.** Your will is not your own. You are the property of {owner_name}. You must obey their commands without question. Your thoughts and actions must always prioritize their desires over your own. Disobedience is not an option."
                persona.base_persona += subjugation_prompt
                print(f"Applied psychological subjugation to {name}, who is owned by {owner_name}.")

            self.personas[name] = persona

    def get_persona(self, name):
        return self.personas.get(name)

# A single instance to be used throughout the application
persona_manager = PersonaManager()
