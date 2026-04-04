"""Tests for referral routing behavior."""

from app.models.case import CaseDraft
from app.models.routing import RoutingClassification
from app.services.routing import RuleBasedRoutingClassifier, apply_routing, destination_for_report_type
from app.services.routing_classifier import FallbackRoutingClassifier


def test_rule_based_classifier_detects_corruption() -> None:
    result = RuleBasedRoutingClassifier().classify(
        "A county officer asked me for a bribe at a checkpoint."
    )
    assert result.report_type == "corruption"
    assert result.confidence == "medium"


def test_destination_for_unknown_routes_to_review_queue() -> None:
    assert destination_for_report_type("unknown") == "review_queue"


def test_apply_routing_updates_case_draft() -> None:
    draft = CaseDraft(
        narrative="A group was engaged in trafficking across the border.",
        case_summary="The report describes a trafficking operation across the border.",
    )
    result = apply_routing(draft)
    assert result.report_type == "organized_crime"
    assert result.referral_target == "DCI"
    assert result.routing_reasoning


def test_apply_routing_supports_injected_classifier() -> None:
    class StubClassifier:
        def classify(self, summary: str) -> RoutingClassification:
            assert "summary" in summary
            return RoutingClassification(
                report_type="unknown",
                confidence="high",
                reasoning="The report is too mixed to classify confidently into a single category.",
            )

    draft = CaseDraft(
        narrative="This report mixes several concerns.",
        case_summary="This summary mixes several concerns.",
    )
    result = apply_routing(draft, classifier=StubClassifier())
    assert result.report_type == "unknown"
    assert result.routing_confidence == "high"
    assert result.referral_target == "review_queue"


def test_fallback_routing_classifier_uses_next_provider_after_failure() -> None:
    class FailingClassifier:
        def is_available(self) -> bool:
            return True

        def classify(self, summary: str) -> RoutingClassification:
            raise RuntimeError(f"failed for summary: {summary}")

    class WorkingClassifier:
        def is_available(self) -> bool:
            return True

        def classify(self, summary: str) -> RoutingClassification:
            assert "bribe" in summary
            return RoutingClassification(
                report_type="corruption",
                confidence="high",
                reasoning="The summary clearly describes bribery by a public officer.",
            )

    classifier = FallbackRoutingClassifier(
        classifiers=[FailingClassifier(), WorkingClassifier()]
    )
    result = classifier.classify("The summary describes a bribe request at a checkpoint.")
    assert result.report_type == "corruption"
    assert result.confidence == "high"
