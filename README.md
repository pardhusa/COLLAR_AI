# 🤖 Collar Bone AI

A comprehensive AI assistant that can search the web, access social media, generate images, and provide intelligent responses using local AI models.

## 🚀 Features

### 🌐 Web Search
- Real-time web search using SerpAPI
- Get current information and news
- Search results integrated into responses

### 📱 Social Media Integration
- **Reddit**: Access current discussions and trends
- **Twitter/X**: Get real-time tweets and conversations
- Social media data integrated into responses

### 🎨 Image Generation
- **Stability AI**: High-quality image generation
- **Bria AI**: Alternative image generation API
- Automatic image request detection
- Multiple image formats and styles

### 💬 Intelligent Chat
- **Local AI Models**: Using Ollama (llama3, mistral, etc.)
- **Conversation Memory**: Remembers chat history
- **Streaming Responses**: Real-time token streaming
- **Context Awareness**: Uses conversation history

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd COLLAR_BONE_AI
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Ollama
Download and install Ollama from: https://ollama.ai/

Pull the models you want to use:
```bash
ollama pull llama3
ollama pull mistral
```

### 5. Set Up Environment Variables
Create a `.env` file in the root directory:

```env
# Web Search
SERP_API_KEY=your_serpapi_key_here

# Social Media
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=collar_bone_ai/1.0
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# Image Generation
STABILITY_API_KEY=your_stability_api_key
BRIA_API_KEY=your_bria_api_key

# Optional APIs
OPENAI_API_KEY=your_openai_api_key
REPLICATE_API_KEY=your_replicate_api_key
```

## 🚀 Usage

### Start the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### How to Use

1. **Choose AI Model**: Select from available Ollama models in the sidebar
2. **Enable Live Data**: Toggle web search and social media integration
3. **Chat**: Ask questions or request images
4. **Image Generation**: Use phrases like:
   - "Generate image of a sunset"
   - "Create a picture of a cat"
   - "Show me a futuristic city"

## 🔧 API Setup Guide

### SerpAPI (Web Search)
1. Go to https://serpapi.com/
2. Sign up for a free account
3. Get your API key
4. Add to `.env`: `SERP_API_KEY=your_key`

### Reddit API
1. Go to https://www.reddit.com/prefs/apps
2. Create a new app
3. Get Client ID and Secret
4. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   ```

### Twitter API
1. Go to https://developer.twitter.com/
2. Create a new app
3. Get Bearer Token
4. Add to `.env`: `TWITTER_BEARER_TOKEN=your_token`

### Stability AI (Image Generation)
1. Go to https://platform.stability.ai/
2. Sign up and get API key
3. Add credits to your account
4. Add to `.env`: `STABILITY_API_KEY=your_key`

### Bria AI (Image Generation)
1. Go to https://bria.ai/
2. Sign up and get API key
3. Add to `.env`: `BRIA_API_KEY=your_key`

## 📁 Project Structure

```
COLLAR_BONE_AI/
├── app.py                 # Main Streamlit application
├── models/
│   ├── chat_models.py     # AI chat model integration
│   └── image_generator.py # Image generation models
├── apis/
│   ├── serp_api.py        # Web search API
│   ├── reddit_api.py      # Reddit API
│   ├── twitter_api.py     # Twitter API
│   ├── stability_api.py   # Stability AI API
│   └── bria_api.py        # Bria AI API
├── memory/
│   └── memory_manager.py  # Conversation memory
├── utils/
│   └── config.py          # Configuration utilities
├── tests/
│   └── test_apis.py       # API testing
└── requirements.txt       # Python dependencies
```

## 🧪 Testing

Test your API configurations:
```bash
python -m tests.test_apis
```

## 🔍 Troubleshooting

### Ollama Connection Issues
- Make sure Ollama is running: `ollama serve`
- Check if models are downloaded: `ollama list`
- Verify connection to localhost:11434

### API Key Issues
- Check your `.env` file exists and has correct keys
- Verify API keys are valid and have proper permissions
- Some APIs require credits/account activation

### Image Generation Issues
- Stability AI requires credits
- Bria AI may need account verification
- Check API status in the sidebar

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Ollama for local AI models
- SerpAPI for web search
- Stability AI and Bria AI for image generation
- Streamlit for the web interface
