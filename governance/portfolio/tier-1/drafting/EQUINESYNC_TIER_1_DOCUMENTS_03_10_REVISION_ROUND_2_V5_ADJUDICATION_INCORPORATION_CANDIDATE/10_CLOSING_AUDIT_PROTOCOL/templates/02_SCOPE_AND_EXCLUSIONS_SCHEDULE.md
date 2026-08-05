# Scope And Exclusions Schedule

## Document Control

Template name: `SCOPE_AND_EXCLUSIONS_SCHEDULE`.

Template version: `V4_PURPOSE_SPECIFIC_DRAFT`.

## Purpose

Separates in-scope documentary evidence from runtime, legal, production, implementation, certification, or merge claims.

## Required Evidence Fields

`scope_item_id, included_surface, excluded_surface, exclusion_reason, affected_t1c_id, evidence_locator, reviewer_confirmation`

## Scope Boundary

Use this template only for the V4 package and the exact evidence population named in the completed record. Exclude runtime behavior, production use, legal compliance, certification, protected-branch merge, implementation authorization, waiver approval, risk acceptance, and Founder approval unless a later explicit authority record is attached.

## Collection Method

The preparer must identify the source register, row IDs, file paths, SHA-256 values, byte lengths, reviewer role, sampling or full-population method, and any omitted population. The reviewer must mark each required field as `PRESENT`, `ABSENT`, `NOT_APPLICABLE_WITH_REASON`, or `OPEN_PENDING_REVIEW`.

## Required Determinations

1. Confirm whether every required field is populated with evidence rather than placeholder text.
2. Identify unresolved T1C or T1R2-EXT-F items affected by this template.
3. State whether the record is first-party, second-party, machine-assisted, or otherwise limited.
4. Preserve `NOT_CLOSED_BY_THIS_PACKAGE` when independent closure evidence is absent.

## Mandatory Evidence Table

| Field | Evidence locator | SHA-256 or row ID | Result | Limitation |
|---|---|---|---|---|
| scope_item_id | REQUIRED_BEFORE_USE | REQUIRED_BEFORE_USE | OPEN_PENDING_COMPLETION | V4 template only; not completed evidence |
| reviewer_confirmation | REQUIRED_BEFORE_USE | REQUIRED_BEFORE_USE | OPEN_PENDING_COMPLETION | V4 template only; not completed evidence |

## Prohibited Conclusions

This template cannot certify, adopt, activate, authorize implementation, authorize production use, authorize protected-branch merge, approve a waiver, accept risk, assert Founder approval, or close unresolved findings without independent evidence and explicit authority.

## Completion Fields

Preparer, reviewer, review date, evidence population, limitation statement, unresolved item list, and signature or acknowledgement status.
