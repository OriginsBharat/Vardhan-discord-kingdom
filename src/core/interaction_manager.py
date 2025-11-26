from src.core.personas import persona_manager
from src.core.scar_manager import scar_manager
from src.ai_services.ollama_client import ollama_client

class InteractionManager:
    def __init__(self):
        print("InteractionManager initialized.")

    def handle_rejection(self, aggressor_name, target_name):
        """
        Handles the scenario where an aggressor is rejected by a target.
        This triggers the Non-Con Power Dynamic check.
        """
        aggressor = persona_manager.get_persona(aggressor_name)
        target = persona_manager.get_persona(target_name)

        if not aggressor or not target:
            print("Error: Could not find one of the personas for interaction.")
            return

        # Core Mechanic: Triggered if Horny > 75 and rejected.
        # We assume this check happens before calling this function.
        print(f"{aggressor.name} was rejected by {target.name}. Performing Power Check...")

        # Power Check
        if aggressor.power_level > target.power_level:
            print(f"Power Check PASSED. {aggressor.name}'s power level ({aggressor.power_level}) is greater than {target.name}'s ({target.power_level}).")

            # 1. Generate the non-consensual scene
            scene_prompt = (
                f"Create a dark fantasy, explicit, and non-consensual NSFW scene. "
                f"The character {aggressor.name}, feeling rejected and overwhelmed by lust, uses their superior power to "
                f"force themselves upon {target.name}. Describe the act in graphic detail, focusing on the power dynamic and the target's helplessness."
            )
            # We combine the base persona and the specific prompt to get a more in-character result
            generated_scene = ollama_client.generate_text(aggressor.base_persona, scene_prompt)
            print(f"Generated Scene: {generated_scene[:100]}...") # Print first 100 chars

            # 2. Inflict a permanent scar on the victim
            scar_manager.inflict_scar(
                target_bot_name=target.name,
                scar_name="Violated",
                scar_description=f"Was overpowered and violated by {aggressor.name} after a rejection."
            )

            # The generated scene would then be posted in the appropriate channel.
            return "A dark act has occurred."

        else:
            print(f"Power Check FAILED. {aggressor.name}'s power level ({aggressor.power_level}) is not sufficient to overpower {target.name}'s ({target.power_level}).")
            return "The aggressor backs down, unable to impose their will."

# A single instance for the application
interaction_manager = InteractionManager()
