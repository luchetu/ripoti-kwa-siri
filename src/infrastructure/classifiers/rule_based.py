"""RuleBasedRoutingClassifier — keyword fallback, zero external dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from src.domain.entities.routing import RoutingClassification


@dataclass(frozen=True, slots=True)
class RuleBasedRoutingClassifier:

    def classify(self, summary: str) -> RoutingClassification:
        normalized = summary.lower()
        if any(
            term in normalized
            for term in ("bribe", "bribery", "procurement", "abuse of office")
        ):
            return RoutingClassification(
                report_type="corruption",
                confidence="medium",
                reasoning="Report describes a public-office bribery or abuse-of-office allegation.",
            )
        if any(
            term in normalized
            for term in ("trafficking", "extortion", "kidnapping", "criminal group")
        ):
            return RoutingClassification(
                report_type="organized_crime",
                confidence="medium",
                reasoning="Report describes coordinated criminal activity or coercive criminal conduct.",
            )
        return RoutingClassification(
            report_type="unknown",
            confidence="low",
            reasoning="Not enough signal for a confident category decision.",
        )
