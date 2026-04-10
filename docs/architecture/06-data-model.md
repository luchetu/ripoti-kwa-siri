---
title: "Data Model"
description: "The fields that make up an anonymous case record"
---

# Data Model

Every report becomes a **case record** — a structured document that captures
what the caller said without capturing who the caller is. The model is kept
intentionally small for the prototype. The goal is to collect enough to
understand the allegation, issue a tracking code, and route the case correctly.

---

## Design Principles

- **Minimum viable information** — collect only what the call needs
- **Identity separation** — phone number and caller identity live outside the case record
- **Partial reports are valid** — a frightened or rushed caller should not be blocked from submitting
- **Routing without perfection** — a case with unknown location and time can still be classified

---

## The Case Record

### Required fields

These must exist before a case is stored and tracked:

| Field | Type | Description |
|---|---|---|
| `case_id` | string | Internal unique identifier — never shown to the caller |
| `tracking_code` | string | Caller-facing reference, e.g. `Mzito-77` |
| `report_type` | enum | `corruption` · `organized_crime` · `unknown` |
| `narrative` | string | The caller's account in their own words |
| `urgency_level` | enum | `normal` · `urgent` · `high_risk` |
| `caller_safety_concern` | boolean | Whether the caller appears unsafe or afraid |
| `referral_target` | enum | `EACC` · `DCI` · `review_queue` |
| `case_summary` | string | Short structured summary for the referral package |
| `status` | enum | `received` · `summarised` · `referred` |

### Preferred fields

Important for usefulness but not always available — the caller may not know:

| Field | Type | Description |
|---|---|---|
| `location` | string | Where it happened — approximate is fine |
| `event_time` | string | When it happened — approximate is fine |
| `entities_involved` | list | People, offices, vehicles, agencies mentioned |
| `source_basis` | enum | `direct_witness` · `victim` · `second_hand` |

### Optional fields

Strengthen the report when available, but do not block submission:

| Field | Type | Description |
|---|---|---|
| `supporting_details` | object | Money amounts, vehicle markings, badge numbers, document references |

---

## Example Record

```yaml
case_id: case_00001
tracking_code: Mzito-77
report_type: corruption
narrative: >
  A county officer stopped the caller at a roadblock near Githurai
  and asked for 2000 KES to let the vehicle pass.
location: Roadblock near Githurai, Nairobi
event_time: Yesterday around 7 PM
entities_involved:
  - county officer
supporting_details:
  money_amount: 2000 KES
  vehicle_markings: unknown
source_basis: direct_witness
urgency_level: normal
caller_safety_concern: false
referral_target: EACC
case_summary: >
  Caller reports that a county officer requested a bribe of 2000 KES
  at a roadblock near Githurai yesterday evening.
status: received
```

---

## What the Agent Is Trying to Learn

Sauti does not fill out a form. It has a conversation. The fields above are
what the conversation is designed to extract. The agent asks:

- **What happened?** → `narrative`
- **Where did it happen?** → `location`
- **When did it happen?** → `event_time`
- **Who or what was involved?** → `entities_involved`
- **How do you know this?** → `source_basis`
- **Is anyone in immediate danger?** → `caller_safety_concern`, `urgency_level`
- **Any useful details?** → `supporting_details`

The agent stops asking when it has enough for a meaningful summary — not when
every field is filled.

---

## Completion Rule

A case is ready for summary and tracking when:

1. The caller has given a meaningful narrative
2. The system has checked for urgency and caller safety
3. The report can be placed into a broad category (`corruption`, `organized_crime`, or `unknown`)
4. The summary has been confirmed or lightly corrected by the caller

Missing location, time, or entity details do not block submission.

---

## Privacy Boundary

The following fields must **never** appear in the case record:

| Data | Reason |
|---|---|
| Phone number | Stripped by the privacy module before persistence |
| Caller name | Never requested unless offered voluntarily |
| National ID | Not relevant to the allegation |
| Home address | Not relevant and creates unnecessary identity risk |

If any of this is received at the telephony layer, it is handled separately
from the case record and is not required for submission. See
[Privacy Layer](./07-privacy-layer).

---

## Case Lifecycle

```
received → summarised → referred
```

| Status | Meaning |
|---|---|
| `received` | Call completed, narrative captured, tracking code issued |
| `summarised` | Case summary built and confirmed |
| `referred` | Routing classifier ran, case forwarded to EACC / DCI / review queue |

---

## What Later Versions Will Add

The prototype model is intentionally narrow. Future versions may add:

- Evidence attachments (photos, documents)
- Transcript references (timestamped segments)
- Referral receipts (acknowledgement from EACC / DCI)
- Institution feedback and case updates
- Caller follow-up history via tracking code
- Richer severity scoring and subcategories
