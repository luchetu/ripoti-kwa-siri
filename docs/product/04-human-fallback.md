---
title: "Human Fallback"
description: "When and how a human operator takes over from the voice agent"
---

# Human Fallback

The voice agent handles the vast majority of calls. But there are situations
where a human is the right choice — and the system must be ready for them.

**The policy in one sentence:** AI-first, human-available, human-on-demand.

---

## When Fallback Should Trigger

### The caller asks for a human

This is the most important trigger. If the caller asks for a person, transfer
immediately. No exceptions.

Examples:
- *"I want to speak to a real person"*
- *"Can I talk to an officer?"*
- *"I don't want to continue with the machine"*

The caller's comfort and trust is more important than completing the AI-led flow.

---

### The caller is in distress or immediate danger

If the caller sounds overwhelmed, panicked, or says they are unsafe, the agent
must not continue the standard intake flow. Collect only what is absolutely
necessary and escalate immediately.

Examples:
- *"I am afraid to keep talking"*
- *"They are outside right now"*
- *"I need help, not a recording"*

---

### The agent is not making progress

If the agent has tried multiple times to collect a core part of the report and
the conversation is going in circles, hand off rather than frustrate the caller.

Signs of this:
- The caller has restated the same thing three or more times without the agent
  moving forward
- The agent keeps asking the same clarifying question
- No usable narrative after several turns

---

### The case is high-risk or involves active harm

Some situations should always have a human available — even if the AI can
technically continue.

Examples:
- Active threats against the caller or a third party
- Ongoing trafficking or confinement
- The caller believes they are being followed or watched

---

### Technical failure

If the voice model becomes unreliable — repeated errors, broken turn-taking,
or unacceptable latency — do not keep the caller on a degraded experience.
Escalate to human or offer a callback.

---

## What the Agent Says When Falling Back

Sauti should hand off calmly and without blaming the caller.

**For a caller request:**
> *"Of course. Let me connect you to a human colleague who can continue this
> report with you."*

**For distress or danger:**
> *"I can hear this is difficult. I am going to connect you to someone who can
> help you directly."*

**For agent failure:**
> *"I am having some difficulty keeping up with the details clearly. I can
> transfer you to a person who can take this from here."*

**Never say:**
- *"I didn't understand you"* — puts the problem on the caller
- *"Your report is incomplete"* — makes the caller feel they failed
- *"I cannot help you"* — feels like a dead end

---

## What Information Must Survive the Handoff

When a human takes over, the case context must transfer with them. The operator
should not ask the caller to start over.

The handoff package must include:

| Field | Why it matters |
|---|---|
| Partial narrative | Operator continues from where Sauti left off |
| Location (if known) | Avoids re-asking |
| Entities involved (if known) | Avoids re-asking |
| Urgency level | Operator knows how fast to move |
| Caller safety concern | Critical for operator safety approach |
| Partial summary (if built) | Gives the operator immediate context |

The human operator continues the **same case**. A new case is only created if
no useful intake was captured before the handoff.

---

## Caller ID During Escalation

This is a critical privacy detail that is easy to overlook.

When the system escalates to a human operator, **the caller's real phone number
must never appear on the operator's screen**. If it does, the entire privacy
guarantee breaks at the moment of escalation.

### What the human operator sees

| What they see | What they must NOT see |
|---|---|
| System / agent number (e.g. the hotline number) | Caller's real phone number |
| Case ID and tracking code | Caller's name or national ID |
| Partial case brief (narrative, urgency, category) | Any raw SIP metadata containing the inbound number |

### How this is enforced

The SIP trunk configuration controls what caller ID is presented on an outbound
leg or transfer. The trunk must be configured to always present the **system's
own number** — not the inbound caller's number — whenever a call is transferred
or a participant is invited to join the room.

In the LiveKit room model, the human operator joins as a room participant. The
room metadata contains the case brief. The operator's interface reads the room
metadata — it does not read raw SIP headers.

```
Caller ──────────────────── LiveKit Room ──────── Human Operator
(SIP participant)                │                (joins room)
                           Room Metadata
                           ─────────────────────────────
                           case_id:              case_00001
                           tracking_code:        Mzito-77
                           urgency:              urgent
                           category:             corruption
                           caller_safety_concern: false
                           narrative:            "Officer at checkpoint..."
                           entities_involved:    ["county officer"]
                           location:             "Near Githurai roundabout"
```

The operator reads the case brief. They never see the caller's number.

---

## The Operator Brief

Before the human operator speaks a single word, they need to know:

1. **Why the call was escalated** — caller request, distress, high-risk, or agent failure
2. **What has already been captured** — so they do not ask the caller to repeat themselves
3. **Urgency level** — so they know how fast to move
4. **Caller safety concern** — so they know how to open the conversation

### What Sauti says to the caller while the brief is delivered

> *"I am connecting you to a colleague now. They will have the details you have
> already shared, so you will not need to repeat anything."*

This short message buys the operator 5–10 seconds to read the brief before
speaking.

### What the operator brief looks like

```
── OPERATOR BRIEF ──────────────────────────────────────
Escalation reason:   Caller requested human
Urgency:             Normal
Safety concern:      No
Category:            Corruption (medium confidence)

Narrative so far:
  Caller reports a county officer at a roadblock near Githurai
  demanded 2000 KES to allow their vehicle to pass. Event
  occurred yesterday evening around 7 PM.

Entities mentioned:  County officer (unidentified)
Location:            Near Githurai roundabout, Nairobi
Tracking code:       Mzito-77
Case ID:             case_00001
────────────────────────────────────────────────────────
```

The operator opens with what they know — not with *"Can you tell me what
happened?"*

---

## Two Fallback Models

### Live Transfer

The human operator joins the same LiveKit room the caller is already in. No new
call setup. No hold music gap. The caller hears Sauti's handoff message, then
hears the operator's voice.

The operator's interface shows the case brief the moment they accept the job.

**Best when:** Operators are staffed and available during call hours.

---

### Review Queue + Callback

If no operator is available, the partial case is saved and flagged for human
follow-up. The caller is given their tracking code.

> *"No one is available right now. Your report has been saved with tracking code
> Mzito-77. A reviewer will contact you or you can check back using that code."*

**Best when:** Staffing is limited or calls come outside operating hours.

---

## Recommended Prototype Approach

For the first version:

1. Configure the SIP trunk to always present the system number — never the inbound caller number — on any transfer or escalation
2. Write the case brief to LiveKit room metadata before inviting the operator
3. Support live transfer if an operator is available
4. Fall back to the review queue if no operator is reachable
5. Always save the partial case before the handoff — never lose intake data
6. Preserve the tracking code across both paths

The caller should always leave with a tracking code. The operator should always
receive the brief before speaking. The caller's number should never appear anywhere
in the operator's view.
