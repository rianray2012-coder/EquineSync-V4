# Review Target Authentication Report

## Exact target

| Field | Expected | Observed | Result |
|---|---|---|---|
| Repository | `rianray2012-coder/EquineSync-V4` | `rianray2012-coder/EquineSync-V4` | PASS |
| PR | `#77` | `#77` open draft | PASS |
| PR branch | `codex/governance-portfolio-scope-taxonomy-closure-maintenance-standard-v1` | matches | PASS |
| Exact PR head | `95672eac54ae1be715e8c612c712506661e1df03` | `95672eac54ae1be715e8c612c712506661e1df03` | PASS |
| Original base | `0863d3f58a1e3eaffbfd0c9778272c207d43c471` | matches PR metadata | PASS |
| Protected branch | `integrate-emergent-final-zip` | matches | PASS |
| Protected head | `1eb384d80daa700ba2e71ee42872cc9bba926332` | matches live `origin/integrate-emergent-final-zip` | PASS |
| Package path | `.../EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0/` | present at head | PASS |
| Package file count | 25 | 25 | PASS |

## Kit authentication

| Artifact | Expected SHA-256 | Observed | Result |
|---|---|---|---|
| `EquineSync_PR77_Independent_Structured_Review_Kit_V1_0.zip` | `9060a4dd082ffd78ba9784a1c47b83483d84e7b67170d88cc6fbc132f5a30971` | match | PASS |

## Key package hashes at exact head

| Artifact | Expected SHA-256 | Bytes | Observed | Result |
|---|---|---|---|---|
| Standard Markdown | `1007b8c119e0956719f422248e01d40ff5e0cfc8e88de3b9a7bec019f549d0ea` | 41484 | match | PASS |
| Machine-readable JSON | `b22592d43237e53a8514728ee00ffe2bb6d23c76b9c095a8d447a3ff90940f03` | 106027 | match | PASS |
| Founder certification schema | `15093a948f6d73343e5edf26d5e20d0dd75b55e3a67939ae2a80a789c6468c01` | 5156 | match | PASS |
| Founder certification matrix | `fefe79e3e193a5f9ec0acf60f3da7cf548a218e3ba7097cb2256f4581e7065de` | 9034 | match | PASS |
| Validation report | `fa4612bbcc60eb28ad6d9121fe8245b440e33f32e6c02e1a641eec4659bc92fb` | 27353 | match | PASS |
| Package manifest | `ae73357b88aff24701649f97def22fa020d88068aacff6af758bd4f5754f658d` | 6703 | match | PASS |
| Checksum ledger | `6958524a8686858779bddb15ca4c79a18075f74d2c6c910442bcf97e669db54a` | 2698 | match | PASS |

## Checksum ledger verification

`sha256sum -c CHECKSUMS.sha256` against the exact-head package: **24/24 OK**.

## Count anchors

| Claim | Observed |
|---|---|
| Normative rule IDs | 39 |
| Source register rows | 39 |
| FCR classes | 10 |
| Adversarial scenarios | 25 |
| Non-self checksum entries | 24 |
| OQ-001..OQ-010 status | all `CLOSED_FOUNDER_DISPOSITION_INCORPORATED` |

## Authentication conclusion

`REVIEW_TARGET_AUTHENTICATED`. Proceeded with backstop defect review against frozen head only. No `REVIEW_TARGET_CHANGED` condition.
