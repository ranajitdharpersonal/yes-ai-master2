import streamlit as st
import time
import os
import base64

# Ensure backend exists
try:
    from core.agent_manager import AgentManager
except ImportError:
    st.error("⚠️ 'core/agent_manager.py' not found! Make sure you are in the right folder.")
    st.stop()

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="YES Ai Master Edition By Ranajit Dhar",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. INITIALIZE ENGINE & STATE ---
if 'manager' not in st.session_state:
    st.session_state.manager = AgentManager()

# Initialize all session states to prevent errors
if 'pipeline_prompt' not in st.session_state:
    st.session_state.pipeline_prompt = ""
if 'auto_run' not in st.session_state:
    st.session_state.auto_run = False
if 'target_mode' not in st.session_state:
    st.session_state.target_mode = "Dev"
if 'mode_selector' not in st.session_state:
    st.session_state.mode_selector = "Dev"

# Existing code er niche ei 3te add
if 'final_result' not in st.session_state:
    st.session_state.final_result = None 
if 'mission_logs' not in st.session_state:
    st.session_state.mission_logs = []   
if 'mission_stats' not in st.session_state:
    st.session_state.mission_stats = {"tokens": 0, "cost": 0.0, "latency": "--"}

# --- 3. SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo2.png", use_container_width=True)
    else:
        st.markdown("### YES Ai Master Edition")

    st.title("🎛️ Control Center")
    st.markdown("---")
    
    # --- CRITICAL FIX: RADIO BUTTON ---
    # We rely ONLY on the 'key' to control the state. No 'index' parameter needed.
    selected_mode = st.radio(
        "Select Operation Mode:",
        ["Dev", "Creator", "Analyst", "Sentinel"],
        key="mode_selector",
        captions=["Code & Software", "Viral Content", "Deep Research", "Quantum Security"]
    )
    
    # Sync global target variable
    st.session_state.target_mode = selected_mode
    
    st.markdown("---")
    st.info(f"⚡ Status: **ONLINE**\n\n🧠 Brain: **{selected_mode} Mode**")

# --- 4. THEME ENGINE ---
# --- 4. ULTRA DARK THEME ENGINE (SECRET WEAPON: RADIAL SPOTLIGHT) ---
theme_colors = {
    "Dev": { 
        # Glowing Green Spotlight from Top
        "bg_gradient": "radial-gradient(circle at 50% 0%, #1a331a 0%, #000000 60%, #000000 100%)", 
        "accent": "#00ff41", 
        "btn_color": "#008f11", 
        "text_color": "#e0e0e0" 
    },
    "Creator": { 
        # Glowing Red/Pink Spotlight from Top
        "bg_gradient": "radial-gradient(circle at 50% 0%, #33001a 0%, #000000 60%, #000000 100%)", 
        "accent": "#ff0055", 
        "btn_color": "#990033", 
        "text_color": "#ffe6ea" 
    },
    "Analyst": { 
        # Glowing Cyan/Deep Blue Spotlight from Top
        "bg_gradient": "radial-gradient(circle at 50% 0%, #001a33 0%, #000000 60%, #000000 100%)", 
        "accent": "#00e5ff", 
        "btn_color": "#006064", 
        "text_color": "#e0f7fa" 
    },
    # THIS BLOCK (Deep Purple Theme)
    "Sentinel": { 
        # Glowing Purple Spotlight
        "bg_gradient": "radial-gradient(circle at 50% 0%, #240046 0%, #000000 60%, #000000 100%)", 
        "accent": "#d000ff",   # Neon Violet
        "btn_color": "#4a0072", # Deep Indigo
        "text_color": "#e0aaff" # Lavender Text
    }
}
current_theme = theme_colors[selected_mode]

