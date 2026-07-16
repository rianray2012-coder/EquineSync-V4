# Master ATLAS Governance

Status: Canon
Owner: Founder / Codex
Effective Date: 2026-07-10
Purpose: Define the permanent governance standard for every EquineSync ATLAS phase, audit package, founder decision, RF handoff, and release-readiness claim.

## ATLAS Lifecycle and Phase Structure

ATLAS is EquineSync's canonical product-audit lifecycle. Each ATLAS phase tests the product against a defined product-reality lens and may generate gated RF implementation phases.

Each ATLAS phase must include:

1. Entry gate and predecessor status.
2. Canon documents reviewed.
3. Scope and explicit non-goals.
4. Evidence ledger.
5. Route/API or equivalent coverage matrix.
6. Scenario, workflow, persona, or domain audit rows.
7. Findings with severity and RF assignment.
8. Founder decision rows.
9. Gate review.
10. Deliverable manifest and package verification.

ATLAS phases do not approve public launch by default. Public launch approval requires an explicit founder release gate separate from the audit lock.

## Gate-State Definitions

| Gate State | Meaning | Allowed Next Step |
| --- | --- | --- |
| `NOT_STARTED` | Phase has not begun. | Create founder-approved phase plan. |
| `IN_PROGRESS` | Audit or implementation evidence is being gathered. | Continue scoped work. |
| `BLOCKED` | P0/P1 defect, missing required input, or unresolved approval prevents progression. | Fix blocker or obtain founder decision. |
| `CONDITIONAL_PASS_PENDING_FOUNDER_AND_EVIDENCE` | Audit is substantially useful but mandatory evidence, verification, or founder rows are incomplete. | Complete remediation package; do not lock. |
| `CONDITIONAL_PASS_PENDING_FOUNDER_LOCK` | Evidence is complete enough for founder lock review, but founder lock is not recorded. | Founder may approve, reject, or request corrections. |
| `PASS` | Evidence supports the phase result, but lock has not necessarily been recorded. | Use only for non-locking review outputs. |
| `LOCKED` | Founder approval, required evidence, tests, and package verification are recorded. | Proceed only to founder-approved next phase. |
| `DEFERRED` | Work is intentionally postponed with owner, reason, and next trigger recorded. | Revisit when trigger occurs. |
| `REOPENED` | Previously locked phase requires correction due to new blocker, contradiction, or canon change. | Run review/fix/relock cycle. |

No ATLAS gate may record `LOCKED` unless the approval table, evidence table, tests, manifest, and package agree.

## Evidence Standards

Evidence must be specific, source-backed, and reusable. Route availability alone is not proof of workflow completion.

Each evidence row should identify:

- Evidence ID.
- Scenario, workflow, persona, or domain row.
- Frontend route or surface.
- Frontend component/file.
- Backend endpoint.
- Backend implementation file.
- Data model or persistence entity.
- Permission or scope enforcement.
- Notification state, including unsent/manual/deferred states.
- Audit mechanism.
- Automated test reference.
- Manual inspection evidence.
- Result.
- Known limitation.
- Commit or working-tree reference.

Unsupported claims such as "route exists," "permissions tested," or "workflow complete" are not sufficient without evidence IDs and supporting files/tests.

## Severity Taxonomy

ATLAS severity must distinguish implementation severity from launch-trust severity.

| Severity | Definition | Lock Effect |
| --- | --- | --- |
| P0 | Active data leak, destructive behavior, payment/production mutation risk, or core login/tenant break. | Blocks lock and release. |
| P1 | Safety, privacy, money, emergency, minor/guardian, medical, owner-trust, or launch-critical workflow defect. | Blocks lock unless founder explicitly defers with documented risk. |
| P2 | Important workflow gap that can be routed to RF work without blocking the current audit lock if not overclaimed. | May lock if assigned, evidenced, and bounded. |
| P3 | Polish, documentation, minor UX, or future enhancement. | Does not block lock if documented. |

Every finding must include:

- Technical severity.
- Product severity.
- Launch-blocking severity.
- Rationale.
- Severity increase conditions.
- Founder decision status.
- RF or future phase assignment.

