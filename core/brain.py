import os
import time
from dotenv import load_dotenv
from groq import Groq
import google.generativeai as genai
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()

class UniversalBrain:
    def __init__(self):
        # MOCK_MODE check (Testing er somoy poisa bachabe)
        self.mock_mode = os.getenv("MOCK_MODE", "False") == "True"

        # Configure Gemini once (Optimization)
        if os.getenv("GOOGLE_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        self.gemini_disabled = False #

        print(f"🧠 Universal Brain Initialized | Mock Mode: {self.mock_mode}")

    def get_response(self, prompt, model_type="brain", max_attempts=1):
        # --- 0. MOCK MODE ---
        if self.mock_mode:
            time.sleep(0.5) 
            return "🤖 [MOCK MODE] Logic Verified.", "Mock-Model", []

        errors = []

        # ==========================================
        # 1️⃣ PRIORITY 1: GEMINI (Hackathon Star)
        # ==========================================
        if os.getenv("GOOGLE_API_KEY") and not self.gemini_disabled:
            try:
            
                model = genai.GenerativeModel("gemini-3-pro-preview")   
                
                response = model.generate_content(f"Expert Agent: {prompt}")
                return response.text, "Gemini 3 Pro (Preview)", errors 
            except Exception as e:
                
            
                self.gemini_disabled = True
                clean_error = str(e)
                if "429" in clean_error: clean_error = "Quota Exceeded (429)"
                elif "400" in clean_error: clean_error = "Bad Request (400)"
                errors.append(f"Gemini: {clean_error}")

        
        elif self.gemini_disabled:
             errors.append("Gemini: Skipped (Circuit Breaker Active)")

        
        else:
            errors.append("Gemini: Key Missing")

        # ==========================================
        # 2️⃣ PRIORITY 2: GROQ (Llama 3)
        # ==========================================
        if os.getenv("GROQ_API_KEY"):
            try:
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800 
                )
                return completion.choices[0].message.content, "Llama 3 (Groq)", errors
            except Exception as e:
                errors.append(f"Groq: {str(e)}")
        else:
            errors.append("Groq: Key Missing")

        # ==========================================
        # 3️⃣ PRIORITY 3: HUGGING FACE (Qwen/Phi)
        # ==========================================
        if os.getenv("HF_TOKEN"):
            try:
                client = InferenceClient(api_key=os.getenv("HF_TOKEN"))
                response = client.chat_completion(
                    model="Qwen/Qwen2.5-7B-Instruct",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                return response.choices[0].message.content, "Qwen 2.5 (HF)", errors
            except Exception as e:
                errors.append(f"HF: {str(e)}")
        else:
            errors.append("HF: Key Missing")

        # ❌ ALL FAILED
        return f"🚨 ALL SYSTEMS FAILED. Errors: {errors}", "System Crash", errors

# --- TEST AREA (Run directly to check) ---
if __name__ == "__main__":
    brain = UniversalBrain()
    print("\n📝 Testing Connection...")
    reply = brain.get_response("Hello! Are you working?", model_type="fast")
    print(f"🤖 Output: {reply}")