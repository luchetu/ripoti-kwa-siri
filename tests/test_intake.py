"""Tests for the intake use case."""

from src.application.use_cases.submit_report import SubmitReportRequest, SubmitReportUseCase
from src.infrastructure.classifiers.fallback import FallbackRoutingClassifier
from src.infrastructure.classifiers.rule_based import RuleBasedRoutingClassifier
from src.infrastructure.config.settings import get_settings
from src.infrastructure.persistence.memory_case_repository import InMemoryCaseRepository
from src.infrastructure.voice.agent import realtime_dependencies_available


def _use_case() -> SubmitReportUseCase:
    return SubmitReportUseCase(
        repository=InMemoryCaseRepository(),
        classifier=RuleBasedRoutingClassifier(),
    )


def test_submit_report_returns_tracking_and_routing() -> None:
    request = SubmitReportRequest(
        narrative="A county officer asked me for a bribe at a checkpoint.",
        location=None,
        event_time=None,
        entities_involved=[],
        supporting_details={},
        source_basis=None,
        caller_safety_concern=False,
        urgency_level="normal",
        caller_metadata={"phone_number": "+254712345678", "caller_name": "Jane"},
    )
    response = _use_case().execute(request)
    assert response.tracking_code
    assert response.report_type == "corruption"
    assert response.referral_target == "EACC"


def test_submit_report_scrubs_phone_number() -> None:
    request = SubmitReportRequest(
        narrative="A bribe was requested.",
        location=None,
        event_time=None,
        entities_involved=[],
        supporting_details={},
        source_basis=None,
        caller_safety_concern=False,
        urgency_level="normal",
        caller_metadata={"phone_number": "+254712345678", "caller_name": "Jane"},
    )
    response = _use_case().execute(request)
    assert response.caller_metadata_preview["phone_number_preview"] == "[redacted]78"
    assert "caller_name" not in response.caller_metadata_preview


def test_tracking_code_is_unpredictable() -> None:
    """Codes should not be sequential — each should be unique."""
    uc = _use_case()
    codes = set()
    for _ in range(10):
        req = SubmitReportRequest(
            narrative="A bribe was requested.",
            location=None, event_time=None, entities_involved=[],
            supporting_details={}, source_basis=None,
            caller_safety_concern=False, urgency_level="normal",
            caller_metadata={},
        )
        codes.add(uc.execute(req).tracking_code)
    assert len(codes) == 10


def test_prompt_loads_sauti_instructions() -> None:
    settings = get_settings()
    from src.infrastructure.config.settings import extract_yaml_block
    instructions = extract_yaml_block(settings.prompt_path, "instructions")
    assert "Sauti" in instructions