st.markdown(f"""
<style>
    header[data-testid="stHeader"] {{ background-color: transparent !important; }}
    [data-testid="stDecoration"] {{ display: none; }}
    .stDeployButton {{ display: none; }}
    .block-container {{ padding-top: 3rem !important; }}
    .stApp {{ background: {current_theme['bg_gradient']}; background-attachment: fixed; }}
    section[data-testid="stSidebar"] {{ background-color: rgba(0, 0, 0, 0.5) !important; border-right: 1px solid rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); }}
    
    .agent-log {{ background-color: rgba(20, 20, 20, 0.8); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid {current_theme['accent']}; color: {current_theme['text_color']}; font-family: 'Courier New', monospace; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
    .agent-success {{ border-left: 4px solid #00C853 !important; color: #fff; }}
    .agent-fail {{ border-left: 4px solid #D50000 !important; color: #fff; }}

    h1, h2, h3 {{ color: {current_theme['accent']} !important; text-shadow: 0 0 10px rgba(0,0,0,0.5); }}
    p, .stMarkdown {{ color: #cccccc; }}
    
    div.stButton > button {{ background-color: {current_theme['btn_color']}; color: white; border: 1px solid rgba(255,255,255,0.1); font-weight: bold; transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1px; }}
    div.stButton > button:hover {{ background-color: {current_theme['btn_color']}; box-shadow: 0 0 15px {current_theme['accent']}; border-color: {current_theme['accent']}; transform: translateY(-2px); }}
    .stTextArea textarea {{ background-color: rgba(0,0,0,0.3) !important; color: #fff !important; border: 1px solid rgba(255,255,255,0.1); }}
</style>
""", unsafe_allow_html=True)

# --- 5. HELPER: BRAIN VIEW (STABLE STRING CONCATENATION) ---
def get_brain_html(status, logs, accent):
    # 1. Status Badge
    if status == "PROCESSING":
        status_badge = (
            f"<span style='color: {accent}; font-weight: bold; font-size: 12px; animation: blink 1s infinite;'>● PROCESSING</span>"
            "<style>@keyframes blink { 50% { opacity: 0.3; } }</style>"
        )
    else:
        status_badge = f"<span style='color: {accent}; font-weight: bold; font-size: 12px; background: rgba(0,255,0,0.1); padding: 4px 8px; border-radius: 4px; border: 1px solid {accent};'>● {status}</span>"

    # 2. Content Logic
    if not logs:
        # IDLE ROSTER
        middle_content = (
            "<div style='height: 350px; display: flex; flex-direction: column; justify-content: center;'>"
            "<div style='font-family: \"Courier New\", monospace; font-size: 14px; color: #e0e0e0;'>"
            "<div style='margin-bottom: 15px; display: flex; align-items: center;'>"
            "<span style='font-size: 22px; margin-right: 15px;'>🧭</span>"
            "<div><div style='font-weight: bold; font-size: 15px;'>Navigator Agent</div><div style='font-size: 12px; color: #888;'>Role: Planner & Strategist</div></div>"
            "</div>"
            "<div style='margin-bottom: 15px; display: flex; align-items: center;'>"
            "<span style='font-size: 22px; margin-right: 15px;'>🔨</span>"
            "<div><div style='font-weight: bold; font-size: 15px;'>Curator Agent</div><div style='font-size: 12px; color: #888;'>Role: Builder & Coder</div></div>"
            "</div>"
            "<div style='margin-bottom: 15px; display: flex; align-items: center;'>"
            "<span style='font-size: 22px; margin-right: 15px;'>⚖️</span>"
            f"<div><div style='font-weight: bold; font-size: 15px;'>Evaluator Agent</div><div style='font-size: 12px; color: {accent};'>Role: Quality Control & Judge</div></div>"
            "</div>"
            "</div>"
            "<div style='margin-top: 25px; text-align: center; font-size: 12px; color: #666; border-top: 1px dashed #333; padding-top: 15px;'>"
            "<i>Waiting for mission directive...</i>"
            "</div>"
            "</div>"
        )
    else:
        # ACTIVE LOGS
        inner_logs = ""
        for log in logs:
            color = "#ccc"
            if "✅" in log or "ACCEPT" in log: color = "#00ff41"
            if "❌" in log or "REJECT" in log: color = "#ff0055"
            if "Navigator" in log: color = "#ffcc00"
            
            inner_logs += f"<div style='margin-bottom: 10px; color: {color}; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 5px;'>{log}</div>"
        
        middle_content = (
            "<div style='height: 350px; overflow-y: auto; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); font-family: monospace; font-size: 13px;'>"
            f"{inner_logs}"
            "</div>"
        )

    # 3. Master Template
    raw_html = (
        "<div style='background-color: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);'>"
        "<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;'>"
        "<span style='color: #bbb; font-size: 20px; letter-spacing: 1px;'>🧠 Brain View</span>"
        f"{status_badge}"
        "</div>"
        f"{middle_content}"
        f"<div style='background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px; border-left: 4px solid {accent}; margin-top: 20px;'>"
        "<div style='font-size: 11px; color: #aaa; margin-bottom: 6px; letter-spacing: 1px; font-weight: bold;'>ACTIVE PROTOCOLS:</div>"
        "<div style='font-size: 13px; color: #fff; display: flex; align-items: center; margin-bottom: 4px;'>"
        "<span style='margin-right: 10px;'>🔄</span> Self-Healing Loop"
        f"<span style='margin-left: auto; color: {accent}; font-size: 11px; font-weight: bold;'>ENABLED</span>"
        "</div>"
        "<div style='font-size: 13px; color: #fff; display: flex; align-items: center;'>"
        "<span style='margin-right: 10px;'>🛡️</span> Auto-Failover"
        f"<span style='margin-left: auto; color: {accent}; font-size: 11px; font-weight: bold;'>READY</span>"
        "</div>"
        "</div>"
        "</div>"
    )
    return raw_html

