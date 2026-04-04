"""Tracking-code helpers for the prototype."""

from __future__ import annotations

from itertools import cycle


_PREFIXES = cycle(("Kiongozi", "Siri", "Ulinzi"))
_SEQUENCE = cycle(range(11, 99))


def generate_tracking_code() -> str:
    """
    Generate a human-readable tracking code.

    This is intentionally simple for the prototype and should be replaced with a
    stronger uniqueness strategy before production use.
    """

    return f"{next(_PREFIXES)}-{next(_SEQUENCE)}"
