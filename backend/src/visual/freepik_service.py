import requests
import base64
import io
from src.config.freepik_config import FREEPIK_CONFIG

class FreepikService:
    def __init__(self):
        self.api_key = FREEPIK_CONFIG.get("api_key")
        self.base_url = FREEPIK_CONFIG.get("base_url")
        self.model = FREEPIK_CONFIG.get("default_model", "mystic")

    def generate_image(self, prompt: str) -> str:
        """
        Generate an image using Freepik Mystic API.
        Returns the base64 string of the generated image.
        """
        if not self.api_key:
            print("Warning: FREEPIK_API_KEY not found.")
            return None

        url = f"{self.base_url}/mystic"
        
        headers = {
            "x-freepik-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "num_images": 1
        }
        
        # #region agent log
        import json, time
        try:
            with open("/Users/nihalnihalani/Desktop/Github/Orchestrator/.cursor/debug.log", "a") as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"verify-sponsors","hypothesisId":"freepik-api","timestamp":int(time.time()*1000),"message":"Calling Freepik","data":{"prompt":prompt, "has_key": bool(self.api_key)}})+"\n")
        except: pass
        # #endregion

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)

            # #region agent log
            try:
                with open("/Users/nihalnihalani/Desktop/Github/Orchestrator/.cursor/debug.log", "a") as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"verify-sponsors","hypothesisId":"freepik-api","timestamp":int(time.time()*1000),"message":"Freepik Response","data":{"status":response.status_code}})+"\n")
            except: pass
            # #endregion

            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    item = data["data"][0]
                    if "base64" in item:
                        return item["base64"]
                    elif "url" in item:
                        # Download URL and convert to base64 for consistency
                        img_resp = requests.get(item["url"])
                        return base64.b64encode(img_resp.content).decode('utf-8')
                
                return None
            else:
                print(f"Freepik API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Freepik Service Exception: {e}")
            return None
