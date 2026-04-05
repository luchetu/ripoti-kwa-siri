# ripoti-kwa-siri Human Fallback Policy

## Purpose

This document defines when and how the `ripoti-kwa-siri` prototype should move from AI-led intake to a human operator.

The goal is not to replace the voice agent. The goal is to make sure callers can still complete a report when the agent is not the right fit for the situation.

## Policy Principle

The prototype should follow this rule:

- `AI-first, human-available, human-on-demand`

This means the voice agent begins intake by default, but a human path must be available when needed.

## When Human Fallback Should Happen

The system should trigger human fallback in the following situations.

### Caller Request

Fallback should happen immediately if the caller asks for a person.

Examples:

- "I want to speak to a human"
- "Can I talk to an officer?"
- "I do not want to continue with the agent"

### Repeated Agent Failure

Fallback should happen if the agent cannot collect the core report after multiple attempts.

Examples:

- repeated misunderstanding
- repeated clarification without progress
- no usable narrative after several turns
- the caller keeps restating the issue without the system moving forward

### Distress or Fear

Fallback should happen if the caller sounds too distressed to continue comfortably with the agent.

Examples:

- caller sounds overwhelmed or panicked
- caller says they are afraid to continue
- caller does not trust the automated system
- caller says they want a person because the issue is too sensitive

### High-Risk or Urgent Cases

Fallback should be available for urgent situations even if the AI can continue.

Examples:

- active threats
- immediate retaliation risk
- ongoing violence
- current trafficking or confinement concerns
- caller says they are not safe

### Technical Failure

Fallback should happen if the voice agent or model becomes unreliable during the call.

Examples:

- repeated model errors
- loss of agent responsiveness
- broken turn-taking
- unacceptable audio quality or latency

## What the Agent Should Say

When fallback is triggered, the caller should hear a short, calm explanation.

Suggested language:

- "I can connect you to a human colleague to continue this report."
- "I am having difficulty collecting the details clearly. I can transfer you to a person if you would prefer."
- "Because this may be urgent, I can hand this over to a human operator now."

The system should not blame the caller or suggest that the report is invalid.

## What Information Should Be Preserved

When fallback happens, the system should preserve any useful information already collected.

That includes:

- partial narrative
- location details
- event time
- involved people or entities
- urgency notes
- caller safety concern
- any partial summary already available

This allows the human operator to continue from the current state instead of restarting the whole intake.

## Human Continuation Rule

The human operator should continue the same case, not create a second one unless the first call failed before any useful intake was captured.

The human path should still aim to produce:

- final case summary
- tracking code
- routing category
- referral target

## Prototype Operational Modes

The prototype may support one of two human fallback models.

### Live Transfer

The caller is transferred directly to an available human operator.

Best when:

- operators are available in real time
- the prototype includes active call-center support

### Review Queue or Callback

The case is flagged for human follow-up if live transfer is not available.

Best when:

- staffing is limited
- the prototype is still testing the voice workflow
- human review is asynchronous

## Recommended Prototype Approach

For the first implementation, the safest design is:

1. support live transfer if an operator is available
2. otherwise place the partial case into a human review queue
3. preserve all captured case details before the handoff

This gives the prototype a graceful fallback without depending entirely on live staffing.

## Relationship to Other Docs

- [call-stages.md](/Users/admin/ripoti-kwa-siri/docs/product/call-stages.md): core AI-led call flow
- [routing-rules.md](/Users/admin/ripoti-kwa-siri/docs/product/routing-rules.md): routing after summary and classification
- [case-data-model.md](/Users/admin/ripoti-kwa-siri/docs/architecture/case-data-model.md): fields that must survive fallback
- [voice-agent-architecture.md](/Users/admin/ripoti-kwa-siri/docs/architecture/voice-agent-architecture.md): how the voice agent fits into the wider system
