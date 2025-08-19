from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from memory.memory_manager import MemoryManager
from apis.serp_api import search_web as web_search
from apis.reddit_api import get_reddit_posts
from apis.twitter_api import get_twitter_posts
try:
    from apis.social_image_extractor import search_images_from_social_media, format_social_images_for_display
except ImportError:
    search_images_from_social_media = None
    format_social_images_for_display = None
# try:
#     from apis.stability_api import generate_stability_image
# except ImportError:
#     generate_stability_image = None

# try:
#     from apis.bria_api import generate_bria_image
# except ImportError:
#     generate_bria_image = None
import re
import json

class ChatModel:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.memory = MemoryManager()
        
        # System prompt for the AI
        self.system_prompt = """You are COLLAR AI, a helpful assistant that can:
1) Search the web for current information
2) Access social media for real-time updates
3) Provide concise, accurate, and up-to-date responses

When live data is available, always produce:
- A brief 3–5 sentence summary of the topic first
- Then 3–5 short bullet highlights (optional)
- Then a Sources section with a markdown list of title and URL for each source
- If an illustrative image URL is provided in context (e.g., Image: <url>), include a single line at the end: Image: <url>
Do NOT output image descriptions; include only a direct image URL if available. Keep the answer compact and skimmable."""

    def get_model(self, name):
        return OllamaLLM(model=name, base_url=self.base_url)

    def detect_image_request(self, user_input):
        """Detect if user explicitly requests AI image generation"""
        image_keywords = [
            'generate image', 'create image', 'make an image', 'make image',
            'draw', 'render an image', 'render image', 'generate a picture',
            'create a picture', 'make a picture'
        ]
        return any(keyword in user_input.lower() for keyword in image_keywords)

    def detect_social_image_request(self, user_input):
        """Detect if user is requesting images from social media"""
        social_image_keywords = [
            'find images', 'get images', 'show images', 'images from', 
            'pictures from', 'photos from', 'social media images',
            'reddit images', 'twitter images', 'instagram images',
            'images on', 'pictures on', 'photos on'
        ]
        return any(keyword in user_input.lower() for keyword in social_image_keywords)

    def extract_image_prompt(self, user_input):
        """Extract the image description from user input"""
        # Remove common request phrases
        prompt = user_input.lower()
        for phrase in ['generate image of', 'create image of', 'make an image of', 'make image of', 'draw', 'generate a picture of', 'create a picture of']:
            prompt = prompt.replace(phrase, '').strip()
        return prompt

    # def generate_image(self, prompt, api_preference="stability"):
    #     """Generate image using preferred API"""
    #     try:
    #         if api_preference == "stability" and generate_stability_image:
    #             return generate_stability_image(prompt)
    #         elif api_preference == "bria" and generate_bria_image:
    #             return generate_bria_image(prompt)
    #         else:
    #             # Try both APIs
    #             if generate_stability_image:
    #                 try:
    #                     return generate_stability_image(prompt)
    #                 except:
    #                     pass
    #             if generate_bria_image:
    #                 try:
    #                     return generate_bria_image(prompt)
    #                 except:
    #                     pass
    #             return ["No image generation APIs available. Please check your API keys."]
    #     except Exception as e:
    #         return [f"Error generating image: {e}"]

    def get_live_data(self, user_input):
        """Get live data from web search and social media"""
        live_data = []
        working_apis = 0
        first_image_url = None
        
        try:
            # Web search
            search_results = web_search(user_input, num_results=3)
            if search_results and not any("error" in result.lower() for result in search_results):
                live_data.append("🌐 **Web Search Results:**")
                live_data.extend([f"• {result}" for result in search_results])
                working_apis += 1
            else:
                live_data.append("⚠️ **Web Search**: API key missing or invalid. Get free key from https://serpapi.com/")
        except Exception:
            live_data.append("⚠️ **Web Search**: API key missing or invalid. Get free key from https://serpapi.com/")

        try:
            # Reddit posts
            reddit_results = get_reddit_posts(user_input, limit=3)
            if reddit_results and not any("error" in result.lower() for result in reddit_results):
                live_data.append("\n📱 **Reddit Posts:**")
                live_data.extend([f"• {result}" for result in reddit_results])
                working_apis += 1
            else:
                live_data.append("\n⚠️ **Reddit**: API credentials missing. Get free credentials from https://www.reddit.com/prefs/apps")
        except Exception:
            live_data.append("\n⚠️ **Reddit**: API credentials missing. Get free credentials from https://www.reddit.com/prefs/apps")

        try:
            # Twitter posts
            twitter_results = get_twitter_posts(user_input, limit=3)
            if twitter_results and not any("error" in result.lower() for result in twitter_results):
                live_data.append("\n🐦 **Twitter Posts:**")
                live_data.extend([f"• {result}" for result in twitter_results])
                working_apis += 1
            else:
                live_data.append("\n⚠️ **Twitter**: API key missing or invalid. Get free token from https://developer.twitter.com/")
        except Exception:
            live_data.append("\n⚠️ **Twitter**: API key missing or invalid. Get free token from https://developer.twitter.com/")

        # Try to fetch a representative image URL from social media
        try:
            if search_images_from_social_media:
                imgs = search_images_from_social_media(user_input, limit=3)
                # pick first image url if present
                for platform in imgs.get('platforms', {}).values():
                    for post in platform.get('posts', []):
                        for img in post.get('images', []):
                            if img.get('url'):
                                first_image_url = img['url']
                                raise StopIteration
        except StopIteration:
            pass
        except Exception:
            pass

        if first_image_url:
            live_data.append(f"\n🖼️ Image: {first_image_url}")

        if working_apis == 0:
            return "❌ **No live data available** - Please set up API keys for web search and social media.\n\n💡 **Quick Setup**:\n• Web Search: Get free key from https://serpapi.com/\n• Reddit: Get free credentials from https://www.reddit.com/prefs/apps\n• See API_SETUP_GUIDE.md for detailed instructions"
        
        return "\n".join(live_data)

    def get_social_images(self, user_input):
        """Get images from social media posts about a topic"""
        if not search_images_from_social_media:
            return "❌ Social image extraction not available. Please check your API keys."
        
        try:
            # Extract the topic from the user input
            # Remove common request phrases
            topic = user_input.lower()
            for phrase in ['find images', 'get images', 'show images', 'images from', 'pictures from', 'photos from', 'social media images', 'reddit images', 'twitter images', 'instagram images', 'images on', 'pictures on', 'photos on']:
                topic = topic.replace(phrase, '').strip()
            
            if not topic:
                return "❌ Please specify a topic to search for images."
            
            # Search for images
            results = search_images_from_social_media(topic, limit=5)
            
            if results["total_images"] == 0:
                return f"❌ No images found for '{topic}' on social media."
            
            # Format results for display
            return format_social_images_for_display(results)
            
        except Exception as e:
            return f"❌ Error searching for social media images: {e}"

    def generate_response_stream(self, model_name, user_input, use_live_data=False):
        """Stream response token-by-token from the model"""

        # Check if user wants social media images
        if self.detect_social_image_request(user_input):
            yield "🖼️ Searching for images from social media...\n\n"
            
            try:
                social_images = self.get_social_images(user_input)
                yield social_images
            except Exception as e:
                yield f"❌ Error searching for social media images: {e}\n"
            return

        # Check if user wants an AI-generated image
        if self.detect_image_request(user_input):
            image_prompt = self.extract_image_prompt(user_input)
            yield "🎨 Generating image for: " + image_prompt + "\n\n"
            
            try:
                images = self.generate_image(image_prompt)
                if images and not images[0].startswith("Error"):
                    yield f"✅ Image generated successfully!\n"
                    yield f"📸 Image data: {images[0][:100]}...\n\n"
                    yield "You can view the generated image in the response data."
                else:
                    yield f"❌ Failed to generate image: {images[0] if images else 'Unknown error'}\n"
                    yield "Please try again or check your API credentials."
            except Exception as e:
                yield f"❌ Image generation error: {e}\n"
            return

        # Get conversation context
        past_convo = self.memory.get_conversation(limit=5)
        context = "\n".join([f"{role}: {msg}" for role, msg in past_convo])

        # Get live data if requested
        live_data = ""
        if use_live_data:
            yield "🔍 Gathering live data...\n"
            live_data = self.get_live_data(user_input)
            yield f"📊 Live Data:\n{live_data}\n\n"

        # Build the prompt
        prompt_template = PromptTemplate(
            input_variables=["system_prompt", "context", "live_data", "user_input"],
            template="""{system_prompt}

Previous conversation:
{context}

{live_data}

User: {user_input}
Assistant:"""
        )

        prompt = prompt_template.format(
            system_prompt=self.system_prompt,
            context=context,
            live_data=live_data,
            user_input=user_input
        )

        model = self.get_model(model_name)

        # Stream tokens
        full_response = ""
        try:
            for chunk in model.stream(prompt):
                full_response += chunk
                yield chunk
        except Exception as e:
            error_msg = f"Error generating response: {e}"
            yield error_msg
            full_response = error_msg

        # Save conversation to memory
        self.memory.save_message("user", user_input)
        self.memory.save_message("assistant", full_response)
