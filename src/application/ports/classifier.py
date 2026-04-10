"""Classifier ports — interfaces the application layer depends on.

Infrastructure provides concrete implementations.
The application layer never imports from infrastructure directly.
"""

from __future__ import annotations

from typing import Protocol

from src.domain.entities.routing import RoutingClassification


class RoutingClassifier(Protocol):
    """Classify a report summary into a routing decision."""

    def classify(self, summary: str) -> RoutingClassification:
        ...


class LiveRoutingClassifier(RoutingClassifier, Protocol):
    """A classifier backed by a live provider that can report availability."""

    def is_available(self) -> bool:
        ...
