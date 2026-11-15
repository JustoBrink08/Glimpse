# Glimpse
*Making the physical world predictable for neurodivergent individuals.*

> **Glimpse** is a real-time, multimodal AI web application that translates unfamiliar physical environments—or user-created drawings—into structured, calming "Social Stories" with audio narration to reduce sensory anxiety before stepping inside.

---

## 🚨 The Problem
For many neurodivergent individuals (such as those with autism or sensory processing sensitivities), entering unpredictable public environments—like a crowded grocery store, a noisy cafeteria, or a doctor's waiting room—can trigger sensory overload and anxiety. 

Existing accessibility solutions rely on text-only prompts (forcing users to write out scenarios hours in advance) or static crowd-mapping data. They fail to bridge the gap in real-time when faced with an unexpected physical space.

---

## 💡 The Solution: Real-Time Sensory Translation
Glimpse uses multimodal AI and evidence-based Social Story™ guardrails to translate any environment in seconds:
1. **Personalize Sensory Preferences:** Set custom sliders for *Story Support Level* (`Mild` / `Moderate` / `High`), *Sound & Noise Sensitivity*, and *Crowd & Lighting Sensitivity*, or add a comfort note.
2. **Snap a Photo or Upload a Drawing:** Take a live photo of the space ahead, upload a hand-drawn scene, or select a sample environment.
3. **AI Atmosphere Analysis:** Powered by **Gemini 2.5 Flash** with strict clinical and sensory-safe guardrails, Glimpse analyzes layout, lighting, crowd density, and potential triggers using literal, non-alarmist language.
4. **Multimodal Social Story (Visual + Audio):** The app renders three calming cards (*What to Expect*, *Sensory Details to Notice*, and *Reassurance & Next Steps*) alongside an instant **Text-to-Speech (TTS)** audio player.

---

## 🛠️ Tech Stack & Architecture
* **Frontend:** Python, Streamlit (mobile-first dark-mode UI with custom CSS animations).
* **AI Engine:** Google GenAI SDK (`google-genai`) running **Gemini 2.5 Flash** with Pydantic Structured Outputs.
* **Audio & Utilities:** `gTTS` (Google Text-to-Speech for in-memory MP3 narration), `Pillow` (image processing), `python-dotenv`.

---

## 📂 Project Structure
```text
gdgc/
├── backend/
│   ├── __init__.py
│   ├── prompts.py          # Master system instructions, clinical guardrails & sensitivity modifiers
│   └── gemini_client.py    # Gemini 2.5 Flash multimodal API call, JSON schema & gTTS audio
├── frontend/
│   ├── __init__.py
│   └── ui_elements.py      # Sensory-safe dark-mode CSS, animations & story cards
├── pitch/
│   ├── api_contract.md     # Frontend <-> Backend data contract & mock data
│   ├── demo_script.md      # Hackathon pitch & live demo walkthrough
│   └── sample_images/      # Backup environment photos for live demos
├── app.py                  # Main Streamlit application & 3-screen state router
├── requirements.txt        # Python dependencies
├── .env                    # Local environment variables (ignored by Git)
└── .gitignore
