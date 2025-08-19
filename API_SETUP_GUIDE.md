# 🔑 API Setup Guide for Collar Bone AI

## 🚨 **Missing API Keys Detected**

Your Collar Bone AI system needs these API keys to work properly. Here's how to get them:

## 1. 🌐 **SerpAPI (Web Search) - FREE**

**Status**: ❌ Missing `SERP_API_KEY`

### How to get it:
1. Go to https://serpapi.com/
2. Click "Sign Up" (it's free)
3. Create an account
4. Get your API key from the dashboard
5. Add to your `.env` file:
   ```
   SERP_API_KEY=your_serpapi_key_here
   ```

**Free Tier**: 100 searches per month

---

## 2. 📱 **Reddit API - FREE**

**Status**: ❌ Missing `REDDIT_CLIENT_SECRET`

### How to get it:
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the details:
   - **Name**: `collar_bone_ai`
   - **Type**: `script`
   - **Description**: `AI assistant for web search and social media`
   - **About URL**: (leave blank)
   - **Redirect URI**: `http://localhost:8501`
4. Click "Create App"
5. Copy the **Client ID** (under the app name)
6. Copy the **Client Secret** (labeled "secret")
7. Add to your `.env` file:
   ```
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_client_secret_here
   REDDIT_USER_AGENT=collar_bone_ai/1.0
   ```

**Free Tier**: Unlimited (with rate limits)

---

## 3. 🐦 **Twitter API - FREE**

**Status**: ⚠️ API key exists but needs verification

### How to get it:
1. Go to https://developer.twitter.com/
2. Sign up for a developer account
3. Create a new app
4. Get your **Bearer Token**
5. Add to your `.env` file:
   ```
   TWITTER_BEARER_TOKEN=your_bearer_token_here
   ```

**Free Tier**: 500,000 tweets per month

---

## 4. 🎨 **Image Generation APIs - PAID**

**Status**: ✅ Both keys are configured

- **Stability AI**: Requires credits (you have the key)
- **Bria AI**: Requires account verification (you have the key)

---

## 📝 **Complete .env File Example**

```env
# Web Search
SERP_API_KEY=your_serpapi_key_here

# Social Media
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=collar_bone_ai/1.0
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# Image Generation
STABILITY_API_KEY=your_stability_api_key_here
BRIA_API_KEY=your_bria_api_key_here
```

---

## 🧪 **Test Your Setup**

After adding the missing keys, run this command to test:

```bash
python check_apis.py
```

You should see:
```
🎉 All APIs are working correctly!
```

---

## 💡 **Quick Start (Minimal Setup)**

If you want to test the system with minimal setup:

1. **Get SerpAPI key** (most important for web search)
2. **Get Reddit credentials** (for social media)
3. **Skip Twitter** for now (optional)

The system will work with just web search and Reddit!

---

## 🆘 **Need Help?**

- Check the main README.md for detailed instructions
- Run `python check_apis.py` to diagnose issues
- All APIs have free tiers available
