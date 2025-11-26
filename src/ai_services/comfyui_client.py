import websocket
import uuid
import json
import urllib.request
import urllib.parse
import os
import random

class ComfyUIClient:
    def __init__(self, server_address="127.0.0.1:8188", output_dir="data/images"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        print("ComfyUIClient initialized.")

    def _get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url = f"http://{self.server_address}/view?{urllib.parse.urlencode(data)}"
        with urllib.request.urlopen(url) as response:
            return response.read()

    def _queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def _get_history(self, prompt_id):
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def generate_image(self, positive_prompt, negative_prompt="bad quality, worst quality", model="sd_xl_base_1.0.safetensors"):
        # Basic SDXL Text-to-Image Workflow
        workflow = {
            "4": {
                "inputs": {"ckpt_name": model},
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {"width": 1024, "height": 1024, "batch_size": 1},
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {"text": positive_prompt, "clip": ["4", 1]},
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {"text": negative_prompt, "clip": ["4", 1]},
                "class_type": "CLIPTextEncode"
            },
            "8": {
                "inputs": {
                    "seed": random.randint(0, 0xffffffffffffffff),
                    "steps": 25,
                    "cfg": 8,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "9": {
                "inputs": {"samples": ["8", 0], "vae": ["4", 2]},
                "class_type": "VAEDecode"
            },
            "10": {
                "inputs": {"filename_prefix": "MyAIWorld", "images": ["9", 0]},
                "class_type": "SaveImage"
            }
        }

        try:
            prompt_id = self._queue_prompt(workflow)['prompt_id']

            # Use websocket to get the final image filename
            ws = websocket.WebSocket()
            ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")

            final_image_data = None
            while True:
                out = ws.recv()
                if isinstance(out, str):
                    message = json.loads(out)
                    if message.get('type') == 'executed' and message.get('data', {}).get('prompt_id') == prompt_id:
                        history = self._get_history(prompt_id)[prompt_id]
                        for node_id, node_output in history['outputs'].items():
                            if 'images' in node_output:
                                image = node_output['images'][0]
                                final_image_data = self._get_image(image['filename'], image['subfolder'], image['type'])
                        break
            ws.close()

            if final_image_data:
                image_path = os.path.join(self.output_dir, f"{uuid.uuid4()}.png")
                with open(image_path, "wb") as f:
                    f.write(final_image_data)
                print(f"Image generated and saved to {image_path}")
                return image_path

            return None

        except Exception as e:
            print(f"Error connecting to or using ComfyUI: {e}")
            return None

import random
comfyui_client = ComfyUIClient()
