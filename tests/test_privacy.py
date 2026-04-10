"""Tests for privacy and scrubbing behavior."""

from src.domain.services.privacy import scrub_phone_number, strip_direct_identifiers


def test_scrub_phone_number_hides_most_digits() -> None:
    assert scrub_phone_number("+254712345678") == "[redacted]78"


def test_strip_direct_identifiers_removes_sensitive_keys() -> None:
    result = strip_direct_identifiers(
        {
            "phone_number": "0712345678",
            "caller_name": "Jane",
            "narrative": "An officer asked me for money.",
        }
    )
    assert "phone_number" not in result
    assert "caller_name" not in result
    assert result["narrative"] == "An officer asked me for money."
