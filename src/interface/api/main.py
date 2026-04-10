"""FastAPI application factory."""

from __future__ import annotations

from typing import Any

from src.interface.api.routes.intake import handle_intake


def create_app(use_case=None, settings=None):
    from fastapi import FastAPI

    from src.infrastructure.config.settings import get_settings
    from src.infrastructure.classifiers.fallback import FallbackRoutingClassifier
    from src.infrastructure.persistence.memory_case_repository import InMemoryCaseRepository
    from src.application.use_cases.submit_report import SubmitReportUseCase

    config = settings or get_settings()
    resolved_use_case = use_case or SubmitReportUseCase(
        repository=InMemoryCaseRepository(),
        classifier=FallbackRoutingClassifier(),
    )

    app = FastAPI(title="ripoti-kwa-siri", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "app": config.app_name}

    @app.post("/intake/preview")
    def intake_preview(payload: dict[str, Any]) -> dict[str, Any]:
        return handle_intake(payload, resolved_use_case)

    return app


try:
    app = create_app()
except ModuleNotFoundError:
    app = None
