# Founder-Directed Codex Revision Directive

## EquineSync Master Product Feature-to-Governance Coverage Matrix V1.0

Directive ID: `EQUINESYNC_FGM_REVIEW_FINDINGS_REVISION_DIRECTIVE_V1_0`

Directive date: `2026-08-04`

Current PR: `rianray2012-coder/EquineSync-V4#80`

Current review snapshot: `9ace3eed6b949d7e3ed38fcbfba21bcaec8e3991`

Current status: `THREE_INDEPENDENT_REVIEWS_RECEIVED_REVISION_REQUIRED_NOT_READY_FOR_FOUNDER_REVIEW`

## 1. Purpose

Codex shall perform an in-place documentary revision of `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0` on the existing PR #80 work branch. The revision shall adjudicate and correct all valid findings raised by Claude, Perplexity, and Cursor while preserving documentary authority boundaries and complete evidence lineage.

The objective is not merely to make validators pass. The objective is to produce a semantically credible, source-supported, decision-useful Feature-to-Governance Matrix whose structural validation, substantive mappings, evidence states, and readiness language agree.

## 2. Controlling review inputs

Treat the following as review evidence, not self-executing authority:

1. `PERPLEXITY_INDEPENDENT_REVIEW_FEATURE_TO_GOVERNANCE_MATRIX.md` — exact received report; disposition `REVISION_REQUIRED_BEFORE_FOUNDER_REVIEW`.
2. `CURSOR_INDEPENDENT_REVIEW_FEATURE_TO_GOVERNANCE_MATRIX.md` — exact received report; disposition `REVISION_REQUIRED_BEFORE_FOUNDER_REVIEW`.
3. `CLAUDE_INDEPENDENT_REVIEW_FEATURE_TO_GOVERNANCE_MATRIX.md` — exact received first-principles review, including findings F1 through F11.

Do not automatically accept or reject a finding based solely on reviewer severity. Determine validity against repository evidence, package contents, controlling governance sources, and reproducible analysis. Where reviewer recommendations conflict, record the conflict and apply the correction that provides the most accurate, least overstated documentary result.

## 3. Scope and branch controls

1. Work only on the existing PR #80 work branch unless an authenticated repository state requires a safe successor branch. If a successor branch is necessary, explain why and preserve PR lineage.
2. Do not directly modify the protected branch.
3. Limit substantive edits to the matrix package and review-response evidence inside its authorized governance path.
4. Do not modify application code, schemas, migrations, provider configuration, CI, deployment configuration, secrets, production data, staging data, or runtime environments.
5. Do not merge PR #80.
6. Do not mark the package Founder approved, authoritative, adopted, active, implemented, runtime verified, certified, or finalized.

## 4. Mandatory finding adjudication

Create `INDEPENDENT_REVIEW_FINDING_ADJUDICATION_REGISTER.csv` with one row per atomic finding. At minimum include:

- `consolidated_finding_id`
- `reviewer_finding_ids`
- `reviewers`
- `finding_title`
- `affected_files`
- `affected_fields`
- `affected_feature_ids`
- `reviewer_severities`
- `final_validity` (`VALID`, `PARTIALLY_VALID`, `NOT_VALID`, `SUPERSEDED`)
- `final_severity`
- `evidence`
- `adjudication_rationale`
- `required_correction`
- `acceptance_test`
- `correction_status`
- `closure_evidence_paths`
- `residual_risk`
- `founder_decision_required`

No finding may be closed merely because a structural validator passes. A `NOT_VALID` or `PARTIALLY_VALID` determination requires evidence and reasoning. Preserve reviewer-specific IDs and do not erase disagreements.

Create a companion `REVIEWER_TO_CONSOLIDATED_FINDING_CROSSWALK.csv` mapping every Claude F1 through F11, every Perplexity F-01 through F-16, and every Cursor F-01 through F-16 to the consolidated register. Claude F11 is a positive control that must be preserved rather than remediated.

## 5. Mandatory correction workstreams

### 5.1 Feature semantics

