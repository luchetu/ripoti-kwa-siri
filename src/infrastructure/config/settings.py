"""Application settings — environment-driven configuration."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

import yaml
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]  # src/infrastructure/config/ → project root


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ripoti-kwa-siri"
    prompt_path: Path = Field(
        default=BASE_DIR / "prompts" / "anonymous_reporting_agent.yaml"
    )

    # Realtime transport
    realtime_url: str | None = None
    realtime_api_key: str | None = None
    realtime_api_secret: str | None = None
    voice_agent_name: str = "sauti"

    # Gemini Live (native audio)
    google_api_key: str | None = None
    voice_live_model: str = "google/gemini-2.5-flash-native-audio-preview-12-2025"
    voice_live_voice: str = "Puck"
    voice_preemptive_generation: bool = True
    routing_model: str = "gemini-2.5-flash"

    # OpenAI fallback
    openai_api_key: str | None = None
    openai_routing_model: str = "gpt-4.1-mini"

    # Telephony and dispatch
    sip_inbound_numbers: list[str] = Field(default_factory=list)
    sip_auth_username: str | None = None
    sip_auth_password: str | None = None
    sip_trunk_name: str = "ripoti-kwa-siri-inbound"
    dispatch_rule_name: str = "ripoti-kwa-siri-inbound"
    dispatch_room_prefix: str = "rks-call-"

    @field_validator("sip_inbound_numbers", mode="before")
    @classmethod
    def _parse_sip_inbound_numbers(cls, value: Any) -> Any:
        if isinstance(value, str):
            if not value.strip():
                return []
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


@lru_cache(maxsize=None)
def load_prompt_document(prompt_path: str | Path) -> Mapping[str, Any]:
    """Load a YAML prompt document once per process."""
    resolved = Path(prompt_path).resolve()
    with resolved.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Prompt file must be a top-level mapping: {resolved}")
    return cast(Mapping[str, Any], data)


def extract_yaml_block(prompt_path: str | Path, key: str) -> str:
    """Read a named top-level string field from a cached YAML prompt document."""
    document = load_prompt_document(prompt_path)
    value = document.get(key)
    if not isinstance(value, str):
        raise ValueError(
            f"Prompt field '{key}' must be a string in {Path(prompt_path).resolve()}"
        )
    return value
