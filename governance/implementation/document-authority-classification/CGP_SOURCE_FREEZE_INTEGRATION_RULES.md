# CGP Source-Freeze Integration Rules

Package ID: `ES-DOC-AUTH-CLASSIFICATION-V1.0.0`
Version: `1.0.0`

## Purpose

These rules define how document-authority classification integrates with CGP-005 and CGP-006.

## CGP-005 Record Requirements

For every selected or governing source, CGP-005 or a CGP-005 appendix must record:

| Field |
| --- |
| `artifact_path` |
| `artifact_name` |
| `classification` |
| `authority_effect` |
| `controlling_status` |
| `lifecycle_status` |
| `source_hash` |
| `version` |
| `approval_status` |
| `adoption_status` |
| `selection_type` |
| `selection_basis` |
| `affected_code_guides` |

Allowed selection types are:

- `NORMATIVE_SELECTED_SOURCE`
- `GOVERNING_CONSTRAINT`
- `SUPPORTING_EVIDENCE`

## CGP-005 Appendix Rule

Use a CGP-005 appendix when all of the following are true:

1. The original frozen normative source bytes remain unchanged.
2. A later governance decision adds a binding constraint.
3. The constraint can be added without replacing the original source set.
4. The appendix records the new governing constraint, source hash, approval status, authority effect, and affected Code Guides.

An appendix must not be used to avoid an amendment when the original source freeze became inaccurate.

## CGP-005 Amendment Rule

Use a CGP-005 amendment when any of the following are true:

- a frozen normative source changed;
- a relied-upon source hash changed;
- source-set membership materially changed;
- controlling status changed;
- a different artifact became controlling;
- the original freeze determination is no longer accurate.

## CGP-006 Drift Review

Before CGP-006 begins or resumes work:

1. Record the authorized drafting baseline.
2. Record current repository HEAD.
3. Compare the two commits.
4. Identify added, changed, deleted, renamed, or relocated files.
5. Resolve each file against the document-authority classification register.
6. Confirm byte identity where relocation or exact-copy treatment is claimed.
7. Determine whether authority, approval, adoption, supersession, controlling status, source-set membership, or source hash changed.
8. Apply `CODE_GUIDE_FREEZE_IMPACT_MATRIX.csv`.
9. Produce a machine-readable repository change-impact receipt.
10. Proceed only if the receipt expressly permits drafting.

## Treatment Rules

| Input result | Required treatment |
| --- | --- |
| Normative change | Stop affected drafting; apply CGP-005 amendment or equivalent source-freeze review. |
| Governance with normative effect | Add as a governing constraint, refresh affected guide inputs, and append or amend CGP-005 where required. |
| Governance only | Perform impact review and document no-effect or required refresh. |
| Custody only | Verify custody consistency and proceed if no underlying authority changed. |
| Historical only | Record and proceed unless authority ambiguity is introduced. |
| Unclassified | Fail closed. |

## Current CGP-005 Determination

Existing CGP-005 records a Founder-accepted two-layer source-freeze model:

- `2511` reference corpus records classified as non-normative reference evidence;
- `139` curated normative crosswalk rows;
- `8714` reference-only exclusion rows;
- Wave 1 guides `ES-CG-00`, `ES-CG-01`, `ES-CG-13`, and `ES-CG-10` marked `SOURCE_FROZEN` for drafting prerequisites only.

No evidence reviewed in this package shows that a frozen normative source byte changed, a selected source hash changed, or original CGP-005 source-set membership became inaccurate.

Therefore the current package does not require a CGP-005 amendment.

## Current PR #23 Determination

PR `#23` merged the `ES-TA-FD-001` through `ES-TA-FD-008` Founder-decision package. The package does not modify Code Guide files or CGP-005 registers, and CGP-006 previously recorded it as non-conflicting context.

This framework classifies the operative Founder decisions as `GOVERNANCE_AUTHORITY` with `GOVERNANCE_WITH_NORMATIVE_EFFECT` because they impose pilot gates, acceptance criteria, authorization constraints, storage failure behavior, durable notification behavior, background-job leadership requirements, offline/replay boundaries, provider-neutral legal e-signature constraints, DocuSign readiness requirements, and controlled pilot-channel limits.

Because the original frozen CGP-005 normative sources remain unchanged but later Founder decisions add binding constraints affecting candidate drafting, PR #23 requires a CGP-005 appendix as `GOVERNING_CONSTRAINT` material before affected Wave 1 candidate drafting proceeds.

## Current CGP-006 Determination

CGP-006 may not proceed unchanged. It may proceed after:

1. this classification package validates;
2. PR #23 governing constraints are represented in a CGP-005 appendix or equivalent Founder-authorized governing-constraint record;
3. CGP-006 input records are refreshed to cite the appendix and preserve the non-adoption, non-activation, and no-implementation boundaries.

Until then, affected candidate drafting for `ES-CG-00`, `ES-CG-01`, `ES-CG-13`, and `ES-CG-10` remains stopped.

## Current Item 05 Determination

Item 05 default-branch work is exact-byte/canonical-path custody integration with retained lifecycle findings. It does not change approved source bytes, approval status, controlling status, or source-set membership. It therefore requires custody refresh only, not a CGP-005 amendment. It can be referenced as custody and PIA lineage evidence, while its retained source-binding findings must remain visible for later implementation-freeze work.
