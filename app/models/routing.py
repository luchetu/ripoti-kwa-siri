"""Routing data structures for classification and destination mapping."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


ReportType = Literal["corruption", "organized_crime", "unknown"]
RoutingConfidence = Literal["high", "medium", "low"]


class RoutingClassification(BaseModel):
    report_type: ReportType
    confidence: RoutingConfidence
    reasoning: str
