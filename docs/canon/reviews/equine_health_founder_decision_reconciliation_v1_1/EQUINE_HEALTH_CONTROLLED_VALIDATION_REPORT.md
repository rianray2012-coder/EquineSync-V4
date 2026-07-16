# Equine Health Controlled Validation Report

## Disposition

`EQUINE_HEALTH_RECONCILIATION_COMPLETE_READY_FOR_FOUNDER_ADOPTION_REVIEW_WITH_NONBLOCKING_P2`

| Validation | Result |
| --- | --- |
| Source preservation | Passed at `81d1d33d45093b89718e877330739c3601ed86ffe9ce6c476a679caab289e4d3` |
| V1.0 predecessor preservation | Passed at `f68d65873599237a65006ea6ce614b427a16e259db132f36c9116b6dec90abfa` |
| Founder responses | 14/14 `FOUNDER_APPROVED_EXACTLY` |
| Decision-to-section mapping | 14/14 |
| Decision-to-requirement mapping | 14/14 |
| Preliminary requirement mapping | 35/35 |
| Cross-canon review | No P0/P1 conflict identified |
| Safeguarding alignment | Passed; separate lifecycle preserved |
| AI V2.0/RF30 alignment | Passed; default-off and non-authoritative |
| Candidate version | V1.1; no collision found |
| P0/P1/P2 | 0 / 0 / 6 |
| Formal machine scans | Blocked; not represented as passed |
| Authority overclaim | None identified |

## Validation Commands

The reconciliation used the following repository-context checks:

```text
shasum -a 256 <uploaded-source> <preserved-source> <candidate>
python3 <inline source, decision, exact-language, crosswalk, JSON, and authority-boundary validator>
rg <secret-patterns> <reconciliation-artifacts> <candidate>
python3 <inline repository-relative reference validator>
git diff --check
unzip -t outputs/equine_health_v1_1_founder_review_evidence.zip
sha256sum -c docs/canon/reviews/equine_health_founder_decision_reconciliation_v1_1/SHA256SUMS
```

The decision-to-requirement crosswalk records only requirements materially affected by each founder decision. The separate requirement-to-section traceability report accounts for all 35 preliminary requirements; unrelated requirements were not falsely assigned to founder decisions.

Package extraction, manifest verification, secret scanning, authority-boundary checks, and diff hygiene are recorded in the final evidence record. Formal repository-wide machine dependency, duplicate, cycle, and orphan scans remain P2 and are not represented as passed.
