"""
app.py
Main Streamlit entry point for Glimpse.
Implements the 3-screen mobile flow:
1. Home & Sensory Preferences (Sliders + Comfort Search Bar)
2. Camera & Drawing Upload Mode
3. Multimodal Story Output (Audio Player + 3 Calming Cards + Follow-up)
"""

import os
from pathlib import Path
import streamlit as st

from Backend.gemini_client import generate_social_story, generate_story_audio
from Frontend.ui_elements import inject_custom_css, render_header, render_story_cards

# 1. Page Configuration
st.set_page_config(
    page_title="Glimpse | Sensory Translator",
    page_icon="☂️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Inject Dark-Mode & Animation CSS
inject_custom_css()

# 3. Initialize Navigation & Session State
if "screen" not in st.session_state:
    st.session_state.screen = "home"
if "sensitivity_level" not in st.session_state:
    st.session_state.sensitivity_level = "Moderate"
if "noise_sensitivity" not in st.session_state:
    st.session_state.noise_sensitivity = "Medium"
if "crowd_tolerance" not in st.session_state:
    st.session_state.crowd_tolerance = "Medium"
if "custom_note" not in st.session_state:
    st.session_state.custom_note = ""
if "story_result" not in st.session_state:
    st.session_state.story_result = None
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None
if "captured_image" not in st.session_state:
    st.session_state.captured_image = None


def go_to_screen(screen_name: str):
    st.session_state.screen = screen_name


# Always render the umbrella logo header at the top
render_header()


# =====================================================================
# SCREEN 1: HOME & SENSORY PREFERENCES (Matches Figma iPhone 16 - 2)
# =====================================================================
if st.session_state.screen == "home":
    # Top Search / Comfort Preference Bar
    st.session_state.custom_note = st.text_input(
        "🔍 Specific place, drawing topic, or comfort preference",
        value=st.session_state.custom_note,
        placeholder="e.g., Doctor's waiting room, I wear noise-canceling headphones...",
    )

    st.write("")  # Clean spacing before the Scan button

    # Primary Pill "Scan" Button
    if st.button("Scan Environment or Drawing"):
        go_to_screen("camera")
        st.rerun()

    st.divider()
    st.caption("🎚️ **Personalize Your Sensory Support**")

    # Slider 1: Overall Story Support Level (Maps to Mild / Moderate / High)
    st.session_state.sensitivity_level = st.select_slider(
        "Story Support & Detail Level",
        options=["Mild", "Moderate", "High"],
        value=st.session_state.sensitivity_level,
    )

    # Slider 2: Sound & Noise Sensitivity
    st.session_state.noise_sensitivity = st.select_slider(
        "Sound & Noise Sensitivity",
        options=["Low", "Medium", "High"],
        value=st.session_state.noise_sensitivity,
    )

    # Slider 3: Crowd & Visual Busyness Sensitivity
    st.session_state.crowd_tolerance = st.select_slider(
        "Crowd & Lighting Sensitivity",
        options=["Low", "Medium", "High"],
        value=st.session_state.crowd_tolerance,
    )


# =====================================================================
# SCREEN 2: PHOTO & DRAWING MODE (Matches Figma iPhone 16 - 3)
# =====================================================================
elif st.session_state.screen == "camera":
    tab_cam, tab_upload, tab_demo = st.tabs(
        ["📷 Live Camera", "🎨 Upload Photo / Drawing", "🖼️ Sample Spaces"]
    )

    selected_image = None

    with tab_cam:
        cam_photo = st.camera_input("Point your camera at the room or a drawing")
        if cam_photo is not None:
            selected_image = cam_photo

    with tab_upload:
        uploaded_file = st.file_uploader(
            "Upload a photo of a room or a hand-drawn scene",
            type=["jpg", "jpeg", "png", "webp"],
        )
        if uploaded_file is not None:
            selected_image = uploaded_file

    with tab_demo:
        sample_dir = Path("Pitch/sample_images")
        sample_files = (
            [
                f
                for f in sample_dir.iterdir()
                if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
            ]
            if sample_dir.exists()
            else []
        )
        if sample_files:
            chosen_sample = st.selectbox(
                "Choose a backup demo photo:",
                options=sample_files,
                format_func=lambda p: p.stem.replace("_", " ").title(),
            )
            if st.button("Use Selected Sample Photo"):
                selected_image = str(chosen_sample)
        else:
            st.info(
                "Drop `.jpg` or `.png` photos inside `Pitch/sample_images/` to use quick demo presets on stage."
            )

    # Trigger Gemini 2.5 Flash as soon as an image is captured/selected
    if selected_image is not None:
        st.session_state.captured_image = selected_image

        # Combine sliders + custom text note into context for Gemini
        combined_context = (
            f"Noise sensitivity: {st.session_state.noise_sensitivity}. "
            f"Crowd/Lighting sensitivity: {st.session_state.crowd_tolerance}. "
            f"User note: {st.session_state.custom_note}"
        ).strip()

        with st.spinner("☂️ Reading the space and crafting your calming story..."):
            story_dict = generate_social_story(
                image_file=selected_image,
                sensitivity_level=st.session_state.sensitivity_level,
                custom_note=combined_context,
            )
            st.session_state.story_result = story_dict
            st.session_state.audio_bytes = generate_story_audio(story_dict)

        go_to_screen("story")
        st.rerun()

    st.write("")
    if st.button("← Back to Preferences"):
        go_to_screen("home")
        st.rerun()


# =====================================================================
# SCREEN 3: STORY & AUDIO OUTPUT (Matches Figma iPhone 16 - 4)
# =====================================================================
elif st.session_state.screen == "story":
    story = st.session_state.story_result or {}

    # 1. Top Audio Player Bar (Matches top play bar in Figma iPhone 16 - 4)
    if st.session_state.audio_bytes:
        st.markdown(
            '<div class="audio-banner"><div class="audio-label">🔊 Listen to Your Social Story</div></div>',
            unsafe_allow_html=True,
        )
        st.audio(st.session_state.audio_bytes, format="audio/mp3")

    # 2. Optional expandable preview of the photo/drawing
    if st.session_state.captured_image is not None:
        with st.expander("View Scanned Photo / Drawing", expanded=False):
            st.image(st.session_state.captured_image, use_container_width=True)

    # 3. Animated 3-Part Story Cards
    render_story_cards(story)

    # 4. Bottom Follow-Up / Refinement Bar (Matches bottom bar in Figma iPhone 16 - 4)
    follow_up = st.text_input(
        "💬 Need to adjust this story?",
        placeholder="Ask anything or add a detail (e.g., 'Focus on where I can sit quietly')",
    )
    if follow_up and st.button("Update Story with Note"):
        with st.spinner("☂️ Updating your story..."):
            updated_context = (
                f"Noise sensitivity: {st.session_state.noise_sensitivity}. "
                f"Crowd/Lighting sensitivity: {st.session_state.crowd_tolerance}. "
                f"Original note: {st.session_state.custom_note}. "
                f"Follow-up request: {follow_up}"
            )
            new_story = generate_social_story(
                image_file=st.session_state.captured_image,
                sensitivity_level=st.session_state.sensitivity_level,
                custom_note=updated_context,
            )
            st.session_state.story_result = new_story
            st.session_state.audio_bytes = generate_story_audio(new_story)
            st.rerun()

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📷 Scan Another"):
            go_to_screen("camera")
            st.rerun()
    with col2:
        if st.button("🎚️ Preferences"):
            go_to_screen("home")
            st.rerun()

