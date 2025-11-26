import requests
import os
from uuid import uuid4

class ChatterboxClient:
    def __init__(self, host="http://localhost:8020"): # Default port for XTTSv2 servers
        self.host = host
        self.output_dir = "data/voices"
        os.makedirs(self.output_dir, exist_ok=True)
        print("ChatterboxClient (XTTSv2) initialized.")

    def generate_voice(self, text, voice_name):
        """
        Generates an audio file from text using a specified voice.

        :param text: The text to be spoken.
        :param voice_name: The name of the voice to use (e.g., "Eka", "Tri").
                           This assumes the XTTSv2 server has voice files named accordingly.
        :return: The file path to the generated .wav file.
        """
        try:
            response = requests.post(
                f"{self.host}/tts",
                json={
                    "text": text,
                    "speaker_wav": f"{voice_name}.wav", # Assumes server has these files
                    "language": "en",
                },
                timeout=60
            )
            response.raise_for_status()

            # Save the audio file
            output_filename = f"{voice_name}_{uuid4()}.wav"
            output_path = os.path.join(self.output_dir, output_filename)
            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"Generated voice for {voice_name} and saved to {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Chatterbox (XTTSv2) server: {e}")
            return None

# A single instance for the application
chatterbox_client = ChatterboxClient()
