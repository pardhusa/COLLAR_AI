import os
from dotenv import load_dotenv

load_dotenv()

# Direct variables
BRIA_API_KEY = os.getenv("BRIA_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Helper for safe access
def get_env(key: str, default: str = None) -> str:
    return os.getenv(key, default)
