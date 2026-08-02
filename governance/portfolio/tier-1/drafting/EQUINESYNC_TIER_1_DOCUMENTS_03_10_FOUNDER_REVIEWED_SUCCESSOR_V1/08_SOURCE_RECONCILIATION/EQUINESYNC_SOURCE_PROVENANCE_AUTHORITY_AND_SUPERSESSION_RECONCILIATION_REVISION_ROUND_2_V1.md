# Document 08 - Source Provenance Authority And Supersession Reconciliation

Readiness determination: `REVISION_ROUND_2_COMPLETE_READY_FOR_FOUNDER_DIRECTIONAL_AND_FINAL_DOCUMENTARY_REVIEW`.

Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

This artifact incorporates `SHARED_TIER_1_DOCUMENTARY_STANDARD_REVISION_ROUND_2_V1.md` by exact reference. If this document and the shared standard conflict, the stricter non-authorizing, evidence-preserving, source-authenticating interpretation controls until Founder direction resolves the conflict.

## Source Disposition Rule

Source scale is converted into disposition fields: authoritative current source, historical retained source, candidate source, duplicate, counterpart, derivative, obsolete copy, superseded source, unresolved identity collision, missing source, broken reference, orphan source, branch-only evidence, and Founder-disposition-required source.

## Concrete Record-Level Example

Each `SRC-RR2-*` row records hash, byte length, repository path, authority state, canonical representation, implementation-use limitation, and whether Founder disposition is required.

<!-- ROUND_3_PART_B_STRUCTURED_CONTENT_BEGIN -->

## Identification

- Document directory: `08_SOURCE_RECONCILIATION`
- Principal narrative file: `EQUINESYNC_SOURCE_PROVENANCE_AUTHORITY_AND_SUPERSESSION_RECONCILIATION_REVISION_ROUND_2_V1.md`
- Revision: `REVISION_ROUND_2_V1` as amended by Round 3 Part A and Round 3 Part B
- Preparer: documentary review preparer; no independent reviewer assigned

## Purpose

Enumerate every source file considered by this programme, record its identity by hash, and record what authority state, duplication state and version state each file is in.

## Scope

2,961 source rows covering 2,884 distinct SHA-256 values, and 68 duplicate clusters holding 145 member rows and 77 redundant copies.

## Exclusions

No canonical representation has been determined for any duplicate cluster, because no canonicality rule has been declared. No supersession relationship has been evidenced. No source is recorded as safe for implementation use.

## Method

`duplicate_cluster_id` is populated by joining `repository_path` to `source_path` in the cluster register. Before the join is written, cluster membership derived from the cluster register is compared for set equality against cluster membership derived independently from SHA-256 equality; the transform aborts if they differ. Every dashboard figure is recomputed from the two registers.

## Contents Inventory

| File | Shape | SHA-256 |
|---|---|---|
| `CHECKSUMS.sha256` | 785 bytes | `2dd7ce62dc99f10d22ed8268c18baf17ac4f8626d243ef7a3c04a4668b566754` |
| `DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv` | 145 rows x 11 columns | `92b1737608be05bfd27cb2a00059f501408ea068c37657a6314817352f964666` |
| `EQUINESYNC_SOURCE_PROVENANCE_AUTHORITY_AND_SUPERSESSION_RECONCILIATION_REVISION_ROUND_2_V1_REVISION_ROUND_2_CRITICAL_REVIEW_REPORT.md` | 1943 bytes | `1896135a1a6785652bcb1b53bc69e20b8d9ae5b1196991779a77f9c839e9f503` |
| `PACKAGE_MANIFEST.json` | 1299 bytes | `b457024a9572390bfd50aa1a0fb4da7ef7f92eb80d835738012930b57aad2efa` |
| `SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv` | 2961 rows x 21 columns | `b8d18226e7d2eff53424457cd5d0e2342e4c33a80e7eacca096930ffbbd74fed` |
| `SOURCE_AUTHORITY_DISPOSITION_REGISTER.json` | 2783382 bytes | `e9d354532490b980ecd6fb18746a362a57ccb449b41947c25b94f2de151f917d` |
| `SOURCE_DISPOSITION_DASHBOARD.csv` | 1 rows x 23 columns | `8860f12e8115c704532db3851c90ef2f5547eda96da535d37a1f35d17937246f` |

`EQUINESYNC_SOURCE_PROVENANCE_AUTHORITY_AND_SUPERSESSION_RECONCILIATION_REVISION_ROUND_2_V1.md` is excluded from its own inventory: a file cannot record its own hash. It is covered by `PACKAGE_MANIFEST.json`.

This inventory is generated from the directory contents by `VALIDATION/apply_round3_partb3.py`. If a file is added, removed or edited without regenerating, the recorded SHA-256 will not match and `VALIDATION/validate_tier1_documents_03_10_rr2.py` will report a manifest failure.

## Known Limitations

`authority_state` values that read in Revision Round 2 as present-tense adoption facts are relabelled as past-tense observations, and every row carries `present_adoption_state=NOT_ADOPTED_BY_THIS_PACKAGE`, but the underlying observation was made from repository contents and was not re-derived from a Founder decision text. 69 rows sit in clusters whose byte-identical members declare different controlling versions; those conflicts are flagged, not resolved.

## Status

`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`

<!-- ROUND_3_PART_B_STRUCTURED_CONTENT_END -->
