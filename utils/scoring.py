from __future__ import annotations

import json
import os
from enum import Enum
from typing import Any

from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError, field_validator

from utils.prompts import ANALYSIS_SYSTEM_INSTRUCTION, build_resume_analysis_prompt


class InvalidAIResponseError(Exception):
    """Raised when Gemini returns output that does not match the expected schema."""


class MissingAPIKeyError(Exception):
    """Raised when no Gemini API key is configured."""


class HiringDecision(str, Enum):
    SHORTLIST = "Shortlist"
    HR_REVIEW = "Escalate to HR Review"
    REJECT = "Reject"


class ResumeAnalysis(BaseModel):
    match_score: int = Field(ge=0, le=100)
    matching_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    candidate_summary: str = Field(min_length=20)
    recommendation: str = Field(min_length=10)
    decision_reasoning: str = Field(min_length=20)

    @field_validator("matching_skills", "missing_skills")
    @classmethod
    def clean_skill_lists(cls, skills: list[str]) -> list[str]:
        cleaned = [skill.strip() for skill in skills if skill and skill.strip()]
        return list(dict.fromkeys(cleaned))


class DecisionResult(BaseModel):
    decision: HiringDecision
    reason: str


def make_decision(score: int) -> DecisionResult:
    """Apply the deterministic assignment decision engine."""

    # The final workflow decision is rule-based so model wording cannot alter it.
    if score > 85:
        return DecisionResult(
            decision=HiringDecision.SHORTLIST,
            reason=(
                "The score is above 85, so the candidate meets the shortlist "
                "threshold for strong resume-to-role alignment."
            ),
        )

    if 60 <= score <= 85:
        return DecisionResult(
            decision=HiringDecision.HR_REVIEW,
            reason=(
                "The score is between 60 and 85, so the candidate should be "
                "reviewed by HR before a final decision."
            ),
        )

    return DecisionResult(
        decision=HiringDecision.REJECT,
        reason=(
            "The score is below 60, so the resume does not meet the minimum "
            "screening threshold for this role."
        ),
    )


def analyze_resume_with_gemini(
    resume_text: str,
    job_description: str,
    api_key: str | None = None,
    model_name: str | None = None,
) -> ResumeAnalysis:
    """Call Gemini and validate the structured resume-screening response."""

    configured_key = api_key or os.getenv("GEMINI_API_KEY")
    if not configured_key:
        raise MissingAPIKeyError(
            "Set GEMINI_API_KEY in Streamlit secrets or as an environment variable."
        )

    prompt = build_resume_analysis_prompt(resume_text, job_description)
    client = genai.Client(api_key=configured_key)
    model = model_name or os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=ANALYSIS_SYSTEM_INSTRUCTION,
            temperature=0.2,
            # Structured output makes the app easier to validate and safer to render.
            response_mime_type="application/json",
            response_schema=ResumeAnalysis,
        ),
    )

    return parse_ai_response(response)


def parse_ai_response(response: Any) -> ResumeAnalysis:
    """Validate Gemini output and reject malformed or incomplete responses."""

    # Some SDK versions expose parsed data, while others only expose response.text.
    parsed = getattr(response, "parsed", None)
    if isinstance(parsed, ResumeAnalysis):
        return parsed
    if isinstance(parsed, dict):
        try:
            return ResumeAnalysis.model_validate(parsed)
        except ValidationError as exc:
            raise InvalidAIResponseError(
                "Gemini parsed response did not match the required schema."
            ) from exc

    raw_text = getattr(response, "text", "") or ""
    if not raw_text.strip():
        raise InvalidAIResponseError("Gemini returned an empty response.")

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise InvalidAIResponseError("Gemini returned invalid JSON.") from exc

    try:
        return ResumeAnalysis.model_validate(payload)
    except ValidationError as exc:
        raise InvalidAIResponseError(
            "Gemini response JSON did not match the required schema."
        ) from exc
