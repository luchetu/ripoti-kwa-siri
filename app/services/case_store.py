"""Prototype case assembly and in-memory storage helpers."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.models.case import CaseDraft
from app.services.routing import apply_routing
from app.services.summary import build_case_summary
from app.services.tracking import generate_tracking_code


class InMemoryCaseStore:
    """Small in-memory store for prototype review and testing."""

    def __init__(self) -> None:
        self._cases: dict[str, dict[str, Any]] = {}

    def save(self, draft: CaseDraft) -> dict[str, Any]:
        case_id = f"case_{uuid4().hex[:8]}"
        payload = draft.model_dump()
        payload["case_id"] = case_id
        self._cases[case_id] = payload
        return payload

    def get(self, case_id: str) -> dict[str, Any] | None:
        return self._cases.get(case_id)


def finalize_case_draft(draft: CaseDraft) -> CaseDraft:
    """Populate the generated fields needed for a first-case preview."""

    draft.case_summary = build_case_summary(draft)
    apply_routing(draft)
    if not draft.tracking_code:
        draft.tracking_code = generate_tracking_code()
    return draft
