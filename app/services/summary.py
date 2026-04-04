"""Summary helpers for anonymous reports."""

from __future__ import annotations

from app.models.case import CaseDraft


def build_case_summary(draft: CaseDraft) -> str:
    """Create a concise hand-off summary from the current case draft."""

    parts: list[str] = []
    if draft.narrative:
        parts.append(draft.narrative.rstrip("."))
    if draft.location:
        parts.append(f"Location: {draft.location}")
    if draft.event_time:
        parts.append(f"Time: {draft.event_time}")
    if draft.entities_involved:
        parts.append(f"Involved: {', '.join(draft.entities_involved)}")
    if draft.caller_safety_concern:
        parts.append("Caller expressed a safety concern")
    return ". ".join(parts).strip() + ("." if parts else "")
