# CGP-002 Repository Integration Receipt

**Prompt ID:** `CGP-002`
**Execution ID:** `CGEXEC-20260726-0001`
**Package ID:** `ES-CGP-002-FOUNDATION-2026-07-26`
**Program:** EquineSync Code Implementation Guide Program
**Repository:** `rianray2012-coder/EquineSync-V4`
**Default branch:** `integrate-emergent-final-zip`

## Pull Request And Merge

| Field | Value |
|---|---|
| Foundation pull request | `#9` |
| Approved branch | `codex/code-guide-program-foundation-cgp-002-v1` |
| Approved head | `39328f98cd78376be2c1dff30f59d1b79e3144b7` |
| Merge method | GitHub pull-request merge commit |
| Foundation merge commit | `87f9564e9b9eefb498916c619e90f515ba595fe5` |
| Receipt pull request | `#10` |
| Receipt commit | `49a5c2ab0e47d73c331b4ab689023705e6ad8a75` |
| Receipt merge commit | `f09a7627addf438c5c8ae31f0ff215dcf6a3da66` |
| Metadata finalization pull request | `PENDING_METADATA_PR` |
| Metadata commit | `PENDING_METADATA_COMMIT` |
| Final default-branch head | `f09a7627addf438c5c8ae31f0ff215dcf6a3da66` |

## Manifest And Checksum Reconciliation

The required pre-merge reconciliation was completed in:

`governance/implementation/code-guides/reviews/CGP_002_MANIFEST_CHECKSUM_RECONCILIATION.md`

Reconciled package counts:

- Artifact manifest count: `133`
- Checksum ledger count: `138`
- Net difference: `5`

The count difference is intentional. Six preexisting CGP-001 custody files are included in checksum custody but excluded from the CGP-002 created-artifact manifest, while `packages/CGP_002_SHA256SUMS.txt` is included in the manifest and intentionally excluded from self-hashing.

No CGP-002-created or materially strengthened artifact remains outside the artifact manifest.

## Validator-To-Test Coverage

The required validator coverage review was completed in:

`governance/implementation/code-guides/reviews/CGP_002_VALIDATOR_TEST_COVERAGE.md`

All fourteen validators have deliberate coverage through applicable fixtures, negative cases, implementation smoke tests, or documented authority-boundary limitations for current `NOT_YET_APPLICABLE` states.

## Final Validation Counts

The accepted and reverified portfolio validation counts are:

| Status | Count |
|---|---:|
| `PASS` | `4` |
| `NOT_YET_APPLICABLE` | `10` |
| `FAIL` | `0` |
| `BLOCKED` | `0` |

`NOT_YET_APPLICABLE` remains distinct from `PASS`.

## Remote Path Verification

The remote default branch contains the approved CGP-002 artifacts under:

`governance/implementation/code-guides/`

Remote path verification is completed by the foundation merge and will be rechecked after receipt and metadata finalization merges.

## Tracker Updates

The program tracker and prompt execution log record:

- `CGP-002` as `ACCEPTED`;
- CGP-002 as repository-integrated / repository-accessioned;
- `CGP-003` as `NOT_ISSUED`.

## Retained Gaps

The following remain reserved for later prompts:

- substantive guide controls;
- substantive guide invariants;
- guide-specific mandatory question answers;
- implementation profiles;
- atlas-to-guide mappings;
- control-to-repository mappings;
- guide review findings;
- guide adoption;
- activation of any guide as an implementation, merge, release, or production control.

## Actions Not Taken

CGP-003 was not begun. No substantive Code Guide controls, domain policies, implementation profiles, application-code changes, PIA amendments, atlas amendments, production CI gates, deployment actions, pilot actions, or activation authority were created or exercised.

## Disposition

`CGP-002_REPOSITORY_INTEGRATION_RECEIPT_METADATA_FINALIZATION_IN_PROGRESS`
