# External Architecture V2.0 Founder Decision and Correction Report

## Founder decision

- Decision: `ACCEPT_WITH_MODIFICATION`
- Decision date: `2026-07-12`
- Constitutional direction approved: `true`
- Controlled canon adoption completed: `false`
- Canon lock completed: `false`
- Implementation or production authority: `false`

## Correction trace

| Finding | Founder direction | Correction | Evidence | State |
| --- | --- | --- | --- | --- |
| `F_EXTERNAL_ADAPTERS-P1-01` | Named providers must be illustrative candidates only and confer no approval, endorsement, preference, mandate, or authority. | Added a controlling provider-candidate disclaimer; replaced “first,” “preferred,” “approved,” and mandatory vendor language; made RF/provider direction separately gated. | Corrected candidate SHA-256 `7d35dca4762c247cae23212fa1844ea1ed94ad6731090b588b2fd1a2670d5d72` | Closed |
| `F_EXTERNAL_ADAPTERS-P1-02` | Remove unverifiable Version 1 preservation assertions. | Replaced complete-review/preservation claims with an evidence-qualified statement and Historical Provenance Exception Ledger requirement. | Original reviewed source preserved at SHA-256 `65d2d706c367d92f1452dc64f945cc39984ea03f58d3ca567b4b3dad875dbe3a` | Closed |

## P2 disposition

`F_EXTERNAL_ADAPTERS-P2-01` remains open and nonblocking. Vendor selection, environment separation, secret ownership, processor contracts, and adapter activation remain future founder and implementation decisions. It does not delay controlled adoption review after the P1 corrections.

## Current findings

- P0: `0`
- Open P1: `0`
- Open P2: `1`

## Provenance

The source reviewed by the founder is preserved unchanged at `docs/canon/history/MASTER_EXTERNAL_ARCHITECTURE_AND_ADAPTER_MODEL_V2_0_REVIEWED_SOURCE.md`. The corrected candidate remains at `docs/canon/candidates/MASTER_EXTERNAL_ARCHITECTURE_AND_ADAPTER_MODEL_V2_0.md`. This is a correction lineage, not a rewrite of historical evidence.

## Stop state

The model may proceed to the separately governed controlled adoption review. It is not adopted, active, or locked. No provider or implementation authority exists.

`EXTERNAL_ARCHITECTURE_V2_0_CORRECTIONS_COMPLETE_READY_FOR_CONTROLLED_ADOPTION_REVIEW`
