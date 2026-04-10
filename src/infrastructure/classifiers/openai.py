"""OpenAIRoutingClassifier — OpenAI JSON-schema structured-output classifier."""

from __future__ import annotations

from src.domain.entities.routing import RoutingClassification
from src.infrastructure.classifiers._prompts import (
    ROUTING_CLASSIFICATION_PROMPT,
    ROUTING_CLASSIFICATION_SCHEMA,
    parse_routing_classification,
)
from src.infrastructure.config.settings import get_settings


class OpenAIRoutingClassifier:

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
            raise RuntimeError(
                "openai and OPENAI_API_KEY are required for OpenAI routing"
            )
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
        if not response.output_text:
            raise RuntimeError("OpenAI routing returned an empty response")
        return parse_routing_classification(response.output_text)
