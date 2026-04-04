"""Preview helpers for local review and tests."""

from __future__ import annotations

from typing import Any

from app.api.routes.intake import serialize_response
from app.api.schemas.intake import IntakeRequest
from app.core.config import AppSettings, get_settings
from app.runtime import AgentBlueprint, PrototypeRuntime, build_agent_blueprint, build_runtime
from app.services.intake_service import submit_intake


def run_intake_preview(payload: dict[str, Any], config: AppSettings | None = None) -> dict[str, object]:
    """Process an intake payload through the prototype pipeline."""

    runtime: PrototypeRuntime = build_runtime(config or get_settings())
    request = IntakeRequest(**payload)
    response = submit_intake(request, runtime["store"])
    return serialize_response(response)


def preview_agent_blueprint(config: AppSettings | None = None) -> AgentBlueprint:
    """Return the review-friendly agent blueprint for local inspection."""

    return build_agent_blueprint(config or get_settings())


__all__ = [
    "preview_agent_blueprint",
    "run_intake_preview",
]
