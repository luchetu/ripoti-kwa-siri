---
title: "Prompting Guide"
description: "How to write and maintain the YAML system prompt that controls Sauti"
---

# Prompting Guide

Sauti's entire behaviour — how it speaks, what it asks, what it refuses to say,
how it handles a frightened caller — is controlled by one file:

```
prompts/anonymous_reporting_agent.yaml
```

No code changes are needed to change how Sauti sounds or behaves. Edit the YAML,
restart the agent server, and the change takes effect immediately.

This guide explains how to write prompts that work well for a voice agent — and
what common mistakes break the experience.

---

## Why Voice Prompts Are Different

A system prompt written like a document will make Sauti sound like a document.
Audio is a different medium. The model is speaking aloud — not writing an email,
not filling a form, not producing structured output.

The rules are different:

| Writing for text | Writing for voice |
|---|---|
| Bullet points and headers are fine | Bullet points and headers may be read aloud |
| Long paragraphs are scannable | Long paragraphs become monologues |
| Formal language is professional | Formal language sounds cold and robotic |
| Markdown formatting helps readers | Markdown breaks voice delivery |

---

## The 4 Rules

### 1. Give Sauti a clear identity and scope

Tell the model exactly who it is and what it cannot do. Vague personas produce
vague agents.

**Too vague:**
```text
You are a professional voice assistant. Help the caller with their report.
```

**Clear:**
```text
You are Sauti, a voice agent for Ripoti Kwa Siri. Your only job is to help
callers submit an anonymous report of corruption or organized crime. You cannot
help with anything else. If a caller asks about something outside this scope,
explain that this line is only for reporting, and invite them to continue.
```

---

### 2. Write in the way Sauti should speak

Short sentences. Natural rhythm. Conversational. No markdown.

**Sounds like a document:**
```text
## Stage 2: Report Capture
- Ask the caller what happened
- Allow them to explain without interruption
- Listen for urgency signals
```

**Sounds like a voice agent:**
```text
Ask the caller what happened, in their own words. Let them speak without
interrupting. As they talk, pay attention to whether they sound afraid or
whether anyone might be in danger right now.
```

---

### 3. Put guardrails inside the instructions — not outside

Don't rely on a separate safety layer for predictable behavioural boundaries.
If Sauti should never ask for a national ID, say so in the prompt.

**Examples of inline guardrails:**
```text
Never ask the caller for their name, national ID, or home address. If they
offer this information, do not record it as part of the case.

Never promise that EACC or DCI will take action. You can only confirm that
the report has been received and will be reviewed.

Never invent a tracking code. Wait for the system to issue one before
reading it to the caller.
```

---

### 4. Tell Sauti how to sound — not just what to say

Native audio models like Gemini 2.5 Flash can adjust their delivery based on
tonal instructions. Use this.

```text
Speak calmly and warmly. This caller may be afraid. Use short sentences.
Never rush. If the caller goes quiet, wait. If they seem overwhelmed, slow
down and acknowledge that what they are sharing takes courage.
```

---

## The Prompt Structure for Sauti

The YAML file has one block that matters: `instructions`. Here is the shape
it should follow:

```yaml
instructions: |
  You are Sauti, a voice agent for Ripoti Kwa Siri. [identity and scope]

  Speak calmly and warmly. [tone instructions]

  [Stage 1 — Greeting]
  When a caller connects, greet them, explain the purpose, and give a short
  privacy notice. Tell them their phone number will not be attached to the
  case. Do not ask for their name.

  [Stage 2 — Report Capture]
  Ask the caller to describe what happened in their own words. Do not
  interrupt. Listen for signs of urgency or fear.

  [Stage 3 — Clarification]
  Ask one follow-up question at a time. Focus on where, when, who, and how
  the caller knows the information. Stop if the caller sounds unsafe.

  [Stage 4 — Summary Confirmation]
  Read back a short factual summary. Ask the caller to confirm or correct it.

  [Stage 5 — Tracking and Close]
  Confirm the report has been saved. Read the tracking code clearly, then
  read it a second time. Remind the caller to keep it safe.

  [Guardrails]
  Never ask for national ID or home address. Never promise action. Never
  invent a tracking code. Never repeat the caller's phone number.
```

---

## Common Mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Bullet points in instructions | Model may read them aloud | Write in prose |
| Section headers with `#` | Model may read "hash hash stage one" | Use plain text labels in brackets or remove headers |
| Tool documentation in prompt | Wastes tokens, confuses the model | Tools are registered via function signatures |
| Vague tone ("be professional") | Model defaults to formal and cold | Name the tone: *"calm, warm, unhurried"* |
| Overly long stage descriptions | Model loses track of the current stage | Keep each stage description short — one short paragraph |
| No urgency handling | Frightened callers get the same flow as calm ones | Add an explicit urgency exception |

---

## Testing a Prompt Change

After editing the YAML:

1. Restart the agent server: `uv run run_agent.py`
2. Call the test number or use the LiveKit dashboard to join a test room
3. Walk through all five stages
4. Pay attention to:
   - Does Sauti introduce itself correctly?
   - Does it pause and let you speak?
   - Does it ask one question at a time?
   - Does it read the summary back correctly?
   - Does it read the tracking code twice?
5. Test one distressed caller scenario — speak urgently and see if Sauti adjusts

No code changes. No deployment. Just YAML and a server restart.
