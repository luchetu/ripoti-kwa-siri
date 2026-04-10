"""GeminiRoutingClassifier — Google Gen AI structured-output classifier."""

from __future__ import annotations

from importlib import import_module

from src.domain.entities.routing import RoutingClassification
from src.infrastructure.classifiers._prompts import (
    ROUTING_CLASSIFICATION_PROMPT,
    ROUTING_CLASSIFICATION_SCHEMA,
    parse_routing_classification,
)
from src.infrastructure.config.settings import get_settings


class GeminiRoutingClassifier:

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
            raise RuntimeError(
                "google-genai and GOOGLE_API_KEY are required for Gemini routing"
            )
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
        if not response.text:
            raise RuntimeError("Gemini routing returned an empty response")
        return parse_routing_classification(response.text)
