"""FallbackRoutingClassifier — tries live providers, falls back to rules."""

from __future__ import annotations

from src.application.ports.classifier import LiveRoutingClassifier
from src.domain.entities.routing import RoutingClassification
from src.infrastructure.classifiers.rule_based import RuleBasedRoutingClassifier


class FallbackRoutingClassifier:
    """
    Classifier chain: Gemini → OpenAI → RuleBased.

    Each live provider is tried in order. If all live providers fail or are
    unavailable, the rule-based classifier is used as a guaranteed fallback.
    """

    def __init__(
        self,
        live_classifiers: list[LiveRoutingClassifier] | None = None,
    ) -> None:
        if live_classifiers is None:
            from src.infrastructure.classifiers.gemini import GeminiRoutingClassifier
            from src.infrastructure.classifiers.openai import OpenAIRoutingClassifier

            live_classifiers = [GeminiRoutingClassifier(), OpenAIRoutingClassifier()]
        self._live = live_classifiers
        self._fallback = RuleBasedRoutingClassifier()

    def is_available(self) -> bool:
        return True  # always available — rule-based guarantees a result

    def classify(self, summary: str) -> RoutingClassification:
        errors: list[str] = []
        for classifier in self._live:
            if not classifier.is_available():
                continue
            try:
                return classifier.classify(summary)
            except Exception as exc:
                errors.append(f"{classifier.__class__.__name__}: {exc}")

        if errors:
            import logging
            logging.getLogger(__name__).warning(
                "live classifiers failed, using rule-based fallback: %s",
                "; ".join(errors),
            )
        return self._fallback.classify(summary)
