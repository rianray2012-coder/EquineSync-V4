# Founder-Controlled Codex Remediation Directive — EquineSync Tier 1 Documents 03–10

Date: 2026-08-04  
Directive status: `AUTHORIZED_FOR_BOUNDED_DOCUMENTARY_REMEDIATION_ONLY`  
Target status: `REVISION_REQUIRED`

## 1. Purpose

Remediate the valid findings consolidated in `EQUINESYNC_TIER_1_DOCS_03_10_CONSOLIDATED_OUTSIDE_REVIEW_REGISTER.md` and produce one authenticated, internally consistent final documentary candidate for Founder review.

This directive does **not** authorize adoption, activation, implementation, production use, deployment, merge to a protected branch, certification, public claims, risk acceptance, waiver approval, or automatic closure of findings.

## 2. Authentication and stop gate

The authenticated outside-review baseline is:

- Repository: `rianray2012-coder/EquineSync-V4`
- Review branch/PR context: PR #83
- Cursor-reviewed commit: `a1a1ff5cf056e7e78c99c4038fb8afcb95aebab7`
- Cursor-reviewed archive: SHA-256 `aa61978cf952a6b93abcb20c009ce28d862734258e7aae7a4a2b12788563545f`, 2,545,176 bytes
- Later PR tip identified but not reviewed by Cursor: `1c053c4a9658e5b47d0cbc0bbf4edf6a995a41e3`
- Claude-reviewed differing archive: SHA-256 `909ba841a1b488ae61a370d74182a5841901a0b061accc568c3d609c3d8a4433`, 2,586,324 bytes

Before editing:

1. Fetch and record the protected branch head, PR #83 base/head, worktree state, and relevant tags.
2. Authenticate the current PR #83 tip and generate or locate its exact reviewer ZIP.
3. Record archive SHA-256, byte length, package root, root manifest digest, and file count.
4. Map `a1a1ff5…`, `1c053c4…`, `aa61978…`, and `909ba841…` into an explicit predecessor/successor table.
5. If the current bytes cannot be tied to a repository commit, stop with `CURRENT_TARGET_AUTHENTICATION_BLOCKED`; do not remediate unidentified bytes.

Use the authenticated current PR #83 tip as the remediation target only after this gate passes. Do not revert valid later remediation merely to reproduce the older review baseline.

## 3. Required work

### Phase A — Current-state disposition

For T1C-001 through T1C-020:

- assign `VALID_OPEN`, `ALREADY_REMEDIATED_WITH_EVIDENCE`, `REMEDIATED_IN_V3_PENDING_REREVIEW`, `NOT_REPRODUCED`, or `RETAINED_NONBLOCKING`;
- cite exact current file, row/field/section, commit, and evidence;
- preserve each Claude, Cursor, and Perplexity source ID;
- explain disagreements; do not close by majority vote;
- prohibit self-closure of high-consequence findings without Second Reviewer/originating-reviewer concurrence.

### Phase B — Mandatory remediation order

1. **Identity and custody:** close T1C-001 and establish one target.
2. **Decision validity:** remediate T1C-002, T1C-003, and T1C-009.
3. **Authority truth:** remediate T1C-005 and T1C-018.
4. **Requirement quality:** remediate T1C-006 and T1C-010; recompute metrics.
5. **Findings integrity:** remediate T1C-007 and establish one authoritative findings population.
6. **Document 10 substance:** remediate T1C-004 and related T1C-014/T1C-015.
7. **Failure-capable assurance:** remediate T1C-008, T1C-011, and T1C-012 with negative fixtures.
8. **Operational documentary quality:** remediate T1C-013, T1C-016, T1C-017, T1C-019, and T1C-020.

### Phase C — Required validator behavior

At minimum, validators must fail on fixtures containing:

- a decision-text lifecycle count that differs from the state register;
- a selected Founder disposition when no Founder decision is recorded;
- an external finding absent from the authoritative findings register;
- a purpose-specific template missing its required fields or normalized-identical to another template;
- a path-keyword-only authority elevation or authoritative candidate path;
- a non-requirement fragment represented as accepted normative text;
- an unknown/unimplemented invalid-state rule;
- an orphan duplicate-cluster foreign key;
- a production/deployment claim without its evidence field;
- a CI failure without analysis;
- repeated identical markdown sections caused by non-idempotent remediation.

A validator report must distinguish `STRUCTURAL_PASS` from `SUBSTANTIVE_CONTROL_PASS`. Do not describe presence/count checks as substantive assurance.

## 4. Required outputs

Produce one new, clearly versioned remediation package containing:

1. `README_FIRST.md`
2. authenticated repository and package custody record
3. updated Documents 03–10 and all supporting registers/schemas/data dictionaries
4. consolidated findings disposition register with T1C and source-review crosswalks
5. per-finding closure evidence register
6. current-state delta report from `a1a1ff5…` and from the authenticated pre-remediation tip
7. updated Founder decision packet with no preselected dispositions
8. validator source and positive/negative fixtures
9. repository-mode and standalone extracted-package validation reports
10. independent Linux/CI reproduction record, if available; otherwise a truthful retained blocker/nonblocking disposition
11. manifests, checksums, manifest-of-manifests, and detached ZIP `.sha256`
12. a bounded independent closure-rereview package and prompt

## 5. Second Reviewer and closure

Patrick K. Spoon Sr., COO, is the designated Second Reviewer for high-consequence governance actions, subject to conflict-of-interest and recusal requirements. Do not fabricate his review or signature. If he is conflicted, unavailable, or has not reviewed the evidence, record that state truthfully and leave the affected finding open.

No finding is closed merely because code changed or validators passed. Closure evidence must identify the defect, exact correction, validation performed, result, reviewer, date, and residual issue status.

## 6. Repository constraints

- Work only on a dedicated branch created from the authenticated authorized target.
- Do not merge PR #83 or any successor PR.
- Do not modify the protected branch directly.
- Preserve predecessor packages and reviews as historical evidence.
- Do not overwrite or relabel prior review artifacts as though they reviewed new bytes.
- Open or update a draft PR only; record its URL, base/head SHAs, and blocked authority state.
- Stop on unexpected repository drift, package mismatch, missing source, or inability to reproduce checksums.

## 7. Completion response

Return:

- repository and package authentication results;
- exact branch, base SHA, final head SHA, and draft PR state;
- disposition of every T1C item and every source-review finding;
- files changed and generated;
- positive and negative validation results;
- unresolved blockers and retained nonblocking items;
- Second Reviewer state;
- explicit confirmation that no adoption, activation, implementation, production use, protected-branch merge, certification, or automatic finding closure occurred.

Required terminal status if all documentary remediation and closure evidence are complete:

`TIER_1_DOCUMENTS_03_10_REMEDIATION_COMPLETE_READY_FOR_BOUNDED_INDEPENDENT_CLOSURE_REREVIEW`

Otherwise use a truthful blocked or revision-required status identifying the exact open items.
