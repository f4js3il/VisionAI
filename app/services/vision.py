import base64
import io
import json
from pathlib import Path

from openai import AsyncOpenAI
from PIL import Image
from config import OPENAI_API_KEY, OPENAI_MODEL


client = AsyncOpenAI(api_key=OPENAI_API_KEY)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
SYSTEM_PROMPT = (PROMPTS_DIR / "SystemPrompt.txt").read_text(encoding="utf-8").strip()

ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "is_plant": {"type": "boolean"},
        "crop": {"type": ["string", "null"]},
        "is_healthy": {"type": ["boolean", "null"]},
        "disease": {"type": ["string", "null"]},
        "confidence": {
            "type": "number",
            "description": "Self-reported confidence between 0 and 1",
        },
        "symptoms": {"type": "array", "items": {"type": "string"}},
        "treatment": {"type": "array", "items": {"type": "string"}},
        "message": {"type": "string"},
    },
    "required": [
        "is_plant",
        "crop",
        "is_healthy",
        "disease",
        "confidence",
        "symptoms",
        "treatment",
        "message",
    ],
    "additionalProperties": False,
}


def image_to_data_url(image: Image.Image) -> str:
    """
    Encode a PIL image as a base64 JPEG data URL for the OpenAI API.
    """
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=90)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


async def                   analyse_crop_image(image: Image.Image) -> dict:
    """
    Send an image to OpenAI and get back a structured crop disease analysis.

    Args:
        image: The (already validated and resized) image to analyse.

    Returns:
        dict: The analysis, matching ANALYSIS_SCHEMA.
    """
    response = await client.responses.create(
        model=OPENAI_MODEL,
        instructions=SYSTEM_PROMPT,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Analyse this image for crop disease."},
                    {"type": "input_image", "image_url": image_to_data_url(image), "detail": "high"},
                ],
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "crop_analysis",
                "schema": ANALYSIS_SCHEMA,
                "strict": True,
            }
        },
    )
    return json.loads(response.output_text)
