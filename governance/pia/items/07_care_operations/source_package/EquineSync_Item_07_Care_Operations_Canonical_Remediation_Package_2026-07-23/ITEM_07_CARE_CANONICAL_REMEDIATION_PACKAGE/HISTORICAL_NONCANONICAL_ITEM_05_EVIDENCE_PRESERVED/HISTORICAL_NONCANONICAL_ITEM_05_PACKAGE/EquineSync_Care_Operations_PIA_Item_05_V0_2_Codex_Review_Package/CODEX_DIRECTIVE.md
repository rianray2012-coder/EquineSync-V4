# Codex Directive: Item 05 Care Operations PIA V0.2 Fresh Structured Review and Repository Integration

## 1. Authority and task boundary

You are authorized to perform a documentary-only intake, repository reconciliation, fresh structured review, and additive repository integration for the EquineSync Care Operations PIA package identified below.

This directive does **not** authorize implementation, application code, database schemas, migrations, infrastructure changes, deployment, production use, pilot enrollment, first-user enrollment, or any modification to locked governance artifacts.

Do not infer additional Founder decisions. Do not convert documentary requirements into implementation authority.

## 2. Controlled package identity

- Official repository: `rianray2012-coder/EquineSync-V4`
- Portfolio position: `Item 05`
- PIA ID: `ES-PIA-CARE-OPERATIONS-V0.2.0`
- Master template: `ES-PIA-MASTER-STANDARD-V1.1`
- Candidate status: `ITEM_05_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`
- Founder decisions: `CARE-FD-001` through `CARE-FD-020`
- Requested review objective: determine whether V0.2 is a complete and traceable documentary baseline suitable for Founder documentary disposition
- Authority effect: `NONE`
- Implementation / schema / migration / deployment / production / pilot / enrollment authority: `FALSE`

The candidate must remain Item 05. Do not renumber it or substitute a neighboring PIA identity.

## 3. Mandatory fail-closed intake

Before branch creation, file copying, staging, commit, or push:

1. Confirm the archive SHA-256 matches the supplied outer checksum.
2. Run `unzip -t` and require success.
3. Extract to a new temporary directory.
4. Run `sha256sum -c CHECKSUMS.sha256` from the extracted package root and require every entry to pass.
5. Confirm `PACKAGE_MANIFEST.json`, the Markdown header, and the machine-readable JSON agree on:
   - Item 05;
   - `ES-PIA-CARE-OPERATIONS-V0.2.0`;
   - V0.2 strengthened-candidate status;
   - CARE-FD-001 through CARE-FD-020;
   - all authority flags remaining false.
6. Confirm the official Git remote resolves to `rianray2012-coder/EquineSync-V4`.
7. Confirm no unrelated Git write, active index lock, rebase, merge, cherry-pick, or dirty worktree is present.
8. Fetch remote refs without altering the working tree.
9. Identify the repository's current canonical Remaining PIA Program baseline and Item 05 registry entry from repository evidence. Do not assume the default branch is the correct integration baseline.

Stop before mutation if any intake check fails or if the repository identifies Care Operations under a different portfolio position or materially different PIA ID. Report exact evidence and do not improvise a reconciliation.

## 4. Repository baseline and branch

After all intake checks pass:

1. Create a new branch from the repository-evidenced canonical Remaining PIA Program baseline.
2. Recommended branch name:
   `codex/item-05-care-operations-pia-v0-2-fresh-structured-review-v1`
3. Preserve all existing historical and locked artifacts byte-for-byte.
4. Use additive changes wherever possible.
5. Do not create a pull request and do not merge.

If the recommended branch name already exists, stop and report rather than force-resetting or reusing it.

## 5. Exact documentary review scope

Perform a fresh review against the repository's exact controlling sources, including the adopted PIA Master Standard, PIA program register, applicable governance canons, authority routing, and supplying-domain contracts.

At minimum, verify:

### A. Structure and template conformance

- all 43 mandatory sections exist, are ordered, and are substantively populated;
- the document uses the exact `ES-PIA-MASTER-STANDARD-V1.1` lifecycle and gate model;
- no mandatory section is satisfied only by cross-reference without enough local operational detail;
- the DOCX, Markdown, and JSON represent the same candidate.