# --- 5B. HELPER: STATS BOX (UPDATED: SKELETON UI) ---
def get_stats_html(status, tokens=0, cost=0.0, latency="--"):
    # Theme color fetch
    try:
        accent = theme_colors[st.session_state.target_mode]['accent']
    except:
        accent = "#00ff41" # Fallback

    # 1. IDLE STATE (The "Standing" Meters - Dimmed)
    if status == "IDLE":
        content = (
            "<div style='margin-top: 5px;'>"
            "<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 13px;'>"
            "<span style='color: #bbb;'>Output Tokens</span>"
            "<span style='color: #fff; font-family: monospace;'>0</span>"
            "</div>"
            "<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 13px;'>"
            "<span style='color: #bbb;'>Latency</span>"
            "<span style='color: #fff; font-family: monospace;'>--</span>"
            "</div>"
            "<div style='border-top: 1px solid rgba(255,255,255,0.1); margin-top: 8px; padding-top: 8px; display: flex; justify-content: space-between; align-items: center; font-size: 14px;'>"
            f"<span style='color: {accent}; font-weight: bold;'>Est. Cost</span>"
            f"<span style='color: {accent}; font-weight: bold; font-family: monospace;'>$0.000000</span>"
            "</div>"
            "</div>"
        )
        
    # 2. RUNNING STATE (Animation)
    elif status == "RUNNING":
        content = (
            "<div style='color: #bbb; font-size: 13px; text-align: center; padding: 25px 10px;'>"
            "<span style='animation: blink 1s infinite;'>⚡ Calibrating Metrics...</span>"
            "</div>"
            "<style>@keyframes blink { 50% { opacity: 0.3; } }</style>"
        )
        
    # 3. DONE STATE (Real Data)
    else:
        content = (
            "<div style='margin-top: 5px;'>"
            "<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 13px;'>"
            "<span style='color: #bbb;'>Output Tokens</span>"
            f"<span style='color: #fff; font-family: monospace;'>{tokens}</span>"
            "</div>"
            "<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 13px;'>"
            "<span style='color: #bbb;'>Latency</span>"
            f"<span style='color: #fff; font-family: monospace;'>{latency}</span>"
            "</div>"
            "<div style='border-top: 1px solid rgba(255,255,255,0.1); margin-top: 8px; padding-top: 8px; display: flex; justify-content: space-between; align-items: center; font-size: 14px;'>"
            f"<span style='color: {accent}; font-weight: bold;'>Est. Cost</span>"
            f"<span style='color: {accent}; font-weight: bold; font-family: monospace;'>${cost:.6f}</span>"
            "</div>"
            "</div>"
        )

    # Master Container
    return (
        "<div style='background-color: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); margin-top: 20px;'>"
        "<div style='font-size: 11px; color: #888; letter-spacing: 2px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 5px;'>MISSION METRICS</div>"
        f"{content}"
        "</div>"
    )


# --- 6. MAIN LAYOUT ---
col_main, col_brain = st.columns([0.65, 0.35], gap="medium")
brain_placeholder = col_brain.empty()

# (For the new box)
with col_brain:
    stats_placeholder = st.empty()

