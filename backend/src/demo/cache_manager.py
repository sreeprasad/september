import json
import os
from typing import Dict, Any, Optional

class CacheManager:
    """
    Manages cached briefing data for reliable demos.
    """
    
    def __init__(self, cache_dir: str = "backend/data/cache"):
        # Adjust path if needed
        if not os.path.exists(cache_dir):
             # Try relative path
             if os.path.exists("backend"):
                 cache_dir = "backend/data/cache"
             else:
                 # Assume we are in backend dir
                 cache_dir = "data/cache"
                 
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_cache_key(self, linkedin_url: str) -> str:
        """
        Generate a safe filename from the URL.
        """
        # Simple extraction of username or unique identifier
        if "linkedin.com/in/" in linkedin_url:
            username = linkedin_url.split("linkedin.com/in/")[-1].strip("/").replace("/", "_")
            return f"profile_{username}.json"
        return "profile_default.json"

    def save_to_cache(self, linkedin_url: str, data: Dict[str, Any]):
        """
        Save briefing data to cache.
        """
        filename = self.get_cache_key(linkedin_url)
        filepath = os.path.join(self.cache_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
            
    def get_from_cache(self, linkedin_url: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from cache if it exists.
        """
        filename = self.get_cache_key(linkedin_url)
        filepath = os.path.join(self.cache_dir, filename)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    return json.load(f)
            except Exception:
                return None
        return None
