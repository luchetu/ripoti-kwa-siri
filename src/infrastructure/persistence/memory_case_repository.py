"""InMemoryCaseRepository — implements ICaseRepository for prototype use."""

from __future__ import annotations

from uuid import uuid4

from src.domain.entities.case import CaseReport
from src.domain.repositories.case_repository import ICaseRepository


class InMemoryCaseRepository:
    """Stores case reports in a plain dict. Not persistent across restarts."""

    def __init__(self) -> None:
        self._store: dict[str, CaseReport] = {}

    def save(self, report: CaseReport) -> str:
        case_id = f"case_{uuid4().hex[:8]}"
        self._store[case_id] = report
        return case_id

    def get(self, case_id: str) -> CaseReport | None:
        return self._store.get(case_id)


# Satisfy the type checker — verify the class implements the protocol
_: ICaseRepository = InMemoryCaseRepository()
