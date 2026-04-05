"""Telephony bridge configuration for inbound call dispatch."""

from __future__ import annotations

from typing import TypedDict

from pydantic import BaseModel, Field

from app.core.config import AppSettings, get_settings


class DispatchAgent(BaseModel):
    agent_name: str = Field(serialization_alias="agentName")


class RoomConfig(BaseModel):
    agents: list[DispatchAgent]


class DispatchRuleIndividual(BaseModel):
    room_prefix: str = Field(serialization_alias="roomPrefix")


class DispatchRuleShape(BaseModel):
    dispatch_rule_individual: DispatchRuleIndividual = Field(
        serialization_alias="dispatchRuleIndividual"
    )


class DispatchRuleCreateRequest(BaseModel):
    name: str
    rule: DispatchRuleShape
    room_config: RoomConfig = Field(serialization_alias="roomConfig")


class InboundTrunkCreateRequest(BaseModel):
    name: str
    numbers: list[str]
    auth_username: str | None = Field(default=None, serialization_alias="authUsername")
    auth_password: str | None = Field(default=None, serialization_alias="authPassword")


class TelephonyBridgeConfig(TypedDict):
    inbound_trunk: dict[str, object]
    dispatch_rule: dict[str, object]


def build_dispatch_rule_request(config: AppSettings | None = None) -> DispatchRuleCreateRequest:
    """Build the individual-room dispatch rule for inbound anonymous reports."""

    settings = config or get_settings()
    return DispatchRuleCreateRequest(
        name=settings.dispatch_rule_name,
        rule=DispatchRuleShape(
            dispatch_rule_individual=DispatchRuleIndividual(
                room_prefix=settings.dispatch_room_prefix,
            )
        ),
        room_config=RoomConfig(
            agents=[DispatchAgent(agent_name=settings.voice_agent_name)]
        ),
    )


def build_inbound_trunk_request(config: AppSettings | None = None) -> InboundTrunkCreateRequest:
    """Build the inbound trunk payload for the reporting hotline."""

    settings = config or get_settings()
    return InboundTrunkCreateRequest(
        name=settings.sip_trunk_name,
        numbers=list(settings.sip_inbound_numbers),
        auth_username=settings.sip_auth_username,
        auth_password=settings.sip_auth_password,
    )


def serialize_dispatch_rule_request(
    request: DispatchRuleCreateRequest,
) -> dict[str, object]:
    """Return a JSON-ready dispatch rule payload using provider field names."""

    return request.model_dump(by_alias=True, exclude_none=True)


def serialize_inbound_trunk_request(
    request: InboundTrunkCreateRequest,
) -> dict[str, object]:
    """Return a JSON-ready inbound trunk payload using provider field names."""

    return request.model_dump(by_alias=True, exclude_none=True)


def export_bridge_config(config: AppSettings | None = None) -> TelephonyBridgeConfig:
    """Return the full telephony bridge config for local review or CLI export."""

    settings = config or get_settings()
    return {
        "inbound_trunk": serialize_inbound_trunk_request(
            build_inbound_trunk_request(settings)
        ),
        "dispatch_rule": serialize_dispatch_rule_request(
            build_dispatch_rule_request(settings)
        ),
    }


def build_livekit_inbound_trunk_request(config: AppSettings | None = None):
    """Build a LiveKit API request object for creating the inbound SIP trunk."""

    from livekit import api

    settings = config or get_settings()
    trunk = api.SIPInboundTrunkInfo(
        name=settings.sip_trunk_name,
        numbers=list(settings.sip_inbound_numbers),
        auth_username=settings.sip_auth_username,
        auth_password=settings.sip_auth_password,
    )
    return api.CreateSIPInboundTrunkRequest(trunk=trunk)


def build_livekit_dispatch_rule_request(config: AppSettings | None = None):
    """Build a LiveKit API request object for creating the SIP dispatch rule."""

    from livekit import api

    settings = config or get_settings()
    rule = api.SIPDispatchRuleInfo(
        name=settings.dispatch_rule_name,
        rule=api.SIPDispatchRule(
            dispatch_rule_individual=api.SIPDispatchRuleIndividual(
                room_prefix=settings.dispatch_room_prefix,
            )
        ),
        room_config=api.RoomConfiguration(
            agents=[api.RoomAgentDispatch(agent_name=settings.voice_agent_name)]
        ),
    )
    return api.CreateSIPDispatchRuleRequest(dispatch_rule=rule)
