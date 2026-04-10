"""ICaseRepository — the domain contract for case persistence.

Infrastructure implements this. The domain and application layers depend
only on this interface, never on a concrete implementation.
"""

from __future__ import annotations

from typing import Protocol

from src.domain.entities.case import CaseReport


class ICaseRepository(Protocol):
    """Persist and retrieve anonymous case reports."""

    def save(self, report: CaseReport) -> str:
        """Persist a report and return its assigned case_id."""
        ...

    def get(self, case_id: str) -> CaseReport | None:
        """Retrieve a report by case_id, or None if not found."""
        ...
