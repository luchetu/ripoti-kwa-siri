"""Intake route — bridges HTTP to SubmitReportUseCase."""

from __future__ import annotations

from typing import Any

from src.application.use_cases.submit_report import SubmitReportRequest, SubmitReportUseCase
from src.interface.api.schemas.intake import IntakeRequest, IntakeResponse


def build_use_case_request(request: IntakeRequest) -> SubmitReportRequest:
    return SubmitReportRequest(
        narrative=request.narrative,
        location=request.location,
        event_time=request.event_time,
        entities_involved=list(request.entities_involved),
        supporting_details=dict(request.supporting_details),
        source_basis=request.source_basis,
        caller_safety_concern=request.caller_safety_concern,
        urgency_level=request.urgency_level,
        caller_metadata=dict(request.caller_metadata),
    )


def handle_intake(payload: dict[str, Any], use_case: SubmitReportUseCase) -> dict[str, Any]:
    request = IntakeRequest(**payload)
    uc_request = build_use_case_request(request)
    result = use_case.execute(uc_request)
    response = IntakeResponse(
        case_id=result.case_id,
        tracking_code=result.tracking_code,
        report_type=result.report_type,
        referral_target=result.referral_target,
        case_summary=result.case_summary,
        caller_metadata_preview=result.caller_metadata_preview,
    )
    return response.model_dump()
