import requests
import json
import asyncio

class OllamaClient:
    def __init__(self, host="http://localhost:11434"):
        self.host = host
        self.model_name = "dolphin-2.2.1-mistral:7b-q4_K_M"
        print("OllamaClient initialized.")

    async def generate_text(self, persona_prompt, user_prompt, context_history=None, max_retries=3):
        """
        Generates text using the Ollama API with retry logic.
        """
        full_prompt = f"{persona_prompt}\\n\\n"
        if context_history:
            full_prompt += "\\n".join(context_history) + "\\n"
        full_prompt += f"User: {user_prompt}\\nAI:"

        for attempt in range(max_retries):
            try:
                # Using asyncio.to_thread to run the synchronous requests call in a separate thread
                response = await asyncio.to_thread(
                    requests.post,
                    f"{self.host}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": full_prompt,
                        "stream": False,
                    },
                    timeout=120
                )
                response.raise_for_status()
                return response.json()["response"].strip()
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to Ollama (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    return "I seem to be having trouble thinking right now... The connection to my mind feels distant."
                await asyncio.sleep(2 ** attempt)  # Exponential backoff: 1, 2, 4 seconds

        return "I am currently unable to think. The connection to my mind has been severed."

# A single instance for the application
ollama_client = OllamaClient()
