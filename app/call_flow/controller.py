"""Intake flow assembly for the anonymous reporting agent."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.core.config import extract_yaml_block


@dataclass(frozen=True, slots=True)
class IntakeFlowController:
    agent_name: str
    instructions: str

    @classmethod
    def from_prompt_path(cls, prompt_path: Path) -> "IntakeFlowController":
        instructions = extract_yaml_block(prompt_path, "instructions")
        return cls(agent_name="Sauti", instructions=instructions)

    def opening_message(self) -> str:
        return (
            "You have reached ripoti-kwa-siri. I can help you submit a "
            "confidential report. Please tell me what happened."
        )
