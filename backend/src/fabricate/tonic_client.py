import requests
from typing import Dict, Any, List, Optional
from src.config.fabricate_config import FABRICATE_CONFIG

class FabricateClient:
    """
    Client for interacting with the Tonic Fabricate API.
    Used for generating synthetic conversation data based on profile context.
    """
    
    def __init__(self):
        self.api_key = FABRICATE_CONFIG.get("api_key")
        self.endpoint = FABRICATE_CONFIG.get("endpoint")
        
        if not self.api_key:
            print("Warning: TONIC_FABRICATE_API_KEY not found in environment variables.")

    def generate(self, prompt: str) -> List[Dict[str, Any]]:
        """
        Send a generation request to Tonic Fabricate.
        """
        if not self.api_key or self.api_key == "mock_key":
            print("Warning: Using mock Tonic Fabricate client (no valid API key).")
            return []

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "format": "json",
            "count": 1 # We usually want one cohesive generation
        }
        
        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error calling Tonic Fabricate API: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Exception calling Tonic Fabricate API: {e}")
            return []
