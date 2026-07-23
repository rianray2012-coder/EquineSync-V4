# Codex Execution Directive
## EquineSync Item 06 Task, Calendar, Scheduling, and Notification PIA

**Directive ID:** `ES-CODEX-TCSN-PIA-2026-07-22-01`  
**Requested disposition:** `REPOSITORY_INTEGRATION_AND_FRESH_STRUCTURED_REVIEW_ONLY`  
**Authority ceiling:** Documentary work only  
**Implementation authority:** `FALSE`  
**Deployment authority:** `FALSE`  
**Enrollment authority:** `FALSE`

## 1. Mission

Integrate the supplied Item 06 PIA package into the official EquineSync repository using the repository's current canonical structure and controls. Then perform a fresh structured review of the V0.2 candidate against the adopted PIA Master Standard, controlling governance, MIAP requirements, approved Founder decisions, and repository conventions.

The review must independently determine whether all five mandatory readiness questions are fully and defensibly answered at the documentary-design level. Do not merely repeat the internal review conclusion.

## 2. Inputs

Treat the following package files as controlled inputs:

- `FOUNDER_DECISION_RECORD.md`
- `assets/EquineSync_Item_06_Task_Calendar_Scheduling_Notification_PIA_V0_1_Draft.md`
- `assets/EquineSync_Item_06_Task_Calendar_Scheduling_Notification_PIA_V0_2_Strengthened_Draft.md`
- `assets/EquineSync_Item_06_V0_1_Internal_Review_and_V0_2_Revision_Report.md`
- `assets/EquineSync_Item_06_V0_2_Documentary_Validation.json`
- `PACKAGE_MANIFEST.csv`
- `CHECKSUMS.sha256`

Verify package checksums before substantive work.

## 3. Founder decisions

`TCSN-FD-001` through `TCSN-FD-020` are resolved for documentary design. Do not reopen, dilute, reverse, or silently reinterpret them.

Special handling for `TCSN-FD-010`:

- Optional SMS is part of the initial controlled scope.
- SMS is not mandatory for every user or notice.
- Voice calling, WhatsApp or comparable consumer channels, and automated emergency calling trees remain deferred unless separately authorized.

If a controlling governance conflict is discovered, record the conflict and stop before changing a Founder decision.

## 4. Mandatory repository preflight

Before editing:

1. Confirm the repository is the official EquineSync repository.
2. Record the remote, default branch, current branch, HEAD commit, worktree state, index state, and applicable repository instructions.
3. Confirm the worktree and index are clean or isolate unrelated changes without modifying them.
4. Locate the adopted PIA Master Standard, Item 06 or remaining-PIA conventions, source registers, MIAP mappings, and locked governance references.
5. Determine the exact canonical destination paths from repository evidence. Do not invent a conflicting directory convention.
6. Create a new documentary branch from the correct authorized baseline. Suggested branch name: `codex/item-06-tcsn-pia-fresh-structured-review-v1`.
7. Preserve the supplied predecessor and package evidence. Do not overwrite or delete V0.1.

If the correct baseline, repository, or destination cannot be established, stop fail-closed and issue a blocked receipt.

## 5. Required review work

Perform a fresh review covering, at minimum:

- exact Master Standard section and order conformance;
- source inheritance, precedence, and conflict treatment;
- all twenty Founder decisions;
- separation of task, event, occurrence, reminder, notification, acknowledgment, acceptance, completion, and escalation;
- authoritative ownership across calendar, barn operations, communication, identity, relationships, permissions, agreements, privacy, safeguarding, health, billing, lessons, shows, and external adapters;
- assignment modes, delegation, substitute coverage, and least privilege;
- recurrence editing and historical preservation;
- time zones, daylight saving, travel, and floating or all-day semantics;
- availability privacy, resource conflicts, welfare constraints, and overrides;
- offline caching, completion, idempotency, revocation, and reconciliation;
- in-app, push, email, digest, optional SMS, failed delivery, fallback, retry, and dead-letter behavior;
- quiet hours, emergency override, notification fatigue, and mandatory notice protection;
- provider neutrality, token handling, webhook authenticity, revocation, exit, and rollback;
- requirements, acceptance criteria, testability, golden paths, adversarial cases, evidence, and traceability;
- operational ownership, support, monitoring, backup, restore, incident response, rollback, and enrollment decision support;
- explicit distinction among as-designed, as-built, as-verified, operational, and enrollment baselines.

## 6. Five mandatory questions

Evaluate each question using only the adopted vocabulary and actual evidence:

1. Can engineering build without making unauthorized product decisions?
2. Can QA determine objectively whether the capability works?
3. Can a reviewer trace the capability to controlling governance and MIAP?
4. Can EquineSync safely operate, support, monitor, recover, and maintain the capability?
5. Can the Founder determine whether the capability is ready for first-user enrollment?

Target outcome: all five are fully satisfied at the documentary-design level.

The current candidate states `YES_WITH_EVIDENCE` for all five. Validate that conclusion. If one or more answers are not supportable, revise the candidate only within approved Founder decisions and controlling governance. If a material new Founder decision is required, record it as an open decision and stop before inventing an answer.

A fully answered fifth question may still produce the current decision `NOT_READY_FOR_FIRST_USER_ENROLLMENT`. Do not confuse decision support with enrollment authorization.

## 7. Required repository outputs

Create or update the repository's canonical equivalents of:

1. V0.1 preserved predecessor.
2. V0.2 or a stronger V0.3 candidate, only if review changes are required.
3. Founder decision register.
4. Source and inheritance register with exact repository paths, versions, hashes, and anchors where the repository standard requires them.
5. Requirement traceability matrix with one row per requirement.
6. Acceptance, test, golden-path, adversarial, and evidence registers where required by the Master Standard.
7. Fresh structured review report.
8. Deterministic validation report.
9. Package manifest and checksum ledger.
10. Founder decision brief stating the exact candidate disposition and unresolved gates.
11. Completion receipt using `CODEX_COMPLETION_RECEIPT_TEMPLATE.md` as the minimum content standard.

Use existing repository naming and location conventions when they differ from the package filenames.

## 8. Review independence and assurance language

Do not claim independent, external, or segregated review unless the required process actually ran under the repository's approved controls.

If a segregated review runtime is required but unavailable or fails preflight:

- preserve the candidate;
- complete only permitted deterministic and repository integration work;
- record the exact blocked condition;
- use a disposition such as `FRESH_STRUCTURED_REVIEW_BLOCKED_BY_RUNTIME_OR_CONTROL_LIMITATION`;
- do not substitute a same-context review while labeling it independent.

## 9. Hard boundaries

Do not:

- implement application code;
- create or modify database schemas or migrations;
- activate push, email, SMS, calendar, or other provider credentials;
- make provider-bound production requests;
- deploy or release;
- enroll users;
- modify locked governance to fit the candidate;
- change approved Founder decisions;
- delete or rewrite the predecessor;
- merge to the default branch;
- create a pull request unless separately directed;
- claim production, operational, verification, or enrollment readiness without executed evidence;
- apply the recommended Founder disposition automatically.

The potential disposition `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED` is reserved for a separate Founder decision after Codex presents the completed review package.

## 10. Validation gates

Before commit, require at least:

- package checksum verification;
- exact file-scope audit;
- section-order and required-section validation;
- unique and contiguous controlled identifiers;
- all Founder decisions mapped;
- all requirements mapped forward to acceptance, tests, evidence, dependencies, and gates;
- backward traceability from tests and evidence to requirements and sources;
- allowed readiness vocabulary only;
- no authority contradiction;
- no undocumented P0 or P1 finding;
- no staged files outside the controlled documentary scope;
- clean diff checks subject to documented repository formatting rules;
- final manifest and checksum verification;
- local and remote branch agreement after push.

## 11. Commit and push rules

Commit and push only the documentary package and required registers on the new branch after all applicable gates pass.

Do not merge and do not create a PR unless separately authorized.

If a gate fails, stop before commit or push unless the repository's evidence-preservation rules require a clearly labeled blocked-evidence commit. Explain the controlling rule in the receipt.

## 12. Required final receipt

Return a concise but complete receipt containing:

- repository and remote;
- starting branch and commit;
- resulting branch and commit;
- exact files added or modified;
- package and candidate hashes;
- review method and whether it was actually independent or segregated;
- all five readiness answers with evidence references;
- P0, P1, and retained P2 findings;
- validation and checksum results;
- worktree and index state;
- push and remote-ref verification;
- exact authority statement;
- recommended Founder disposition;
- explicit statement that no implementation, deployment, production activation, or enrollment occurred.

## 13. Success disposition

Use this only if the fresh review and all repository gates actually pass:

`ITEM_06_TCSN_PIA_FRESH_STRUCTURED_REVIEW_COMPLETE_READY_FOR_FOUNDER_DESIGN_DISPOSITION_NO_IMPLEMENTATION_AUTHORITY`

Otherwise issue the narrowest accurate blocked or revision-required disposition.