1. Replace all 314 templated feature descriptions with feature-specific descriptions.
2. Each description must identify, as applicable: purpose, primary workflow, principal actors, material data, authority boundary, and business outcome.
3. Do not impose an arbitrary word count where a shorter description is genuinely complete, but reject syntactic templates and mechanically substituted domain/name prose.
4. Add or strengthen per-row intent-source traceability so the feature description is supported by a row-specific source or explicitly labeled as a planning inference.
5. Disambiguate duplicate feature names across domains where the name alone could mislead a reviewer.
6. Re-evaluate downstream personas, governance mappings, risk, evidence, gaps, and dependencies after descriptions are rewritten; do not preserve old values merely for count stability.

Acceptance evidence must include automated template detection plus documented human semantic review across every domain, all critical rows, all rows formerly labeled `FULLY_COVERED`, and all new-PIA candidates.

### 5.2 Coverage and readiness terminology

1. Reconcile the meaning of `FULLY_COVERED`, `GOVERNANCE_READY`, and the parallel `EVIDENCE_ONLY_GAP` classification.
2. Do not allow a label reasonably read as implementation or conformity readiness when every row remains implementation-unverified and runtime-unverified.
3. Prefer explicit documentary terminology such as `DOCUMENTARY_GOVERNANCE_LAYERS_COMPLETE_UNVERIFIED` unless authenticated governing methodology requires another accurate label.
4. Reconcile the 11 affected rows against governing PIA source state, lifecycle state, repository evidence quality, unresolved conflicts, and dependency inconsistencies.
5. A row relying on an unlocated or successor-pending PIA may not be presented as unqualified fully covered.
6. Update readiness methodology, dashboard, reports, queues, and validators consistently.

### 5.3 PIA source identity and supplement sequencing

1. Verify the actual repository state of PIAs 01–10 at the current work-branch baseline. Do not rely exclusively on the prior realignment register if later authenticated source packages exist.
2. Create a row-level `PARENT_PIA_SOURCE_STATE` field or equivalent authoritative linkage in the supplement decision register.
3. Block supplement drafting recommendations where a parent PIA source cannot be authenticated.
4. Make PIA source-identity reconciliation an explicit prerequisite where necessary.
5. Reassess all 14 supplement groupings after authenticating the parent PIA foundation.
6. Preserve the Marketplace/Provider Network/Community new-PIA question as a proposal unless separately decided by the Founder.

### 5.4 Field dictionary and data contract

Replace the boilerplate field dictionary with a substantive data contract. For every matrix field specify:

- field-specific meaning
- data type
- allowed values or format
- source or authority basis
- owning role
- derivation method
- null/blank handling
- maintenance trigger
- whether the field is authoritative, derived, planning-only, or evidentiary

Synchronize controlled values with validator constants. Add tests that fail when the field dictionary and validator vocabularies diverge.

### 5.5 Evidence lifecycle and repository-path hygiene

1. Remove prose, sentinel strings, and limitation notes from `IMPLEMENTATION_EVIDENCE_PATHS`.
2. Move limitations into a dedicated evidence-limitation or verification-notes field.
3. Store only normalized repository paths in path fields.
4. Use explicit evidence tiers such as `PATH_CONFIRMED`, `CODE_INSPECTED`, `TEST_EXECUTED`, and `RUNTIME_VERIFIED`; do not collapse them.
5. Treat keyword-matched paths as `KEYWORD_MATCH_ONLY` or equivalent, not as implementation evidence.
6. Reinspect weak examples identified by reviewers, including Marketplace rows citing `Signup.jsx`, incident rows citing shared dashboard/emergency files, platform search citing billing-search UI, and authentication rows citing feature pages.
7. For a feature not located, leave the implementation path empty and state `NOT_FOUND` in the proper status field.
8. Require proposition-level source support rather than applying the Backend Permission Capability Map and universal context sources indiscriminately to every row.

### 5.6 Semantic governance mapping

