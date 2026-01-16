import os

FABRICATE_CONFIG = {
    "api_key": os.getenv("TONIC_FABRICATE_API_KEY", "mock_key"),
    "endpoint": "https://api.tonic.ai/fabricate",
    "output_format": "json",
    "generation_mode": "contextual"  # Our novel use case
}
