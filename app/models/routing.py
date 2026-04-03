"""Routing data structures for classification and destination mapping."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ReportType = Literal["corruption", "organized_crime", "unknown"]
RoutingConfidence = Literal["high", "medium", "low"]


@dataclass(frozen=True, slots=True)
class RoutingClassification:
    report_type: ReportType
    confidence: RoutingConfidence
    reasoning: str
