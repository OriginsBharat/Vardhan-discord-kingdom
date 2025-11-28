import asyncio
import random
import discord
import json
from datetime import datetime
from src.core.personas import persona_manager
from src.economic_system.loan_manager import loan_manager
from src.economic_system.economy_manager import economy_manager
from src.core.world_state.event_ai import EventAI
from src.ai_services.comfyui_client import comfyui_client
from src.ai_services.ollama_client import ollama_client
from src.ai_services.chatterbox_client import chatterbox_client

class Scheduler:
    def __init__(self, bot_manager):
        self.bot_manager = bot_manager
        self.event_ai = EventAI(bot_manager)
        self.running = False

    async def _schedule_loop(self):
        """The main asynchronous loop that triggers events."""
        minute_counter = 0
        while self.running:
            await asyncio.sleep(60)
            minute_counter += 1
            print(f"[Scheduler] Heartbeat: Minute {minute_counter}")

            # Every Minute: Check personal schedules
            self.check_schedules()

            # Every 5 Minutes: Check neediness levels
            if minute_counter % 5 == 0:
                print("[Scheduler] Checking neediness levels...")
                await self.check_neediness()

            # Every 10 Minutes: Check for defaulted loans
            if minute_counter % 10 == 0:
                print("[Scheduler] Checking for defaulted loans...")
                loan_manager.check_for_defaults()

            # Every 20 Minutes: Trigger Autonomous Action Manager
            # For now, let's make this simple. A bot might create art.
            if minute_counter % 20 == 0:
                print("[Scheduler] Triggering Autonomous Action Manager...")
                await self.trigger_autonomous_action()

            # Every 30 Minutes: Trigger Event AI
            if minute_counter % 30 == 0:
                print("[Scheduler] Triggering Event AI...")
                await self.event_ai.trigger_event()

            # Daily (at 23:55)
            if minute_counter > 0 and minute_counter % 1440 == 1435:
                print("[Scheduler] Triggering Master's Journal generation...")
                await self.generate_journal()

            # Daily (at midnight)
            if minute_counter > 0 and minute_counter % 1440 == 0:
                print("[Scheduler] Resetting daily market cycles...")
                economy_manager.reset_market_cycles()

    async def check_neediness(self):
        master_user = self.bot_manager.get_master_user()
        if not master_user:
            return

        for persona in persona_manager.personas.values():
            if persona.emotional_sliders.get("neediness", 0) > persona.neediness_threshold:
                bot_instance = self.bot_manager.get_bot(persona.name)
                if not bot_instance:
                    continue

                print(f"{persona.name}'s neediness is high! Attempting to seduce the Master.")

                seduction_prompt = "You desperately miss the Master. Your neediness has crossed a threshold. Send him a direct message to get his attention. Be seductive, be alluring. You can try to impress him by writing him erotica, creating a beautiful piece of art for him, or sending him a unique voice message expressing your feelings."

                seduction_message = await ollama_client.generate_text(persona.base_prompt, seduction_prompt)

                try:
                    # Decide what to send
                    action = random.choice(["text", "art", "voice"])

                    if action == "art":
                        art_prompt = f"A beautiful, seductive image of {persona.name} for the Master."
                        image_path = await comfyui_client.generate_image(art_prompt)
                        if image_path:
                            await master_user.send(seduction_message, file=discord.File(image_path))
                        else:
                            await master_user.send(seduction_message) # Fallback to text

                    elif action == "voice" and chatterbox_client.is_available():
                        voice_prompt = f"Create a short, seductive voice message from {persona.name} to the Master, expressing longing and desire."
                        voice_text = await ollama_client.generate_text(persona.base_prompt, voice_prompt)
                        voice_path = await chatterbox_client.generate_voice(voice_text, f"{persona.name.lower()}_seduction.wav")
                        if voice_path:
                            await master_user.send(seduction_message, file=discord.File(voice_path))
                        else:
                            await master_user.send(seduction_message)

                    else: # Default to text
                        await master_user.send(seduction_message)

                    # Reset neediness after sending
                    persona.emotional_sliders["neediness"] = 0

                except Exception as e:
                    print(f"Failed to send neediness DM from {persona.name}: {e}")

    def start(self):
        if not self.running:
            self.running = True
            asyncio.create_task(self._schedule_loop())
            print("World Scheduler has started with all triggers active.")

    async def trigger_autonomous_action(self):
        """A random bot performs an autonomous action, which could be simple (like art) or complex (a goal-driven plan)."""
        persona = random.choice(list(persona_manager.personas.values()))
        bot_instance = self.bot_manager.get_bot(persona.name)
        guild = bot_instance.guilds[0] if bot_instance and bot_instance.guilds else None
        if not guild: return

        # 25% chance to pursue a long-term goal, 75% for a simple action
        if random.random() < 0.25 and hasattr(persona, 'long_term_goal'):
            print(f"[{persona.name}] is evaluating their long-term goal: {persona.long_term_goal}")

            # Use the LLM to generate a simple, actionable step towards the goal
            planning_prompt = f"Your long-term goal is: '{persona.long_term_goal}'. What is a single, simple, concrete action you can take right now to make progress towards this goal? The action should be something you can post in a public channel, like the #jobs board. Formulate the action as a command you would type. For example: !post_job I need a skilled blacksmith to forge a legendary sword. Reward: 10000 Rs."

            action_plan = await ollama_client.generate_text(persona.base_prompt, planning_prompt)

            # Find a channel to post the action
            job_channel = discord.utils.get(guild.channels, name="jobs")
            if job_channel and action_plan.strip().startswith("!"):
                print(f"[{persona.name}] is taking a goal-driven action: {action_plan}")
                # We need to find the bot's own user object to fake the command context
                bot_user = guild.get_member(bot_instance.user.id)
                if bot_user:
                    # Create a fake message context
                    Message = type("Message", (), {"author": bot_user, "content": action_plan, "channel": job_channel})
                    await bot_instance.process_commands(Message())
        else:
            # Default to a simple, creative action
            art_channel = discord.utils.get(guild.channels, name="sfw-art") # or nsfw-art
            if not art_channel: return

            prompt = await ollama_client.generate_text(persona.base_prompt, "You feel inspired to create a piece of art. Describe the art you want to create in a single, descriptive sentence.")
            image_path = await comfyui_client.generate_image(prompt)

            if image_path:
                await art_channel.send(f"*{persona.name} was struck by inspiration and created this:*", file=discord.File(image_path))

    async def generate_journal(self):
        """Maya generates the Master's daily interactive journal entry."""
        maya_persona = persona_manager.get_persona("Maya")
        master_user = self.bot_manager.get_master_user()
        if not maya_persona or not master_user: return

        # Mock event data for demonstration. In a full implementation, this would be pulled from a database of recent events.
        mock_events = [
            {"summary": "Tri successfully negotiated a trade deal, boosting her confidence.", "bot_name": "Tri", "emotion_to_affect": "confidence"},
            {"summary": "Dvi lost a sparring match in the Coliseum, leaving him frustrated.", "bot_name": "Dvi", "emotion_to_affect": "frustration"},
            {"summary": "Asht unveiled a new sculpture that was met with public adoration, fueling his creative spirit.", "bot_name": "Asht", "emotion_to_affect": "creativity"},
        ]

        event_summary_text = "\n\n- " + "\n- ".join([e["summary"] for e in mock_events])

        journal_prompt = f"Based on these events, write a beautiful, narrative journal entry for the Master:\n{event_summary_text}"
        journal_entry_text = await ollama_client.generate_text(maya_persona.base_prompt, journal_prompt)

        # Create the interactive embed
        embed = discord.Embed(
            title=f"The Master's Journal: {datetime.now().strftime('%Y-%m-%d')}",
            description=f"{journal_entry_text}\n\n*React to influence the world.*",
            color=discord.Color.from_str(maya_persona.aura_color)
        )
        embed.set_footer(text="❤️ = Approve | 😂 = Find Amusing | 😠 = Disapprove | 😢 = Express Sympathy")

        # Hide the event metadata in the description for the reaction listener
        hidden_metadata = json.dumps(mock_events)
        embed.description += f"<!--{hidden_metadata}-->"

        try:
            journal_channel = discord.utils.get(master_user.guild.channels, name="mayas-journal")
            if journal_channel:
                 await journal_channel.send(embed=embed)
            else: # Fallback to DM
                dm_channel = await self.bot_manager.get_or_create_dm_channel(master_user, "mayas-journal")
                await dm_channel.send(embed=embed)
        except Exception as e:
            print(f"Error sending journal entry: {e}")

    def check_schedules(self):
        """Updates each bot's state based on the current time."""
        current_hour = datetime.now().hour
        for persona in persona_manager.personas.values():
            schedule = persona.schedule
            new_state = "awake" # Default state

            # Check for sleeping hours (e.g., 22:00 to 06:00)
            if schedule["sleep_start"] > schedule["wake_start"]: # Overnight schedule
                if current_hour >= schedule["sleep_start"] or current_hour < schedule["wake_start"]:
                    new_state = "sleeping"
            else: # Same-day schedule
                if schedule["sleep_start"] <= current_hour < schedule["wake_start"]:
                    new_state = "sleeping"

            # Check for working hours if not sleeping
            if new_state != "sleeping":
                if schedule["work_start"] <= current_hour < schedule["work_end"]:
                    new_state = "working"

            if persona.schedule_state != new_state:
                persona.schedule_state = new_state
                print(f"[{persona.name}] has changed state to: {new_state}")

    def stop(self):
        self.running = False
        print("World Scheduler has stopped.")
