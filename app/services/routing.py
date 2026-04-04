"""Routing classification and destination mapping for anonymous reports."""

from __future__ import annotations

from dataclasses import dataclass

from app.models.case import CaseDraft
from app.models.routing import ReportType, RoutingClassification
from app.services.routing_classifier import FallbackRoutingClassifier, RoutingClassifier


@dataclass(frozen=True, slots=True)
class RuleBasedRoutingClassifier:
    """Small local fallback classifier when live provider calls are unavailable."""

    def classify(self, summary: str) -> RoutingClassification:
        normalized = summary.lower()
        if any(term in normalized for term in ("bribe", "bribery", "procurement", "abuse of office")):
            return RoutingClassification(
                report_type="corruption",
                confidence="medium",
                reasoning="The report describes a public-office bribery or abuse-of-office allegation.",
            )
        if any(term in normalized for term in ("trafficking", "extortion", "kidnapping", "criminal group")):
            return RoutingClassification(
                report_type="organized_crime",
                confidence="medium",
                reasoning="The report describes coordinated criminal activity or coercive criminal conduct.",
            )
        return RoutingClassification(
            report_type="unknown",
            confidence="low",
            reasoning="The report does not yet contain enough signal for a confident category decision.",
        )


def destination_for_report_type(report_type: ReportType) -> str:
    """Map a broad category to the prototype destination."""

    if report_type == "corruption":
        return "EACC"
    if report_type == "organized_crime":
        return "DCI"
    return "review_queue"


def apply_routing(
    draft: CaseDraft,
    classifier: RoutingClassifier | None = None,
) -> CaseDraft:
    """Mutate a draft with the current best routing decision and return it."""

    if classifier is None:
        live_classifier = FallbackRoutingClassifier()
        classifier = live_classifier if live_classifier.is_available() else RuleBasedRoutingClassifier()
    routing_text = draft.case_summary or draft.narrative
    classification = classifier.classify(routing_text)
    draft.report_type = classification.report_type
    draft.routing_confidence = classification.confidence
    draft.routing_reasoning = classification.reasoning
    draft.referral_target = destination_for_report_type(classification.report_type)
    return draft
