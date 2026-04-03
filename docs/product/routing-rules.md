# ripoti-kwa-siri Routing Rules

## Purpose

This document defines the first routing rules for the `ripoti-kwa-siri` prototype. The goal is to keep routing simple, understandable, and easy to audit while the product is still at the prototype stage.

This is not a full legal or institutional routing policy. It is a lightweight decision guide for early case handling.

In the prototype flow, routing classification happens after the call once the system has built a final case summary.

## Routing Principles

- use a small number of routing categories
- prefer clarity over perfect precision
- allow uncertain reports to remain valid
- avoid blocking a report because the category is ambiguous
- support manual review when the correct destination is unclear

## Prototype Routing Categories

The first version should use only three broad categories:

- `corruption`
- `organized_crime`
- `unknown`

These categories should be enough to support the first version of intake, summary, and referral.

## Initial Destination Mapping

| Category | Default destination |
|---|---|
| `corruption` | `EACC` |
| `organized_crime` | `DCI` |
| `unknown` | `review_queue` |

## Category Guidance

### Corruption

Use `corruption` when the report is mainly about:

- bribery
- procurement fraud
- abuse of office
- misuse of public resources
- unexplained payments for public services
- conflicts of interest in public decision-making

Typical examples:

- an officer demands money to release a document
- a public official requests a bribe at a roadblock
- a government vehicle is used in an illegal payment scheme
- a procurement process appears manipulated for personal gain

Default prototype destination:

- `EACC`

### Organized Crime

Use `organized_crime` when the report is mainly about:

- trafficking
- extortion
- coordinated criminal groups
- violent intimidation connected to criminal activity
- kidnapping or abduction
- criminal conspiracy involving multiple actors

Typical examples:

- a caller reports a trafficking network
- a group is demanding payment under threat
- multiple people appear to be coordinating criminal activity
- the report describes organized intimidation or illegal movement of people or goods

Default prototype destination:

- `DCI`

### Unknown

Use `unknown` when:

- the report is too incomplete to classify confidently
- the report mixes several categories and the main issue is unclear
- the caller is rushed, afraid, or unable to provide enough context
- the information may still be valuable, but the destination is uncertain

Default prototype destination:

- `review_queue`

## Decision Rule for the Prototype

The prototype should use the simplest possible routing rule:

1. Build the final case summary from the completed intake.
2. Classify that summary into `corruption`, `organized_crime`, or `unknown`.
3. If it is `corruption`, route to `EACC`.
4. If it is `organized_crime`, route to `DCI`.
5. If it is unclear or mixed, route to `review_queue`.

The system should not force a precise classification when the report is incomplete.

## Urgency vs Routing

Urgency is not the same thing as destination.

A report can be:

- `urgent` and still be categorized as `corruption`
- `urgent` and categorized as `organized_crime`
- `urgent` and still remain `unknown`

Urgency affects how the call should be handled and how quickly the case should be reviewed. It does not automatically change the routing category.

## Examples

### Example 1

Report:

> A county officer demanded money to let a vehicle pass at a checkpoint.

Classification:

- `corruption`

Destination:

- `EACC`

### Example 2

Report:

> A group is threatening traders for money every week and appears to be working together.

Classification:

- `organized_crime`

Destination:

- `DCI`

### Example 3

Report:

> The caller says something illegal is happening at an office but cannot explain clearly and sounds frightened.

Classification:

- `unknown`

Destination:

- `review_queue`

## Manual Review Principle

If the system is not confident, the report should still be accepted. The safer prototype behavior is to place the case in `review_queue` rather than force it into the wrong destination.

## Notes for Later Versions

Later versions may add:

- subcategories inside corruption
- subcategories inside organized crime
- county or sector-specific routing
- direct routing to additional institutions
- richer confidence scoring and audit reasons for each routing decision
