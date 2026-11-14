# Glimpse
*Making the physical world predictable for neurodivergent individuals.*

> **Glimpse** is a real-time, multimodal AI web application that translates chaotic or unfamiliar physical environments into structured, calming "Social Stories" to reduce sensory anxiety before stepping inside.

---

## 🚨 The Problem
For many neurodivergent individuals (such as those with autism or severe sensory processing sensitivities), entering unpredictable public environments—like a crowded grocery store, a noisy cafeteria, or a sterile doctor's waiting room—can trigger overwhelming sensory overload and anxiety. 

Existing accessibility solutions rely on text-only prompts (forcing users to write out scenarios hours in advance) or static crowd-mapping data. They fail to bridge the gap in real-time when faced with a physical, unexpected space.

---

## 💡 The Solution: Real-Time Sensory Translation
Glimpse uses the power of multimodal AI to bridge that gap instantly:
1. **Snap a Photo:** The user opens Glimpse on their iPhone and takes a quick photo of the environment they are about to enter.
2. **AI Atmosphere Analysis:** Powered by the **Gemini 2.5 Flash** API, Glimpse analyzes the spatial layout, crowds, lighting, and potential noise triggers.
3. **Instant Social Story:** The app generates a structured, reassuring narrative breaking down *What to Expect*, *Sensory Triggers to Note*, and *Reassurance*, transforming an intimidating space into a predictable environment.

---

## 🛠️ Tech Stack & Architecture
* **Frontend:** Python, Streamlit, `streamlit-shadcn-ui` (for modern, accessible UI components).
* **AI Engine:** Google GenAI SDK (`google-genai`) running **Gemini 2.5 Flash** for rapid multimodal image-and-text reasoning.
* **Environment & Utilities:** Python-dotenv, Pillow (for image processing).

---

## 📂 Project Structure


