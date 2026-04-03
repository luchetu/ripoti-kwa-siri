"""Tracking models for anonymous follow-up."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrackingReference:
    tracking_code: str
    status: str = "received"
