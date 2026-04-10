"""Case summary builder — pure domain logic, no external dependencies."""

from __future__ import annotations

from src.domain.entities.case import CaseReport


def build_case_summary(report: CaseReport) -> str:
    """Create a concise handoff summary from the current case report."""
    parts: list[str] = []
    if report.narrative:
        parts.append(report.narrative.rstrip("."))
    if report.location:
        parts.append(f"Location: {report.location}")
    if report.event_time:
        parts.append(f"Time: {report.event_time}")
    if report.entities_involved:
        parts.append(f"Involved: {', '.join(report.entities_involved)}")
    if report.caller_safety_concern:
        parts.append("Caller expressed a safety concern")
    return ". ".join(parts).strip() + ("." if parts else "")
