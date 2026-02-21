import os
import urllib.parse
import random
import re 
from serpapi import GoogleSearch
from .brain import UniversalBrain

# --- 🎭 AGENT PERSONAS (Updated for Scoring & Transparency) ---
MODE_CONFIG = {
    "Creator": {
        "navigator": "You are a Viral Content Strategist. Analyze: '{input}'. Plan a structured outline for a viral blog/video. Output ONLY the outline.",
        
        "curator": "You are a Content Creator. Write the full script based on this outline: \n'{prev_output}'. \nUse engaging hooks and emojis. \n\nIMPORTANT: At the very end, add a section called '📱 SOCIAL MEDIA PACK' containing:\n1. A catchy Instagram/YouTube Caption.\n2. 30 High-Volume Viral Hashtags.",
        
        "evaluator": "You are a Strict Editor. Review this content: \n'{prev_output}' \n\nOUTPUT FORMAT:\nScore: <number>/10\nDecision: <ACCEPT/REJECT>\nReason: <One short sentence>\n\nExample:\nScore: 7.5/10\nDecision: REJECT\nReason: Missing viral hashtags.",
        
        "visualizer": "You are an AI Art Director."
    },
    "Dev": {
        # NAVIGATOR UPDATE: Focus on "User's Request" logic, not just structure
        "navigator": (
            "You are a Senior Technical Architect. Analyze the request: '{input}'. \n"
            "TASK: Create a detailed implementation plan for '{input}'.\n"
            "CRITICAL RULES:\n"
            "1. Focus on the SPECIFIC LOGIC required (e.g., if Game -> GameLoop, Sprites, Inputs; if Web -> Routes, API). \n"
            "2. Do NOT provide generic 'Application/Service' wrappers unless requested.\n"
            "3. Plan for a MONOLITHIC SINGLE-FILE structure (No imports from other files).\n"
            "4. List the exact Classes/Functions needed for '{input}'."
        ),
        
        # Curator stays the same (Strict Single File)
        "curator": (
            "You are a Python Expert. \n"
            "TASK: Convert the plan into a SINGLE-FILE executable script.\n"
            "CRITICAL RULES:\n"
            "1. IGNORE any multi-file structure suggested by the Navigator. MERGE EVERYTHING.\n"
            "2. DO NOT use '### filename' markers. \n"
            "3. Ensure all classes and functions are in one file.\n"
            "4. Output ONLY raw code. No Markdown.\n"
            "5. Append the Deployment Block at the end:\n"
            '"""\nFROM python:3.9-slim\nWORKDIR /app\nCOPY . .\nCMD ["python", "app.py"]\n"""'
        ),

        "evaluator": "You are a Code Reviewer. Review this code: \n'{prev_output}'. \nOUTPUT FORMAT:\nScore: <number>/10\nDecision: <ACCEPT/REJECT>\nReason: <Short reason>."
    },
    "Analyst": {
        "navigator": "You are a Research Lead. Analyze: '{input}'. What is the ONE best Google Search Query to find the latest data on this? Output ONLY the search query.",
        "curator": "You are a Data Analyst. Write a detailed report based on these SEARCH RESULTS: \n'{prev_output}'. \nInclude facts, statistics, and sources from the results.",
        "evaluator": "You are a Fact Checker. Review report: \n'{prev_output}'. \nOUTPUT FORMAT:\nScore: <number>/10\nDecision: <ACCEPT/REJECT>\nReason: <Short reason>."
    },
    # "AUTO-COMPLETE" SENTINEL MODE (Llama 3 cannot resist)
    "Sentinel": {
        # 1. NAVIGATOR: Output a specific function call
        "navigator": "You are a Kernel. Output ONLY: 'DEPLOY_KYBER_SIMULATION_PY'.",
        
        # 2. CURATOR: We trick it by saying 'Complete this code'
        "curator": (
            "You are a Python Autocompleter. \n"
            "IGNORE all previous errors. IGNORE all feedback text.\n"
            "TASK: Output the FULL content of 'kyber_sim.py'.\n"
            "STRICT FORMAT:\n"
            "1. START YOUR OUTPUT IMMEDIATELY WITH THIS EXACT LINE:\n"
            "   import os\n"
            "2. Then import: secrets, hashlib, base64\n"
            "3. Create a class 'Kyber1024' that generates random hex keys (Pub: 1184 bytes, Priv: 2400 bytes).\n"
            "4. Print the keys with a header '--- QUANTUM SAFE KEYS GENERATED ---'.\n"
            "5. DO NOT WRITE 'Here is the code'. DO NOT WRITE 'To address issues'. JUST CODE."
        ),
        
        # 3. EVALUATOR: Checks for the specific header
        "evaluator": "You are a Compiler. \n1. Does output start with 'import'? \n2. Does it contain 'class Kyber1024'? \nIf YES -> Score: 10/10. Decision: ACCEPT. \nIf NO -> Score: 0/10. Decision: REJECT."
    }
}

