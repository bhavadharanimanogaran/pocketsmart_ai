import json
from typing import Any
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError
from app.config import settings
from app.schemas import RecommendationResponse

class AIRecommendation(BaseModel):
    planner: str
    budget: int
    budget_summary: str
    allocation: dict[str, int] = Field(default_factory=dict)
    recommendations: list[dict[str, Any]]
    tips: list[str]
    disclaimer: str = "Prices and availability are estimates unless supplied by an authorized provider."

def _client():
    if not settings.GEMINI_API_KEY or not settings.AI_ENABLED:
        return None
    return genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_ai(prompt: str, image_bytes: bytes | None = None, mime_type: str | None = None) -> dict:
    client = _client()
    if not client:
        raise RuntimeError("Gemini is not configured")

    contents = [prompt]
    if image_bytes and mime_type:
        contents.insert(0, types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AIRecommendation,
            temperature=0.7,
            max_output_tokens=5000,
        ),
    )
    if getattr(response, "parsed", None):
        parsed = response.parsed
        if isinstance(parsed, BaseModel):
            return parsed.model_dump()
    return json.loads(response.text)

def normalize_ai(result: dict, planner: str, budget: int) -> dict:
    result["planner"] = planner
    result["budget"] = budget
    validated = RecommendationResponse.model_validate(result)
    return validated.model_dump()
