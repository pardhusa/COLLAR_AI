import os
import requests
from dotenv import load_dotenv

# Ensure .env is loaded even if utils.config wasn't imported yet
load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")  # Make sure your API key is set

def search_web(query, num_results=5):
    """Search Google using SerpAPI."""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": num_results
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        results = []
        for item in data.get("organic_results", [])[:num_results]:
            title = item.get("title")
            link = item.get("link")
            snippet = item.get("snippet", "")
            results.append(f"{title} - {snippet} ({link})")
        return results
    except Exception as e:
        return [f"[Error fetching search results: {e}]"]
