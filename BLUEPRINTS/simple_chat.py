from langchain_ollama import OllamaLLM

# Paste the Colab public URL here:
OLLAMA_URL = "https://vinyl-refers-double-prescribed.trycloudflare.com"

def get_model_choice():
    print("\nChoose model:")
    print("1. LLaMA3 (8B)")
    print("2. Mistral")
    choice = input("Enter 1 or 2: ").strip()
    return "llama3:8b" if choice == "1" else "mistral"

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    model_name = get_model_choice()
    chat_model = OllamaLLM(model=model_name, base_url=OLLAMA_URL)
    response = chat_model.invoke(user_input)
    print(f"{model_name}:", response)