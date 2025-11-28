import requests
import os
import asyncio
from uuid import uuid4

class ChatterboxClient:
    def __init__(self, host="http://localhost:8020"):
        self.host = host
        self.output_dir = "data/voices_generated" # Use a separate dir for output
        os.makedirs(self.output_dir, exist_ok=True)
        # We need to know where the source voices are
        self.source_voices_dir = os.path.abspath("data/voices")
        self.available = self.check_server_availability()
        if self.available:
            print("ChatterboxClient (XTTSv2) initialized and server is available.")
        else:
            print("Warning: Chatterbox (XTTSv2) server not found. Voice features will be disabled.")

    def check_server_availability(self):
        try:
            requests.get(f"{self.host}/speakers_list", timeout=3)
            return True
        except requests.exceptions.RequestException:
            return False

    def is_available(self):
        return self.available

    async def generate_voice(self, text: str, output_filename: str, voice_name: str):
        """
        Generates an audio file from text using a specified voice sample.
        """
        if not self.available:
            return None

        source_wav_path = os.path.join(self.source_voices_dir, f"{voice_name}.wav")
        if not os.path.exists(source_wav_path):
            print(f"Error: Voice sample not found for {voice_name} at {source_wav_path}")
            return None

        # The v2 API expects a file upload, not just a name.
        files = {'speaker_wav': (f'{voice_name}.wav', open(source_wav_path, 'rb'), 'audio/wav')}
        payload = {
            "text": text,
            "language": "en"
        }

        try:
            response = await asyncio.to_thread(
                requests.post,
                f"{self.host}/tts_to_audio/",
                data=payload,
                files=files,
                timeout=60
            )
            response.raise_for_status()

            output_path = os.path.join(self.output_dir, output_filename)
            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"Generated voice for {voice_name} and saved to {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Chatterbox (XTTSv2) server: {e}")
            return None

chatterbox_client = ChatterboxClient()
