"""HTTP request and response schemas for the intake endpoint."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class IntakeRequest(BaseModel):
    narrative: str
    location: str | None = None
    event_time: str | None = None
    entities_involved: list[str] = Field(default_factory=list)
    supporting_details: dict[str, str] = Field(default_factory=dict)
    source_basis: str | None = None
    caller_safety_concern: bool = False
    urgency_level: str = "normal"
    caller_metadata: dict[str, str] = Field(default_factory=dict)


class IntakeResponse(BaseModel):
    case_id: str
    tracking_code: str
    report_type: str
    referral_target: str
    case_summary: str
    caller_metadata_preview: dict[str, Any]
