# CGP-002 Manifest and Checksum Reconciliation

**Prompt ID:** `CGP-002`  
**Execution ID:** `CGEXEC-20260726-0001`  
**Package ID:** `ES-CGP-002-FOUNDATION-2026-07-26`  
**Branch:** `codex/code-guide-program-foundation-cgp-002-v1`

## Reconciliation Summary

The returned CGP-002 package reported:

- Artifact manifest count: `131`
- Checksum ledger count: `136`
- Net count difference: `5`

After adding the two required pre-merge reconciliation review artifacts, the regenerated package reports:

- Artifact manifest count: `133`
- Checksum ledger count: `138`
- Net count difference: `5`

The set comparison confirms both count pairs reflect the same intentional custody-accounting difference, not an omitted CGP-002-created or materially strengthened artifact.

## Set Difference

### Checksum Ledger Entries Not Listed In The CGP-002 Created-Artifact Manifest

The checksum ledger includes the following six preexisting CGP-001 custody files:

| Path | Classification | Treatment |
|---|---|---|
| `receipts/CGP_001_CREATED_ARTIFACT_MANIFEST.json` | Preexisting CGP-001 scaffold custody file | Included in checksum ledger for whole-directory custody; intentionally excluded from CGP-002 created-artifact manifest. |
| `receipts/CGP_001_PROGRAM_INITIALIZATION_RECEIPT.md` | Preexisting CGP-001 scaffold custody file | Included in checksum ledger for whole-directory custody; intentionally excluded from CGP-002 created-artifact manifest. |
| `receipts/CGP_001_REPOSITORY_INTEGRATION_RECEIPT.md` | Preexisting CGP-001 repository-integration custody file | Included in checksum ledger for whole-directory custody; intentionally excluded from CGP-002 created-artifact manifest. |
| `receipts/CGP_001_SESSION_RECEIPT.md` | Preexisting CGP-001 scaffold custody file | Included in checksum ledger for whole-directory custody; intentionally excluded from CGP-002 created-artifact manifest. |
| `receipts/CGP_001_SHA256SUMS.txt` | Preexisting CGP-001 checksum ledger | Included in checksum ledger for whole-directory custody; intentionally excluded from CGP-002 created-artifact manifest. |
| `receipts/CGP_001_VALIDATION_REPORT.md` | Preexisting CGP-001 validation custody file | Included in checksum ledger for whole-directory custody; intentionally excluded from CGP-002 created-artifact manifest. |

### Manifest Entry Not Listed In The Checksum Ledger

The artifact manifest includes one CGP-002 custody file that is intentionally excluded from its own checksum ledger:

| Path | Classification | Treatment |
|---|---|---|
| `packages/CGP_002_SHA256SUMS.txt` | CGP-002 checksum ledger | Included in the created-artifact manifest; excluded from checksum hashing to avoid self-referential checksum instability. |

## Count Explanation

The ledger has six additional CGP-001 custody entries and omits one self-referential checksum-ledger entry. This produces the accepted net difference in both the returned package and the regenerated reconciliation package:

`136 checksum-ledger entries - 131 manifest entries = 5 net entries`

`138 checksum-ledger entries - 133 manifest entries = 5 net entries`

## Omission Review

No CGP-002-created or materially strengthened artifact was found outside the artifact manifest.

The omitted checksum-ledger entries are preexisting CGP-001 custody files. They are not CGP-002-created artifacts and are retained in the checksum ledger to preserve directory-level custody continuity.

## Disposition

`RECONCILED_NO_CGP_002_ARTIFACT_OMISSION`
