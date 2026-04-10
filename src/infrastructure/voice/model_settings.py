"""Voice model settings — loaded from environment config."""

from __future__ import annotations

from dataclasses import dataclass

from src.infrastructure.config.settings import get_settings


@dataclass(frozen=True, slots=True)
class VoiceModelSettings:
    live_model: str
    live_voice: str
    preemptive_generation: bool


def load_voice_model_settings() -> VoiceModelSettings:
    settings = get_settings()
    return VoiceModelSettings(
        live_model=settings.voice_live_model,
        live_voice=settings.voice_live_voice,
        preemptive_generation=settings.voice_preemptive_generation,
    )
