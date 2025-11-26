import requests
import json

class OllamaClient:
    def __init__(self, host="http://localhost:11434"):
        self.host = host
        self.model_name = "dolphin-2.2.1-mistral:7b-q4_K_M"
        print("OllamaClient initialized.")

    def generate_text(self, persona_prompt, user_prompt, context_history=None):
        """
        Generates text using the Ollama API.

        :param persona_prompt: The base persona of the bot.
        :param user_prompt: The specific user message or action the bot is responding to.
        :param context_history: A list of previous messages for conversational context.
        :return: The generated text string.
        """
        full_prompt = f"{persona_prompt}\\n\\n"

        if context_history:
            full_prompt += "\\n".join(context_history) + "\\n"

        full_prompt += f"User: {user_prompt}\\nAI:"

        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False,  # We want the full response at once
                },
                timeout=120 # 2 minute timeout
            )
            response.raise_for_status()

            # The response is a JSON object with the generated text
            return response.json()["response"].strip()

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            return "I am currently unable to think. The connection to my mind has been severed."

# A single instance for the application
ollama_client = OllamaClient()
