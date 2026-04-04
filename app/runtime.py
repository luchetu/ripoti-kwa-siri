"""Core runtime assembly for the ripoti-kwa-siri prototype."""

from __future__ import annotations

from typing import TypedDict

from app.call_flow.controller import IntakeFlowController
from app.core.config import AppSettings, get_settings
from app.models.case import CaseDraft
from app.services.case_store import InMemoryCaseStore


class PrototypeRuntime(TypedDict):
    config: AppSettings
    intake: IntakeFlowController
    store: InMemoryCaseStore


class AgentBlueprint(TypedDict):
    agent_name: str
    prompt_path: str
    opening_message: str
    required_case_fields: list[str]


def build_runtime(config: AppSettings | None = None) -> PrototypeRuntime:
    """Build the minimal runtime objects needed by the first prototype."""

    config = config or get_settings()
    intake = IntakeFlowController.from_prompt_path(config.prompt_path)
    store = InMemoryCaseStore()
    return {
        "config": config,
        "intake": intake,
        "store": store,
    }


def build_agent_blueprint(config: AppSettings | None = None) -> AgentBlueprint:
    """Return a review-friendly summary of how the voice agent is configured."""

    runtime = build_runtime(config)
    intake: IntakeFlowController = runtime["intake"]
    return {
        "agent_name": intake.agent_name,
        "prompt_path": str(runtime["config"].prompt_path),
        "opening_message": intake.opening_message(),
        "required_case_fields": list(CaseDraft.required_fields()),
    }
