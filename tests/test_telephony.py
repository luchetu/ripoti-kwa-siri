"""Tests for telephony room-bridging payloads."""

from app.core.config import AppSettings
from app.integrations.telephony import (
    build_dispatch_rule_request,
    build_inbound_trunk_request,
    export_bridge_config,
    serialize_dispatch_rule_request,
    serialize_inbound_trunk_request,
)


def test_dispatch_rule_targets_sauti_agent_and_room_prefix() -> None:
    settings = AppSettings(
        voice_agent_name="sauti",
        dispatch_rule_name="ripoti-kwa-siri-inbound",
        dispatch_room_prefix="rks-call-",
    )

    payload = serialize_dispatch_rule_request(build_dispatch_rule_request(settings))

    assert payload["name"] == "ripoti-kwa-siri-inbound"
    assert payload["rule"]["dispatchRuleIndividual"]["roomPrefix"] == "rks-call-"
    assert payload["roomConfig"]["agents"][0]["agentName"] == "sauti"


def test_inbound_trunk_payload_includes_numbers_and_auth() -> None:
    settings = AppSettings(
        sip_trunk_name="ripoti-kwa-siri-inbound",
        sip_inbound_numbers=["+254700000000"],
        sip_auth_username="hotline",
        sip_auth_password="secret",
    )

    payload = serialize_inbound_trunk_request(build_inbound_trunk_request(settings))

    assert payload["name"] == "ripoti-kwa-siri-inbound"
    assert payload["numbers"] == ["+254700000000"]
    assert payload["authUsername"] == "hotline"
    assert payload["authPassword"] == "secret"


def test_export_bridge_config_returns_both_payloads() -> None:
    settings = AppSettings(
        voice_agent_name="sauti",
        dispatch_rule_name="ripoti-kwa-siri-inbound",
        dispatch_room_prefix="rks-call-",
        sip_trunk_name="ripoti-kwa-siri-inbound",
        sip_inbound_numbers=["+254700000000"],
    )

    payload = export_bridge_config(settings)

    assert "inbound_trunk" in payload
    assert "dispatch_rule" in payload
    assert payload["dispatch_rule"]["roomConfig"]["agents"][0]["agentName"] == "sauti"
    assert payload["inbound_trunk"]["numbers"] == ["+254700000000"]
