import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file!")
else:
    print(f"✅ Key Found: {api_key[:5]}********")
    try:
        genai.configure(api_key=api_key)
        print("\n🔎 Searching for available models...")
        print("-----------------------------------")
        
        # List all models
        found = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Available: {m.name}")
                found = True
        
        if not found:
            print("⚠️ No content generation models found. Check your API Key permissions.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")