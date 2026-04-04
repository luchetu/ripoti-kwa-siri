"""HTTP-facing helpers for prototype intake APIs."""

from __future__ import annotations

from app.api.schemas.intake import IntakeResponse


def serialize_response(response: IntakeResponse) -> dict[str, object]:
    """Convert the response model into plain JSON-ready data."""

    return response.model_dump()
