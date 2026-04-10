"""CaseReport — the core domain entity for an anonymous report."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CaseReport(BaseModel):
    """Immutable record of an anonymous report from intake through routing."""

    report_type: str = "unknown"
    routing_confidence: str = "low"
    routing_reasoning: str = ""
    narrative: str = ""
    location: str | None = None
    event_time: str | None = None
    entities_involved: list[str] = Field(default_factory=list)
    supporting_details: dict[str, str] = Field(default_factory=dict)
    source_basis: str | None = None
    urgency_level: str = "normal"
    caller_safety_concern: bool = False
    tracking_code: str | None = None
    referral_target: str = "review_queue"
    case_summary: str = ""
    status: str = "received"

    @staticmethod
    def required_fields() -> tuple[str, ...]:
        return (
            "report_type",
            "narrative",
            "urgency_level",
            "caller_safety_concern",
            "referral_target",
            "status",
        )

    def is_ready_for_summary(self) -> bool:
        return bool(self.narrative.strip())
