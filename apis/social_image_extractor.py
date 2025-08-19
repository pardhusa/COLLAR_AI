import requests
import re
import os
from typing import List, Dict
from utils.config import get_env

def extract_images_from_reddit_posts(query: str, limit: int = 5) -> List[Dict]:
    """
    Extract images from Reddit posts about a specific topic
    
    Args:
        query (str): Search query
        limit (int): Number of posts to search
    
    Returns:
        List[Dict]: List of posts with images
    """
    try:
        import praw
        
        reddit = praw.Reddit(
            client_id=get_env("REDDIT_CLIENT_ID"),
            client_secret=get_env("REDDIT_SECRET"),
            user_agent="collar_bone_ai/1.0"
        )
        
        results = []
        for submission in reddit.subreddit("all").search(query, limit=limit):
            post_data = {
                "title": submission.title,
                "url": submission.url,
                "author": str(submission.author),
                "score": submission.score,
                "subreddit": str(submission.subreddit),
                "created_utc": submission.created_utc,
                "images": []
            }
            
            # Check if post has images
            if hasattr(submission, 'is_self') and not submission.is_self:
                # Direct image links
                if submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    post_data["images"].append({
                        "url": submission.url,
                        "type": "direct_image"
                    })
                
                # Gallery posts
                elif hasattr(submission, 'gallery_data') and submission.gallery_data:
                    for item in submission.gallery_data['items']:
                        media_id = item['media_id']
                        if hasattr(submission, 'media_metadata') and media_id in submission.media_metadata:
                            metadata = submission.media_metadata[media_id]
                            if 's' in metadata and 'u' in metadata['s']:
                                post_data["images"].append({
                                    "url": metadata['s']['u'].replace('&amp;', '&'),
                                    "type": "gallery_image"
                                })
                
                # Imgur links
                elif 'imgur.com' in submission.url:
                    # Try to get direct image from Imgur
                    imgur_id = submission.url.split('/')[-1].split('.')[0]
                    direct_url = f"https://i.imgur.com/{imgur_id}.jpg"
                    post_data["images"].append({
                        "url": direct_url,
                        "type": "imgur_image"
                    })
            
            # Only include posts with images
            if post_data["images"]:
                results.append(post_data)
        
        return results
        
    except Exception as e:
        return [{"error": f"Reddit image extraction error: {e}"}]

def extract_images_from_twitter_posts(query: str, limit: int = 5) -> List[Dict]:
    """
    Extract images from Twitter posts about a specific topic
    
    Args:
        query (str): Search query
        limit (int): Number of posts to search
    
    Returns:
        List[Dict]: List of posts with images
    """
    try:
        headers = {"Authorization": f"Bearer {get_env('TWITTER_BEARER_TOKEN')}"}
        url = "https://api.twitter.com/2/tweets/search/recent"
        params = {
            "query": f"{query} has:images",  # Only tweets with images
            "max_results": min(max(limit, 10), 100),
            "tweet.fields": "text,created_at,author_id,attachments",
            "expansions": "attachments.media_keys",
            "media.fields": "url,preview_image_url,type"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        tweets = data.get("data", [])
        media = {item["media_key"]: item for item in data.get("includes", {}).get("media", [])}
        
        for tweet in tweets:
            if "attachments" in tweet and "media_keys" in tweet["attachments"]:
                tweet_images = []
                for media_key in tweet["attachments"]["media_keys"]:
                    if media_key in media:
                        media_item = media[media_key]
                        if media_item["type"] in ["photo", "animated_gif"]:
                            image_url = media_item.get("url") or media_item.get("preview_image_url")
                            if image_url:
                                tweet_images.append({
                                    "url": image_url,
                                    "type": media_item["type"]
                                })
                
                if tweet_images:
                    results.append({
                        "text": tweet["text"],
                        "author_id": tweet["author_id"],
                        "created_at": tweet["created_at"],
                        "images": tweet_images
                    })
        
        return results
        
    except Exception as e:
        return [{"error": f"Twitter image extraction error: {e}"}]

def search_images_from_social_media(query: str, platforms: List[str] = None, limit: int = 5) -> Dict:
    """
    Search for images from social media posts about a specific topic
    
    Args:
        query (str): Search query
        platforms (List[str]): List of platforms to search ('reddit', 'twitter')
        limit (int): Number of posts per platform
    
    Returns:
        Dict: Results from all platforms
    """
    if platforms is None:
        platforms = ['reddit', 'twitter']
    
    results = {
        "query": query,
        "total_images": 0,
        "platforms": {}
    }
    
    if 'reddit' in platforms:
        try:
            reddit_results = extract_images_from_reddit_posts(query, limit)
            results["platforms"]["reddit"] = {
                "posts": reddit_results,
                "image_count": sum(len(post.get("images", [])) for post in reddit_results if "error" not in post)
            }
            results["total_images"] += results["platforms"]["reddit"]["image_count"]
        except Exception as e:
            results["platforms"]["reddit"] = {"error": str(e), "image_count": 0}
    
    if 'twitter' in platforms:
        try:
            twitter_results = extract_images_from_twitter_posts(query, limit)
            results["platforms"]["twitter"] = {
                "posts": twitter_results,
                "image_count": sum(len(post.get("images", [])) for post in twitter_results if "error" not in post)
            }
            results["total_images"] += results["platforms"]["twitter"]["image_count"]
        except Exception as e:
            results["platforms"]["twitter"] = {"error": str(e), "image_count": 0}
    
    return results

def format_social_images_for_display(results: Dict) -> str:
    """
    Format social media image results for display
    
    Args:
        results (Dict): Results from search_images_from_social_media
    
    Returns:
        str: Formatted string for display
    """
    if not results or "platforms" not in results:
        return "No images found."
    
    output = [f"🖼️ **Images found for '{results['query']}': {results['total_images']} total**\n"]
    
    for platform, data in results["platforms"].items():
        if "error" in data:
            output.append(f"❌ **{platform.title()}**: {data['error']}")
            continue
        
        if data["image_count"] == 0:
            output.append(f"⚠️ **{platform.title()}**: No images found")
            continue
        
        output.append(f"✅ **{platform.title()}**: {data['image_count']} images found")
        
        for i, post in enumerate(data["posts"][:3], 1):  # Show first 3 posts
            if platform == "reddit":
                output.append(f"  📍 **{post['title'][:50]}...**")
                output.append(f"  👤 u/{post['author']} | ⬆️ {post['score']} | 📍 r/{post['subreddit']}")
                for img in post["images"][:2]:  # Show first 2 images per post
                    output.append(f"  🖼️ {img['url']}")
            elif platform == "twitter":
                output.append(f"  📍 **{post['text'][:50]}...**")
                for img in post["images"][:2]:  # Show first 2 images per post
                    output.append(f"  🖼️ {img['url']}")
            output.append("")
    
    return "\n".join(output)
