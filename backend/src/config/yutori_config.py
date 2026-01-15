import os
from dotenv import load_dotenv

load_dotenv()

YUTORI_CONFIG = {
    "api_key": os.getenv("YUTORI_API_KEY"),
    "browser_mode": "cloud",  # Use cloud browser
    "timeout": 60,  # 60 second timeout
    "decision_mode": "intelligent"  # Enable intelligent prioritization
}
