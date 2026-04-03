# ripoti-kwa-siri Service Flow

## Product Goal

Enable a citizen to safely report corruption or organized crime by phone, receive a private tracking code, and have the report routed to the correct authority without requiring an in-person visit.

## End-to-End Journey

### 1. The Call

The citizen dials a dedicated reporting number. The platform answers with either a voice agent or a trained human intake agent.

Example opening:

> You have reached ripoti-kwa-siri. You can report corruption or organized crime here. We will record your report without attaching your phone number to the case file.

### 2. The Shield

The caller receives a short explanation of privacy protections and limitations.

Goals:

- reassure the caller
- avoid false promises
- explain what will and will not be stored

Suggested system behavior:

- scrub the phone number from the case record
- avoid collecting the caller's name unless necessary
- present a short consent and safety notice

### 3. The Interview

The system captures the narrative, then asks clarifying questions that improve case usefulness.

Core prompts:

- What happened?
- Where did it happen?
- When did it happen?
- Who was involved?
- How do you know this information?
- Did you notice any vehicle, office, badge, account, or document details?
- Is anyone in immediate danger?

Example follow-up:

> You mentioned a government vehicle. Do you remember the color, registration number, or any markings on the side?

### 4. The Receipt

After the report is saved, the system issues a tracking code instead of an occurrence-book reference that requires a physical visit.

Example:

> Your tracking code is Kiongozi-77. Keep it safe. You can use it later to check whether your report has been received or referred.

Product requirements:

- tracking codes must be easy to read aloud
- tracking codes must not be sequential
- tracking codes must be unique and difficult to guess

### 5. The Hand-off

The case is summarized, categorized, and referred to the right institution.

Examples:

- `EACC`: bribery, procurement fraud, abuse of office, unexplained wealth
- `DCI`: organized crime, trafficking, extortion, criminal conspiracy
- `Other approved bodies`: sector-specific or county-level oversight cases

The referral package should include:

- anonymous case ID
- tracking code
- summary of allegations
- event timeline
- location details
- involved entities
- risk or urgency flags
- available evidence or witness context

## Recommended Folder Structure

```text
ripoti-kwa-siri/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── routes/
│   │   └── schemas/
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── call_flow/
│   │   ├── intake.py
│   │   ├── questions.py
│   │   ├── summary.py
│   │   └── tracking.py
│   ├── integrations/
│   │   ├── telephony.py
│   │   ├── realtime.py
│   │   └── llm.py
│   ├── services/
│   │   ├── case_store.py
│   │   ├── privacy.py
│   │   └── routing.py
│   └── models/
│       ├── case.py
│       └── tracking.py
├── tests/
│   ├── test_intake.py
│   ├── test_privacy.py
│   └── test_routing.py
├── infra/
│   ├── containers/
│   └── scripts/
└── docs/
    ├── architecture/
    └── product/
```

This structure keeps the prototype in one app while still separating the important concerns:

- `app/call_flow`: reporting journey and interview logic
- `app/integrations`: provider-specific adapters kept at the edge
- `app/services`: privacy, routing, and persistence logic
- `app/models`: simple data structures for cases and tracking
- `tests`: small behavior-focused checks for the first version

## Non-Functional Requirements

- `Privacy`: do not expose caller identity in the standard case record
- `Auditability`: preserve internal action logs for oversight and integrity
- `Resilience`: keep the intake path available during call spikes or partner outages
- `Traceability`: every referral should have a delivery and acknowledgement trail
- `Human override`: allow trained staff to take over high-risk or sensitive calls

## Open Product Decisions

- Will the first release be fully automated, human-assisted, or hybrid?
- Will callers be able to check status by phone, SMS, or both?
- What exact wording can be legally used for privacy assurances?
- Which institutions are in scope for the first routing version?
