"""
Backend/gemini_client.py
Handles multimodal Gemini 2.5 Flash API calls, structured JSON enforcement,
and Text-to-Speech (TTS) audio generation for Glimpse.
"""

import json
import os
from io import BytesIO
from dotenv import load_dotenv
from google import genai
from google.genai import types
from gtts import gTTS
from PIL import Image
from pydantic import BaseModel, Field

from Backend.prompts import SYSTEM_INSTRUCTION, build_user_prompt

# Load environment variables from .env
load_dotenv()


# 1. Pydantic Schema to guarantee Gemini outputs the exact API Contract keys
class SocialStoryResponse(BaseModel):
    what_to_expect: str = Field(
        description="Objective, predictable breakdown of the space or drawing, what happens here, and what people typically do."
    )
    triggers: str = Field(
        description="Neutral, factual heads-up on sensory inputs to notice (lighting, sounds, crowd movement, smells, or visual busyness)."
    )
    reassurance: str = Field(
        description="A warm, grounding takeaway offering 1-2 optional, concrete self-regulation steps."
    )


def _load_pil_image(image_input) -> Image.Image:
    """
    Safely converts a Streamlit UploadedFile, BytesIO, file path string,
    or existing PIL Image into a PIL Image object for Gemini.
    """
    if isinstance(image_input, Image.Image):
        return image_input

    # Reset stream pointer if it's a Streamlit camera/file upload object
    if hasattr(image_input, "seek"):
        image_input.seek(0)

    return Image.open(image_input)


def generate_social_story(
    image_file,
    sensitivity_level: str = "Moderate",
    custom_note: str = ""
) -> dict:
    """
    Master backend function matching Pitch/api_contract.md.
    Takes an image and sensitivity preferences, calls Gemini 2.5 Flash,
    and returns a structured Python dictionary.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY is missing from .env")
        return _error_fallback("API key is missing. Please check your .env file.")

    try:
        # Initialize the Google GenAI client
        client = genai.Client(api_key=api_key)

        # Convert input into a PIL Image
        pil_image = _load_pil_image(image_file)

        # Build the dynamic user prompt based on slider settings
        user_prompt = build_user_prompt(
            sensitivity_level=sensitivity_level,
            custom_note=custom_note
        )

        # Call Gemini 2.5 Flash with Structured Outputs enabled
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[pil_image, user_prompt],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=SocialStoryResponse,
                temperature=0.3,  # Low temperature keeps output literal and grounded
            ),
        )

        # Extract the parsed response safely
        if response.parsed:
            story_data = response.parsed.model_dump()
        else:
            story_data = json.loads(response.text)

        return {
            "status": "success",
            "what_to_expect": story_data.get("what_to_expect", ""),
            "triggers": story_data.get("triggers", ""),
            "reassurance": story_data.get("reassurance", ""),
        }

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return _error_fallback()


def generate_story_audio(story_dict: dict) -> bytes | None:
    """
    Takes the dictionary returned by generate_social_story() and converts it
    into MP3 audio bytes in memory so Streamlit's st.audio() can play it directly.
    """
    if not story_dict or story_dict.get("status") == "error":
        return None

    try:
        narration_script = (
            f"Here is what to expect. {story_dict.get('what_to_expect', '')} "
            f"Sensory details to notice. {story_dict.get('triggers', '')} "
            f"Remember. {story_dict.get('reassurance', '')}"
        )

        tts = gTTS(text=narration_script, lang="en", slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.read()

    except Exception as e:
        print(f"TTS Audio Error: {e}")
        return None


def _error_fallback(custom_reason: str = "") -> dict:
    """
    Guaranteed fallback dictionary matching Pitch/api_contract.md
    so the frontend UI never crashes during a live demo.
    """
    return {
        "status": "error",
        "what_to_expect": custom_reason or "We couldn't quite make out the room clearly.",
        "triggers": "Unable to scan sensory details right now.",
        "reassurance": "Take a deep breath and try snapping the photo again in clearer lighting.",
    }
