"""FastAPI application entrypoint for the ripoti-kwa-siri prototype."""

from __future__ import annotations

from typing import Any

from app.api.routes.intake import serialize_response
from app.api.schemas.intake import IntakeRequest
from app.core.config import AppSettings, get_settings
from app.runtime import AgentBlueprint, PrototypeRuntime, build_agent_blueprint, build_runtime
from app.services.intake_service import submit_intake


def create_app(config: AppSettings | None = None):
    """
    Create a minimal FastAPI app for local review and integration.

    The import stays inside this function so the rest of the prototype can be
    reviewed without requiring the web stack to be installed immediately.
    """

    from fastapi import FastAPI

    config = config or get_settings()
    runtime: PrototypeRuntime = build_runtime(config)
    app = FastAPI(title="ripoti-kwa-siri prototype", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "app": config.app_name}

    @app.get("/agent/blueprint")
    def agent_blueprint() -> AgentBlueprint:
        return build_agent_blueprint(config)

    @app.post("/intake/preview")
    def intake_preview(payload: dict[str, Any]) -> dict[str, object]:
        request = IntakeRequest(**payload)
        response = submit_intake(request, runtime["store"])
        return serialize_response(response)

    return app


try:
    app = create_app()
except ModuleNotFoundError:
    app = None
