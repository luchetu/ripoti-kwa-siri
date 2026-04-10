"""Tracking code generation — cryptographically random, collision-resistant."""

from __future__ import annotations

import secrets

_PREFIXES = ("Kiongozi", "Siri", "Ulinzi")


def generate_tracking_code() -> str:
    """
    Generate a human-readable, unpredictable tracking code.

    Format: {prefix}-{6-hex-chars}  e.g. "Kiongozi-3f9a12"

    Uses secrets.choice and secrets.token_hex so codes are:
    - Unpredictable (no cycle, no sequential counter)
    - Unique enough for prototype scale (16^6 = 16M combinations per prefix)
    - Human-speakable over a phone call
    """
    prefix = secrets.choice(_PREFIXES)
    suffix = secrets.token_hex(3)  # 3 bytes = 6 hex chars
    return f"{prefix}-{suffix}"
