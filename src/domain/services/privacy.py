"""Privacy rules — stripping and scrubbing caller-linked identifiers."""

from __future__ import annotations

REDACTED = "[redacted]"


def scrub_phone_number(phone_number: str | None) -> str | None:
    """Mask all but the last two digits of a phone number."""
    if not phone_number:
        return None
    digits = "".join(ch for ch in phone_number if ch.isdigit())
    if len(digits) <= 2:
        return REDACTED
    return f"{REDACTED}{digits[-2:]}"


def strip_direct_identifiers(payload: dict[str, str]) -> dict[str, str]:
    """Return a copy of caller data with all direct identity keys removed."""
    blocked = {"phone_number", "caller_name", "national_id", "home_address"}
    return {key: value for key, value in payload.items() if key not in blocked}
