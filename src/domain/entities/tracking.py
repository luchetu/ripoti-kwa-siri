"""TrackingReference — value object for caller follow-up."""

from __future__ import annotations

from pydantic import BaseModel


class TrackingReference(BaseModel):
    tracking_code: str
    status: str = "received"
