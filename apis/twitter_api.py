import os
import requests
from dotenv import load_dotenv

load_dotenv()

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def get_twitter_posts(query, limit=3):
    """
    Search Twitter/X for recent tweets containing the query.
    Requires Twitter API Bearer Token in .env
    """
    try:
        headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
        url = "https://api.twitter.com/2/tweets/search/recent"
        params = {
            "query": query,
            "max_results": min(max(limit, 10), 100),  # Twitter API requires 10-100
            "tweet.fields": "text,created_at"
        }

        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()

        tweets = [tweet["text"] for tweet in data.get("data", [])]
        return tweets or ["No recent tweets found."]

    except Exception as e:
        return [f"Error fetching tweets: {e}"]