with col_main:
    # Header
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(f"""
<div style="display: flex; align-items: center; margin-bottom: 25px;">
<img src="data:image/png;base64,{data}" style="border-radius: 50%; width: 160px; height: 160px; margin-right: 20px; border: 2px solid {current_theme['accent']}; box-shadow: 0 0 10px {current_theme['accent']}; object-fit: cover;">
<div>
<h1 style="margin: 0; padding: 0; line-height: 1.2; color: {current_theme['accent']}; text-shadow: 0 0 10px rgba(0,0,0,0.5);">YES Ai Master Edition</h1>
<p style="margin: 4px 0 0 0; font-size: 14px; font-weight: 400; color: #ffffff; letter-spacing: 0.5px;">The Unified End-to-End Autonomous Workforce | Engineered by a Solo Developer</p>
<p style="margin: 4px 0 0 0; font-size: 13px; color: #bbbbbb;">Copyright © 2026 Ranajit Dhar. All rights reserved.</p>
</div>
</div>
""", unsafe_allow_html=True)
    else:
        st.title("🧠 YES Ai Master Edition")

    # Input Area
    input_val = st.session_state.pipeline_prompt 
    
    placeholders = {
        "Dev": "Ex: Create a Python snake game...",
        "Creator": "Ex: Write a viral LinkedIn post...",
        "Analyst": "Ex: Research the latest trends...",
        "Sentinel": "Ex: Generate a Kyber-1024 Quantum-Safe Key Pair..."
    }
    current_placeholder = placeholders.get(selected_mode, "Ex: Enter your mission...")

    user_input = st.text_area(
        "Enter Mission Directive:", 
        value=input_val, 
        height=100, 
        placeholder=current_placeholder
    )
    
    launch_btn = st.button("🚀 Launch Mission", type="primary", use_container_width=True)

    st.markdown("### 📝 Mission Output")
    output_container = st.container()
    download_section = st.empty()
    pipeline_section = st.empty()

# --- 7. LOGIC EXECUTION LOOP ---
mission_ran = False

if (launch_btn or st.session_state.auto_run) and user_input:
    
    mission_ran = True
    st.session_state.auto_run = False
    st.session_state.pipeline_prompt = "" 

    # 1. Start Loading
    brain_placeholder.markdown(get_brain_html("PROCESSING", ["System: Initializing Agent Swarm..."], current_theme['accent']), unsafe_allow_html=True)
    
    # (Start Timer)
    stats_placeholder.markdown(get_stats_html("RUNNING"), unsafe_allow_html=True)
    start_time = time.time()


    with st.spinner(f"🤖 Agents are collaborating in {selected_mode} Mode..."):
        # Run Mission
        final_result, logs, image_url = st.session_state.manager.run_mission(user_input, mode=selected_mode)
        
        # 2. Log Stream
        current_logs = []
        # ... (existing code) ...
        for log in logs:
            current_logs.append(log)
            brain_placeholder.markdown(get_brain_html("PROCESSING", current_logs, current_theme['accent']), unsafe_allow_html=True)
            time.sleep(0.15) 

        # CORRECTED BLOCK (Variable name fix)
        st.session_state.final_result = final_result
        st.session_state.mission_logs = logs
        st.session_state.mission_stats = {
            "tokens": int(len(final_result.split()) * 1.3),  # <-- Was 'result', now 'final_result'
            "cost": (len(final_result.split()) * 1.3 / 1000000) * 0.50,
            "latency": f"{round(time.time() - start_time, 2)}s"
        }
        
