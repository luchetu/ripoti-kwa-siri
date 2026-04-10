"""Routing destination mapping — pure domain rule, no external dependencies."""

from __future__ import annotations

from src.domain.entities.routing import ReportType


def destination_for_report_type(report_type: ReportType) -> str:
    """Map a report category to the appropriate investigative body."""
    if report_type == "corruption":
        return "EACC"
    if report_type == "organized_crime":
        return "DCI"
    return "review_queue"
