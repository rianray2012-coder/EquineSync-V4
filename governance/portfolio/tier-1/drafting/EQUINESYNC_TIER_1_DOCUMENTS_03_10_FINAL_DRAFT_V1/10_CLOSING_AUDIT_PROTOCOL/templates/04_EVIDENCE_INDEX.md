# Evidence Index

## Document Control

- Template ID: `T1FD-AUDIT-TEMPLATE-04`
- Template name: `EVIDENCE_INDEX`
- Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`
- First-party status: `FIRST_PARTY_DOCUMENTARY_INSTRUMENT_ONLY`
- Disposition state: `NO_DISPOSITION_SELECTED`

## Purpose

Evidence index.

## Triggering Event

Evidence is linked to findings, decisions, or validators.

## Required Inputs

Evidence ID; artifact path; row locator; hash; related finding or decision.

## Required Evidence

Referenced records; validation output; review notes.

## Exclusions

No unlocated evidence or generic bundle references for closure.

## Responsible Preparer

Evidence index preparer.

## Required Reviewer

Governance reviewer.

## Approval Or Acknowledgement Field

Index acknowledgement only; blank until an authenticated Founder or reviewer action is supplied.

## Authority Effect

Creates no closure authority by itself. This template does not authorize adoption, activation, implementation, production use, certification completion, merge, or protected-branch mutation.

## Prohibited Conclusions

Do not imply evidence has been accepted by Founder.

## Completion Criteria

Every evidence row resolves to a package file or external authenticated input.

## Reopening Or Supersession Effect

Reopened when a referenced file changes hash.

## Instrument-Specific Control

The preparer must record a concrete evidence locator for this instrument's purpose and must mark the row `INCOMPLETE` if the locator is absent.

## Example Row

`EXAMPLE_ONLY_NOT_A_FINDING_OR_DECISION` | `T1FD-AUDIT-TEMPLATE-04` | `NO_DISPOSITION_SELECTED` | `EVIDENCE_LOCATOR_REQUIRED`
