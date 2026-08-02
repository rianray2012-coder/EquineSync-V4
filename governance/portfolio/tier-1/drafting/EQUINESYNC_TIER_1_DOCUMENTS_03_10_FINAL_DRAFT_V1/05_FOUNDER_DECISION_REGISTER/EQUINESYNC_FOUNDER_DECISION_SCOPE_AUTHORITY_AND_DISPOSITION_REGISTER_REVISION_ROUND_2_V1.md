# Document 05 - Founder Decision Scope Authority And Disposition

Readiness determination: `REVISION_ROUND_2_COMPLETE_READY_FOR_FOUNDER_DIRECTIONAL_AND_FINAL_DOCUMENTARY_REVIEW`.

Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

This artifact incorporates `SHARED_TIER_1_DOCUMENTARY_STANDARD_REVISION_ROUND_2_V1.md` by exact reference. If this document and the shared standard conflict, the stricter non-authorizing, evidence-preserving, source-authenticating interpretation controls until Founder direction resolves the conflict.

## Decision Scope Rule

Decision existence, decision evidence, decision scope, and authority effect are separate fields. A Founder decision that modifies a proposal must preserve modification text.

## Concrete Record-Level Example

`FD-T1R2-002` records accountable-role appointment as requiring Founder authority. It does not invent a named owner and does not infer acceptance from package preparation.

<!-- ROUND_3_PART_B_STRUCTURED_CONTENT_BEGIN -->

## Identification

- Document directory: `05_FOUNDER_DECISION_REGISTER`
- Principal narrative file: `EQUINESYNC_FOUNDER_DECISION_SCOPE_AUTHORITY_AND_DISPOSITION_REGISTER_REVISION_ROUND_2_V1.md`
- Revision: `REVISION_ROUND_2_V1` as amended by Round 3 Part A and Round 3 Part B
- Preparer: documentary review preparer; no independent reviewer assigned

## Purpose

Present the questions that exceed the authority of a documentary package, and record the disposition of each, if any.

## Scope

Five decisions, FD-T1R2-001 to FD-T1R2-005, recorded identically in `FOUNDER_DECISION_DISPOSITION_REGISTER.csv` and in the package-root `FOUNDER_DECISION_PACKET.csv` and `FOUNDER_DECISION_PACKET.md`.

## Exclusions

No decision is recorded. `selected_disposition` is the null literal `NO_DISPOSITION_SELECTED` on all five rows, `exact_decision_text` is `NO_FOUNDER_DECISION_RECORDED_IN_THIS_PACKAGE`, and `authority_granted` is `NONE_BY_THIS_PACKAGE`.

## Method

Each `question_presented` string is written byte-identically into the disposition register, the packet CSV and the packet Markdown by a single transform, so the three artifacts cannot drift apart. Where Revision Round 2 wording differed between artifacts, the narrower wording is canonical and the wider variant is retained in a `round_2_..._retained` column.

## Contents Inventory

| File | Shape | SHA-256 |
|---|---|---|
| `CHECKSUMS.sha256` | 573 bytes | `a0e18c072eee0df3ff09845cff76c2c94c7b437b4c9f26e90ea7a43235aa3d42` |
| `EQUINESYNC_FOUNDER_DECISION_SCOPE_AUTHORITY_AND_DISPOSITION_REGISTER_REVISION_ROUND_2_V1_REVISION_ROUND_2_CRITICAL_REVIEW_REPORT.md` | 1949 bytes | `c2120a15bf6e477b89543c2bf1358548e4dad53493b19cdc828ed5cb9b5f643b` |
| `FOUNDER_DECISION_DISPOSITION_REGISTER.csv` | 5 rows x 27 columns | `2e41cf76ba093c2c69ee7090bafab45dd46a93af968fd23bd6664868569805e8` |
| `FOUNDER_DECISION_DISPOSITION_REGISTER.json` | 8969 bytes | `3f59b313b8520344442fca203e151f8977e26ba0bf652d64d7dbca01abddb0ac` |
| `PACKAGE_MANIFEST.json` | 936 bytes | `8dc127b45291915d4d147d364a4808453c913765ad6b906b15fc41a5a424f55f` |

`EQUINESYNC_FOUNDER_DECISION_SCOPE_AUTHORITY_AND_DISPOSITION_REGISTER_REVISION_ROUND_2_V1.md` is excluded from its own inventory: a file cannot record its own hash. It is covered by `PACKAGE_MANIFEST.json`.

This inventory is generated from the directory contents by `VALIDATION/apply_round3_partb3.py`. If a file is added, removed or edited without regenerating, the recorded SHA-256 will not match and `VALIDATION/validate_tier1_documents_03_10_rr2.py` will report a manifest failure.

## Known Limitations

Recording that no decision has been made is the whole of what this document does. It does not advise, and `recommended_option` is `NO_RECOMMENDATION_MADE_BY_THIS_PACKAGE` for all five decisions.

## Status

`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`

<!-- ROUND_3_PART_B_STRUCTURED_CONTENT_END -->
