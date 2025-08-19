import os
import praw  # Python Reddit API Wrapper
from dotenv import load_dotenv

load_dotenv()

# Load credentials from environment variables
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_SECRET")  # Changed to match your .env file
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "collar_bone_ai/1.0")

def get_reddit_posts(query, limit=3):
    """
    Search Reddit for a query and return a list of post titles + URLs.
    Requires Reddit API credentials in .env
    """
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        results = []
        for submission in reddit.subreddit("all").search(query, limit=limit):
            results.append(f"{submission.title} ({submission.url})")

        return results

    except Exception as e:
        return [f"Error fetching Reddit posts: {e}"]
