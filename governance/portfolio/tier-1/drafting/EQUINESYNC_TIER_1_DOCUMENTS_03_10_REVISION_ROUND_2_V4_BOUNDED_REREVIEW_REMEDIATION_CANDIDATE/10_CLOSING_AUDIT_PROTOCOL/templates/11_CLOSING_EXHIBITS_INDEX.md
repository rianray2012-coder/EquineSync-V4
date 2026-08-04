# Closing Exhibits Index

## Document Control

Template name: `CLOSING_EXHIBITS_INDEX`.

Template version: `V4_PURPOSE_SPECIFIC_DRAFT`.

## Purpose

Lists the evidence exhibits a reviewer considered, including excluded or superseded exhibits.

## Required Evidence Fields

`exhibit_id, exhibit_name, source_path, sha256, byte_length, related_t1c_id, inclusion_reason, exclusion_note`

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
| exhibit_id | REQUIRED_BEFORE_USE | REQUIRED_BEFORE_USE | OPEN_PENDING_COMPLETION | V4 template only; not completed evidence |
| exclusion_note | REQUIRED_BEFORE_USE | REQUIRED_BEFORE_USE | OPEN_PENDING_COMPLETION | V4 template only; not completed evidence |

## Prohibited Conclusions

This template cannot certify, adopt, activate, authorize implementation, authorize production use, authorize protected-branch merge, approve a waiver, accept risk, assert Founder approval, or close unresolved findings without independent evidence and explicit authority.

## Completion Fields

Preparer, reviewer, review date, evidence population, limitation statement, unresolved item list, and signature or acknowledgement status.
