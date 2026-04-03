# ripoti-kwa-siri

`ripoti-kwa-siri` is a voice-first anonymous reporting platform for corruption and organized crime tips. It is designed so a citizen can call a dedicated number, safely share what they know, receive a tracking code, and have the report routed to the right investigative body without requiring a face-to-face visit.

This repository is currently at the prototype architecture stage. The goal is to prove the reporting flow with a small codebase before splitting the system into larger services.

## Service Flow

1. `The Call`: a citizen calls the hotline to report corruption, abuse of office, trafficking, extortion, or organized crime.
2. `The Shield`: the intake flow explains that the report will be stored without attaching the caller's phone number to the case record.
3. `The Interview`: the agent listens, captures the story, and asks clarifying questions that improve investigative value.
4. `The Receipt`: the caller receives a unique tracking code such as `Kiongozi-77`.
5. `The Hand-off`: the report is summarized, the final summary is classified, and the case is securely routed to the appropriate investigative body.

## Prototype Architecture

```mermaid
flowchart LR
    A["Citizen Caller"] --> B["Dedicated Hotline"]
    B --> C["Telephony Gateway"]
    C --> D["Anonymous Reporting Backend"]

    D --> E["Call Flow Module"]
    D --> F["Privacy Service"]
    D --> G["Case Store"]
    D --> H["Routing Service"]

    E --> E1["Interview Questions"]
    E --> E2["Summary Builder"]
    G --> G1["Tracking Code Generator"]

    H --> I["EACC"]
    H --> J["DCI"]
    H --> K["Other Approved Bodies"]

    D --> L["Audit Logs"]
```

## Voice Agent Architecture

For the prototype, `ripoti-kwa-siri` uses a single caller-facing voice agent named `Sauti`. The design stays intentionally simple:

- one real-time voice session
- one main voice agent
- one runtime prompt from `prompts/anonymous_reporting_agent.yaml`
- one structured five-stage call flow
- backend support for privacy, tracking, storage, summary-based classification, and routing

```mermaid
flowchart TD
    A["Citizen Caller"] --> B["Telephony Entry"]
    B --> C["Real-Time Voice Session"]
    C --> D["Sauti Voice Agent"]

    D --> E["Greeting and Reassurance"]
    D --> F["Initial Report Capture"]
    D --> G["Clarification"]
    D --> H["Summary Confirmation"]
    D --> I["Tracking and Close"]

    D --> J["Case Store"]
    D --> K["Privacy Handling"]
    D --> L["Tracking Code Generation"]
    D --> M["Summary Classification And Routing"]

    M --> N["EACC"]
    M --> O["DCI"]
    M --> P["Review Queue"]
```

See [voice-agent-architecture.md](/Users/admin/ripoti-kwa-siri/docs/architecture/voice-agent-architecture.md) for the fuller design.

## Repository Structure

```text
ripoti-kwa-siri/
├── README.md
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── schemas/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── call_flow/
│   │   ├── controller.py
│   ├── integrations/
│   │   ├── telephony.py
│   │   ├── realtime.py
│   │   └── llm.py
│   ├── preview.py
│   ├── runtime.py
│   ├── services/
│   │   ├── case_store.py
│   │   ├── intake_service.py
│   │   ├── privacy.py
│   │   ├── routing.py
│   │   ├── summary.py
│   │   └── tracking.py
│   └── models/
│       ├── case.py
│       └── tracking.py
├── run_agent.py
├── run_api.py
├── tests/
│   ├── test_intake.py
│   ├── test_privacy.py
│   └── test_routing.py
├── infra/
│   ├── containers/
│   └── scripts/
└── docs/
    ├── architecture/
    │   ├── ripoti-kwa-siri-architecture.md
    │   ├── case-data-model.md
    │   └── voice-agent-architecture.md
    └── product/
        ├── ripoti-kwa-siri-service-flow.md
        ├── routing-rules.md
        └── call-stages.md
```

## What Each Area Means

- `app/api`: webhook endpoints, health endpoints, and request schemas
- `app/main.py`: FastAPI application entrypoint for the prototype preview API
- `app/call_flow`: the intake controller for the voice agent
- `app/integrations`: provider-specific adapters kept at the edge of the prototype
- `app/runtime.py`: shared runtime assembly for the voice agent and preview paths
- `app/preview.py`: local preview helpers used by tests and review flows
- `app/services`: core prototype logic for intake, privacy, case storage, summary, post-call classification, tracking, and routing
- `app/models`: simple case and tracking data models
- `run_agent.py`: root entrypoint for the real-time voice agent
- `run_api.py`: root entrypoint for the FastAPI preview app
- `tests`: small focused tests for intake, privacy, and routing behavior
- `infra`: local container and helper scripts for running the prototype
- `docs`: architecture notes, service flows, and product decisions

## Prototype Scope

- handle intake for one anonymous report from start to finish
- generate a tracking code
- scrub caller identifiers before storing the case
- create a short referral summary
- classify the final summary into a broad routing category
- route the case to a mock or early hand-off endpoint

## Design Principles

- `Anonymous by default`: the case record should not carry direct caller identity
- `Minimize data`: ask only for details that help routing or investigation
- `Track without identity`: the caller uses a tracking code instead of an in-person reference
- `Route intelligently`: each case goes to the institution best suited to act on it
- `Audit internally`: keep internal accountability without exposing the caller

## Important Note

Claims such as `encrypted`, `anonymous`, or `scrubbed` should only be shown to users when the actual telephony, storage, and hand-off implementation truly supports them.

## Setup (uv)

- Install uv: https://docs.astral.sh/uv/getting-started/installation/
- Install dependencies: `uv sync`
- Copy environment: `cp .env.example .env.local` and set your keys (realtime URL/key/secret and model choices)
- Run the real-time agent: `uv run run_agent.py`
- Run the REST preview (optional): `uv run run_api.py`
