# Accession Or Repository Custody Receipt

## Document Control

- Template ID: `T1FD-AUDIT-TEMPLATE-14`
- Template name: `ACCESSION_OR_REPOSITORY_CUSTODY_RECEIPT`
- Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`
- First-party status: `FIRST_PARTY_DOCUMENTARY_INSTRUMENT_ONLY`
- Disposition state: `NO_DISPOSITION_SELECTED`

## Purpose

Accession or repository-custody receipt.

## Triggering Event

A package is placed under repository custody.

## Required Inputs

Package hash; branch; commit; path; accession state.

## Required Evidence

Commit SHA; file list; checksum; PR link.

## Exclusions

No adoption, activation, or merge authority from accession.

## Responsible Preparer

Repository custodian.

## Required Reviewer

Governance reviewer.

## Approval Or Acknowledgement Field

Custody acknowledgement only; blank until an authenticated Founder or reviewer action is supplied.

## Authority Effect

Repository custody only. This template does not authorize adoption, activation, implementation, production use, certification completion, merge, or protected-branch mutation.

## Prohibited Conclusions

Do not imply protected-branch merge unless merge receipt exists.

## Completion Criteria

Receipt identifies exact commit and package bytes.

## Reopening Or Supersession Effect

Superseded by later custody receipt.

## Instrument-Specific Control

The preparer must record a concrete evidence locator for this instrument's purpose and must mark the row `INCOMPLETE` if the locator is absent.

## Example Row

`EXAMPLE_ONLY_NOT_A_FINDING_OR_DECISION` | `T1FD-AUDIT-TEMPLATE-14` | `NO_DISPOSITION_SELECTED` | `EVIDENCE_LOCATOR_REQUIRED`