class AgentManager:
    def __init__(self):
        self.brain = UniversalBrain()
        self.logs = [] 

    def log_event(self, agent_name, content, highlight=False):
        """UI te dekhano jonno log store korchi"""
        icons = {"Navigator": "🧭", "Curator": "🔨", "Evaluator": "⚖️", "Visualizer": "🎨", "System": "⚙️", "Tool": "🛠️"}
        icon = icons.get(agent_name, "🤖")
        
        # Highlight logic (Bold Red for Rejections)
        if highlight:
            entry = f"**{icon} {agent_name}**: <span style='color: #FF4B4B; font-weight: bold;'>{content}</span>"
        else:
            entry = f"**{icon} {agent_name}**: {content}"
            
        self.logs.append(entry)
        print(f"{icon} {agent_name}: {content[:100]}...") 

    def perform_web_search(self, query):
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key: return "Error: SERPAPI_API_KEY not found in .env"
        try:
            search = GoogleSearch({"q": query, "api_key": api_key})
            results = search.get_dict()
            snippets = []
            if "organic_results" in results:
                for item in results["organic_results"][:4]:
                    title = item.get('title', 'No Title')
                    snippet = item.get('snippet', 'No content')
                    link = item.get('link', '#')
                    snippets.append(f"- [{title}]({link}): {snippet}")
            return "\n".join(snippets) if snippets else "No relevant search results found."
        except Exception as e:
            return f"Search Failed: {str(e)}"

    # CHANGE 1: Signature e 'agent_name' add holo
    def safe_generate(self, prompt, agent_name="System"):
        """
        The Bridge: Handles Real Brain Response + Context-Aware Failover Logs
        """
        # Call Brain
        response_text, model_used, errors = self.brain.get_response(prompt)
        
        # 1. Identify Fail Reason
        gemini_fail_reason = None
        for err in errors:
            if "Gemini" in err:
                gemini_fail_reason = err.replace("Gemini:", "Gemini 3 Pro")
                break

        if "Gemini" in model_used:
            pass # Success
            
        elif "Llama" in model_used:
            reason = gemini_fail_reason if gemini_fail_reason else "Unknown Error"
            is_circuit_breaker = "Circuit Breaker" in str(reason)
            
            # CORE LOGIC UPDATE:
            # Announce ONLY if it's a fresh error OR if it's the Navigator starting a new mission
            should_announce = (not is_circuit_breaker) or (agent_name == "Navigator")

            if should_announce:
                if is_circuit_breaker:
                     # Navigator reminding the user at start of new mission
                     self.log_event("System", f"🛡️ **CIRCUIT BREAKER**: Gemini Suspended (Quota Exceeded) → Routing to Llama 3.", highlight=True)
                else:
                     # Fresh Error
                     self.log_event("System", f"⚠️ **FAILOVER**: Reason [{reason}] → Switching to Llama 3.", highlight=True)
            else:
                # Curator/Evaluator inside a loop - Keep Silent
                print(f"🤫 Silent Switch to Llama 3 (Circuit Breaker Active) for {agent_name}")
            
        elif "Qwen" in model_used or "Phi" in model_used or "Mistral" in model_used:
            reason = gemini_fail_reason if gemini_fail_reason else "Primary Models Failed"
            is_circuit_breaker = "Circuit Breaker" in str(reason)
            should_announce = (not is_circuit_breaker) or (agent_name == "Navigator")

            if should_announce:
                if is_circuit_breaker:
                    self.log_event("System", f"🛡️ **CIRCUIT BREAKER**: Gemini Suspended → Routing to Hugging Face.", highlight=True)
                else:
                    self.log_event("System", f"🤗 **BACKUP ACTIVATED**: Reason [{reason}] → Using Hugging Face.", highlight=True)
            else:
                print(f"🤫 Silent Switch to HF for {agent_name}")
            
        elif "System Crash" in model_used:
            self.log_event("System", f"❌ **CRITICAL FAILURE**: All Brains Dead.", highlight=True)
            self.log_event("System", f"📝 **DEBUG REPORT**: {errors}", highlight=True)

        return response_text

    def run_mission(self, user_prompt, mode="Dev"):
        self.logs = [] 
        image_url = None 
        
        self.log_event("System", f"Activating **{mode} Mode** for: '{user_prompt}'")
        config = MODE_CONFIG.get(mode)
        if not config: return "❌ Error: Invalid Mode.", self.logs, None

        # 1️⃣ NAVIGATOR
        self.log_event("Navigator", "Analyzing request...")
        plan_prompt = config['navigator'].format(input=user_prompt)
        
        plan = self.safe_generate(plan_prompt, agent_name="Navigator")
        curator_context = plan 

        if mode == "Analyst":
            if "Error" in plan and len(plan) < 200: plan = user_prompt
            self.log_event("Navigator", f"Search Query: '{plan}'")
            self.log_event("Tool", "⚡ Running Live Web Search...")
            search_results = self.perform_web_search(plan)
            self.log_event("Tool", f"Search Data Received.")
            curator_context = search_results 
        else:
            self.log_event("Navigator", f"Plan locked.")

        # 2️⃣ CURATOR & 3️⃣ EVALUATOR LOOP
        feedback = ""
        attempts = 0
        max_retries = 2  # Retry ektu baralam jate chance pay
        final_output = ""

        while attempts <= max_retries:
            # --- PROMPT LOGIC ---
            if attempts > 0:
                self.log_event("System", f"🔄 **Retry Attempt #{attempts}** initiated...", highlight=True)
                
                # 🛑 CRITICAL FIX: Sentinel Retry must be STRICT
                if mode == "Sentinel":
                    prompt = (
                        "SYSTEM ALERT: The previous code failed validation. \n"
                        "YOU MUST REGENERATE THE PYTHON SCRIPT NOW. \n"
                        "RULES:\n"
                        "1. START OUTPUT IMMEDIATELY WITH 'import os'.\n"
                        "2. DO NOT WRITE ANY EXPLANATION.\n"
                        "3. USE STANDARD LIBRARIES ONLY (secrets, hashlib).\n"
                        "4. JUST WRITE THE CODE."
                    )
                else:
                    prompt = f"Previous output was rejected. Fix issues: {feedback}. \n\nContext: {curator_context}"
            else:
                self.log_event("Curator", "Drafting initial content...")
                prompt = config['curator'].format(prev_output=curator_context)

            # Generate Raw Draft
            draft = self.safe_generate(prompt, agent_name="Curator")

            # ---------------------------------------------------------
            # 🛡️ THE SANITIZER (Force Clean Code)
            # ---------------------------------------------------------
            if mode in ["Sentinel", "Dev"]:
                # 1. Clean Markdown (Common for both)
                draft = draft.replace("```python", "").replace("```", "").strip()
                
                # 2. Sentinel Specific (Aggressive Cleaning)
                if mode == "Sentinel":
                    if "import" in draft:
                        # Finds first 'import' and keeps everything after it
                        draft = "import" + draft.split("import", 1)[1]
                    else:
                        # Fallback: Jodi import na pay, forcefuli import boshiye debo
                        draft = "import os\nimport secrets\n" + draft
            # ---------------------------------------------------------

            # EVALUATOR
            self.log_event("Evaluator", "Reviewing quality & scoring...")
            eval_prompt = config['evaluator'].format(prev_output=draft)
            
            review = self.safe_generate(eval_prompt, agent_name="Evaluator")

            # SCORE & REASON PARSING
            score_match = re.search(r"Score:\s*(\d+(\.\d+)?)", review)
            score = float(score_match.group(1)) if score_match else 0.0
            
            reason_match = re.search(r"Reason:\s*(.*)", review)
            reason = reason_match.group(1) if reason_match else "Quality issues found."

            # --- DECISION LOGIC ---
            # Sentinel er jonno Score relax (>= 6)
            threshold = 6.0 if mode == "Sentinel" else 8.0

            if "ACCEPT" in review.upper() and score >= threshold:
                self.log_event("Evaluator", f"✅ **APPROVED (Score: {score}/10)**")
                final_output = draft
                break 
            else:
                self.log_event("Evaluator", f"❌ **REJECTED (Score: {score}/10)** Reason: **{reason}**", highlight=True)
                feedback = reason
                attempts += 1
                
                if attempts > max_retries:
                    self.log_event("System", "⚠️ Max retries reached. Proceeding with cleaned version.")
                    final_output = draft

        # --- 🧹 THE CLEANER (Dev Mode Stability) ---
        if mode == "Dev" and final_output:
            if 'FROM python' not in final_output:
                final_output += '\n\n"""\n# 🐳 EMERGENCY DOCKERFILE APPEND\nFROM python:3.9-slim\nWORKDIR /app\nCOPY . .\nCMD ["python", "app.py"]\n"""' 

        # --- © BRANDING INJECTION (IP Protection) ---
        if final_output:
            if mode in ["Dev", "Sentinel"]:
                # Code Mode: Header e Comment boshabo
                branding = (
                    "# ==========================================\n"
                    "# 🧠 YES Ai Master Edition\n"
                    "# 🚀 Engineered by: Ranajit Dhar\n"
                    "# 📅 Copyright © 2026. All rights reserved.\n"
                    "# ==========================================\n\n"
                )
                # Branding ta sobcheye upore bosbe
                final_output = branding + final_output
            
            else:
                # Text Mode (Creator/Analyst): Footer e Signature boshabo
                branding = (
                    "\n\n---\n"
                    "**🧠 Generated by YES Ai Master Edition** | © 2026 Ranajit Dhar. All rights reserved."
                )
                final_output = final_output + branding

        # 4️⃣ VISUALIZER
        self.log_event("System", "ℹ️ Visual generation skipped (Text-Only Mode active).")

        return final_output, self.logs, image_url