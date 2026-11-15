"""
Frontend/ui_elements.py
Custom dark-mode styling, smooth CSS fade-in animations, SVG umbrella branding,
and accessible story card components matching the Glimpse Figma wireframes.
"""

import streamlit as st


def inject_custom_css():
    """
    Injects sensory-safe dark mode CSS, purple slider accents, pill buttons,
    and smooth keyframe animations into the Streamlit app.
    """
    st.markdown(
        """
        <style>
        /* Hide default Streamlit chrome for a native mobile app feel */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Constrain width to mimic an iPhone mobile viewport */
        .block-container {
            max-width: 430px !important;
            padding-top: 1.8rem !important;
            padding-bottom: 3rem !important;
        }

        /* Main dark charcoal background matching Figma */
        .stApp {
            background-color: #1E1E1E;
            color: #F3F4F6;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Smooth fade-in animation for screen transitions and cards */
        @keyframes fadeInSlideUp {
            from {
                opacity: 0;
                transform: translateY(12px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .glimpse-animate {
            animation: fadeInSlideUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        /* Header & Umbrella Logo styling */
        .glimpse-header {
            text-align: center;
            margin-bottom: 1.5rem;
            animation: fadeInSlideUp 0.5s ease-out forwards;
        }
        .glimpse-title {
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: #FFFFFF;
            margin: 0.4rem 0 0.2rem 0;
        }
        .glimpse-tagline {
            font-size: 0.9rem;
            color: #C4B5FD;
            margin: 0;
            font-weight: 400;
        }

        /* Pill-shaped white primary button (matches Figma 'Scan' button) */
        div.stButton > button {
            width: 100%;
            background-color: #FFFFFF !important;
            color: #18181B !important;
            border: none !important;
            border-radius: 9999px !important;
            padding: 0.75rem 1.5rem !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 20px rgba(124, 58, 237, 0.25) !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        }
        div.stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 24px rgba(124, 58, 237, 0.4) !important;
            background-color: #F5F3FF !important;
        }

        /* Story Output Cards */
        .story-card {
            background-color: #2A2A2E;
            border: 1px solid #3F3F46;
            border-left: 5px solid #8B5CF6;
            border-radius: 16px;
            padding: 1.15rem 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
            animation: fadeInSlideUp 0.5s ease-out forwards;
        }
        .story-card-triggers {
            border-left-color: #A78BFA;
        }
        .story-card-reassurance {
            border-left-color: #34D399;
        }
        .story-card-title {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #C4B5FD;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }
        .story-card-body {
            font-size: 1.02rem;
            line-height: 1.55;
            color: #F3F4F6;
            margin: 0;
        }

        /* Audio player container */
        .audio-banner {
            background-color: #2A2A2E;
            border: 1px solid #4C1D95;
            border-radius: 16px;
            padding: 0.85rem 1rem;
            margin-bottom: 1.1rem;
            animation: fadeInSlideUp 0.35s ease-out forwards;
        }
        .audio-label {
            font-size: 0.8rem;
            color: #DDD6FE;
            font-weight: 600;
            margin-bottom: 0.35rem;
        }

        /* Round the camera and uploaded image frames */
        div[data-testid="stCameraInput"] video,
        div[data-testid="stImage"] img {
            border-radius: 16px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """
    Renders the purple umbrella SVG icon (matching Screen 1 of Figma)
    along with the Glimpse title and calming tagline.
    """
    st.markdown(
        """
        <div class="glimpse-header">
            <svg width="54" height="54" viewBox="0 0 24 24" fill="none"
                 xmlns="http://www.w3.org/2000/svg" style="margin: 0 auto; display: block;">
                <path d="M12 3C7.03 3 3 7.03 3 12H21C21 7.03 16.97 3 12 3Z"
                      fill="#7C5CBF"/>
                <path d="M12 12V19C12 20.1 11.1 21 10 21C8.9 21 8 20.1 8 19"
                      stroke="#7C5CBF" stroke-width="2.2" stroke-linecap="round"/>
            </svg>
            <h1 class="glimpse-title">Glimpse</h1>
            <p class="glimpse-tagline">Making the physical world predictable.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_story_cards(story_dict: dict):
    """
    Renders the three structured Social Story sections as calming,
    rounded dark-mode cards with smooth animations.
    """
    what_to_expect = story_dict.get("what_to_expect", "")
    triggers = story_dict.get("triggers", "")
    reassurance = story_dict.get("reassurance", "")

    st.markdown(
        f"""
        <div class="story-card" style="animation-delay: 0.05s;">
            <div class="story-card-title">📍 What to Expect</div>
            <p class="story-card-body">{what_to_expect}</p>
        </div>

        <div class="story-card story-card-triggers" style="animation-delay: 0.15s;">
            <div class="story-card-title">🎧 Sensory Details to Notice</div>
            <p class="story-card-body">{triggers}</p>
        </div>

        <div class="story-card story-card-reassurance" style="animation-delay: 0.25s;">
            <div class="story-card-title">🌿 Reassurance & Next Steps</div>
            <p class="story-card-body">{reassurance}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
