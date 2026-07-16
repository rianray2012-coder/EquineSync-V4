# Financial Truth V2.1 Deliverable Manifest

**Package state:** `ADOPTED_AND_LOCKED`  
**Generated:** `2026-07-13T18:44:51Z`  
**Source commit:** `9f812280542f6e9c43935563badec2de1448947b`  
**Working-tree classification:** Reviewed governance-only overlay  
**Immutable canon SHA-256:** `0a5302bba0240ba6acd9871b7453916ff212f91ce2f1622b9a4e236701f52604`  
**Checksum ledger:** `SHA256SUMS.txt`  
**Checksum ledger SHA-256:** `4293a928480312ef14c694521d1d0a0d5366d0e817ae7b826d9179610fdf732e`

## Controlling and preserved artifacts

- `docs/canon/MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1.md`
- `docs/canon/history/MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1_FOUNDER_APPROVED_SOURCE.md`
- `docs/canon/history/MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_0_CANDIDATE.md`

## Decision and review evidence

- Founder adoption and lock directive
- Founder approval JSON record
- Adoption report
- Lock report
- V2.0-to-V2.1 delta matrix
- Preservation matrix
- Findings register
- Non-implementation and non-production attestation
- Executable lock validator

## Governance updates

- Canon Index and historical provenance exception ledger
- Artifact, dependency, lock, state, ownership, findings and authorization registries
- Implementation Atlas traceability and current program board
- RF32 dependency record
- Future Payments and Financial Rails dependency record
- Accounting-integration dependency record

## Integrity and authority

The checksum ledger contains 26 path-bound records. The package must be verified from the repository root with:

```bash
shasum -a 256 -c docs/canon/reviews/financial_truth_v2_1/SHA256SUMS.txt
python3 docs/canon/reviews/financial_truth_v2_1/validate_financial_truth_v2_1_lock.py
```

The package creates constitutional authority only. Runtime, schema/migration, provider, payment, accounting-write, collections, production and launch authority remain `FALSE`.

`FINANCIAL_TRUTH_AND_RESPONSIBILITY_V2_1_ADOPTED_AND_LOCKED`
