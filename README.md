<table width="100%">
  <tr>
    <td width="20%" align="center">
      <img src="logo2.png" alt="YES Ai Logo" width="180" />
    </td>
    <td width="80%" align="left">
      <h1 style="border-bottom: none; margin-bottom: 0;">🧠 YES AI MASTER EDITION</h1>
      <h3>The Unified End-to-End Autonomous Workforce | Engineered by a Solo Developer</h3>
      <p>
        <img src="https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge&logo=statuspage" alt="Status" />
        <img src="https://img.shields.io/badge/Stack-Gemini%203%20(Primary%20Brain)%20%E2%80%A2%20Llama%203%20(Failover)%20%E2%80%A2%20Qwen%20(Survival)-orange?style=for-the-badge" alt="Multi-Model Stack" />
        <br>
        <img src="https://img.shields.io/badge/Copyright-%C2%A9%202026%20Ranajit%20Dhar-blue?style=for-the-badge" alt="Copyright" />
        <a href="https://yesai-master-ranajitdhar.streamlit.app" target="_blank">
  <img src="https://img.shields.io/badge/Live_Demo-Streamlit_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo" />
</a>
      </p>
    </td>
  </tr>
</table>

---

## 🚀 What is YES AI Master Edition?

**YES AI Master Edition is not a chatbot.**

It is a **multi‑agent, multi‑brain, self‑healing, auto‑failover AI operating system** designed to think, recover, explain itself, and adapt in real‑time. Unlike traditional wrappers that crash when an API fails, YES AI is built to survive.

 **At its core, YES AI Master Edition is architected around Gemini 3 as its primary reasoning and orchestration engine.**

 ❝ One prompt in. A coordinated AI workforce out. ❞


 ## ⚡ Judge TL;DR (30-Second Overview)

 * 🧠 **Not a Chatbot** — A multi-agent AI operating system.
 * 🔄 **Self-Healing by Design** — Auto-retry & evaluator loops.
 * 🛡️ **Unbreakable AI** — Gemini-first reasoning with intelligent auto-failover (Llama → Qwen).
 * 🔮 **Unified Pipeline** — Chain Dev, Analyst, Creator & Sentinel modes.
 * 🧬 **Quantum-Ready** — Sentinel Mode generates Kyber-1024 safe keys.
 * 📊 **Glass-Box Observability** — Live "Brain View", Real-time Cost & Token tracking.

---

## 🔥 Core Philosophy (Why This Exists)

We moved beyond simple wrappers to build a resilient system.

| Traditional AI Wrappers ❌ | 🧠 YES AI Master Edition ✅ |
| :--- | :--- |
| **Single Model Dependency** | **Multi‑Brain Orchestration** (Gemini → Llama → Qwen) |
| **Silent Failures** (Crash on 429 / 5xx) | **Transparent Failover Logs** & Circuit Breakers |
| **Black‑box Output** | **Self‑Explaining Decisions** (Live "Brain View") |
| **Stateless / Forgetful** | **Consent-Based Memory** & Context Awareness |
| **Fragile Execution** | **Self‑Healing + Auto‑Retry Loops** |

---

## 🛡️ The "Unbreakable" Logic: Auto‑Failover Intelligence

Most AI tools stop working when they hit an API Quota error. **YES Ai gets smarter.**
*Gemini 3 remains the system’s cognitive core; failover models exist solely to preserve continuity, not to replace intelligence depth.*

### 💡 The Real-World Scenario
**🚫 The Old Way:**
> *User is working on a critical demo.*
> **AI:** "Error 429: Resource has been exhausted."
> **Result:** ❌ **CRASH.** The demo fails, and the user is stuck.

**✅ The YES Ai Way:**
> *User is working on the same demo.*
> **Gemini 3 Pro:** "Error 429: Quota Exceeded."
> **YES Ai Brain:** ⚠️ *"Primary Brain failed. Engaging Backup Circuit."*
> **Llama 3 (Groq):** *"I have taken over the request. Processing..."*
> **Result:** 🚀 **SUCCESS.** The user never noticed the failure.

