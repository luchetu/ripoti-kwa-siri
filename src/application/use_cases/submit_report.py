"""SubmitReportUseCase — orchestrates intake from raw request to stored case."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.application.ports.classifier import RoutingClassifier
from src.domain.entities.case import CaseReport
from src.domain.repositories.case_repository import ICaseRepository
from src.domain.services.privacy import scrub_phone_number, strip_direct_identifiers
from src.domain.services.routing import destination_for_report_type
from src.domain.services.summary import build_case_summary
from src.domain.services.tracking import generate_tracking_code


@dataclass(frozen=True, slots=True)
class SubmitReportRequest:
    narrative: str
    location: str | None
    event_time: str | None
    entities_involved: list[str]
    supporting_details: dict[str, str]
    source_basis: str | None
    caller_safety_concern: bool
    urgency_level: str
    caller_metadata: dict[str, str]


@dataclass(frozen=True, slots=True)
class SubmitReportResponse:
    case_id: str
    tracking_code: str
    report_type: str
    referral_target: str
    case_summary: str
    caller_metadata_preview: dict[str, Any]


class SubmitReportUseCase:
    """
    Accepts a raw intake request, finalises the case, and persists it.

    Dependencies are injected — the use case knows nothing about FastAPI,
    databases, or LLM providers.
    """

    def __init__(
        self,
        repository: ICaseRepository,
        classifier: RoutingClassifier,
    ) -> None:
        self._repository = repository
        self._classifier = classifier

    def execute(self, request: SubmitReportRequest) -> SubmitReportResponse:
        report = self._build_report(request)
        report = self._finalise(report)
        case_id = self._repository.save(report)
        return SubmitReportResponse(
            case_id=case_id,
            tracking_code=report.tracking_code or "",
            report_type=report.report_type,
            referral_target=report.referral_target,
            case_summary=report.case_summary,
            caller_metadata_preview=self._metadata_preview(request.caller_metadata),
        )

    # ------------------------------------------------------------------ private

    def _build_report(self, request: SubmitReportRequest) -> CaseReport:
        return CaseReport(
            narrative=request.narrative,
            location=request.location,
            event_time=request.event_time,
            entities_involved=list(request.entities_involved),
            supporting_details=dict(request.supporting_details),
            source_basis=request.source_basis,
            caller_safety_concern=request.caller_safety_concern,
            urgency_level=request.urgency_level,
        )

    def _finalise(self, report: CaseReport) -> CaseReport:
        """Build summary, classify, route, and assign tracking code."""
        summary = build_case_summary(report)
        classification = self._classifier.classify(summary)
        return report.model_copy(
            update=dict(
                case_summary=summary,
                report_type=classification.report_type,
                routing_confidence=classification.confidence,
                routing_reasoning=classification.reasoning,
                referral_target=destination_for_report_type(classification.report_type),
                tracking_code=generate_tracking_code(),
            )
        )

    def _metadata_preview(
        self, caller_metadata: dict[str, str]
    ) -> dict[str, Any]:
        cleaned: dict[str, Any] = dict(strip_direct_identifiers(caller_metadata))
        if "phone_number" in caller_metadata:
            cleaned["phone_number_preview"] = scrub_phone_number(
                caller_metadata["phone_number"]
            )
        return cleaned
