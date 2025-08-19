# Setup Guide

## Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
# API Keys
STABILITY_API_KEY=your_stability_api_key_here
BRIA_API_KEY=your_bria_api_key_here
SERPAPI_KEY=your_serpapi_key_here

# Social Media API Keys
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_SECRET=your_reddit_secret_here
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
```

## Getting API Keys

### Stability AI
1. Go to https://platform.stability.ai/
2. Sign up or log in
3. Navigate to your account settings
4. Generate an API key
5. Copy the key to your `.env` file

### Other APIs
- **Bria AI**: Visit their platform to get an API key
- **SerpAPI**: Get from https://serpapi.com/
- **Reddit**: Create an app at https://www.reddit.com/prefs/apps
- **Twitter**: Get from Twitter Developer Portal

## Testing

After setting up your `.env` file, you can test the APIs:

```bash
python -m tests.test_apis
``` 