# Button chapa hok ba na hok, jodi Memory te Result thake, tobe dekhano hobe
if st.session_state.final_result:
    
    #NEW: Restore Brain Logs on Refresh
    if not mission_ran:
        brain_placeholder.markdown(get_brain_html("ONLINE", st.session_state.mission_logs, current_theme['accent']), unsafe_allow_html=True)
    # 1. Update Stats Box (Memory theke data niye direct show korchi)
    stats = st.session_state.mission_stats
    stats_placeholder.markdown(get_stats_html("DONE", tokens=stats["tokens"], cost=stats["cost"], latency=stats["latency"]), unsafe_allow_html=True)

    # Result Section
    with output_container:
        # Sentinel ar Dev mode ke Code hisabe treat kora
        if selected_mode in ["Dev", "Sentinel"]: 
            # FIXED: 'st.session_state.final_result' use (Local variable noy)
            st.code(st.session_state.final_result, language="python")
        else:
            st.markdown(st.session_state.final_result)

    # Artifacts Section
    with download_section.container():
        st.markdown("---")
        st.markdown("### 💾 Mission Artifacts")
        c1, c2 = st.columns(2)
        
        def get_colab_link():
            return "https://colab.research.google.com/#create=true&language=python"

        # LOGIC UPDATE: Dev AR Sentinel dujonei same facility pabe
        if selected_mode in ["Dev", "Sentinel"]:
            with c1:
                # Sentinel hole nam hobe 'kyber_secure.py', Dev hole 'deploy.py'
                fname = "kyber_secure.py" if selected_mode == "Sentinel" else "deploy.py"
                
                # FIXED: 'data' parameter e session state use kora
                st.download_button(
                    "📦 Download Package (App + Dockerfile)", 
                    st.session_state.final_result, 
                    fname, 
                    "text/x-python", 
                    type="primary", 
                    use_container_width=True
                )
            with c2:
                st.link_button("🚀 Open Sandbox (Google Colab)", get_colab_link(), type="secondary", use_container_width=True)
            
            with st.expander("📋 Click here to Copy Code"):
                # FIXED: Code copy block eo session state
                st.code(st.session_state.final_result, language="python")
        else:
            # Creator/Analyst er jonno sudhu Text Download
            # FIXED: Data parameter fix
            st.download_button(
                "📄 Download Content", 
                st.session_state.final_result, 
                "content.md", 
                use_container_width=True
            )

    # Pipeline Buttons
    with pipeline_section.container():
        st.markdown("### 🔮 Next Steps (Pipeline)")
        c1, c2, c3 = st.columns(3)

        # TRIGGER FUNCTION: Updates the Radio Button Key directly
        def trigger_pipeline(target_mode, prompt):
            st.session_state["mode_selector"] = target_mode 
            st.session_state.target_mode = target_mode
            st.session_state.pipeline_prompt = prompt
            st.session_state.auto_run = True

        def end_session():
            st.session_state.pipeline_prompt = ""
            st.session_state.auto_run = False
            # Optional: Clear results on end
            st.session_state.final_result = None

        if selected_mode == "Dev":
            # ✅ Fixed: st.session_state.final_result
            c1.button("📊 Analyze (-> Analyst)", on_click=trigger_pipeline, args=("Analyst", f"Analyze logic:\n{st.session_state.final_result}"))
            c2.button("🐛 Debug (-> Dev)", on_click=trigger_pipeline, args=("Dev", f"Fix bugs:\n{st.session_state.final_result}"))
        
        elif selected_mode == "Analyst":
            # ✅ Fixed: st.session_state.final_result
            c1.button("✨ Post (-> Creator)", on_click=trigger_pipeline, args=("Creator", f"Make LinkedIn post:\n{st.session_state.final_result}"))
            c2.button("💻 Dash (-> Dev)", on_click=trigger_pipeline, args=("Dev", f"Visualize data:\n{st.session_state.final_result}"))
        
        elif selected_mode == "Creator":
            # ✅ Fixed: st.session_state.final_result
            c1.button("📉 SEO (-> Analyst)", on_click=trigger_pipeline, args=("Analyst", f"Check SEO:\n{st.session_state.final_result}"))
            if c2.button("💾 Save to CMS"): 
                st.toast("✅ Content saved to Local Session History.", icon="💾")
                time.sleep(1)
        
        elif selected_mode == "Sentinel":
            # ✅ Fixed: st.session_state.final_result
            c1.button("🔍 Audit (-> Analyst)", on_click=trigger_pipeline, args=("Analyst", f"Audit this encryption protocol:\n{st.session_state.final_result}"))
            c2.button("💻 Integrate (-> Dev)", on_click=trigger_pipeline, args=("Dev", f"Integrate key:\n{st.session_state.final_result}"))
        
        c3.button("🏁 End Task", on_click=end_session, type="primary")

# --- 8. IDLE STATE ---
# Only show IDLE if no result exists AND mission is not running
if not st.session_state.final_result and not mission_ran:
    brain_placeholder.markdown(get_brain_html("ONLINE", [], current_theme['accent']), unsafe_allow_html=True)
    stats_placeholder.markdown(get_stats_html("IDLE"), unsafe_allow_html=True)