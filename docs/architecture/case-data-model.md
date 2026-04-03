# ripoti-kwa-siri Case Data Model

## Purpose

This document defines the minimum case record for the `ripoti-kwa-siri` prototype. Its job is to keep the voice agent focused on collecting only the information needed to understand a report, issue a tracking code, and route the case to the right institution.

This is not a full production schema. It is a prototype-level data model designed to guide conversation design, case summaries, and early backend structure.

## Design Principles

- collect the minimum useful information
- separate case facts from caller identity
- support anonymous follow-up through a tracking code
- make routing possible without requiring a perfect report
- allow partial reports when the caller is afraid, rushed, or uncertain

## Minimum Case Record

Every case in the prototype should aim to capture the following fields.

| Field | Purpose | Required for prototype |
|---|---|---|
| `case_id` | Internal unique identifier for the report | Yes |
| `tracking_code` | Caller-facing reference for follow-up | Yes |
| `report_type` | Broad category such as corruption, organized crime, or unknown | Yes |
| `narrative` | The caller's main account of what happened | Yes |
| `location` | Where the event happened, even if approximate | Preferred |
| `event_time` | When the event happened, even if approximate | Preferred |
| `entities_involved` | People, offices, agencies, groups, or vehicles involved | Preferred |
| `supporting_details` | Useful details such as money amount, vehicle markings, badge identifiers, office name, or document references | Optional |
| `source_basis` | How the caller knows the information, such as direct witness, victim, or second-hand information | Preferred |
| `urgency_level` | Whether the case appears normal, urgent, or high-risk | Yes |
| `caller_safety_concern` | Whether the caller appears unsafe, threatened, or afraid to continue speaking | Yes |
| `referral_target` | Intended receiving institution such as EACC, DCI, or review queue | Yes |
| `case_summary` | Short structured summary for hand-off | Yes |
| `status` | Early lifecycle state such as received, summarized, or referred | Yes |

## Required vs Preferred vs Optional

### Required

These fields should exist before the prototype considers a report valid enough to store and track:

- `case_id`
- `tracking_code`
- `report_type`
- `narrative`
- `urgency_level`
- `caller_safety_concern`
- `referral_target`
- `case_summary`
- `status`

### Preferred

These fields are important for usefulness, but the caller may not know them:

- `location`
- `event_time`
- `entities_involved`
- `source_basis`

### Optional

These fields strengthen the report when available but should not block submission:

- `supporting_details`

## Privacy Boundary

The case record should not rely on direct caller identity.

The prototype should treat the following as outside the standard case record:

- phone number
- caller name
- national ID
- exact home address

If any of this information is received operationally, it should be handled separately from the core case record and should not be required for submission.

## Example Prototype Shape

```yaml
case_id: case_00001
tracking_code: Kiongozi-77
report_type: corruption
narrative: A county officer asked the caller for money at a roadblock.
location: Roadblock near Githurai, Nairobi
event_time: Yesterday around 7 PM
entities_involved:
  - county officer
supporting_details:
  money_amount: 2000 KES
  vehicle_markings: unknown
source_basis: direct witness
urgency_level: normal
caller_safety_concern: false
referral_target: EACC
case_summary: Caller reports that a county officer requested a bribe of 2000 KES at a roadblock near Githurai yesterday evening.
status: received
```

## What the Agent Should Try to Learn

The agent does not need to fill every field perfectly. It should focus on these questions:

- What happened?
- Where did it happen?
- When did it happen?
- Who or what entity was involved?
- How does the caller know this?
- Is there any immediate danger?
- Is there any detail that would help identify the event?

## Completion Rule for the Prototype

The prototype can consider a report ready for summary and tracking when:

- the caller has provided a meaningful narrative
- there is enough context to understand the nature of the allegation
- the system has checked for urgency or caller safety concerns
- the report can be placed into a broad routing category

The caller should not be blocked from completing a report just because exact names, times, or identifiers are missing.

## Initial Routing Categories

To keep the prototype simple, use only these categories:

- `corruption`
- `organized_crime`
- `unknown`

Example early mapping:

- bribery, procurement fraud, abuse of office -> `corruption`
- trafficking, extortion, criminal conspiracy -> `organized_crime`
- unclear, incomplete, or mixed cases -> `unknown`

## Notes for Later Versions

Later versions may add:

- evidence attachments
- transcript references
- referral receipts
- institution feedback
- caller follow-up history
- richer severity scoring