1. Perform a human semantic validation of every PIA, Code Guide, ADR, operating standard, runbook, privacy, reporting, AI, and safeguarding mapping.
2. Add validator-backed domain-owner constraints only where they are supported by governing sources; do not replace human review with brittle keyword allowlists.
3. Replace placeholder `ES-CG-00` references with the actual expected Code Guide IDs where they can be authenticated. If no precise guide exists, state a truthful gap rather than inventing an identifier.
4. Identify planning proposals separately from existing governance artifacts.
5. Reassess whether accessibility, vendor/third-party risk, AI/model governance, security assurance, regulatory mapping, safeguarding, records retention, and incident-response controls are actually absent, already governed by existing canon, or require a proposed artifact. Do not create duplicate governance merely because a keyword was absent from the matrix.
6. Record exact source evidence for each disposition.

### 5.7 Risk and readiness calibration

1. Add a per-row `RISK_RATIONALE` or equivalent, identifying the factors supporting severity and likelihood.
2. Reassess risk at feature level rather than assigning uniform domain or governance-state templates.
3. Do not force artificial statistical diversity merely to meet a distribution target; however, investigate and explain clustering.
4. Mark scores `UNCALIBRATED_PLANNING_ONLY` until calibration is complete if the work cannot truthfully support decision-grade scoring.
5. Recompute dashboards and queues after correction.
6. Keep governance readiness distinct from implementation verification and release readiness.

### 5.8 Dependencies

1. Revalidate the dependency graph semantically, including the universal `PLATFORM-001` dependency and the 292-row identity/communications/relationship/task hubs.
2. Introduce dependency type where useful, such as `HARD`, `SOFT`, `DATA`, `AUTHORIZATION`, or `PLANNING_INFERENCE`.
3. Replace `DEPENDENCY_BASIS` values that merely repeat confidence with actual reasoning.
4. Resolve or explicitly define the ten `DEPENDS_ON_FEATURE_IDS` versus `BLOCKED_BY_FEATURE_IDS` inconsistencies.
5. Preserve acyclicity and inverse-link validation.
6. Describe universal shell/root dependency counts as architecture-wide planning relationships, not empirically verified blast radius.

### 5.9 Conflict decomposition and queue derivation

1. Decompose mega-conflict entries into atomic, actionable propositions.
2. Each conflict must identify affected features/artifacts, conflict type, evidence, owner, resolution authority, proposed disposition, and closure criteria.
3. Derive `CONFLICT_RESOLUTION_QUEUE` membership from atomic conflict records.
4. Remove the validator exemption that permits opaque conflict-queue membership.
5. Do not allow an unqualified documentary-complete row to remain in an unresolved conflict queue without a retained-gap explanation.

### 5.10 Personas, taxonomy, planning fields, and duplicate names

1. Reassign personas per feature and distinguish primary, secondary, observer, guardian, and administrator roles where applicable.
2. Require a basis for unusually broad persona sets.
3. Resolve taxonomy-only `*-000` parent identifiers by adding explicit taxonomy records or a validated taxonomy-only designation.
4. Disambiguate duplicate feature names.
5. Populate `RELEASE_TARGET`, `MVP_CLASSIFICATION`, and effort only if supported by documented planning criteria; otherwise mark them truthfully as unassigned/unknown and remove misleading decision framing.

### 5.11 Validator, tests, and generated outputs

1. Add negative tests for materially wrong but vocabulary-valid mappings where a deterministic constraint is justified.
2. Add path-field hygiene tests.
3. Add tests for checksum tamper, missing files, fully-covered overstatement, field-dictionary vocabulary drift, conflict-queue derivation, parent-ID resolution, and dependency-field consistency.
4. Make authorized-path verification fail closed when the required comparison baseline cannot be authenticated, or record a truthful validation block.
5. Align every adversarial `PASS` claim with an actual executable test or clearly label it as manually inspected.
6. Generate Markdown dashboards from authoritative structured data or verify their key tables against that data.
7. Ensure regenerated hashes cannot conceal semantically stale summaries by including freshness/derivation checks.
8. Establish and document a single authoritative structured source plus deterministic regeneration tooling for derived CSV, JSON, Markdown, dashboard, queue, and register outputs. Do not require manual synchronization across static exports.

### 5.12 Governance ownership and throughput

