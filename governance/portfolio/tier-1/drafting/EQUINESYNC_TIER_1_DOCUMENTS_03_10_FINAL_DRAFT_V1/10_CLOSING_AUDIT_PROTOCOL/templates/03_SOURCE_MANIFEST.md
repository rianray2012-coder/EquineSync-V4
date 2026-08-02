# Source Manifest

## Document Control

- Template ID: `T1FD-AUDIT-TEMPLATE-03`
- Template name: `SOURCE_MANIFEST`
- Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`
- First-party status: `FIRST_PARTY_DOCUMENTARY_INSTRUMENT_ONLY`
- Disposition state: `NO_DISPOSITION_SELECTED`

## Purpose

Source manifest.

## Triggering Event

Package or repository source evidence is assembled.

## Required Inputs

Source path; SHA-256; byte length; custody source; version status.

## Required Evidence

Source file bytes; checksum records; repository locator.

## Exclusions

No source-precedence conclusion without reconciliation checks.

## Responsible Preparer

Evidence custodian.

## Required Reviewer

Governance reviewer.

## Approval Or Acknowledgement Field

Manifest acknowledgement only; blank until an authenticated Founder or reviewer action is supplied.

## Authority Effect

Documents evidence custody only. This template does not authorize adoption, activation, implementation, production use, certification completion, merge, or protected-branch mutation.

## Prohibited Conclusions

Do not imply source approval, adoption, or canonical status.

## Completion Criteria

All listed sources have hash and byte length.

## Reopening Or Supersession Effect

Superseded by a later manifest with complete delta.

## Instrument-Specific Control

The preparer must record a concrete evidence locator for this instrument's purpose and must mark the row `INCOMPLETE` if the locator is absent.

## Example Row

`EXAMPLE_ONLY_NOT_A_FINDING_OR_DECISION` | `T1FD-AUDIT-TEMPLATE-03` | `NO_DISPOSITION_SELECTED` | `EVIDENCE_LOCATOR_REQUIRED`
