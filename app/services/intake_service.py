"""Business logic for transforming and storing prototype intake requests."""

from __future__ import annotations

from app.api.schemas.intake import IntakeRequest, IntakeResponse
from app.models.case import CaseDraft
from app.services.case_store import InMemoryCaseStore, finalize_case_draft
from app.services.privacy import scrub_phone_number, strip_direct_identifiers


def build_case_from_request(request: IntakeRequest) -> CaseDraft:
    """Convert an intake request into the internal case draft."""

    return CaseDraft(
        narrative=request.narrative,
        location=request.location,
        event_time=request.event_time,
        entities_involved=list(request.entities_involved),
        supporting_details=dict(request.supporting_details),
        source_basis=request.source_basis,
        caller_safety_concern=request.caller_safety_concern,
        urgency_level=request.urgency_level,
    )


def build_metadata_preview(caller_metadata: dict[str, str]) -> dict[str, str | None]:
    """Return a scrubbed preview of caller metadata for review."""

    cleaned: dict[str, str | None] = dict(strip_direct_identifiers(caller_metadata))
    if "phone_number" in caller_metadata:
        cleaned["phone_number_preview"] = scrub_phone_number(caller_metadata["phone_number"])
    return cleaned


def submit_intake(request: IntakeRequest, store: InMemoryCaseStore) -> IntakeResponse:
    """Process a prototype intake request and return a reviewable response."""

    draft = build_case_from_request(request)
    finalize_case_draft(draft)
    stored = store.save(draft)
    return IntakeResponse(
        case_id=stored["case_id"],
        tracking_code=stored["tracking_code"],
        report_type=stored["report_type"],
        referral_target=stored["referral_target"],
        case_summary=stored["case_summary"],
        caller_metadata_preview=build_metadata_preview(request.caller_metadata),
    )
