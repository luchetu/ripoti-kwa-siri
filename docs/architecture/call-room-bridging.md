# ripoti-kwa-siri Call Room Bridging

## Purpose

This document explains how an inbound phone call should be bridged into a real-time room so the `Sauti` voice agent can join and handle intake.

It follows the current LiveKit telephony and agent dispatch documentation and is aligned with the installed `livekit-agents` 1.5.x API shape used by this repo.

## High-Level Flow

The bridging model is:

1. a caller dials the reporting number
2. the inbound trunk accepts the call
3. a dispatch rule creates or selects a room
4. the caller is placed into that room as a SIP participant
5. the `Sauti` agent is dispatched into the same room
6. the voice session starts and the agent begins speaking

This means the phone call is not connected directly to the agent process.
The call is first bridged into a room, and the agent joins that room as another participant.

## Why This Is the Right Pattern

This is the standard agent telephony pattern in the current LiveKit docs:

- inbound calls are accepted through an inbound trunk
- dispatch rules decide what room is used
- dispatch rules can also specify which agent should join
- explicit agent dispatch is recommended for inbound SIP calls

For `ripoti-kwa-siri`, that is the best fit because:

- each caller should get an isolated room
- the agent name is explicit and stable
- the setup works cleanly with later human transfer or supervisor joins

## Recommended Bridging Design

The prototype should use:

- one inbound trunk for the hotline
- one dispatch rule using an individual room strategy
- one explicitly named agent: `sauti`

The room naming strategy should create a fresh room per call, for example with a prefix such as:

- `rks-call-`

This avoids mixing callers in a shared room and keeps the telephony flow aligned with the anonymous reporting model.

## Dispatch Rule Shape

The current docs recommend explicit agent dispatch for inbound SIP calls through the dispatch rule's room configuration.

Conceptually, the dispatch rule should look like this:

```json
{
  "name": "ripoti-kwa-siri-inbound",
  "rule": {
    "dispatchRuleIndividual": {
      "roomPrefix": "rks-call-"
    }
  },
  "roomConfig": {
    "agents": [
      {
        "agentName": "sauti"
      }
    ]
  }
}
```

This means:

- every inbound caller is bridged into a dedicated room
- the room name is generated with the given prefix
- the `sauti` agent is dispatched into that same room automatically

## Agent Runtime Alignment

The voice runtime must register the same agent name that the dispatch rule references.

In this project, that happens in:

- [app/integrations/realtime.py](/Users/admin/ripoti-kwa-siri/app/integrations/realtime.py)

The key alignment rule is:

- dispatch rule agent name: `sauti`
- runtime session decorator agent name: `sauti`

If these names do not match, the call can be bridged into a room but the intended agent will not be dispatched correctly.

## Current Runtime Pattern

The current runtime shape should be:

1. register the session entrypoint with `agent_name="sauti"`
2. create an `AgentSession`
3. start the session in the room from `ctx.room`
4. use `room_options` with audio input settings
5. generate the opening reply after the session starts

This matches the current Python `AgentSession.start(...)` API in `livekit-agents` 1.5.x, where `room_options` is the up-to-date parameter and `room_input_options` is deprecated.

## What the Caller Becomes

When the call is bridged, the caller becomes a SIP participant in the room.

That matters because:

- the agent can interact with the caller like any other room participant
- additional participants can be added later if needed
- a human operator can join the same room in later versions

This is the foundation for future warm-transfer or human-escalation designs.

## Human Fallback Implication

Because the caller is already in a room, human fallback can later be implemented in one of two ways:

- dispatch or invite a human participant into the same room
- transfer the caller to a human-operated room if operationally required

For the prototype, the first option is the better long-term direction because it preserves context and avoids rebuilding the call state.

## Operational Notes

- use one room per inbound call
- use explicit agent dispatch for SIP inbound calls
- keep the agent name stable across infrastructure and code
- keep the opening prompt short so the caller can begin speaking quickly
- preserve the room-based design because it supports later human fallback

## Relationship to Other Docs

- [voice-agent-architecture.md](/Users/admin/ripoti-kwa-siri/docs/architecture/voice-agent-architecture.md): how the voice agent fits into the system
- [human-fallback-policy.md](/Users/admin/ripoti-kwa-siri/docs/product/human-fallback-policy.md): when to involve a human
- [call-stages.md](/Users/admin/ripoti-kwa-siri/docs/product/call-stages.md): the intake stages once the call is in the room

## Sources

- [Accepting inbound calls](https://docs.livekit.io/sip/accepting-calls)
- [Agent dispatch](https://docs.livekit.io/agents/build/dispatch/)
- [Gemini Live API plugin](https://docs.livekit.io/agents/models/realtime/plugins/gemini.md)
