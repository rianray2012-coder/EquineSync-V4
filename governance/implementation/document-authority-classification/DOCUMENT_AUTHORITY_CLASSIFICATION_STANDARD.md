# EquineSync Document Authority Classification Standard

Package ID: `ES-DOC-AUTH-CLASSIFICATION-V1.0.0`
Version: `1.0.0`
Created: `2026-07-27`
Repository: `rianray2012-coder/EquineSync-V4`
Default branch reviewed: `integrate-emergent-final-zip`
Reviewed head: `4afe3ccd84d9f8be1bc5c79bb27068676d993a70`

## Purpose

This standard defines how EquineSync documentary artifacts are classified for authority, custody, and Code Guide impact control.

It exists so a reviewer, Codex process, or later automation can determine consistently whether a repository change has no Code Guide effect, requires custody verification only, requires governance-impact review, requires a CGP-006 input refresh, requires a CGP-005 appendix, requires a CGP-005 source-freeze amendment, requires affected drafting or implementation to stop, or creates an unresolved authority conflict.

## Scope

This standard applies to documentary artifacts used by EquineSync governance, PIA integration, technical-audit disposition, Code Guide source-freeze control, repository custody, and implementation authorization.

It does not authorize runtime implementation, application-code changes, schema changes, database migrations, infrastructure changes, CI changes, deployment changes, production configuration, pilot activation, enrollment, release, production use, provider activation, payment processing, or native-app publication.

## Authority Model

Every artifact must be classified at the file level when it is used to make an authority, implementation, source-freeze, or custody determination. Package-level classification is permitted only as a summary of reviewed component files.

The authority classes are:

| Class | Meaning | Default treatment |
| --- | --- | --- |
| `NORMATIVE_AUTHORITY` | Directly establishes required product behavior, system behavior, implementation requirements, system boundaries, acceptance conditions, or binding technical constraints. | A substantive change stops affected drafting or implementation until source-freeze treatment and validation pass. |
| `GOVERNANCE_AUTHORITY` | Controls or influences approval, adoption, scope, sequencing, risk treatment, pilot posture, release posture, implementation authorization, deferral, escalation, supersession, review disposition, or interpretation of another source. | Perform governance-impact review and determine whether the artifact has normative effect. |
| `CUSTODY_EVIDENCE` | Proves provenance, exact-byte preservation, repository placement, package completeness, source accession, checksum consistency, branch custody, PR custody, or validation. | Verify consistency and proceed only if no underlying authority changed. |
| `HISTORICAL_REFERENCE` | Preserves predecessor, superseded, archived, or non-controlling material. | Keep lineage visible and proceed unless ambiguity or duplicate authority is introduced. |
| `UNCLASSIFIED` | Authority, lifecycle, or effect is unresolved. | Treat as high impact and stop affected drafting or implementation. |

## Required Separate Fields

The following concepts must not be collapsed:

| Field | Meaning |
| --- | --- |
| Artifact classification | The artifact's documentary authority class. |
| Artifact approval status | Whether the artifact is Founder-approved, program-approved, review-approved, not approved, not applicable, or unknown. |
| Artifact controlling status | Whether the artifact is controlling, co-controlling, supporting, historical, superseded, non-controlling, or unknown. |
| Artifact lifecycle status | Whether the artifact is draft, candidate, approved, adopted, integrated, superseded, archived, retired, or unknown. |
| Artifact source-freeze membership | Whether the artifact is selected by CGP-005 as a normative selected source, governing constraint, supporting evidence, not selected, or unknown. |
| Artifact implementation effect | Whether the artifact directly changes product behavior, constrains implementation, only controls process, only proves custody, or remains undetermined. |

Approval does not equal controlling status. Controlling status does not equal source-freeze membership. Source-freeze membership does not equal implementation authorization.

## Classification Criteria

Classify an artifact as `NORMATIVE_AUTHORITY` when it directly defines any mandatory behavior, acceptance criterion, interface contract, schema, workflow, authorization rule, privacy requirement, security requirement, safeguarding requirement, implementation-control requirement, or system boundary.

Classify an artifact as `GOVERNANCE_AUTHORITY` when it controls approval, adoption, sequencing, risk disposition, release posture, implementation authorization, deferral, supersession, interpretation, or pilot posture. Then classify its authority effect as either `GOVERNANCE_ONLY` or `GOVERNANCE_WITH_NORMATIVE_EFFECT`.

Classify a governance artifact as `GOVERNANCE_WITH_NORMATIVE_EFFECT` when it creates a mandatory implementation requirement, prohibits an implementation behavior, changes interpretation of a normative source, changes which artifact is controlling, changes approval or supersession state, creates a binding implementation boundary, changes acceptance criteria, or creates a pilot, release, deployment, provider, or channel constraint that affects design or code.

Classify an artifact as `CUSTODY_EVIDENCE` when it only proves bytes, hashes, manifests, package composition, repository placement, branch custody, PR custody, validation, or historical continuity.

Classify an artifact as `HISTORICAL_REFERENCE` when it preserves superseded, predecessor, or archived material and does not itself control current behavior.

Classify an artifact as `UNCLASSIFIED` when the evidence is incomplete, contradictory, disputed, or insufficient to determine authority effect.

## Precedence

When multiple classifications could apply, use this precedence:

1. `NORMATIVE_AUTHORITY`
2. `GOVERNANCE_AUTHORITY` with `GOVERNANCE_WITH_NORMATIVE_EFFECT`
3. `GOVERNANCE_AUTHORITY` with `GOVERNANCE_ONLY`
4. `CUSTODY_EVIDENCE`
5. `HISTORICAL_REFERENCE`
6. `UNCLASSIFIED`