### 🧠 How the Circuit Breaker Works
* **Primary Brain:** 🟢 `Gemini 3 Pro` (Planning, Reasoning, Reflection)
* **Continuity Brain:** 🟡 `Llama 3 on Groq` (Low-latency failover)
* **Survival Brain:** 🔴 `Qwen / Phi` (Emergency Fallback)

**Logic:** If Gemini fails repeatedly, the system triggers the **Circuit Breaker**, silently disabling the faulty model and routing all traffic to Llama 3. **Zero user interruption.**


## 🧬 High-Level Architecture

The system uses a **Universal Brain Router** to ensure 100% uptime.
```mermaid
graph TD
    User[User Prompt] --> UI[Streamlit Command Center]
    UI --> AM[Agent Manager]
    
    subgraph "🤖 Agent Swarm"
        AM --> Nav["Navigator: Architect"]
        Nav -->|Plan| Cur["Curator: Builder"]
        Cur -->|Draft Content| Eval["Evaluator: Quality Control"]
    end
    
    subgraph "🧠 Universal Brain (The Router)"
        Cur -.-> G{"Gemini 3 Pro"}
        G -- Success --> Out[Output]
        G -- "Fail (429 / 5xx)" --> L{"Llama 3 (Groq)"}
        L -- Success --> Out
        L -- Fail --> H{"Qwen (HuggingFace)"}
        H -- Success --> Out
        H -- Fail --> Err[Graceful Error]
        Out -.->|Return Text| Cur
    end
    
    Eval -- "Rejected ❌ (Score < 8)" --> Cur
    Eval -- "Approved ✅ (Score ≥ 8)" --> Final[🎉 Final Artifact]
    %% 👇 BRANDING ADDED HERE 👇
    Final -.- Brand["🧠 YES AI MASTER EDITION<br/>© 2026 Ranajit Dhar"]
    
    %% Styling for Branding
    style Brand fill:#000,stroke:#00ff41,stroke-width:2px,color:#fff,font-weight:bold
```
---

## 🎛️ Operation Modes (Personas)

YES Ai adapts its personality and tools based on the selected mode:

### 🧑‍💻 DEV MODE (Matrix Green Theme)
* **Role:** Senior Technical Architect.
* **Capabilities:** Generates monolithic, self-contained Python scripts.
* **Self-Repair:** Includes an **Auto-Debug Loop** to identify and patch logic errors before output. 🛠️
* **Validation:** Auto-appends `Dockerfile` for immediate deployment.
* **X-Factor:** Produces **Production-Ready Code**, not just snippets.

### 🎨 CREATOR MODE (Neon Pink Theme)
* **Role:** Viral Content Strategist.
* **Capabilities:** Writes engaging blogs, scripts, and posts.
* **Validation:** Auto-generates a **Social Media Pack** (Captions + 30 Viral Hashtags).
* **X-Factor:** Ready to copy-paste directly to LinkedIn/YouTube.

### 📊 ANALYST MODE (Deep Cyan Theme)
* **Role:** Lead Researcher & Data Scientist.
* **Capabilities:** Performs **Live Web Search** via SERPAPI.
* **Validation:** Citations, facts, and structured reports.
* **X-Factor:** No hallucinations—only grounded truth.

### 🛡️ SENTINEL MODE (Royal Purple Theme)
 **🧪 Sentinel Mode is an experimental research module showcasing how Gemini-driven agents can extend into future-grade security domains.**
* **Role:** Quantum Security Specialist.
* **Capabilities:** Generates **Kyber-1024** Quantum-Safe encryption keys.
* **Validation:** Strict compiler-style checks for security compliance.
* **X-Factor:** Uses advanced prompt engineering to bypass standard LLM refusals for security research.

---
## 🔮 Unified Pipeline Engine

Don't just stop at one task. YES Ai Master Edition allows **Cross-Mode Chaining**, effectively creating an autonomous assembly line where agents pass work to each other.

