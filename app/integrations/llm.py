"""Voice-model configuration for the prototype runtime."""

from __future__ import annotations

from dataclasses import dataclass

from app.core.config import get_settings


@dataclass(frozen=True, slots=True)
class VoiceModelSettings:
    live_model: str
    live_voice: str
    preemptive_generation: bool


def load_voice_model_settings() -> VoiceModelSettings:
    """Load Gemini Live settings from the environment."""

    settings = get_settings()
    return VoiceModelSettings(
        live_model=settings.voice_live_model,
        live_voice=settings.voice_live_voice,
        preemptive_generation=settings.voice_preemptive_generation,
    )
