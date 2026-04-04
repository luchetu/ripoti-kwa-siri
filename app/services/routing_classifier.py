"""Structured-output routing classifiers with provider fallback."""

from __future__ import annotations

from importlib import import_module
from typing import Protocol

from app.core.config import get_settings
from app.models.routing import RoutingClassification


ROUTING_CLASSIFICATION_PROMPT = """
Classify this report. Reply with JSON only.
{
  "report_type": "corruption" | "organized_crime" | "unknown",
  "confidence": "high" | "medium" | "low",
  "reasoning": "one sentence"
}
""".strip()


ROUTING_CLASSIFICATION_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "report_type": {
            "type": "string",
            "enum": ["corruption", "organized_crime", "unknown"],
        },
        "confidence": {
            "type": "string",
            "enum": ["high", "medium", "low"],
        },
        "reasoning": {"type": "string"},
    },
    "required": ["report_type", "confidence", "reasoning"],
}


def parse_routing_classification(payload: str) -> RoutingClassification:
    """Parse a structured routing-classification response."""

    return RoutingClassification.model_validate_json(payload)


class RoutingClassifier(Protocol):
    """Interface for routing classifiers backed by rules or external models."""

    def classify(self, summary: str) -> RoutingClassification:
        """Return a structured routing classification for a report summary."""
        ...


class LiveRoutingClassifier(RoutingClassifier, Protocol):
    """Interface for live provider classifiers that can report availability."""

    def is_available(self) -> bool:
        """Return whether the live provider can make requests."""
        ...


class GeminiRoutingClassifier:
    """Direct Gemini classifier using the Google Gen AI SDK."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        settings = get_settings()
        self._api_key = api_key or settings.google_api_key
        self._model = model or settings.routing_model

    def is_available(self) -> bool:
        if not self._api_key:
            return False
        try:
            import_module("google.genai")
        except ModuleNotFoundError:
            return False
        return True

    def classify(self, summary: str) -> RoutingClassification:
        if not self.is_available():
            raise RuntimeError("google-genai and GOOGLE_API_KEY are required for Gemini routing")

        genai = import_module("google.genai")

        client = genai.Client(api_key=self._api_key)
        response = client.models.generate_content(
            model=self._model,
            contents=f"{ROUTING_CLASSIFICATION_PROMPT}\n\nCase summary:\n{summary}",
            config={
                "response_mime_type": "application/json",
                "response_json_schema": ROUTING_CLASSIFICATION_SCHEMA,
            },
        )
        payload = response.text
        if not payload:
            raise RuntimeError("Gemini routing returned an empty response payload")
        return parse_routing_classification(payload)


class OpenAIRoutingClassifier:
    """Direct OpenAI classifier used when Gemini is unavailable or fails."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        settings = get_settings()
        self._api_key = api_key or settings.openai_api_key
        self._model = model or settings.openai_routing_model

    def is_available(self) -> bool:
        if not self._api_key:
            return False
        try:
            from openai import OpenAI  # noqa: F401
        except ModuleNotFoundError:
            return False
        return True

    def classify(self, summary: str) -> RoutingClassification:
        if not self.is_available():
            raise RuntimeError("openai and OPENAI_API_KEY are required for OpenAI routing fallback")

        from openai import OpenAI

        client = OpenAI(api_key=self._api_key)
        response = client.responses.create(
            model=self._model,
            input=[
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": ROUTING_CLASSIFICATION_PROMPT}],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": f"Case summary:\n{summary}"}],
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "routing_classification",
                    "schema": ROUTING_CLASSIFICATION_SCHEMA,
                    "strict": True,
                }
            },
        )
        payload = response.output_text
        if not payload:
            raise RuntimeError("OpenAI routing returned an empty response payload")
        return parse_routing_classification(payload)


class FallbackRoutingClassifier:
    """Try Gemini first, then OpenAI, and surface the first successful result."""

    def __init__(self, classifiers: list[LiveRoutingClassifier] | None = None) -> None:
        self._classifiers = classifiers or [GeminiRoutingClassifier(), OpenAIRoutingClassifier()]

    def is_available(self) -> bool:
        return any(classifier.is_available() for classifier in self._classifiers)

    def classify(self, summary: str) -> RoutingClassification:
        errors: list[str] = []
        for classifier in self._classifiers:
            if not classifier.is_available():
                continue
            try:
                return classifier.classify(summary)
            except Exception as exc:
                errors.append(f"{classifier.__class__.__name__}: {exc}")

        details = "; ".join(errors) if errors else "no live routing providers are configured"
        raise RuntimeError(f"Routing classification failed: {details}")