### 🔗 The "Neuro-Link" Workflow
The system allows output from one mode to be instantly piped into another for refinement, analysis, or publication.

```mermaid
graph LR
    %% Nodes
    Dev[💻 Dev Mode]
    An[📊 Analyst Mode]
    Cr[🎨 Creator Mode]
    Sen[🛡️ Sentinel Mode]

    %% Connections based on app.py logic
    Dev -->|Analyze Logic| An
    Dev -.->|Self-Debug| Dev
    
    An -->|Turn Report to Post| Cr
    An -->|Build Dashboard| Dev
    
    Cr -->|Check SEO Score| An
    
    Sen -->|Audit Security| An
    Sen -->|Integrate Key| Dev

    %% Styling
    style Sen fill:#4a0072,stroke:#d000ff,stroke-width:2px
    style Dev fill:#0f3312,stroke:#00ff41,stroke-width:2px
    style An fill:#002b36,stroke:#00e5ff,stroke-width:2px
    style Cr fill:#33001a,stroke:#ff0055,stroke-width:2px
```



## 📊 Real-Time Observability & Mission Metrics

Unlike black-box agents, YES Ai provides **Enterprise-Grade Transparency**. We track every millisecond and every cent.

<div align="center">
  <img src="mission.png" alt="Mission Metrics & Artifacts" width="35%" />
  <br>
  <em>(Screenshot: Live dashboard showing Token usage, Cost estimation, and Latency)</em>
</div>

### 🚀 Key Metrics Tracked:
* **📉 Cost Approximation:** Calculates session cost in real-time (e.g., `$0.000246`) based on input/output token logic.
* **⚡ Latency Monitor:** Tracks response time to ensure the Circuit Breaker isn't adding overhead.
* **🔢 Token Counter:** Live tracking of context window usage to prevent overflow.

---

## 📦 Instant Sandbox & Artifacts (The "Trust" Layer)

We don't just generate code; we provide the environment to run it.

<div align="center">
  <img src="sandbox.png" alt="Mission Metrics & Artifacts" width="50%" />
  <br>
</div>

* **🚀 Open Sandbox (Google Colab):** One-click button to instantly launch generated code in a secure cloud environment. No local setup needed.
* **🐳 Docker Ready:** Every "Dev Mode" and "Sentinel Mode" output includes a `Dockerfile` for immediate containerization.
* **💾 Persistent Session:** Data survives browser refreshes (Session State Management).

---

## 🛠️ Installation & Setup For Judges & Reviewers (Optional: Run Locally)

<div align="center">
  <br>
  <a href="https://yesai-master-ranajitdhar.streamlit.app" target="_blank">
    <img src="https://img.shields.io/badge/🚀_Skip_Installation_&_Try_Live_Demo-Click_Here-FF4B4B?style=for-the-badge" height="35" alt="Live Demo"/>
  </a>
  <br><br>
  <em>Note: The Judges can test the system directly via the <strong>Live Demo Link</strong> above.<br>This section is for technical verification only.</em>
  <br><br>
</div>

1.  **Clone & Install**
    ```bash
    git clone https://github.com/ranajitdharpersonal/yes-ai-master
    pip install -r requirements.txt
    ```

2.  **Environment Setup (Architecture Requirement)**
    The system requires a Multi-Model backend. If running locally, you need a `.env` file with:
    * `GOOGLE_API_KEY` (Primary Brain)
    * `GROQ_API_KEY` (Failover Brain)
    * `HF_TOKEN`(Survival Brain)
    * `SERPAPI_API_KEY`: **[Optional]** Required for **Analyst Mode** (Live Web Search).

3.  **Run**
    ```bash
    streamlit run app.py
    ```

## 👨‍💻 Built By

**Ranajit Dhar**
* *Solo Developer · Commerce Grad turned AI Engineer · YES AI Systems Designer*
* **Copyright © 2026. All rights reserved.**

**⭐ Final Note:**
This project was intentionally designed to explore the upper limits of what Gemini-powered agent systems can become.
**Not perfect. But resilient.**
