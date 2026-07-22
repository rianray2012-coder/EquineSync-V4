# Pilot A Mode B Attempt 04 Founder Disposition Package

`FINAL_FOUNDER_DISPOSITION_RECORDED`

## Controlling disposition

`PILOT_A_CONFIGURATION_IDENTIFIED_EXECUTION_VALIDATED_ACCEPTED_FOR_RECORDED_SYNTHETIC_SCOPE_WITH_DISCLOSED_LIMITATIONS`

This package records the four express Founder responses for Pilot A Mode B Attempt 04. Finality is limited to `FD-PH1-A04-001` through `FD-PH1-A04-004`.

## Preserved evidence anchors

- Attempt 03: `34c427c0196d3f8273ac3ea88ad05a2bbe5a2c29`
- Attempt 04: `ebd6a1ed18a2231b450e7bbfb58035198bfcb93c`
- Attempt 04 parent: exact Attempt 03 commit
- Disposition starting commit: `05eaa53be3e5e6aa00814eaeee49f145b3bc6c49`
- Disposition branch: `codex/founder-review-phase1-pilot-a-mode-b-attempt-04-founder-disposition-v1`

## Express Founder decisions

| Decision | Response | Qualification or effect |
| --- | --- | --- |
| `FD-PH1-A04-001` | `ACCEPT_AS_VALIDATED_FOR_RECORDED_SYNTHETIC_SCOPE` | Bounded Phase 1 Pilot acceptance only |
| `FD-PH1-A04-002` | `RETAIN_AS_DISCLOSED_LIMITATIONS` | Six severity variances remain explicit qualifications |
| `FD-PH1-A04-003` | `REQUIRE_NEW_VERSION_SCHEMA_CORRECTION` | `NEW_VERSION_ONLY_DO_NOT_CHANGE_ATTEMPT_04` |
| `FD-PH1-A04-004` | `RETAIN_PHASE_2_NOT_AUTHORIZED` | `REQUIRES_SEPARATE_WRITTEN_AUTHORIZATION_PHASE_2_REMAINS_NOT_AUTHORIZED` |

## Package contents

| File | Purpose |
| --- | --- |
| `README.md` | Package index, final status, and boundaries |
| `FOUNDER_DECISION_BRIEF.md` | Source-faithful questions, evidence, options, recommendations, and recorded answers |
| `FOUNDER_DECISION_RECORD.md` | Controlling decision record and disposition classifications |
| `ATTEMPT_04_FOUNDER_DECISION_REGISTER.csv` | Machine-readable four-row Founder decision register |
| `ATTEMPT_04_EVIDENCE_LINKAGE.md` | Commit, decision, variance, manifest, and role-output traceability |
| `ATTEMPT_04_AUTHORIZATION_BOUNDARIES.md` | Continuing prohibitions and downstream gates |
| `EVIDENCE_MATERIALIZATION_RECORD.md` | Bounded object-retrieval and repository-state record |
| `PACKAGE_SOURCE_AND_CHECKSUM_VERIFICATION_REPORT.md` | Deterministic source, structure, response, and boundary validation |
| `ATTEMPT_04_FOUNDER_DISPOSITION_MANIFEST.csv` | Size and SHA-256 manifest for the eight content artifacts |
| `SHA256SUMS.txt` | SHA-256 ledger for the eight content artifacts plus the manifest |

The manifest excludes itself and `SHA256SUMS.txt` to prevent recursive hashing. `SHA256SUMS.txt` covers the manifest and all eight content artifacts and excludes only itself.

## Continuing statuses

- Future schema: `NEW_VERSION_SCHEMA_CORRECTION_REQUIRED_SEPARATE_AUTHORIZATION`
- Phase 2: `PHASE_2_NOT_AUTHORIZED_REQUIRES_SEPARATE_EXPRESS_WRITTEN_FOUNDER_DIRECTIVE`
- Automatic continuation: `NOT_AUTHORIZED`

## Scope boundary

This package does not approve or adopt the synthetic candidate as production governance; ratify any PIA, canon, policy, architecture, schema, or implementation; establish independent review; qualify the runtime for a fresh review; authorize a new review, rerun, role execution, provider/model call, schema work, Phase 2, implementation, migration, deployment, activation, release, enrollment, or production activity.

No work may continue from this package without a new express Founder directive.
