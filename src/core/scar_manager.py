from src.core.personas import persona_manager

class ScarManager:
    def __init__(self):
        # In a real system, scars would be persisted in a database.
        print("ScarManager initialized.")

    def inflict_scar(self, target_bot_name, scar_name, scar_description):
        """
        Inflicts a permanent psychological scar on a bot.
        """
        persona = persona_manager.get_persona(target_bot_name)
        if not persona:
            print(f"Error: Could not find persona for {target_bot_name} to inflict scar.")
            return

        scar = {
            "name": scar_name,
            "description": scar_description,
        }

        persona.psychological_scars.append(scar)
        print(f"Inflicted scar '{scar_name}' on {target_bot_name}. Their psyche is now permanently altered.")

        # This is where the magic happens: the scar is appended to the base persona.
        # This ensures all future interactions with the LLM are influenced by this trauma.
        persona.base_persona += f"\\n\\n**Psychological Scar: {scar_name}** - {scar_description}"

# A single instance for the application
scar_manager = ScarManager()
