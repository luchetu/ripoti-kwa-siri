"""Tests for referral routing behavior."""

from src.domain.entities.routing import RoutingClassification
from src.domain.services.routing import destination_for_report_type
from src.infrastructure.classifiers.rule_based import RuleBasedRoutingClassifier
from src.infrastructure.classifiers.fallback import FallbackRoutingClassifier


def test_rule_based_classifier_detects_corruption() -> None:
    result = RuleBasedRoutingClassifier().classify(
        "A county officer asked me for a bribe at a checkpoint."
    )
    assert result.report_type == "corruption"
    assert result.confidence == "medium"


def test_destination_for_unknown_routes_to_review_queue() -> None:
    assert destination_for_report_type("unknown") == "review_queue"


def test_fallback_classifier_uses_next_provider_after_failure() -> None:
    class FailingClassifier:
        def is_available(self) -> bool:
            return True

        def classify(self, summary: str) -> RoutingClassification:
            raise RuntimeError(f"failed: {summary}")

    class WorkingClassifier:
        def is_available(self) -> bool:
            return True

        def classify(self, summary: str) -> RoutingClassification:
            return RoutingClassification(
                report_type="corruption",
                confidence="high",
                reasoning="Describes bribery by a public officer.",
            )

    classifier = FallbackRoutingClassifier(
        live_classifiers=[FailingClassifier(), WorkingClassifier()]
    )
    result = classifier.classify("The summary describes a bribe at a checkpoint.")
    assert result.report_type == "corruption"
    assert result.confidence == "high"


def test_fallback_classifier_falls_back_to_rule_based_when_all_live_fail() -> None:
    class FailingClassifier:
        def is_available(self) -> bool:
            return True

        def classify(self, summary: str) -> RoutingClassification:
            raise RuntimeError("unavailable")

    classifier = FallbackRoutingClassifier(live_classifiers=[FailingClassifier()])
    result = classifier.classify("A bribe was requested at a government office.")
    assert result.report_type == "corruption"