### B. Founder-decision incorporation

- every `CARE-FD-001` through `CARE-FD-020` decision is traceable to requirements, workflows, data, permissions, acceptance criteria, tests, or explicit scope boundaries;
- no Founder decision is diluted, contradicted, expanded, or silently deferred;
- no unapproved product decision has been inserted by the drafter.

### C. Domain and authority boundaries

Verify that Care Operations:

- owns routine care execution, tasking, factual observation, escalation chronology, and operational location coordination only within authorized scope;
- does not become authoritative for diagnosis, veterinary instructions, medication truth, nutrition formulation, billing liability, employment discipline, horse ownership, relationship authority, or access-control policy;
- distinguishes task from authority, completion from proof, observation from diagnosis, sending from acknowledgment, and metrics from permission to surveil;
- preserves human authority for turnout compatibility, welfare judgment, professional care, and emergency decisions.

### D. Requirements and workflows

Review all 64 normative requirement records and all 14 workflows for:

- unambiguous actor and system responsibility;
- explicit preconditions and authority checks;
- required and prohibited behavior;
- state transitions and failure paths;
- offline and synchronization behavior;
- evidence, audit, retention, and correction behavior;
- acceptance criteria and test linkage;
- work-package and release-gate linkage.

### E. Data, permissions, and interfaces

Review the 22 entities, 7 state models, 15 permission records, APIs, events, jobs, integrations, and UI contracts for:

- clear canonical ownership and derivative/projection labeling;
- facility, horse, actor, relationship, purpose, time, delegation, guardian, consent, sensitivity, and emergency context;
- least privilege and non-disclosure of unrelated horse, owner, staff, safeguarding, investigation, or professional data;
- idempotency, ordering, retry, reconciliation, duplicate prevention, and stale-write handling;
- preservation of predecessor and supersession history.

### F. Safety, failure, operations, and quality attributes

Review:

- missed, late, impossible, refused, substituted, escalated, and emergency care behavior;
- notification-versus-acknowledgment semantics;
- low-connectivity and offline access controls;
- AI boundaries and human review requirements;
- monitoring, alerting, audit, recovery, backup, rollback, continuity, and support requirements;
- quantitative targets, configuration controls, and any unresolved owner assignments;
- migration and legacy-data assumptions.

### G. Proof and readiness

Confirm or correct the documentary counts and uniqueness assertions for:

- 64 requirements;
- 40 acceptance criteria;
- 58 tests;
- 14 workflows;
- 22 entities;
- 7 state models;
- 15 permission records;
- 10 golden paths;
- 36 adversarial scenarios;
- 25 evidence records;
- 9 work packages.

Evaluate all five mandatory readiness questions independently. A permitted target disposition is:

1. Engineering buildability: `YES_WITH_EVIDENCE` only if the documentary package removes unauthorized product decisions and provides implementable contracts.
2. Objective QA verification: `YES_WITH_EVIDENCE` only if acceptance criteria, tests, expected results, and evidence are objectively determinable.
3. Governance and MIAP traceability: `YES_WITH_EVIDENCE` only if exact repository sources, authority routing, and work-package traceability are established.
4. Operational safety and recovery: `NO` until implementation, runbooks, monitoring, recovery, rehearsal, and operational evidence exist.
5. Controlled first-user enrollment: `NO` until implementation, operational readiness, support, privacy, training, enrollment controls, and executed evidence exist.

Do not upgrade Questions 4 or 5 on documentary evidence alone.

## 6. Source and runtime constraints

- Use exact repository sources and record paths and hashes.
- Do not fabricate missing source registration, contract approval, ownership assignment, quantitative targets, or evidence.
- Do not use web search as a substitute for repository authority.
- Do not invoke provider-bound diagnostics, external model calls, unrestricted runtime, or hidden network activity as part of package intake.
- If a repository-mandated formal review gate requires unavailable runtime permissions or provider access, stop that gate fail-closed. You may preserve completed deterministic static review evidence, but you must label the formal review as blocked and must not claim it passed.
- Do not bypass, weaken, patch around, or reclassify a mandatory gate merely to obtain a passing disposition.

## 7. Revision rule

