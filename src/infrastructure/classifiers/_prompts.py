"""Shared prompt and schema for routing classification."""

from __future__ import annotations

from src.domain.entities.routing import RoutingClassification

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
    return RoutingClassification.model_validate_json(payload)
