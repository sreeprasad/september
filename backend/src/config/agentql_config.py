import os
from dotenv import load_dotenv

load_dotenv()

AGENTQL_CONFIG = {
    "api_key": os.getenv("AGENTQL_API_KEY"),
    "extraction_mode": "semantic",  # Use semantic extraction
    "output_format": "json",
    "include_confidence_scores": True
}