Preserve V0.2 exactly as supplied.

If the fresh review identifies material documentary corrections:

1. Do not overwrite V0.2.
2. Create a V0.3 successor with matching DOCX, Markdown, and machine-readable JSON.
3. Create a finding-to-correction matrix.
4. Preserve every unchanged Founder decision and every authority restriction.
5. Re-run deterministic validation and render the successor DOCX for visual inspection.
6. Do not describe V0.3 as adopted, approved, implementation-ready, operationally ready, or enrollment-ready without the corresponding Founder disposition and evidence.

If no material corrections are required, retain V0.2 and create a fresh-review receipt rather than changing the candidate merely to create activity.

## 8. Required repository outputs

Create an Item 05 review/integration directory consistent with the repository's established Remaining PIA Program structure. Include, at minimum:

1. preserved package payload or exact repository-native copies;
2. `FRESH_STRUCTURED_REVIEW_REPORT.md`;
3. `FRESH_STRUCTURED_REVIEW_FINDINGS.csv`;
4. `SOURCE_AND_AUTHORITY_RECONCILIATION.md`;
5. `FOUNDER_DECISION_TRACEABILITY.md` or equivalent matrix;
6. `DOCUMENTARY_VALIDATION_REPORT.json`;
7. `REPOSITORY_INTEGRATION_RECEIPT.md`;
8. an updated package manifest and checksum ledger for newly created review artifacts;
9. V0.3 successor files and revision report only if material corrections are required.

Use repository naming conventions when they are stricter than these suggested names.

## 9. Validation before commit

Before commit:

- confirm the diff is limited to the new Item 05 documentary review/integration family and any strictly required program-register update;
- confirm no locked or historical artifact changed;
- verify every checksum ledger;
- validate JSON syntax;
- validate CSV structure and line endings according to repository policy;
- confirm no TODO, TBD, placeholder, fake citation, unresolved merge marker, or internal tool token remains;
- confirm every authority flag remains false;
- confirm Questions 4 and 5 remain `NO` unless actual non-documentary evidence exists and separate Founder authority permits reevaluation;
- render every new or revised DOCX and inspect all pages for clipping, overlap, broken tables, missing glyphs, and incorrect headers/footers;
- run all applicable deterministic repository checks that do not violate the runtime constraints above.

If any validation fails, do not commit a claimed passing review.

## 10. Commit and push

If the review/integration result is valid:

1. Stage only the intended Item 05 files.
2. Commit once with a clear documentary message, for example:
   `docs(pia): integrate and review Item 05 Care Operations V0.2`
3. Push the new branch to the official remote.
4. Verify that the remote branch tip exactly matches the local commit.
5. Leave the worktree and index clean.
6. Do not create a PR and do not merge.

If the formal review is blocked after deterministic work is preserved, use a commit message and final disposition that explicitly state the blocked condition. Do not use `PASS`, `APPROVED`, `ADOPTED`, or `READY_FOR_IMPLEMENTATION` language.

## 11. Final receipt to Founder

Report:

- repository and official remote;
- canonical starting baseline and commit;
- created branch;
- ending commit and remote-ref verification;
- exact repository paths created or modified;
- intake checksum results;
- review findings by severity and disposition;
- whether V0.2 was retained or V0.3 was created;
- all five readiness answers with concise evidence;
- source or contract gaps that remain;
- runtime-gate status;
- explicit authority statement confirming no implementation or enrollment authority was created;
- clean worktree/index status;
- confirmation that no PR or merge was created.

## 12. Stop conditions

Stop before mutation, or stop before further mutation as applicable, if any of the following occurs:

- outer or inner checksum failure;
- archive-test failure;
- Item 05 or PIA-ID mismatch;
- conflict with the repository's canonical PIA program register;
- ambiguous integration baseline;
- dirty worktree or unrelated active Git write;
- existing target branch;
- locked artifact would need modification;
- missing controlling source that prevents an honest traceability conclusion;
- mandatory runtime gate cannot be lawfully executed;
- review would require invention of a Founder decision;
- requested action would create implementation, operational, pilot, or enrollment authority.

When stopped, provide a precise fail-closed receipt. Do not partially characterize an incomplete gate as passed.