Ambiguity must not be resolved by assigning the least restrictive classification. An uncertain artifact receives the highest reasonably applicable impact treatment until its authority, status, and effect are expressly determined.

## Evidence Requirements

A classification record must cite enough evidence for an independent reviewer to reproduce the classification. Acceptable evidence includes:

- exact repository path;
- package ID;
- source hash;
- package hash;
- baseline commit;
- last reviewed commit;
- approval record;
- adoption record;
- source-freeze row;
- manifest entry;
- checksum ledger;
- validation report;
- repository integration receipt;
- PR number and merge commit;
- documented non-authorization boundary.

Exact-byte claims require checksum evidence. Path-only claims are insufficient.

## Source-Freeze Impact Rules

Use `FREEZE_AMENDMENT_REQUIRED` when a frozen normative source changed, a relied-upon source hash changed, source-set membership materially changed, controlling status changed, or a different artifact became controlling.

Use `FREEZE_APPENDIX_REQUIRED` when the original frozen source bytes remain unchanged but later governance authority adds a binding constraint that must travel with the affected Code Guide input set as a governing constraint.

Use `CGP_006_INPUT_REFRESH_REQUIRED` when source-freeze bytes remain unchanged but CGP-006 must re-read, re-index, or incorporate current governing context before candidate drafting continues.

Use `CUSTODY_REFRESH_ONLY` when a custody record, manifest, receipt, package ledger, or exact-byte canonical placement changed and no underlying normative or governance authority changed.

Use `NO_EFFECT` only when the reviewed change has no authority, custody, drafting, implementation, or source-freeze effect.

Use `UNDETERMINED` when the required evidence is missing or contradictory. Treat it as a stop condition.

## Identical-Byte Relocation

Moving or copying an identical normative artifact to a canonical path does not automatically create a substantive normative change.

It must trigger verification of byte identity, source hash, controlling status, path references, manifest references, source-freeze references, and duplicate-authority risk.

If exact-byte identity and unchanged authority are confirmed, classify the change as custody refresh or normative custody relocation. If the path itself is a controlling reference, perform impact review before allowing drafting or implementation to continue.

## Historical And Superseded Artifacts

Historical and superseded artifacts must remain visible for lineage and conflict review. They must not be silently treated as current authority, deleted to remove conflict, or rewritten to match current authority. If a historical artifact claims current controlling status, classify the condition as `UNCLASSIFIED_HIGH_IMPACT` until resolved.

## Approval, Adoption, And Controlling Status

Founder approval is strong evidence of approval status. It is not by itself proof that an artifact is currently controlling, adopted, selected in CGP-005, or implementation-authorizing.

Adoption records must identify the adopted artifact, version, source hash or exact package, scope, effective date, supersession effect, and non-authorization boundaries.

Controlling-status records must identify whether the artifact is controlling, co-controlling, supporting, historical, superseded, non-controlling, or unknown.

## Reclassification And Supersession

Reclassification requires a new register record or a revision record that preserves the prior classification, evidence basis, reviewer, commit, date, and reason for change.

Supersession requires a written supersession basis, a superseding artifact identity, scope, effective date, and effect on current source-freeze membership. A superseded artifact must remain traceable as historical evidence.

## Baseline Drift

Before CGP-006 begins or resumes candidate drafting, the authorized drafting baseline and current repository head must be compared. Added, changed, deleted, renamed, and relocated files must be resolved against the classification register and impact matrix.

CGP-006 may not blindly continue against an older repository head after relevant governance or normative inputs merge.

## PIA Relationship

Founder-approved PIAs and their controlling registers can be normative authority when they define product behavior, required workflows, actor boundaries, contracts, acceptance criteria, privacy requirements, safeguarding requirements, or implementation constraints.

PIA historical predecessors are historical references unless they retain a current controlling claim. PIA manifests, package checksums, and repository integration receipts are custody evidence unless they alter source identity, controlling status, approval, adoption, supersession, or source-set membership.

## Technical-Audit Relationship

Technical-audit findings and Founder decisions are not harmless merely because they are documentary. A Founder decision that imposes an implementation requirement, acceptance criterion, pilot gate, provider constraint, release constraint, or mandatory remediation sequence has `GOVERNANCE_WITH_NORMATIVE_EFFECT`.

Technical-audit custody files, source registers, manifests, validation reports, checksum ledgers, and PR receipts remain custody evidence unless they alter the authority of the underlying decisions.

## CGP-005 Relationship

CGP-005 remains the controlling Wave 1 two-layer source-freeze model:

- curated guide-specific normative freezes control candidate drafting inputs;
- reference corpus rows remain non-normative discovery evidence;
- reference-only exclusions remain excluded from normative use.

Later governance authority with normative effect must not be silently promoted into CGP-005 normative selected sources. It must be handled by explicit appendix or amendment treatment.

## CGP-006 Relationship

CGP-006 is issued for bounded Wave 1 candidate drafting only. It cannot begin affected drafting until the document-classification gate passes and any required CGP-005 appendix, CGP-005 amendment, or CGP-006 input refresh is complete and validated.

## Later Implementation Work

No implementation may rely on an unclassified, disputed, or context-only source as if it were controlling implementation authority. Implementation work must use the classified source set, preserve non-authorization boundaries, and stop when a governing constraint or unresolved authority conflict affects the work.
