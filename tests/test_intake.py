"""Tests for the intake flow."""

from app.api.schemas.intake import IntakeRequest
from app.call_flow.controller import IntakeFlowController
from app.core.config import get_settings
from app.preview import preview_agent_blueprint, run_intake_preview
from app.services.case_store import InMemoryCaseStore
from app.services.intake_service import build_metadata_preview, submit_intake


def test_intake_flow_loads_agent_prompt() -> None:
    controller = IntakeFlowController.from_prompt_path(get_settings().prompt_path)
    assert controller.agent_name == "Sauti"
    assert "You are Sauti" in controller.instructions

def test_submit_intake_returns_tracking_and_routing() -> None:
    request = IntakeRequest(
        narrative="A county officer asked me for a bribe at a checkpoint.",
        caller_metadata={"phone_number": "+254712345678", "caller_name": "Jane"},
    )
    response = submit_intake(request, InMemoryCaseStore())
    assert response.tracking_code
    assert response.report_type == "corruption"
    assert response.referral_target == "EACC"


def test_build_metadata_preview_scrubs_phone_number() -> None:
    preview = build_metadata_preview(
        {"phone_number": "+254712345678", "caller_name": "Jane", "note": "safe"}
    )
    assert preview["phone_number_preview"] == "[redacted]78"
    assert "caller_name" not in preview


def test_build_agent_blueprint_exposes_runtime_shape() -> None:
    blueprint = preview_agent_blueprint()
    assert blueprint["agent_name"] == "Sauti"
    assert blueprint["opening_message"].startswith("You have reached ripoti-kwa-siri")


def test_run_intake_preview_processes_payload_end_to_end() -> None:
    result = run_intake_preview(
        {
            "narrative": "A county officer asked me for a bribe at a checkpoint.",
            "caller_metadata": {"phone_number": "+254712345678"},
        }
    )
    assert result["tracking_code"]
    assert result["referral_target"] == "EACC"
