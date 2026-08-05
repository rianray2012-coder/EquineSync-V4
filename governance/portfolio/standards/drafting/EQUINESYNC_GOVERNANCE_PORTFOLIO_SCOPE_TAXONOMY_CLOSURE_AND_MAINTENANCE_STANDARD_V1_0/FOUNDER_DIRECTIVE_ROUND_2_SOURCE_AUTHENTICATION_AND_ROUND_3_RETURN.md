# FOUNDER DIRECTIVE
## ROUND 2 REVIEW SOURCE AUTHENTICATION, FINDING-LEVEL TRACEABILITY, AND ROUND 3 RETURN

**Target:** EquineSync Governance Portfolio Scope, Taxonomy, Closure, and Maintenance Standard V1.0
**Repository:** `rianray2012-coder/EquineSync-V4`
**Pull request:** PR #77
**Current branch:** `codex/governance-portfolio-scope-taxonomy-closure-maintenance-standard-v1`
**Current reported head:** `44088a41ba114489a798b12a12888c39b5a180ac`
**Current truthful status:** `ROUND_2_FINDINGS_REVISION_INCOMPLETE_BLOCKING_DEFECTS_REMAIN`

## Purpose

Resolve the remaining blocking source-authentication condition by incorporating the exact Cursor, Claude, and Perplexity Round 2 targeted re-review reports as repository-native evidence, then rebuild the finding-disposition record at the individual-finding level.

This directive authorizes documentary revision, source authentication, validation, and preparation of a Round 3 re-review candidate only.

It does not authorize adoption, activation, implementation, pilot use, production use, FCR issuance, protected-branch merge, or automatic finding closure.

## Required source ingestion

Import the following exact files byte-for-byte into a stable repository-native review-source path:

1. `Cursor_Round_2_TARGETED_INDEPENDENT_REREVIEW_REPORT_2026-08-03.md`
2. `Claude_Round_2_TARGETED_INDEPENDENT_RE_REVIEW.md`
3. `Perplexity_Round_2_GOVERNANCE_STANDARD_RE_REVIEW.md`

For each file:

- preserve exact bytes;
- record filename, SHA-256, and byte length;
- assign a stable source ID;
- record reviewer identity and review date;
- classify provenance as `EXACT_REPOSITORY_NATIVE_SOURCE_BYTES`;
- record the source in `SOURCE_AND_AUTHORITY_REGISTER.csv`;
- include it in `PACKAGE_MANIFEST.json`;
- include it in `CHECKSUMS.sha256`;
- retain the original review language unchanged.

## Finding-level disposition rebuild

Replace the current 11-row consolidated Round 2 matrix with one row per actual reviewer finding.

Required behavior:

- preserve every Cursor finding;
- preserve every Claude finding;
- preserve every Perplexity finding;
- preserve each reviewer's original finding ID, severity, title, and disposition;
- create a `consensus_group_id` only as an additional linkage, never as a substitute for individual rows;
- populate `changed_files` for every remediated finding;
- populate `changed_sections_or_fields`;
- cite exact validation checks or test fixtures;
- record reviewer-specific closure evidence;
- record any severity normalization rationale;
- do not mark a finding closed merely because a file exists;
- do not use generic boilerplate in place of finding-specific remediation.

Required closure statuses:

- `OPEN`
- `PARTIALLY_REMEDIATED`
- `REMEDIATED_PENDING_VALIDATION`
- `REMEDIATED_PENDING_REREVIEW`
- `CLOSED_BY_INDEPENDENT_REREVIEW`
- `REJECTED_WITH_RECORDED_RATIONALE`
- `DEFERRED_WITH_BLOCKING_LIMITATION`

## Remaining Round 2 remediation requirements

Verify that the current candidate actually includes and correctly implements all previously directed repairs, including:

- validation reports derived from actual executions;
- no `PASS` for human, legal, privacy, or external review unless independently completed;
- repaired adversarial JSON pointers and Markdown anchors;
- correct human-readable source SHA-256 and byte length;
- read-only `--check`;
- committed checksum verification before regeneration in CI;
- non-null and non-empty required FCR payloads;
- correct lifecycle terminal flags;
- dimensional separation of lifecycle, authority, certification, evidence, and readiness;
- clean production authorization path with zero exceptions;
- supersession or removal of legacy templates;
- non-waivable core binding all FCR mechanisms;
- operative second review or a truthful blocking limitation;
- Governance Maintenance Standard supersession record.

## Validation requirements

Execute from the exact repository candidate:

1. Verify committed checksums before any regeneration.
2. Run the generator in strictly read-only check mode.
3. Run the package validator.
4. Run schema positive and negative fixtures.
5. Run lifecycle graph and terminality tests.
6. Run all JSON Pointer and Markdown anchor resolution tests.
7. Run one-to-one review-source-to-disposition completeness checks.
8. Run reviewer attribution and severity reconciliation checks.
9. Run package tests.
10. Create a new output ZIP from the exact final commit.

Every validation result must derive from actual execution and retain its log.

## Required return

Return:

- repository state;
- protected branch and head;
- working branch and final head;
- PR state and merge state;
- exact source authentication table;
- per-reviewer finding counts;
- disposition counts;
- file inventory;
- validation commands, exit codes, and log paths;
- unresolved limitations;
- new ZIP path and SHA-256.

## Permitted final statuses

Use exactly one:

- `ROUND_2_FINDINGS_REMEDIATED_READY_FOR_TARGETED_ROUND_3_REREVIEW`
- `ROUND_2_FINDINGS_REVISION_INCOMPLETE_BLOCKING_DEFECTS_REMAIN`
- `ROUND_2_FINDINGS_REVISION_BLOCKED_REPOSITORY_OR_SOURCE_CONDITION`

## Authority limitation

`ROUND_2_SOURCE_AUTHENTICATION_AND_DOCUMENTARY_REMEDIATION_AUTHORIZED_NO_ADOPTION_ACTIVATION_IMPLEMENTATION_PILOT_PRODUCTION_FCR_MERGE_OR_AUTOMATIC_CLOSURE_AUTHORITY`