If a workflow would become dangerous or materially misleading when publicly represented as complete, classify it as launch P1 even when current implementation severity remains P2.

## Traceability Requirements

Every ATLAS phase and RF phase must trace to the canon before implementation is treated as ready.

Minimum traceability:

1. Product Vision section or founder doctrine reference.
2. Business objective.
3. Customer problem.
4. Success metric.
5. Persona.
6. Lifecycle stage.
7. Ecosystem relationship.
8. Permission rule.
9. Operational workflow.
10. Data or analytics requirement.
11. AI boundary, where applicable.
12. Testable acceptance criterion.
13. Approved ATLAS/RF phase.

Every RF package must begin with founder intent traceability. It should answer why the work exists, which Product Vision sections it supports, what customer problem it solves, and how success will be measured.

When canon conflicts, Codex must stop and request founder decision rather than smoothing the conflict away.

## Audit Deliverables

Each ATLAS package should include, when applicable:

- Phase plan.
- Master report.
- Scenario or workflow library.
- Evidence ledger.
- Route/API coverage matrix.
- Gap report.
- Critical workflow fix plan.
- RF proposal ledger or handoff.
- Gate review.
- Deliverable manifest.
- Output report in `outputs/`.
- Package zip with internal manifest.
- Tests proving the package contract.
- Product Vision / business objective traceability.
- Lifecycle-stage mapping.
- Analytics event requirements.
- AI event or AI non-goal requirements.
- Permission matrix for cross-role actions.
- Domain model references for new first-class objects.
- Cross-feature dependency map.

Generated packages must include the final reviewed versions, not stale pre-review artifacts.

## Founder Approval Workflow

Founder approval is required for:

- ATLAS phase lock.
- RF phase authorization.
- Public launch approval.
- P0/P1 deferral.
- First-class entity changes.
- Ownership, custody, minors, emergency access, medical, money, marketplace, AI authority, analytics scoring, destructive migrations, or production-data operations.

Founder approval must be recorded in a durable artifact such as `outputs/<phase>_founder_approval.json` or an equivalent founder decision ledger.

Founder lock approval does not imply public launch approval unless the approval artifact explicitly says so.

## Engineering Approval Workflow

Engineering approval requires:

- Scope boundaries and non-goals recorded.
- Relevant source files reviewed.
- Behavior changes limited to the approved phase.
- No production data mutation unless explicitly authorized.
- Tests updated for new behavior or evidence contracts.
- Generated docs and package rebuilt after changes.
- Secret patterns excluded from reports and packages.
- Diff hygiene reviewed before lock.

Engineering may mark remediation complete, but cannot substitute for founder lock when founder lock is required.

## QA Requirements

QA must record the focused verification path for every ATLAS lock.

Minimum QA:

- Focused phase tests.
- Carry-forward tests for predecessor gates when relevant.
- Package integrity check.
- Stale wording or contradictory status scan.
- Evidence ledger completeness check.
- Route/API coverage completeness check.
- Secret-shape scan for generated reports.
- Confirmation that public launch remains unapproved unless explicitly authorized.

For behavior-changing RF phases, QA must also include happy path, denial path, exception path, degraded path, recovery path, notification state, audit evidence, mobile behavior, duplicate prevention, conflict handling, and visibility boundaries.

## Release-Readiness Criteria

ATLAS lock is not release readiness.

Release readiness requires:

- All launch-blocking P0/P1 findings cleared or founder-deferred in a release-specific gate.
- UAT evidence for every launch-critical role.
- Permission and data-boundary proof.
- Billing/payment truth proof when money is involved.
- Notification/delivery truth proof when communication is involved.
- Mobile and degraded-state claims matching actual implementation.
- No visible feature shell represented as complete workflow.
- Founder release approval recorded separately from ATLAS lock.

## Future ATLAS Application Rule

ATLAS3, ATLAS4, ATLAS5, ATLAS6, ATLAS7, ATLAS8, ATLAS9, and any future ATLAS phases must use this governance standard unless the founder explicitly revises it.

Codex must not reinvent the ATLAS process for each phase. It should reuse this document, cite deviations, and preserve the same evidence discipline created during ATLAS2.