1. Review whether every unresolved action is unnecessarily routed to the Founder or whether existing governance permits identified domain owners, reviewers, or the designated Second Reviewer to perform bounded review or recommendation functions.
2. Do not delegate Founder-reserved approval authority without an authenticated governance source.
3. Distinguish decision authority, review responsibility, subject-matter consultation, implementation ownership, and evidence-verification responsibility.
4. Add a decision-routing field or companion register only if supported by current governance; otherwise identify the single-point-of-throughput risk as a retained issue.
5. Preserve Claude's positive finding regarding authority-boundary discipline: do not weaken the existing `NO_*` disclaimers or adversarial controls.

## 6. Founder-decision register

Add a ripeness state for each Founder question:

- `RIPE`
- `RIPE_WITH_CAUTION`
- `PREREQUISITE_CORRECTION_REQUIRED`
- `DEFERRED`
- `MOOT_AS_POSED`

Reassess all Founder questions only after correction. Do not retain `READY_FOR_FOUNDER_REVIEW` merely because a question exists.

## 7. Required deliverables

Produce inside the authorized package or a clearly linked review-response subdirectory:

1. Revised matrix CSV, JSON, and Markdown.
2. Revised field dictionary.
3. `INDEPENDENT_REVIEW_FINDING_ADJUDICATION_REGISTER.csv`.
4. `REVIEWER_TO_CONSOLIDATED_FINDING_CROSSWALK.csv`.
5. `SEMANTIC_VALIDATION_REPORT.md` with reviewer, sample/full-review scope, evidence, exceptions, and unresolved issues.
6. `PIA_SOURCE_IDENTITY_AND_SUPPLEMENT_PREREQUISITE_REPORT.md`.
7. `EVIDENCE_PATH_REVALIDATION_REPORT.md`.
8. `DEPENDENCY_SEMANTIC_REVIEW_REPORT.md`.
9. `CONFLICT_DECOMPOSITION_REGISTER.csv`.
10. `RISK_AND_READINESS_RECALIBRATION_REPORT.md`.
11. Updated methodologies, dashboards, queues, registers, manifest, and checksums.
12. `REVISION_CLOSURE_REPORT.md` showing every accepted finding and its closure evidence.
13. `UNRESOLVED_FINDINGS_AND_FOUNDER_DECISIONS.md`.
14. Fresh validation and test reports.

## 8. Validation requirements

At minimum run and report:

- package checksum verification
- package manifest verification
- CSV and JSON parsing
- CSV/JSON parity
- field-dictionary/schema parity
- controlled-vocabulary parity
- duplicate and referential-integrity checks
- PIA/source-identity checks
- evidence-path syntax and evidence-tier checks
- dependency inverse-link and cycle checks
- conflict-to-queue derivation checks
- risk/readiness recomputation
- dashboard and queue recomputation
- validator unit tests, including new negative tests
- `git diff --check`
- authorized-path verification against an authenticated base

Structural `PASS` results must be reported as structural results only. Provide separate semantic validation conclusions.

## 9. Required final report

Return:

1. authenticated starting and ending repository state;
2. exact changed-file list;
3. finding counts by validity, severity, and closure status;
4. corrections completed;
5. unresolved findings and reasons;
6. validation commands and exact outcomes;
7. remaining Founder decisions and their ripeness;
8. authority-boundary confirmation;
9. one final documentary status.

The final status may be `REVISION_COMPLETE_READY_FOR_TARGETED_REREVIEW` only if every valid blocker and high finding is corrected with closure evidence. Do not declare `READY_FOR_FOUNDER_REVIEW` in this execution. A targeted independent rereview or separately authorized Founder decision must determine later readiness.

## 10. Explicit non-authorization

This directive does **not** authorize:

- direct protected-branch mutation
- merger of PR #80 or any successor PR
- Founder approval
- authoritative designation
- adoption or activation of governance
- application-code modification
- schema or migration modification
- CI or deployment modification
- provider configuration
- runtime or production claims without evidence
- staging, pilot, launch, or production use
- certification or public compliance claims
- automatic closure of reviewer findings

Required status during execution:

`FOUNDER_DIRECTED_DOCUMENTARY_REVISION_AUTHORIZED_NO_MERGE_ACTIVATION_IMPLEMENTATION_DEPLOYMENT_PILOT_OR_PRODUCTION_AUTHORITY`
