---
title: "Ripoti Kwa Siri"
description: "Anonymous phone-based corruption and crime reporting for Kenya"
---

# Ripoti Kwa Siri

**Ripoti Kwa Siri** means *Report Secretly* in Swahili. It is a voice-first platform that lets
any Kenyan citizen report corruption or organized crime by phone — without giving their name,
without visiting a police station, and without fear of exposure.

The caller receives a private tracking code at the end of the call. The report is routed
automatically to the right institution: **EACC** for corruption cases, **DCI** for organized
crime, or a human review queue when the category is unclear.

---

## The Problem It Solves

Most corruption goes unreported. The barriers are:

- **Fear of retaliation** — being seen walking into a station or naming a powerful person
- **Distance and cost** — getting to a physical reporting office in time
- **Distrust** — uncertainty about whether the report will go anywhere

Ripoti Kwa Siri removes all three. A caller dials a number from anywhere, speaks freely, and
hangs up with a tracking code. The system handles everything else.

---

## How a Call Works

A call moves through five stages. The voice agent (powered by a large language model) guides
the conversation naturally without sounding like a form.

| Stage | What happens |
|---|---|
| **1. Greeting** | The agent welcomes the caller, explains the purpose, and gives a brief privacy notice |
| **2. Report capture** | The caller describes what happened in their own words — uninterrupted |
| **3. Clarification** | The agent asks targeted follow-up questions: where, when, who, how |
| **4. Summary confirmation** | The agent reads back a short summary and the caller confirms or corrects it |
| **5. Tracking and close** | A unique tracking code (e.g. `Mzito-77`) is issued and the call ends |

After the call, the case is routed to the correct institution automatically.

---

## Privacy by Design

The platform is built around one rule: **the caller's phone number must never appear in the
case file**.

- The phone number is stripped or tokenised before the case is saved
- The case record contains only what the caller chose to share verbally
- Tracking codes are human-readable but non-sequential — they cannot be guessed or enumerated
- Audit logs record operator and system actions separately from the investigative record

---

## Routing

Once the call ends, an LLM reads the case summary and classifies it. The system
uses a **FallbackRoutingClassifier** — it tries Gemini 2.5 Flash first and falls
back to OpenAI if Gemini is unavailable. If both fail, the case is automatically
placed in the review queue for a human to classify.

The classifier returns a category, a confidence level, and a one-sentence reason
that is written to the audit log.

| Category | Destination | Typical report |
|---|---|---|
| `corruption` | EACC | Bribery, procurement fraud, abuse of office |
| `organized_crime` | DCI | Trafficking, extortion, criminal conspiracy |
| `unknown` | Review queue | Incomplete, ambiguous, or low-confidence reports |

No report is rejected for being unclear. If the LLM cannot classify confidently,
the case goes to a human reviewer rather than being dropped.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Voice agent | LiveKit Agents SDK |
| Speech-to-text | Deepgram Nova-3 |
| Language model | Gemini 2.5 Flash (primary), OpenAI fallback |
| Text-to-speech | Cartesia Sonic-2 |
| Backend | FastAPI (Python) |
| Routing classification | FallbackRoutingClassifier → Gemini → OpenAI → Review queue |
| Configuration | Pydantic Settings + YAML system prompt |

---

## Documentation Map

### Product — what it does and why

| Document | What it covers |
|---|---|
| [Service Flow](./product/01-service-flow) | The full end-to-end citizen journey from first ring to referral |
| [Call Stages](./product/02-call-stages) | The five conversation stages the agent moves through on every call |
| [Routing Rules](./product/03-routing-rules) | How the LLM decides between EACC, DCI, and review queue |
| [Human Fallback](./product/04-human-fallback) | When and how a human operator takes over, caller ID masking, operator brief |
| [Prompting Guide](./product/05-prompting-guide) | How to write and maintain the YAML system prompt |

### Architecture — how it is built

| Document | What it covers |
|---|---|
| [System Overview](./architecture/01-overview) | All modules, data flow, and prototype folder structure |
| [Voice Pipeline](./architecture/02-voice-pipeline) | STT → LLM → TTS stack, Sauti agent, session assembly |
| [Call Bridging](./architecture/03-call-bridging) | SIP trunk → LiveKit room → agent dispatch, caller ID masking |
| [Session Lifecycle](./architecture/04-session-lifecycle) | How the agent server starts, handles a call, and shuts down |
| [Routing Classifier](./architecture/05-routing-classifier) | FallbackRoutingClassifier — Gemini → OpenAI → review queue if both fail |
| [Data Model](./architecture/06-data-model) | The fields that make up an anonymous case record |
| [Privacy Layer](./architecture/07-privacy-layer) | Phone stripping, caller ID masking at escalation, tracking code design |

## Key Concepts

**Tracking code** — A unique, non-sequential identifier issued to the caller at the end of
every call. Format: `Word-Number` (e.g. `Mzito-77`). The caller uses this to follow up
without revealing their identity.

**FallbackRoutingClassifier** — The routing system tries Gemini first, falls back to OpenAI
if Gemini is unavailable. If both fail, the case is placed in the review queue for a human
to classify. No report is ever dropped because a provider is down.

**YAML system prompt** — The agent's personality, privacy rules, and conversation flow are
defined in a single YAML file loaded at startup. No code changes are needed to adjust how
the agent speaks.

**Review queue** — Cases the system cannot confidently classify go here instead of being
dropped. A human reviewer assigns the correct destination.
