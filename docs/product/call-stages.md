# ripoti-kwa-siri Call Stages

## Purpose

This document defines the core call stages for the `ripoti-kwa-siri` prototype. It exists to align the voice prompt, the case data model, and the routing rules around one shared conversation flow.

The prototype should follow a simple structure. The agent should sound natural and adaptive, but the underlying call flow should remain predictable.

## Overview

The prototype call should move through five stages:

1. greeting and reassurance
2. initial report capture
3. clarification
4. summary confirmation
5. tracking and close

These stages are product stages, not framework-specific runtime states. They describe what the agent is trying to accomplish at each part of the call.

## Stage 1: Greeting and Reassurance

### Goal

Welcome the caller, establish trust, and explain the reporting purpose without overpromising.

### What the agent should do

- greet the caller warmly
- explain that this line is for reporting corruption or organized crime
- explain that the report is handled confidentially
- avoid promising guarantees the system may not truly provide
- invite the caller to describe what happened

### Example outcome

By the end of this stage, the caller understands:

- they are in the right place
- they can begin sharing the report
- they do not need to start with their identity

## Stage 2: Initial Report Capture

### Goal

Get the caller's first uninterrupted version of the story.

### What the agent should do

- ask what happened in the caller's own words
- let the caller explain before drilling into details
- avoid interrupting too early
- listen for the broad report type and whether there may be any immediate danger

### What the agent should try to learn

- the main allegation
- whether the report sounds like corruption, organized crime, or unknown
- whether the caller sounds frightened, rushed, or unsafe

### Example completion signal

This stage is complete when the caller has given a meaningful first account of the event.

## Stage 3: Clarification

### Goal

Gather the minimum useful details needed to understand and route the report.

### What the agent should do

- ask one short follow-up question at a time
- clarify where it happened
- clarify when it happened
- clarify who or what entity was involved
- ask how the caller knows the information
- ask for useful identifying details only when relevant

### Useful details may include

- vehicle color or markings
- badge or office details
- money amount
- document or account references
- sequence of events

### What the agent should avoid

- interrogating the caller
- demanding details they do not know
- pushing for personal identity information

### Urgent exception

If the caller appears to be in immediate danger, this stage should shrink dramatically. The agent should switch to a safety-first version of clarification and collect only the most essential facts.

## Stage 4: Summary Confirmation

### Goal

Confirm that the agent understood the report correctly before closing the call.

### What the agent should do

- give a short factual summary
- mention the main event
- mention the place if known
- mention the time if known
- mention the involved person or entity if known
- ask the caller to confirm or correct the summary

### Example outcome

By the end of this stage, the caller has either:

- confirmed the summary
- or made one or two corrections that are reflected back briefly

## Stage 5: Tracking and Close

### Goal

End the call clearly and respectfully, while giving the caller a way to follow up.

### What the agent should do

- explain that the report has been captured
- provide the tracking code if available
- read the tracking code slowly and clearly
- repeat the tracking code once
- remind the caller to keep it safe
- close the conversation respectfully

### What the agent should avoid

- inventing a tracking code
- inventing referral outcomes
- promising that another institution will take a specific action

## Call Completion Rule

The prototype can close the call when:

- the caller has provided a meaningful narrative
- the system has checked for urgency or caller safety concerns
- the report has enough detail for a broad routing category
- the summary has been confirmed or lightly corrected
- the caller has been given a tracking code or a clear explanation of the next step

## How This Connects to Other Docs

- [ripoti-kwa-siri-service-flow.md](/Users/admin/ripoti-kwa-siri/docs/product/ripoti-kwa-siri-service-flow.md): the broader product journey
- [case-data-model.md](/Users/admin/ripoti-kwa-siri/docs/architecture/case-data-model.md): the fields the conversation is trying to collect
- [routing-rules.md](/Users/admin/ripoti-kwa-siri/docs/product/routing-rules.md): the simple category and destination logic used after intake
- [anonymous_reporting_agent.yaml](/Users/admin/ripoti-kwa-siri/prompts/anonymous_reporting_agent.yaml): the runtime prompt that should reflect these stages in natural spoken language
